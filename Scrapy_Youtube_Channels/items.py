import scrapy


class YoutubeChannelItem(scrapy.Item):
    channel_id = scrapy.Field()
    # channel_handle = scrapy.Field()
    profile_url = scrapy.Field()
    picture_url = scrapy.Field()
    title = scrapy.Field()
    followers = scrapy.Field()
    videos = scrapy.Field()
    join_date = scrapy.Field()
    description = scrapy.Field()
    trailer_url = scrapy.Field()
    trailer_title = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    country = scrapy.Field()
    location = scrapy.Field()
    views = scrapy.Field()
    emails = scrapy.Field()


class YoutubeVideoItem(scrapy.Item):
    channel_url = scrapy.Field()
    channel_name = scrapy.Field()
    video_title = scrapy.Field()
    video_age = scrapy.Field()
    video_length = scrapy.Field()
    video_views = scrapy.Field()
    video_url = scrapy.Field()