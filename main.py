import os
import re
from gooey import Gooey, GooeyParser
import scrapy
from scrapy.crawler import CrawlerProcess


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class iwaraSpider(scrapy.Spider):
    name = "renamer"

    def start_requests(self):
        urls = []
        for files in os.listdir("./"):
            if files.lower().endswith("source.mp4"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                request = scrapy.Request(url=url, callback=self.parse)
                request.cb_kwargs['oldname'] = "./" + files
                yield request
            elif files.lower().endswith("Source.mp4.xltd"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                print(url)

    def parse(self, response, oldname):
        newname = response.css('a.username::text').get() + " - " + response.css('h1.title::text').get()
        newname = validateTitle(newname)
        newname = "./" + newname + ".mp4"
        print(oldname + " -----> " + newname)
        os.rename(oldname,newname)

@Gooey()
def main():
    parser = GooeyParser(description='Process some integers.')
    parser.add_argument('filename', help="选择目标文件夹", widget='DirChooser')
    parser.parse_args()

if __name__ == '__main__':
    main()
    process = CrawlerProcess()
    process.crawl(iwaraSpider)
    process.start()