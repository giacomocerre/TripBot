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

def convertiPrezzo(e):
    if '-' in e:
        prezzo = 0
        e = e.split(' - ')
        e[0] = e[0].count('*')
        e[1] = e[1].count('*')
        prezzo = float(e[0])+float(e[1])
        prezzo = float(prezzo/2)
    else:
        prezzo = float(e.count('*'))
    return prezzo
class TripbotSpider(scrapy.Spider):
    name = 'tripbot'
    allowed_domains = ["www.tripadvisor.it"]
    base_url = "www.tripadvisor.it"
    # URL TEXT
    f = open("url_Ristoranti(all_UE).txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    # start_urls = ["https://www.tripadvisor.it/Restaurant_Review-g187890-d3393985-Reviews-Lo_Scrigno_dei_Sapori-Palermo_Province_of_Palermo_Sicily.html"]
    def parse(self, response):
                #CURRENT URL SELECTOR CUTTING AND REPLACING
                url = response.request.url.split("Review")[1].replace('-',"")
                # SELECTOR -> CSS
                names          = response.css('.heading_title::text').extract()
                rating         = response.css('.overallRating::text').extract()
                reviews        = response.css('.seeAllReviews::text').extract()
                price_votes    = response.css('.header_tags.rating_and_popularity::text').extract()
                street         = response.css('.street-address::text').extract()
                locality       = response.css('.locality::text').extract()
                
                # SELCTOR -> XPATH
                city      = response.xpath('//div[@class="prw_rup prw_restaurants_header_eatery_pop_index"]//span[@class="header_popularity popIndexValidation"]//a/text()').extract_first()
                region    = response.xpath('//ul[@class="breadcrumbs"]//li[2]//a//span/text()').extract_first()
                votes     = response.css('.is-6').xpath("span/@class").extract()
                categorie = response.xpath('//div[@class="table_section"]//div[@class="content"]//a/text()').extract()

                # LISTE VARIABILI
                voti = []
                for vote in votes:
                    if vote != 'text':
                        voti.append(str(vote.split('_')[3]))
                if len(voti) == 3:
                    voti.append(0)

                # ADDRESS
                citta = city.split(' ')[-1]
                print(citta)
                address = street + locality
                for nome, rating, nRec, eur_votes, cat in zip(names, rating, reviews, price_votes, categorie):
                    # CUTTING
                    rating = rating[:-1]
                    nRec      = nRec[:-11]
                    eur_votes       = eur_votes.split(',')[0]
                    # REPLACING
                    rating = float(rating.replace(',','.'))
                    nRec = int(nRec.replace('.',''))
                    for eur_votes in price_votes:
                        eur_votes = eur_votes.replace("€","*")
                        eur_votes = convertiPrezzo(eur_votes)
                        # CATEGORIE
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
                    # SAVING
                        scraped_info = {
                            'ID'                : url,
                            'Nome'              : nome,
                            'Rating'            : float(rating),
                            'Punteggio_Prezzo'  : float(eur_votes),  
                            'Numero_Recensioni' : int(nRec),
                            'Servizio'          : voti[0],
                            'Cucina'            : voti[1],
                            'Qualità'           : voti[2],
                            'Atmosfera'         : voti[3],
                            'Regione'           : region,
                            'Citta'             : citta,
                            'Indirizzo'         : address[0],
                            'Pesce'             : self.pesce,
                            'Pizza'             : self.pizza,
                            'FastFood'          : self.fastf,
                            'Vegetariano'       : self.vege,
                            'Glutine'           : self.glut,
                            'Asiatico'          : self.asia,   
                        }
                        yield scraped_info




