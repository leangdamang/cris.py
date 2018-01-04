
import scrapy
from scrapy.spiders import BaseSpider
from pymongo import MongoClient
from sklearn.externals import joblib
import pymongo


client = MongoClient()
db = client.recipes
pages = db.pages

class SeriousSpider(BaseSpider):
    name = 'seriousspider'

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
        }

    start_urls = joblib.load('http://www.seriouseats.com/recipes/2017/08/chicken-nanbansu-yakitori-recipe.html')



    def parse(self, response):
        data = {}
        data['url'] = response.url
        data['title'] =  response.xpath('//h1[@class = "title recipe-title fn"]/text()').extract()[0]
        data['image'] =  response.xpath('//div[@class = "se-pinit-image-container"]/img/@src').extract()[0]
        data['notes'] =  response.xpath('//div[@class = "recipe-introduction-body"]/p').extract()[1]
        data['time'] = response.xpath('//span [@class ="info"]/text()').extract()[1]
        data['ingredients_list'] = response.xpath('//div [@class = "recipe-ingredients"]/ul/li/text()').extract()
        data['instructions'] = " ".join(response.xpath('//div[@class = "recipe-procedure-text"]/p/text()').extract())
        data['tags_list'] = response.xpath('//ul[@class = "tags"]/li/a/text()').extract()
        pages.replace_one(data, data, upsert = True)
