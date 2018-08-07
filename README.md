# Youtube Channel / Video Information Crawlers
This is a Scrapy project to scrape millions of Youtube Channels information and Videos information.


## Spiders

This project contains two spiders and you can list them using the `list` command:

    $ scrapy list
    channel_crawler
    video_crawler

channel_crawler spider extracts millions of Youtube Channels Information into .xlsx / .csv format.

video_crawler spider reads Channels from .xlsx file and extracts Videos Information from those channels.


## Running the spiders
    $ scrapy crawl channel_crawler -o top youtube channels to scrape.xlsx
    $ scrapy crawl video_crawler -o result.csv
