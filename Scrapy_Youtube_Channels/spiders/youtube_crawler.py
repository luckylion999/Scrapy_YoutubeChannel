import math
import datetime

import scrapy

from Scrapy_Youtube_Channels.utils import get_nth
from Scrapy_Youtube_Channels.items import YoutubeChannelItem


class YoutubeChannelCrawler(scrapy.Spider):
    name = 'channel_crawler'
    allowed_domains = ['channelcrawler.com', 'youtube.com']
    channel_crawler_url = 'https://channelcrawler.com/'

    start_url = ('http://channelcrawler.com/eng/results/136105/sort:Channel.subscribers/direction:desc')

    categories = {
        'Autos & Vehicles': 2,
        'Comedy': 23,
        'Education': 27,
        'Entertainment': 24,
        'Film and Animation': 1,
        'Gaming': 20,
        'Howto & Style': 26,
        'Music': 10,
        'News & Politics': 25,
        'Nonprofits & Activism': 29,
        'People & Blogs': 22,
        'Pets & Animals': 15,
        'Science & Technology': 28,
        'Sports': 17,
        'Travel & Events': 19,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.1.2325.162 Safari/537.16',
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            callback=self.parse,
            meta={'first': self.channel_crawler_url},
        )

    def parse(self, response):
        for c in response.css('div.channel'):
            data = c.css('small::text').extract()
            item = YoutubeChannelItem()
            item['emails'] = []
            item['views'] = item['location'] = None

            item['profile_url'] = c.css('h4 a::attr(href)').extract_first()
            item['channel_id'] = item['profile_url'].rsplit('/', 1)[-1]
            item['title'] = c.css('h4 a::attr(title)').extract_first()
            item['country'] = c.css('h4 img::attr(title)').extract_first()
            item['picture_url'] = c.css('a > img::attr(src)').extract_first()
            item['category_name'] = c.css('small b::text').extract_first() \
                                     .strip()
            item['category_id'] = self.categories.get(item['category_name'],
                                                      99)
            item['description'] = get_nth(c.css('a::attr(title)').extract(),
                                          n=1)
            item['followers'] = int(
                    get_nth(data, y='', n=0).split()[0].replace(',', ''))
            item['videos'] = int(
                    get_nth(data, y='', n=1).split()[0].replace(',', ''))
            try:
                item['join_date'] = datetime.datetime.strptime(
                        get_nth(data, y='', n=2).split(':')[1].strip(),
                        '%d.%m.%Y').date()
            except ValueError:
                item['join_date'] = None

            item['trailer_url'] = c.css('small a::attr(href)').extract_first()
            item['trailer_title'] = c.css('small a::attr(title)').extract_first()
            alt_title = c.css('small a::text').extract_first()
            if (alt_title is not None and
                    len(alt_title) > len(item['trailer_title'] or '')):
                item['trailer_title'] = alt_title

            yield item

        first = response.meta.pop('first', None)
        if first:
            results = response.css('.results-title::text').extract_first()
            N = int(results.split()[0].replace(',', ''))
            url = response.url + '/page:'
            for i in range(2, math.ceil(N / 20) + 1):
                if i == 2:
                    last = first
                else:
                    last = url + str(i - 1)
                headers = {
                    'Referer': last,
                }
                yield scrapy.Request(url + str(i), callback=self.parse,
                                     meta=response.meta, headers=headers,
                                     priority=N - i)
