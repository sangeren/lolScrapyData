# -*- coding: utf-8 -*-
import scrapy
import json
import re
import csv


# URL: http://www.op.gg/summoner/matches/ajax/detail/gameId=3386101347&summonerId=57541180&gameTime=1539795564

class QuotesSpider(scrapy.Spider):
    name = "game"

    start_urls = [
        'http://www.op.gg/summoner/matches/ajax/detail/gameId=3386101347&summonerId=57541180&gameTime=1539795564',
    ]


    def parse(self, response):

        yield {
            'position1': response.css('table.Result-WIN tr.Row th.HeaderCell::text').extract_first()
            # ,
            # 'win': response.css('table.Result-WIN tr.Row td a::attr(href)'),
            # 'position2': response.css('table.Result-LOSE tr.Row th.HeaderCell::text').extract_first(),
            # 'loss': response.css('table.Result-LOSE tr.Row td a::attr(href)')
        }

# scrapy shell "http://www.op.gg/summoner/matches/ajax/detail/gameId=3386101347&summonerId=57541180&gameTime=1539795564"
# response.xpath('//div[@class="SummonerLayout tabWrap _recognized"]').extract_first()
# response.css('div.SummonerLayout"]').extract_first()
