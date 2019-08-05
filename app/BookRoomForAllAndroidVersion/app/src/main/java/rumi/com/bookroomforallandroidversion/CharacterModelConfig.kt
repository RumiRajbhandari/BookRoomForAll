package rumi.com.bookroomforallandroidversion

import java.util.*

/**
 * The most of those information can be found in MNIST.ipynb
 */
object CharacterModelConfig {
    var MODEL_FILENAME = "resnet_handwriting.tflite"

    val INPUT_IMG_SIZE_WIDTH = 32
    val INPUT_IMG_SIZE_HEIGHT = 32
    val FLOAT_TYPE_SIZE = 4
    val PIXEL_SIZE = 1
    val MODEL_INPUT_SIZE =
        FLOAT_TYPE_SIZE * INPUT_IMG_SIZE_WIDTH * INPUT_IMG_SIZE_HEIGHT * PIXEL_SIZE

    val OUTPUT_LABELS = Collections.unmodifiableList(
        Arrays.asList(
            "empty",
            "क",
            "ख",
            "ग",
            "घ",
            "ङ",
            "च",
            "छ",
            "ज",
            "झ",
            "ञ",
            "ट",
            "ठ",
            "ड",
            "ढ",
            "ण",
            "त",
            "थ",
            "द",
            "ध",
            "न",
            "प",
            "फ",
            "ब",
            "भ",
            "म",
            "य",
            "र",
            "ल",
            "व",
            "श",
            "ष",
            "स",
            "ह",
            "क्ष",
            "त्र",
            "ज्ञ",
            "11",
            "22",
            "33",
            "44",
            "55",
            "66",
            "77",
            "88",
            "99",
            "00"
        )
    )

    val MAX_CLASSIFICATION_RESULTS = 3
    val CLASSIFICATION_THRESHOLD = 0.1f
}
