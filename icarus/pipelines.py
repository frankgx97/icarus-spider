# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import os
from db import *
 
reload(sys)
sys.setdefaultencoding('utf8')

url_prefix = 'http://static.guoduhao.cn/nyanfm/bg/'
download_path = '/var/web/static/nyanfm/bg/'

class IcarusPipeline(object):
    def process_item(self, item, spider):
        print '============='
        print item['image_url'][0]
        bg = Bg(
            url=url_prefix + item['image_url'][0].split('/')[7]
        )
        try:
            bg.save()
            print '##db wrote##'
        except:
            print '!!!db failed!!!'
        #这不是正确的下载文件的方法，不要学我
        os.system("wget '"+item['image_url'][0]+"' -P '"+download_path+"'")
        print '*************'