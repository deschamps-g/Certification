import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

df = pd.read_json('hotel_url.json')

class ScrapbookingHotelsSpider(scrapy.Spider):
    
    name = "scrapbooking_hotels"
    start_urls = df['url'].tolist()[:]
    
    def parse(self, response):
        name = response.xpath('//div[@id="hp_hotel_name"]/div/h2/text()').get()
        description = response.xpath('//*[@id="property_description_content"]/div/p/text()').get()
        rating = response.xpath('//div[@data-testid="review-score-right-component"]/div[1]/text()').get()
        lat_lon = response.css('a#hotel_address::attr(data-atlas-latlng)').get()
                
        url = response.url
        city = df[df['url'] == url]['city'].iloc[0]

        yield {
            'city' : city,
            'lat' : lat_lon.split(",")[0],
            'lon' : lat_lon.split(",")[1],             
            'name' : name,
            'rating' : rating,
            'url' : response.url,
            'description': description.replace("\n", "<br>")       # this way the description is ready to be displayed in a web browser or on a plotly express map
        }

filename = f"hotels_data.json"

if filename in os.listdir('.'):
        os.remove('' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/123.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        '' + filename: {"format": "json", 'encoding' : 'utf8'}
    }
})

process.crawl(ScrapbookingHotelsSpider)
process.start()