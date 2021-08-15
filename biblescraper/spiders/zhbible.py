import scrapy, os, re, jieba
from biblescraper.items import BiblescraperItem

class ZhbibleSpider(scrapy.Spider):
    name = 'zhbible'
    allowed_domains = ['hkbs.org.hk']
    start_urls = []
    language = 'zh-TW'
    version = 'RCUV2'
    books = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR",
             "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS", "JOL", "AMO",
             "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL", "MAT", "MRK", "LUK", "JHN", "ACT", "ROM",
             "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE",
             "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
    chapters = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48,
                12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1,
                13, 5, 5, 3, 5, 1, 1, 1, 22]
    new_testament = ["MAT","MRK","LUK","JHN","ACT","ROM","1CO","2CO","GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI","TIT","PHM","HEB","JAS","1PE","2PE","1JN","2JN","3JN","JUD","REV"]

    def __init__(self):
        if os.environ.get('BIBLE_VERSION'):
            self.version = os.environ.get('BIBLE_VERSION')
        if os.environ.get('DEBUG') == 'Yes':
            for i in range(0, len(self.books)):
                for j in range(0, self.chapters[i]+1):
                    self.start_urls.append('http://rcuv.hkbs.org.hk/bb/%s/%s/%s/' % (self.version, self.books[i], j))
        else:
            if os.environ.get('BIBLE_BOOK'):
                selected_book = os.environ.get('BIBLE_BOOK')
            else:
                selected_book = 'MAT'
            if os.environ.get('BIBLE_CH_START'):
                ch_start = int(os.environ.get('BIBLE_CH_START'))
            else:
                ch_start = 3
            if os.environ.get('BIBLE_CH_END'):
                ch_end = int(os.environ.get('BIBLE_CH_END'))
            else:
                ch_end = 4
            for ch in range(ch_start, ch_end + 1):
                print(ch)
                self.start_urls.append('http://rcuv.hkbs.org.hk/bb/%s/%s/%s/' % \
                                       (self.version, selected_book, ch))

    def parse(self, response):
        urlpart = re.split('/', response.url)
        items = []
        if re.search('^[0-9]*$', urlpart[6]):
            chapter = int(urlpart[6])
        else:
            chapter = -1
        version = urlpart[4]
        book = urlpart[5]
        book_order = self.books.index(book)
        if book in self.new_testament:
            testament = 'N'
        else:
            testament = 'O'
        verses = response.xpath('//p/span')
        verse_count = 0
        for verse in verses:
            verse_count += 1
            item = BiblescraperItem()
            item['language'] = self.language
            item['version'] = version
            item['testament'] = testament
            item['book_order'] = book_order
            item['book'] = book
            item['type'] = 'SCR'
            item['chapter'] = chapter
            item['verse'] = verse_count
            item['position'] = 0
            item['scripture'] = ''
            verse_parts = re.sub('(<i>|</i>)', '', verse.extract())
            verse_parts = re.sub('(<span>|</span>)', '', verse_parts)
            verse_parts = re.sub('<sup[^<]*</sup>', '<sup>', verse_parts)
            verse_parts = re.sub(' ', '', verse_parts)
            verse_parts = re.split('<sup>', verse_parts)
            verse_len = []
            verse_len_total = 0
            for i in verse_parts:
                verse_len_total += len(i)
                verse_len += [ verse_len_total ]
                item['scripture'] += i
            item['words'] = '|'.join(jieba.cut_for_search(item['scripture']))
            items.append(item)
            sup_count = 0
            for i in verse.xpath('sup/@title').extract():
                item = BiblescraperItem()
                item['language'] = self.language
                item['version'] = version
                item['testament'] = testament
                item['book_order'] = book_order
                item['book'] = book
                item['type'] = 'SUP'
                if re.search('^[0-9]*$', urlpart[6]):
                    item['chapter'] = int(urlpart[6])
                else:
                    item['chapter'] = 0
                item['verse'] = verse_count
                item['position'] = verse_len[sup_count]
                item['scripture'] = i
                item['words'] = '|'.join(jieba.cut_for_search(i))
                items.append(item)
                sup_count += 1
        return items



