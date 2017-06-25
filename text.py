#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import json

class LagouSpider:
    def __init__(self):
        #self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
        self.headers = {
                "Accept" : "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding" : "gzip, deflate, br",
                "Accept-Language" : "zh-CN,zh;q=0.8",
                "Connection" : "keep-alive",
                "Content-Length" : "64",
                "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie" : "user_trace_token=20170427164201-69a5df4baad542d78c914d34215f7dfd; LGUID=20170427164202-623da73e-2b25-11e7-b3e5-5254005c3644; JSESSIONID=ABAAABAAAFCAAEG4D909E1D839661654758E1501BDB6ACD; _gid=GA1.2.787653314.1497537104; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497144860,1497537101,1497511530; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497511530; _ga=GA1.2.1589758517.1493282521; LGSID=20170615143141-4b249c2c-5194-11e7-9c5e-5254005c3644; LGRID=20170615152528-ce9d78ec-519b-11e7-9c5e-5254005c3644; TG-TRACK-CODE=index_navigation; SEARCH_ID=b089e64c92c0471cae3212d2ce4e5b43; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%8C%97%E4%BA%AC",
                "Host" : "www.lagou.com",
                "Origin": "https://www.lagou.com",
                "Referer" : "https://www.lagou.com/zhaopin/quanzhangongchengshi/?labelWords=label",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
                "X-Anit-Forge-Code" : "0",
                "X-Anit-Forge-Token" : "None",
                "X-Requested-With" : "XMLHttpRequest"
            }
        self.baseURL = "http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
        self.positionName = raw_input("请输入需要查询的职位名:")
        self.cityName = raw_input("请输入需要查询的城市名:")
        self.endPage = int(raw_input("请输入需要爬取的页数:"))
        self.page = 1

    def startWork(self):
        # 报是存储了所有职位的信息
        position_list = []
        # 循环发送每一页的请求
        while self.page <= self.endPage:
            # 获取每一页的职位信息列表
            item_list = self.loadPage()
            # 将数据保存在position_list里
            position_list = position_list + item_list
            # 每发出去一个页面的请求，self.page 自增1
            self.page += 1
        # 调用方法将数据写入到本次磁盘文件里
        self.writePage(position_list)

    def loadPage(self):
        # 表单数据
        formdata = {"first" : "true", "pn" : self.page, "kd" : self.positionName}
        # 查询字符串
        params = { "city" : self.cityName, "needAddtionalResult" : "false"}
        #pa = urllib.urlencode(params)
        #url = self.baseURL + "&" +  pa
        #urllib2.Request(url, data, headers)
        # urllib2.urkopen(request)

        # 将表单数据、查询字符串参数，和请求报头一起发送 post 请求,获取响应
        response = requests.post(self.baseURL, params = params, data = formdata, headers = self.headers)
        time.sleep(1)
        # 直接从响应里调取json格式的数据
        #jsonobj = json.loads(response.read()) # urllib2用法
        jsonobj = response.json()
        #print jsonobj
        # 一直获取到result数据，就是每一页的15条职位信息的列表
        result_list = jsonobj["content"]["positionResult"]["result"]
        """
        item_list = []
        for result in result_list:
            item = {}
            item["companyFullName"] = result["companyFullName"]
            item["city"] = result["city"]
            item["salary"] = result["salary"]
            item["district"] = result["district"]
            item["createTime"] = result["createTime"]
            item["education"] = result["education"]
            item["workYear"] = result["workYear"]
            item_list.append(item)
        """
        print "获取数据成功... %s 页" % self.page
        return result_list

    def writePage(self, position_list):
        with open("lagou.json", "w") as f:
            # ensure_ascii 表示禁用ascii编码格式来处理中文，使用Unicode处理
            content = json.dumps(position_list, ensure_ascii = False)
            # 将数据转码为utf-8
            f.write(content.encode("utf-8"))
            #f.write(content)


if __name__ == "__main__":
    spider = LagouSpider()
    spider.startWork()







