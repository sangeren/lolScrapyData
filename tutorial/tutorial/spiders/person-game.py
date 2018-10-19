# -*- coding: utf-8 -*-
import scrapy
import csv

class OneGamepider(scrapy.Spider):
    name = "person-game"

    def start_requests(self):
        filename = 'E:\explore\scrapy\lol-getdatas\\tutorial\onepersonallgame.csv'
        with open(filename) as f:
            reader = csv.reader(f)
            head_row = next(reader)
            for row in reader:
                yield scrapy.Request(url='http://www.op.gg/summoner/matches/ajax/detail/gameId=' + row[1]+'&summonerId='+row[2]+'&gameTime='+row[0], callback=self.parse)


    def parse(self, response):
        yield {
            'one': response.css('table.GameDetailTable th[colspan="4"]::text').extract()[1].replace('\n\t', '').replace('\t', ''),
            'two': response.css('table.GameDetailTable th[colspan="4"]::text').extract()[3].replace('\n\t', '').replace('\t', ''),
            'oneTeam':  response.css('div.__spc32::text').extract()[0:5],
            'twoTeam': response.css('div.__spc32::text').extract()[5:10],
            'url':response.url
            # 'b': response.css("small.author::text").extract_first(),
        }

    # next_page_url = response.css("li.next > a::attr(href)").extract_first()
    # if next_page_url is not None:
    #     yield scrapy.Request(response.urljoin(next_page_url))
#   response.xpath('//div[@class="Image __sprite __spc32 __spc32-140"]/text()').extract()
#