#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE:
# Il nome della città non viene estratto correttamente se la città non è capoluogo di provincia
# id_ristorante viene inizializzato a 0 ogni volta che il ragno cambia pagina web
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

# def convertiPrezzo(e):
#     if '-' in e:
#         prezzo = 0
#         e = e.split(' - ')
#         e[0] = e[0].count('*')
#         e[1] = e[1].count('*')
#         prezzo = float(e[0])+float(e[1])
#         prezzo = float(prezzo/2)
#     else:
#         prezzo = float(e.count('*'))
#     return prezzo
class TripbotSpider(scrapy.Spider):
    name = 'tripbot'
    allowed_domains = ["www.tripadvisor.it"]
    base_url = "www.tripadvisor.it"
    # URL TEXT
    f = open("url_tutte_le_citta_UE.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    # count = 0
    def parse(self, response):
                # SELCTOR -> XPATH
                url_ristorante = response.xpath('//a[@class="photo_link"]/@href').extract()  
                for link in url_ristorante:
                    # SAVING
                    scraped_info = {
                        'url' : "https://www.tripadvisor.it"+link,
                    }
                    next_url = response.xpath('//a[contains(text(), "Avanti")]/@href').extract()
                    # TESTING, CALL, SAVE IN FILE
                    if(next_url and len(next_url) > 0):
                        for site in next_url:
                            yield Request(url="http://www.tripadvisor.it" + site, callback=self.parse)
                        yield scraped_info




