import os
import re
from gooey import Gooey, GooeyParser
import scrapy
from scrapy.crawler import CrawlerProcess

target = "./"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class iwaraSpider(scrapy.Spider):
    name = "renamer"

    def start_requests(self):
        urls = []
        for files in os.listdir(target):
            if files.lower().endswith("source.mp4"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                request = scrapy.Request(url=url, callback=self.parse)
                request.cb_kwargs['oldname'] = target + files
                yield request
            elif files.lower().endswith("Source.mp4.xltd"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                print(url)

    def parse(self, response, oldname):
        newname = response.css('a.username::text').get() + " - " + response.css('h1.title::text').get()
        newname = validateTitle(newname)
        newname = target + newname + ".mp4"
        print(oldname + " -----> " + newname)
        os.rename(oldname,newname)

@Gooey(
    language="chinese")
def main():
    parser = GooeyParser(description='Iwara视频批量重命名工具.')
    parser.add_argument('target', help="选择目标文件夹", widget='DirChooser')
    return parser.parse_args()

if __name__ == '__main__':
    args = main()
    target = args.target + r'\\'
    process = CrawlerProcess()
    process.crawl(iwaraSpider)
    process.start()