# coding:utf-8
import requests
import agent
import json
from lxml import etree
from redis import *
import time
# try:
class lagou_python():
    def __init__(self):
        #主页报头
        self.headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Connection":"keep-alive",
                "Content-Length":"26",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie":"user_trace_token=20170612174453-7e824176a19d4c89ba8eab3fd11b6fa0; LGUID=20170612174503-cf10c07f-4f53-11e7-9ab4-5254005c3644; JSESSIONID=ABAAABAACDBABJBEC7D582EA93B3D0402F2440A574E2317; _gat=1; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2F%3Ftn%3Dbaiduhome_pg; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _putrc=40581905F95937C1; login=true; unick=%E7%8E%8B%E4%B9%8B%E7%92%9E; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; SEARCH_ID=b2f75b957f174b02a18d6f9c21d7ca07; index_location_city=%E5%8C%97%E4%BA%AC; X_HTTP_TOKEN=b5dcfc9f0caa0aa0179a429ad0ef2013; _gid=GA1.2.382590469.1498356592; _ga=GA1.2.366575400.1497260700; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1498377334,1498459040,1498465360,1498528624; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1498529037; LGSID=20170627095705-ebadb6cd-5adb-11e7-9ecf-5254005c3644; LGRID=20170627100358-e1e2bdec-5adc-11e7-8c9e-525400f775ce",
                "Host":"www.lagou.com",
                "Origin":"https://www.lagou.com",
                "Referer":"https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
                "X-Anit-Forge-Code":"0",
                "X-Anit-Forge-Token":"None",
                "X-Requested-With":"XMLHttpRequest"
            }
        #职位报头
        self.headers2={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "user_trace_token=20170612174453-7e824176a19d4c89ba8eab3fd11b6fa0; LGUID=20170612174503-cf10c07f-4f53-11e7-9ab4-5254005c3644; JSESSIONID=ABAAABAACDBABJBEC7D582EA93B3D0402F2440A574E2317; X_HTTP_TOKEN=b5dcfc9f0caa0aa0179a429ad0ef2013; SEARCH_ID=df832fbc71a24baca2b2813d1c20c782; index_location_city=%E5%8C%97%E4%BA%AC; _putrc=40581905F95937C1; login=true; unick=%E7%8E%8B%E4%B9%8B%E7%92%9E; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=search_code; _gid=GA1.2.382590469.1498356592; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1498377334,1498459040,1498465360,1498528624; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1498555557; _ga=GA1.2.366575400.1497260700; LGSID=20170627163048-ebfde400-5b12-11e7-9ee4-5254005c3644; LGRID=20170627172559-a13a1ee4-5b1a-11e7-9ee6-5254005c3644",
            "Host": "www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?oquery=python&fromSearch=true&labelWords=relative&city=%E5%8C%97%E4%BA%AC",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
            
            
        }
        #代理ip设置
        self.proxies = {"http":"http://61.176.215.7:8080"}
        
        self.city = raw_input("输入城市")
        self.position = raw_input("输入职位")
        self.page = int(raw_input("输入页数"))
    
    def spider_main(self):#对主页进行爬虫提取
        i = 1
        while i <= self.page:
            formdata = {"first": "true", "pn": str(i), "kd": self.position}
            #px排序规则 new,default;gj 工作年限:"3年及以下"
            # params = {"city": self.city, "needAddtionalResult": "false"}
            params = {"city": self.city, "needAddtionalResult": "false","px":"new","gj":"3年及以下"}
            url = "http://www.lagou.com/jobs/positionAjax.json"
            #对主页进行post请求
            response = requests.post(url,
                                     params=params,
                                     data=formdata,
                                     headers=self.headers,
                                     proxies=self.proxies
                                     )
            response = response.json()
            print "正在读取第"+str(i)+"页....."
            self.json_url(response)#json分析提取
            print "第"+str(i)+"页结束........"
            i += 1
        print "抓取完毕"
    
    def json_url(self,info):#json分析提取
        # url = "https://www.lagou.com/jobs/3272647.html"#职位url
        info = info["content"]["positionResult"]["result"]
        for id in info:
            # 提取职位id
            position_id = id["positionId"] #int
            # 提取公司名称
            global company_name
            company_name = id["companyShortName"]
            company_name = company_name.encode("utf-8") #str

            # info_1[company_name] = position_id#公司名与id字典配对
            
            #公司名列表
            global company_name_list
            company_name_list = []
            company_name_list.append(company_name)
            
            #职位id列表
            global position_id_list
            position_id_list = []
            position_id_list.append(position_id)
            
            #对职位信息进行抓取
            url = "https://www.lagou.com/jobs/" + str(position_id) + ".html"
            self.url_spider(url)
    
    def url_spider(self,url):#对职业要求进行提取数据

        html = requests.get(url,headers =self.headers2,proxies = self.proxies).text
        html = etree.HTML(html)
        #xpath提取数据
        job_info = html.xpath('//dd[@class="job_bt"]/div//text()')
        # job_text = html.xpath('/html/body/div[2]/div/div[1]/div/span/text()')
        data = ""
        #整合职位要求data数据
        for info in job_info:
            time.sleep(0.2)
            # print type(info)#<type 'lxml.etree._ElementUnicodeResult'>
            data = data +"\n" + info
        self.redis_w(company_name,data)# 传入redis数据库

        
    def redis_w(self,name,info):# 传入redis数据库
        #默认为127.0.0.1
        print "正在录入"+name+"信息...."
        data = StrictRedis(host="localhost",port = 6379,db=0)
        data.set(name,info)

        print name+"录入结束"
    
if __name__ == '__main__':
    run = lagou_python()
    run.spider_main()
        
# except Exception,e:
#     print Exception,":",e
#
#     with open("error.txt","ab") as f:
#         f.write(str(e))