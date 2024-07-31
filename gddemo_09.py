# _*_ coding : utf-8 _*_
# @Time : 2024/7/25 17:07
# @Author : zl
# @File : gddemo_09
# @Project : pythonProjectzl
# url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
# cname: 南京
# pid:
# pageIndex: 2
# pageSize: 10

# cname: 南京
# pid:
# pageIndex: 1
# pageSize: 10

import urllib.request
import urllib.parse

import jsonpath
import pandas
import sqlite3
import json

# df =pandas.DataFrame()
# df.head

# with sqlite3.connect('') as db:
#     df.to_sql('',con=db)

def creat_request(page):
    baseurl = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    data = {
        'cname': '南京',
        'pid': '',
        'pageIndex': page,
        'pageSize': '10'
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    request = urllib.request.Request(url=baseurl, headers=headers, data=data)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # json.loads()
    return content


def down_load(page, content):
    with open('kfc' + str(page) + '.json', 'w', encoding='utf-8') as fp:
        fp.write(content)
def jsonopen(page):
    with open('kfc'+str(page)+'.json','r',encoding='utf-8') as file:
        obj = json.load(file)
        objpandas = pandas.json_normalize(obj,max_level=2)
        print(objpandas)
        store = jsonpath.jsonpath(obj,'$..storeName')
        address = jsonpath.jsonpath(obj,'$..addressDetail')
        province = jsonpath.jsonpath(obj,'$..provinceName')
        city = jsonpath.jsonpath(obj,'$..cityName')
        # l=len(store),l的值由rownum判断为好点的处理
        i = 0
        l = 10
        for  i in range(0,l):
            print(f"store : {store[i]},province : {province[i]},city : {city[i]},address : {address[i]}")
            i=i+1


if __name__ == '__main__':
    start_page = int(input('input start:'))
    end_page = int(input('input end:'))
    for page in range(start_page, end_page + 1):
        request = creat_request(page)
        content = get_content(request)
        down_load(page, content)
        jsonopen(page)
