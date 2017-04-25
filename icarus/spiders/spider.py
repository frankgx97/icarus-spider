#coding:utf8
import sys
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from icarus.items import IcarusItem
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
 
class icarus_spider(CrawlSpider):#CrawlSpider类继承自Spider类，可以通过定义rules属性实现递归抓取
    name = "icarus"
    allowed_domains = ["icarus.silversky.moe"]#允许抓取的域名
    start_urls = ["http://icarus.silversky.moe:666/category/illustration/little-low-res-wallpaper/page/1"]#起始url
 
    #定义rules属性
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'\/category\/illustration\/little-low-res-wallpaper\/page\/\d')),#使用正则表达式匹配符合要求的网页
             callback=None,#回调函数
             follow=True#是否跟进此页上的url，如果callback为空的话则默认为true
            ),
        Rule(SgmlLinkExtractor(allow=(r'\/illustration\/\d+')),
             callback='download_image',
             follow=False
            ),
    )

    def download_image(self,response):
        sel = Selector(response)
        item = IcarusItem()
        image_url = sel.xpath("//a[@class='highslide-image']/@href").extract()
        item['image_url'] = [n for n in image_url]
        yield item   
 
    def parse_item(self, response):
    #抓取网页后会默认调用parse函数进行处理
        sel = Selector(response)
        #使用xpath选取html元素
        title = sel.xpath("//title").extract()
        item = IcarusItem()
        #由于sel.xpath().extract()返回的是一个list，所以先使用for遍历
        item['title'] = [n for n in title]#将title中的内容赋值给item
 
        yield item#将item中的数据交由pipeline进一步处理
