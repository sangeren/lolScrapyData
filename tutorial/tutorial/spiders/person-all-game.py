# -*- coding: utf-8 -*-
import scrapy
import json
import re
import csv


class QuotesSpider(scrapy.Spider):
    name = "person-all-game"

    def start_requests(self):
        filename = 'E:\explore\scrapy\lol-getdatas\\tutorial\personstest.csv'
        with open(filename) as f:
            reader = csv.reader(f)
            head_row = next(reader)
            for row in reader:
                yield scrapy.Request(url='http://' + row[0][2:], callback=self.parse)

        #         # 行号从2开始
        #         print(reader.line_num, row)
        #     print(list(reader))
        # urls = [
        #     'http://www.op.gg/summoner/userName=deadhard'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        moreBaseUrl = 'http://www.op.gg/summoner/matches/ajax/averageAndList/startInfo='
        # 1538920626&summonerId=57541180'

        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        last_infor = response.xpath('//div[@class="GameListContainer"]/@data-last-info').extract_first()
        summone_id = response.xpath('//div[@class="GameListContainer"]/@data-summoner-id').extract_first()

        # for quote in response.xpath('//div[@class="GameItemWrap"]'):
        #     yield {
        #         'summonerid': quote.xpath('./div[@class="GameItem Win"]/@data-summoner-id').extract_first(),
        #         'gametime': quote.xpath('./div[@class="GameItem Win"]/@data-game-time').extract_first(),
        #         'gameid': quote.xpath('./div[@class="GameItem Win"]/@data-game-id"]/text()').extract()
        #     }
        for quote in response.css('div.GameItemWrap'):
            yield {
                'gametype': quote.css('div.GameType::text').extract_first().replace('\n', '').replace('\t', ''),
                'summonerid': quote.css('div.GameItem::attr(data-summoner-id)').extract_first(),
                'gametime': quote.css('div.GameItem::attr(data-game-time)').extract_first(),
                'gameid': quote.css('div.GameItem::attr(data-game-id)').extract()
            }

        if last_infor is not None:
            # next_page = response.urljoin(next_page)
            yield scrapy.Request(url=moreBaseUrl + last_infor + '&summonerId=' + summone_id,
                                 callback=self.parse_one_game)

    def parse_one_game(self, response):
        moreBaseUrl = 'http://www.op.gg/summoner/matches/ajax/averageAndList/startInfo='
        # 1538920626&summonerId=57541180'

        jsonresponse = json.loads(response.body_as_unicode())
        last_info = jsonresponse["lastInfo"]

        html = jsonresponse["html"].replace('\n\t', '').replace('\t', '')
        gametype = re.findall("class=\"GameType\">(.+?)<", html)
        summoner_ids = re.findall("data-summoner-id=\"(.+?)\"", html)
        game_ids = re.findall("data-game-id=\"(.+?)\"", html)
        game_times = re.findall("data-game-time=\"(.+?)\"", html)
        for index, val in enumerate(summoner_ids):
            yield {
                'gametype': gametype[index],
                'summonerid': val,
                'gametime': game_times[index],
                'gameid': game_ids[index]
            }

        if len(summoner_ids) > 0:
            yield scrapy.Request(url=moreBaseUrl + bytes(last_info) + '&summonerId=' + bytes(summoner_ids[0]),
                                 callback=self.parse_one_game)

# scrapy shell "http://www.op.gg/summoner/userName=deadhard"
# response.xpath('//div[@class="SummonerLayout tabWrap _recognized"]').extract_first()
# response.css('div.SummonerLayout"]').extract_first()
