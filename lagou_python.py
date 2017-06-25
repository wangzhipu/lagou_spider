# coding:utf-8
import requests
import agent
import json
class lagou_python():
    def __init__(self):
        self.headers = agent.headers
        self.url = ("http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false")
        
        
    def page(self):
        pass
        i = 1
        while i<2:
            
            data = {
                "first": "false",
                "pn": i,
                "kd": "pyhton爬虫",
        
            }
            params = {
                "gj": "3年及以下",
                    "px":"default",
            "city":"北京",
            "needAddtionalResult":"false"
            }

            response = requests.post(self.url,params = params,data = data,headers = self.headers)
            response = response.text
            
            # response = response.json()
            # print type(response)
            self.write(response)
            i += 1
    
    def spider(self,response_info):
        print response_info
        
    
    def write(self,info):
        info = json.dumps(info, ensure_ascii = False)
        print type(info)

        info = info.encode("utf-8")
        print type(info)
        with open("filename.json","wb") as f:
            f.write(info)



if __name__ == '__main__':
    run = lagou_python()
    run.page()