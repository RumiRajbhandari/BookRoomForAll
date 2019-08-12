# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy import Request


class OnlinekhabarSpider(scrapy.Spider):
    name = 'onlinekhabar'  # name of spider, scrapy crawl <spidername> to start this spider
    # custom_settings = {
    #    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    # }

    allowed_domains = [
        'onlinekhabar.com']  # allowed domains, if using this spider you try to crawl other domain like hello.com, it won't, yo can add more allowed domains if you need to crawl different websites using same spider
    start_urls = [
        'https://www.onlinekhabar.com/content/news']  # this is the first url that scrapy scrapes, can be more than 1
    data_dir = 'ok_news'

    def parse(self,
              response):  # by default, scrapy crawls the urls specified in start_urls and call parse method with the response of that url
        # response is the response of this link https://www.onlinekhabar.com/content/news

        # at this stage you should know about list, dict
        news_item = {}
        news = response.css('a.title__regular')
        for a_tag in news:
            link = a_tag.css('::attr(href)').extract_first()

            # From here you can crawl the news url again like this

            # Whatever is in callback will be called after the crawling the url provided, by default callback is parse
            # if callback is not present, it will call parse
            yield Request(link, callback=self.parse_news)

        next_page = response.xpath('//a[contains(@class, "next")]/@href').extract_first()
        if next_page and news:  # will prevent infinite loop
            yield Request(next_page)  # no callback means default i.e. parse so it calls itself

    def parse_news(self, response):
        news = {}
        news['link'] = response.url
        news['title'] = self.parse_title(response)
        news['authors'] = self.parse_authors(response)
        news['description'] = self.parse_description(response)
        news['content'] = self.parse_content(response)
        news['published_date'] = self.parse_published_date(response)
        news['image'] = self.parse_image(response)
        self.save(news)
        yield news

    def save(self, news):
        if self.data_dir is not None:
            with open(os.path.join(self.data_dir, news["link"].replace("/", "_") + '.txt'), "w") as f:
                f.write(news["content"])

    @staticmethod
    def parse_title(response):
        return response.xpath('//h2[@class="mb-0"]/text()').extract_first()

    @staticmethod
    def parse_authors(response):
        return response.xpath('//div[@class="author__wrap"]/label/text()').extract_first()

    @staticmethod
    def parse_description(response):
        return '\n'.join(response.xpath('//div[contains(@class, "main__read--content")]//text()').extract())

    @staticmethod
    def parse_content(response):
        return ' \n'.join(response.xpath(
            '//div[contains(@class, "main__read--content")]/p//text()').extract()).replace('\xa0', ' ').strip()

    @staticmethod
    def parse_published_date(response):
        return response.xpath('//div[contains(@class, "post__time")]/span/text()').extract_first()

    @staticmethod
    def parse_image(response):
        return response.xpath('//div[contains(@class,"dtl-img")]/img/@src').extract_first()
