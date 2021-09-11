import os
import re
import scrapy

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class iwaraSpider(scrapy.Spider):
    name = "renamer"

    def start_requests(self):
        urls = []
        for files in os.listdir("./"):
            if files.endswith("source.mp4"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                request = scrapy.Request(url=url, callback=self.parse)
                request.cb_kwargs['oldname'] = "./" + files
                yield request
            elif files.endswith("Source.mp4.xltd"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                print(url)

    def parse(self, response, oldname):
        print("-----------------------------------------")
        newname = response.css('a.username::text').get() + " - " + response.css('h1.title::text').get()
        newname = validateTitle(newname)
        newname = "./" + newname + ".mp4"
        print(oldname)
        print(newname)
        os.rename(oldname,newname)
        print("-----------------------------------------")