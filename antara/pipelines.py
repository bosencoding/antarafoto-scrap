# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy import log

class AntaraPipeline(object):
    def process_item(self, item, spider):
        return item

class DomImagePipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
            # for image_url in item['image_urls']:
        yield Request(item['image_urls'][0], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    
    def thumb_path(self, request, thumb_id, response=None, info=None):
        item = request.meta['item']
        # image_guid = thumb_id + request.url.split('/')[-1]
        # return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)
        return u'domestic/thumbs/{[folder_name]}/{[file_name]}'.format(item, item)
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        #log.msg(image_guid, level=log.DEBUG)
        return u'domestic/full/{[folder_name]}/{[file_name]}'.format(item, item)

class IntImagePipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
            # for image_url in item['image_urls']:
        yield Request(item['image_urls'][0], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        #log.msg(image_guid, level=log.DEBUG)
        return u'internasional/{[folder_name]}/{[file_name]}'.format(item, item)


class CrImagePipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
            # for image_url in item['image_urls']:
        yield Request(item['image_urls'][0], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        #log.msg(image_guid, level=log.DEBUG)
        return u'cerita/{[folder_name]}/{[file_name]}'.format(item, item)