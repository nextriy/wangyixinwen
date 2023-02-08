#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 0009 11:51
# @Author  : captain
# @Email   : 2067266431@qq.com
# @File    : 网易新闻内容爬取.py
# @Software: PyCharm

import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.cccom']
    start_urls = ['https://news.163.com/']
   #存储五个板块对应详情页的url
    models_urls = [] 


    #实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='C:\\Users\\Administrator\\Desktop\\就业爬虫学习路线\\编程学习\\爬虫学习\\张晓波老师爬虫学习\\第八章_scrapy框架\\wangyiPro\\wangyiPro\\spiders\\chromedriver.exe')

    def parse(self, response):
        try:
            li_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
            alist = [2,3,4,6,7]
            for index in alist:
                model_url = li_list[index].xpath('./a/@href').extract_first()
                self.models_urls.append(model_url)
        except:
            print("出错了")

        #依次对每一个板块对应的页面进行请求
        for url in self.models_urls:
            yield scrapy.Request(url,callback=self.parse_model)

    #每一个板块对应的新闻标题相关的内容都是动态加载（动态加载出来）
    def parse_model(self,response): #解析每一个板块页面中对应新闻的标题和新闻详情页的url
        # response.xpath()
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        # div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()

            # 实例化一个item对象
            item = WangyiproItem()
            item['title'] = title

            #对新闻详情页的url发起请求
            yield scrapy.Request(url=new_detail_url,callback=self.parse_detail,meta={'item':item})

    # 解析新闻内容（非动态加载出来）
    def parse_detail(self,response):
        # content = response.xpath('//*[@id="endText"]//text()').extract()
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)  # 过滤新闻内容
        item = response.meta['item']
        item['content'] = content

        yield item

    # 关闭浏览器
    def closed(self,spider):
        self.bro.quit()


