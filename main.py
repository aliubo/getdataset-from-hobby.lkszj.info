import requests
import json
import math
import csv

def getRequestAns(url, header = {}, body = ''):
    res = requests.post(url, body, headers= header)
    return res.text

def generateHeader():
    return {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

def generateBody(pageSize, pageNum):
    template = '{"searchStr":"", "pageSize":"%s", "pageNum":"%s","order":""}'
    return template%(pageSize, pageNum)

def getOnePage(pageSize, pageNum):
    url = 'http://hobby.lkszj.info/search'
    return getRequestAns(url, generateHeader(), generateBody(pageSize, pageNum))

def getTotalNum():
    url = 'http://hobby.lkszj.info/random'
    res = getRequestAns(url, generateHeader())
    return json.loads(res)['count']

def jsonToCsv(jsondata, path):
    keys = jsondata[0].keys()
    f = open(path, "w+", newline='', encoding='utf_8_sig')
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jsondata)
    f.close()

def getAllTable():
    totalNum = getTotalNum()                    # 获取总数量
    onePageNum = 50                             # 每页获取数量，经测试最多50条
    pageNum = math.ceil(totalNum / onePageNum)  # 页数 
    allTable = []

    print("---------------------")
    print("总数据条目  :", totalNum)
    print("每页下载数量:", onePageNum)
    print("总页数:", pageNum)
    print("---------------------")
    print("开始爬取...")

    for i in range(pageNum):
        # 显示进度
        if i%50 == 0:
            print("\n总页数%d, 进度 %4d-%4d: "%(pageNum, i+1, min(i+50,pageNum)), end='')
        print("#", end='')  
        # 获取并处理数据
        ans = getOnePage(onePageNum, i+1)
        jsondata = json.loads(ans)['list']
        allTable += jsondata
    return allTable

def main():
    ans = getAllTable()
    jsonToCsv(ans, "./lkstable.csv")
    print("\n完成")

if __name__ == '__main__':
    main()
