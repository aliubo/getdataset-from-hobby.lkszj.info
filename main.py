import requests
import json
import math
import csv

def getRequestAns(url, header, body):
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

def jsonToCsv(jsondata, path):
    keys = jsondata[0].keys()
    f = open(path, "w+", newline='', encoding='utf-8')
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jsondata)
    f.close()

def getAllTable():
    allItemCnt = 31237
    oneItem = 50
    pageNum = math.ceil(allItemCnt / oneItem)
    allTable = []
    for i in range(pageNum):
        print("进度：%d / %d"%(i+1, pageNum))
        ans = getOnePage(oneItem, i+1)
        jsondata = json.loads(ans)['list']
        allTable += jsondata
    return allTable

def main():
    ans = getAllTable()
    savedata = jsonToCsv(ans, "./lkstable.csv")
    print("完成")

if __name__ == '__main__':
    main()
