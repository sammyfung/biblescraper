# biblescraper
Chinese Bible web scraper for Chinese word segmentation project

This project is aimed to scrape Chinese bible scriptures in order to build a database for better word segmentation on Chinese Bible scriptures, to solve the problem of poor word search on Chinese bible.

Data can be exported to CSV, XML or XML with Scrapy build-in data exporter.

## Installation

The project requires python 3, scrapy and jieba.

```
$ pip install -r requirements
```

## Execution

The default mode of web scraper scrapes Matthew 3 (馬太福音 3 章) and export to a CSV file (test_data.csv)

```
$ scrapy crawl zhbible -o test_data.csv
```

You can use environment variables to set which Chinese bible version (CUNP1, CUNP2, RCUV1, RCUV2), books, starting and ending chapter to be scraped. Available values can be found in the source code.  

Examples: scraping Genesis 1 (創世記 1 章)

```
$ export BIBLE_VERSION=CUNP2
$ export BIBLE_BOOK=GEN
$ export BIBLE_CH_START=1
$ export BIBLE_CH_END=1
$ scrapy crawl zhbible
```

Full DEBUG Modes: Please set the environment variable DEBUG.

```
$ export DEBUG=Yes
$ scrapy crawl zhbible
```

## Sponsor

If you would like to support my open source or christian technology project, please sponsor via [GitHub](https://github.com/sponsors/sammyfung), [Patreon](https://www.patreon.com/sammyfung) and [PayPal](https://sammy.hk/paypal/).



