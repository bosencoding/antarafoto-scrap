# Scrapy Images
# ImageHD Domestic Crawler of Antara Property
# This code is property of PT.Metranet by Bussiness Division 
# Writed by @hanyandriyanto - 2017 

import scrapy
import re
import urlparse
from scrapy.http import FormRequest
from scrapy.http import Request
from antara.items import AntaraItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class LoginSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES' : {'antara.pipelines.DomImagePipelines': 1}
    }
    name = "antara-domestic"
    allowed_domains = ["download.antarafoto.com"]
    start_urls = ["http://download.antarafoto.com"]
    
    # Login to Antara Foto
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'username', 'password':'password'}, callback=self.after_login)

    # Scraping antarafoto layer 1
    def after_login(self, response) :
        if "authentication failed" in response.body:
            self.login.error("Login Failed")
            return
        baseurl = 'https://download.antarafoto.com'
        for page in range(0,2):
            level1_url = 'https://download.antarafoto.com/list/%d' % (page)
            yield scrapy.Request(url = level1_url, callback = self.definition )

    def definition(self, response): 
        href = response.xpath('//*[@id="mid_spc_2"]/table').css('a').xpath('@href').extract()
        baseonURL = ['https://download.antarafoto.com' + s for s in href]  
        for x in baseonURL:
            yield scrapy.Request(url = x, callback = self.hires) 

    def hires(self, response):
        item = AntaraItem() 
        item['file_name'] = response.css('p.copyright::text').extract_first().split()[0]
        item['folder_name'] = response.css('span.title::text').extract_first()
        item['image_urls'] = response.xpath('//*[@id="mid_spc_3"]/table[1]').css('a').xpath('@href').extract()
        item['image_urls'] = [urlparse.urljoin(response.url, url) for url in item['image_urls']]
        yield item
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
