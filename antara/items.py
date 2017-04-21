# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AntaraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    file_name = scrapy.Field()
    folder_name = scrapy.Field()
    hd_img_url = scrapy.Field()
    hires_urls = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
