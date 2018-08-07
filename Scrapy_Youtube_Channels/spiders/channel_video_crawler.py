import scrapy
import re
import xlrd
import json
import requests
from urllib.parse import urljoin
from lxml import html
from Scrapy_Youtube_Channels.items import YoutubeVideoItem


class ChannelVideoCrawler(scrapy.Spider):
    name = 'video_crawler'
    allowed_domains = ['youtube.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    }

    def start_requests(self):
        channel_video_url_list = []
        channel_url_list = []
        channel_name_list = []

        file = xlrd.open_workbook("top youtube channels to scrape.xlsx")
        sheet = file.sheet_by_index(0)
        for k in range(1, sheet.nrows):
            channel_video_url_list.append(str(sheet.row_values(k)[11]))
            channel_url_list.append(str(sheet.row_values(k)[7]))
            channel_name_list.append(str(sheet.row_values(k)[8]))

        for i in range(len(channel_url_list)):
            item = YoutubeVideoItem()
            item['channel_name'] = channel_name_list[i]
            item['channel_url'] = channel_url_list[i]
            yield scrapy.Request(
                url=channel_video_url_list[i],
                headers=self.headers,
                meta={'item': item},
                callback=self.parse
            )

    def parse(self, response):
        item = response.meta.get('item')

        data = re.search('ytInitialData"] = (.*?);', response.body_as_unicode(), re.DOTALL)
        if data:
            data = json.loads(data.group(1))

        json_data = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs')[1]\
                        .get('tabRenderer', {}).get('content', {}).get('sectionListRenderer', {}).get('contents')[0]\
                        .get('itemSectionRenderer', {}).get('contents')[0].get('gridRenderer', {})

        video_array = json_data.get('items')

        for video in video_array:
            item['video_title'] = video.get('gridVideoRenderer', {}).get('title', {}).get('simpleText')
            item['video_age'] = video.get('gridVideoRenderer', {}).get('publishedTimeText', {}).get('simpleText')
            item['video_views'] = video.get('gridVideoRenderer', {}).get('viewCountText', {}).get('simpleText')
            item['video_length'] = video.get('gridVideoRenderer', {}).get('thumbnailOverlays')[0]\
                                    .get('thumbnailOverlayTimeStatusRenderer').get('text', {}).get('simpleText')
            item['video_url'] = urljoin(response.url,
                                        video.get('gridVideoRenderer', {}).get('navigationEndpoint', {}).get('commandMetadata', {})
                                        .get('webCommandMetadata', {}).get('url'))
            yield item

        continue_data = json_data.get('continuations')[0].get('nextContinuationData', {})
        ctoken = continue_data.get('continuation')

        for j in range(4):
            ajax_url = 'https://www.youtube.com/browse_ajax?ctoken={ctoken}&continuation={ctoken}'.format(ctoken=ctoken)
            new_data = requests.get(ajax_url).json()
            content = html.fromstring(new_data.get('content_html', {})).xpath('//div[@class="yt-lockup-thumbnail"]')[0]
            title_array = content.xpath('//a[contains(@class, "yt-uix-tile-link")]/@title')
            href_array = content.xpath('//a[contains(@class, "yt-uix-tile-link")]/@href')
            views_array = content.xpath('//ul[@class="yt-lockup-meta-info"]/li[1]/text()')
            age_array = content.xpath('//ul[@class="yt-lockup-meta-info"]/li[2]/text()')
            length_array = content.xpath('//span[@class="video-time"]/span/text()')

            for i in range(len(title_array)):
                item['video_title'] = str(title_array[i])
                item['video_url'] = urljoin(response.url, str(href_array[i]))
                item['video_age'] = str(age_array[i])
                item['video_views'] = str(views_array[i])
                item['video_length'] = str(length_array[i])
                yield item

            next_data = new_data.get('load_more_widget_html', {})
            if next_data:
                continuation = str(html.fromstring(next_data).xpath('//button/@data-uix-load-more-href')[0])
                continuation = re.search('&continuation=(.*)', continuation, re.DOTALL)
                ctoken = continuation.group(1)
