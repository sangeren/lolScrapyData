# -*- coding: utf-8 -*-
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "person-list"
    start_urls = [
        'http://www.op.gg/ranking/ladder/',
    ]

    def parse(self, response):
        for line in response.css("tr.ranking-table__row"):
            yield {
                'rank': line.css("td.ranking-table__cell--rank::text").extract_first(),
                'summoner': line.css("td.ranking-table__cell--summoner a::attr(href)").extract_first()
            }

        next_page_url = response.css("li.ranking-pagination__item--disable+li>a::attr(href)").extract_first()
        if next_page_url is not None and "/page=50" not in next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))

        # if len(summoner_ids) > 0:
        #     yield scrapy.Request(url=moreBaseUrl + bytes(last_info) + '&summonerId=' + bytes(summoner_ids[0]),
        #                          callback=self.parse_one_game)
