import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

places = pd.read_csv('./places.csv').columns.to_list()

class ScrapbookingURLSpider(scrapy.Spider):
    
    name = "scrapbooking_url"

    nb_hotel = 20 
    order = 'review_score_and_price'
    filter = 'ht_id%3D204'                  # filter code for "show only hotels"
    apart = 0   	                        # to filter out rental flats, aparthotels and so on

    start_urls = []
    
    for place in places:
        place = place.replace(" ", "-")
        start_urls.append(f'https://www.booking.com/searchresults.html?ss={place}&ac_suggestion_list_length={nb_hotel}&nflt={filter}&shw_aparth={apart}')

    def parse(self, response):

        cards = response.xpath('//div[@data-testid="property-card"]')        

        for card in cards:              
            hotel_url = card.xpath('.//a/@href').get()
            city = response.url.split('ss=')[1].split('&')[0]       # we don't know on which url/city the spider is working, we get this info back from the current URL
            
            yield {
                'city' : city,
                'url': hotel_url.split("?")[0]                      # we keep the significant part of the URL, apart "?" we get params that aren't useful for us     
            }

filename = f"hotel_url.json"

if filename in os.listdir('.'):
        os.remove('' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/123.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        '' + filename: {"format": "json", 'encoding' : 'utf8'},
    }
})

process.crawl(ScrapbookingURLSpider)
process.start()