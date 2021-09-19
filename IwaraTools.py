import os
import re
from gooey import Gooey, GooeyParser
import scrapy
from scrapy.crawler import CrawlerProcess

target = "./"
todo = False
log = False

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class iwaraSpider(scrapy.Spider):
    name = "renamer"
    logfile = None

    def start_requests(self):
        if log:
            self.logfile = open(target + "\IwaraToolsLog.txt", "a", encoding="utf-8")
        for files in os.listdir(target):
            if files.lower().endswith("source.mp4"):
                url = 'https://www.iwara.tv/videos/'+ files.split("_")[1]
                request = scrapy.Request(url=url, callback=self.parse)
                request.cb_kwargs['oldname'] = target + files
                yield request
            elif files.lower().find("source.mp4.")!=-1 and todo:
                print('发现未完成下载 https://www.iwara.tv/videos/'+ files.split("_")[1])
                if log:
                    logfile.write( '发现未完成下载 https://www.iwara.tv/videos/'+ files.split("_")[1] +"\n")

    def parse(self, response, oldname):
        newname = response.css('a.username::text').get() + " - " + response.css('h1.title::text').get()
        newname = validateTitle(newname)
        newname = target + newname + ".mp4"
        if os.path.exists(newname):
            print(newname + "已存在,请自行修改" + oldname)
            return
        print(oldname + " 重命名为 " + newname)
        if log:
            self.logfile.write( oldname + " 重命名为 " + newname +"\n")
        os.rename(oldname,newname)

@Gooey(
    program_name='IwaraTools',
    image_dir='./',
    language="chinese")
def main():
    parser = GooeyParser(description='Iwara视频批量重命名工具.')
    parser.add_argument('target', help="选择目标文件夹", widget='DirChooser')
    parser.add_argument('--info', help="显示调试信息", action='store_true')
    parser.add_argument('--todo', help="列举未下载完的文件", action='store_true')
    parser.add_argument('--log', help="保存记录到IwaraToolsLog.txt", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = main()
    todo = args.todo
    log = args.log
    target = args.target + r'\\'
    level = 'WARNING'
    if args.info:
        level = 'INFO'
    process = CrawlerProcess({'LOG_LEVEL': level})
    process.crawl(iwaraSpider)
    process.start()