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
        'ITEM_PIPELINES' : {'antara.pipelines.IntImagePipelines': 1}
    }
    name = "antara-inter"
    allowed_domains = ["download.antarafoto.com"]
    start_urls = ["http://download.antarafoto.com"]
    
    # Login to Antara Foto
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'username', 'password':'password'}, callback=self.after_login)

    # Change to International Mode
    def after_login(self, response) :
        if "authentication failed" in response.body:
            self.login.error("Login Failed")
            return
        inter_mode = response.xpath('//*[@id="topmost"]/a[2]/@href').extract_first()
        address = 'https://download.antarafoto.com'
        url_international = address + inter_mode     
        yield scrapy.Request(url = url_international, callback = self.next)


    def next(self, response):

        next_link = response.xpath('//*[@id="nav_spc_r"]/a/@href').extract_first()
        domain = 'https://download.antarafoto.com'
        next_url = domain + next_link
        thumb = response.css('p.thumb').extract_first()
        href = response.xpath('//*[@id="mid_spc_2"]/table').css('a').xpath('@href').extract()
        print thumb
        print href
        baseurl = 'https://download.antarafoto.com/list/2'
        yield scrapy.Request(url = baseurl, callback = self.definition )

    # Loop the next for new content
    def definition(self, response):
        next_link = response.xpath('//*[@id="nav_spc_r"]/a[2]/@href').extract_first()
        domain = 'https://download.antarafoto.com'
        next_url = domain + next_link
        thumb = response.css('p.thumb').extract_first()
        href = response.xpath('//*[@id="mid_spc_2"]/table').css('a').xpath('@href').extract()
        baseonURL = ['https://download.antarafoto.com' + s for s in href]  
        for x in baseonURL:
            yield scrapy.Request(url = x, callback = self.hires) 

        yield scrapy.Request(next_url,self.definition)

    def hires(self, response):
        # hd_image_link = response.xpath('//*[@id="mid_spc_3"]/table[1]').css('a').xpath('@href').extract()
        item = AntaraItem() 
        item['file_name'] = response.css('p.copyright::text').extract_first().split()[0]
        item['folder_name'] = response.css('span.title::text').extract_first()
        item['image_urls'] = response.xpath('//*[@id="mid_spc_3"]/table[1]').css('a').xpath('@href').extract()
        item['image_urls'] = [urlparse.urljoin(response.url, url) for url in item['image_urls']]
        yield item