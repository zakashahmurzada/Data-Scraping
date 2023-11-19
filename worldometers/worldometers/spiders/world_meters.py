import scrapy
import logging

class WorldMetersSpider(scrapy.Spider):
    name = "world_meters"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link)

            yield response.follow(url=link, callback = self.parse_country, meta={'country_name': name}) # At here in self.parse_country we are calling the below function

    
    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath('.//td[1]/text()').get() # Brings year part from each row which index of td is 1 stands for year
            population = row.xpath('.//td[2]/strong/text()').get() # td index 2 contains population inside it

            yield {  # with the help of yield function we are returning them back
                'country_name' : name,
                'year': year,  
                'population': population
            }