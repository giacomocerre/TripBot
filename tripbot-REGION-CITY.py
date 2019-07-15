#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ESTRAE I LINK DELLE 20 CITTà PIù IMPORTANTI DI OGNI REGIONE ITALINA
#              (
#              )
#              (
#        /\  .-"""-.  /\
#       //\\/  ,,,  \//\\
#       |/\| ,;;;;;, |/\|
#      //\\\;-"""-;///\\
#     //  \/   .   \/  \\
#   (| ,-_|tripbot|_-, |)
#     //`__\.-.-./__`\\
#   // /.-(() ())-.\ \\
#  (\ |)   '---'   (| /)
#   ` (|           |) `
#     \)           (/

import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http     import HtmlResponse, Request

class TripbotSpider(scrapy.Spider):
    name = 'tripbot'
    allowed_domains = ["www.tripadvisor.it"]
    base_uri = "www.tripadvisor.it"
    f = open("url_Stati_UE.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    # start_urls = ["https://www.tripadvisor.it/Restaurants-g187886-oa20-Sicily.html"]

    def parse(self, response):
            # next_url = response.xpath('//div[@class="geo_name"]//a/@href').extract()
            next_url = response.xpath('//*[@id="LOCATION_LIST"]/ul/li/a/@href').extract()
            for url in next_url:
                    scraped_info = {
                        'regionLink' : "https://www.tripadvisor.it" + url,
                    }
                    clicca_avanti = response.xpath('//a[@class="guiArw sprite-pageNext  pid0"]/@href').extract()
                    if(clicca_avanti and len(clicca_avanti) > 0):
                        for click in clicca_avanti:
                            yield Request(url="http://www.tripadvisor.it" + click, callback=self.parse)
                        yield scraped_info
