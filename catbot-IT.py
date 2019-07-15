#              .__....._             _.....__,
#                 .": o :':         ;': o :".
#                 `. `-' .'.       .'. `-' .'  
#                   `---'             `---' 
#
#         _...----...      ...   ...      ...----..._
#      .-'__..-""'----    `.  `"`  .'    ----'""-..__`-.
#     '.-'   _.--"""'       `-._.-'       '"""--._   `-.`
#     '  .-"'                  :                  `"-.  `
#       '   `.              _.'"'._              .'   `
#             `.       ,.-'"       "'-.,       .'
#               `.                           .'
#                 `-._                   _.-'
#                     `"'--...___...--'"`

# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http     import HtmlResponse, Request

class CatbotSpider(scrapy.Spider):
    name = 'catbot'
    allowed_domains = ['www.tripadvisor.it']
    f = open("url_tutte_le_citta.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        self.categorie = []
        codice    = response.xpath('//a[@class="property_title"]/@href').extract()
        cuisines  = response.xpath('//div[@class="cuisines"]')
        for div in cuisines:
            self.categorie.append(div.xpath('./a[@class="item cuisine"]/text()').extract())
        
        for cod, cat in zip(codice, self.categorie):
            cod = cod.split('Review')[1]
            cod = cod.replace('-','')

            # valori default
            self.pesce = 0; self.pizza = 0; self.fastf = 0
            self.vege  = 0; self.glut  = 0; self.asia  = 0
            # controllo categorie
            if 'Pesce' in cat:
                self.pesce = 1
            if 'Pizza' in cat:
                self.pizza = 1
            if 'Fast food' in cat:
                self.fastf = 1
            if 'Per vegetariani' in cat:
                self.vege  = 1
            if 'Opzioni senza glutine' in cat:
                self.glut  = 1
            if 'Asiatica' in cat:
                self.asia  = 1

            scraped_info = {
                'ID' :         cod,
                # CATEGORIE: pesce pizza fast-food vegetariano glutine asiatico
                'Pesce':       self.pesce,
                'Pizza':       self.pizza,
                'Fast-Food':   self.fastf,
                'Vegetariano': self.vege,
                'Glutine':     self.glut,
                'Asiatico':    self.asia,
            }
            next_url = response.xpath('//a[contains(text(), "Avanti")]/@href').extract()
            # TESTING, CALL, SAVE IN FILE
            if(next_url and len(next_url) > 0):
                for site in next_url:
                    yield Request(url="http://www.tripadvisor.it" + site, callback=self.parse)
                yield scraped_info