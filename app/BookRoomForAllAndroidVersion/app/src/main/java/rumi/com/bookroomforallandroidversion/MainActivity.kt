package rumi.com.bookroomforallandroidversion

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.media.ThumbnailUtils
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.util.DisplayMetrics
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import java.io.FileNotFoundException
import java.io.IOException
import java.util.*

class MainActivity : AppCompatActivity() {

    lateinit var characterClassifier: CharacterClassifier
    var tts: TextToSpeech? = null
    var outputText = ""

    val RESULT_LOAD_IMG = 111

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        loadMnistClassifier()
        iv_take_photo.setOnClickListener {
            constraint_camera.visibility = View.VISIBLE
            constraint_photo.visibility = View.GONE
            vCamera.isActivated = true

        }

        btnTakePhoto.setOnClickListener {
            onTakePhoto()
        }

        iv_gallery.setOnClickListener {
            getImageFromAlbum()
        }

        iv_speak.setOnClickListener {
            speak()
        }
    }

    private fun loadMnistClassifier() {
        try {
            characterClassifier =
                CharacterClassifier.classifier(assets, CharacterModelConfig.MODEL_FILENAME)
        } catch (e: IOException) {
            Toast.makeText(
                this,
                "Character model couldn't be loaded. Check logs for details.",
                Toast.LENGTH_SHORT
            ).show()
            e.printStackTrace()
        }
    }

    override fun onStart() {
        super.onStart()
        vCamera.onStart()
    }

    override fun onResume() {
        super.onResume()
        vCamera.onResume()
    }

    override fun onPause() {
        vCamera.onPause()
        super.onPause()
    }

    override fun onStop() {
        vCamera.onStop()
        super.onStop()
    }

    fun onTakePhoto() {
        vCamera.captureImage { cameraKitView, picture -> onImageCaptured(picture) }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        vCamera.onRequestPermissionsResult(requestCode, permissions, grantResults)
    }

    private fun onImageCaptured(picture: ByteArray) {
        vCamera.isActivated = false

        constraint_camera.visibility = View.GONE
        constraint_photo.visibility = View.VISIBLE
        val bitmap = BitmapFactory.decodeByteArray(picture, 0, picture.size)
        processAndPredictImage(bitmap)
    }

    private fun processAndPredictImage(bitmap: Bitmap) {
        ivPreview.setImageBitmap(bitmap)
        tv_placeholder.visibility = View.GONE

        val squareBitmap =
            ThumbnailUtils.extractThumbnail(bitmap, getScreenWidth(), getScreenWidth())

        val preprocessedImage = ImageUtils.prepareImageForClassification(squareBitmap)

        val recognitions = characterClassifier.recognizeImage(preprocessedImage)
        if (recognitions.isNotEmpty()) {
            outputText = recognitions[0].title
            tv_output.text = String.format("Output: %s", outputText)
        } else
            tv_output.text = String.format("Output: ")
    }

    private fun getScreenWidth(): Int {
        val displayMetrics = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(displayMetrics)
        return displayMetrics.widthPixels
    }

    private fun getImageFromAlbum() {
        val photoPickerIntent = Intent(Intent.ACTION_PICK)
        photoPickerIntent.type = "image/*"
        startActivityForResult(photoPickerIntent, RESULT_LOAD_IMG)
    }

    override fun onActivityResult(reqCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(reqCode, resultCode, data)


        if (resultCode == Activity.RESULT_OK) {
            try {
                val imageUri = data!!.data
                val imageStream = contentResolver.openInputStream(imageUri!!)
                val selectedImage = BitmapFactory.decodeStream(imageStream)
                ivPreview.setImageBitmap(selectedImage)
                processAndPredictImage(selectedImage)
            } catch (e: FileNotFoundException) {
                e.printStackTrace()
                Toast.makeText(this, "Something went wrong", Toast.LENGTH_LONG).show()
            }
        } else {
            Toast.makeText(this, "You haven't picked Image", Toast.LENGTH_LONG).show()
        }
    }

    private fun speak() {
        tts = TextToSpeech(this, TextToSpeech.OnInitListener { status ->
            if (status == TextToSpeech.SUCCESS) {
                var result = tts?.setLanguage(Locale("nep", "NEP"))
                if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    Toast.makeText(this, "Lang not supported", Toast.LENGTH_SHORT).show()
                } else {
                    tts?.speak(outputText, TextToSpeech.QUEUE_ADD, null)
                }
            }
        })
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        super.onDestroy()
    }
}
