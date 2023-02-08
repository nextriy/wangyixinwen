# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from time import sleep

class WangyiproDownloaderMiddleware(object):
    def process_request(self, request, spider):
        return None
    

     #该方法拦截五大板块对应的响应对象，进行篡改
    def process_response(self, request, response, spider):
        # 获取了在爬虫类中定义的浏览器对象
        self.bro = spider.bro  
        # 挑选出指定的响应对象进行篡改，通过request指定response
        if request.url in spider.models_urls:
            #五个板块对应的url进行请求
            self.bro.get(request.url) 
            sleep(3)
            page_text = self.bro.page_source  #包含了动态加载的新闻数据
            # 实例化一个新的响应对象（符合需求：包含动态加载出的新闻数据），替代原来旧的响应对象
            # 基于selenium便捷的获取动态加载数据
            new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)

            return new_response
        else:
            #response #其他请求对应的响应对象
            return response


    def process_exception(self, request, exception, spider):
        pass
