# -*- coding:utf-8 -*-
import requests
import json
import os

URL = {
    "bookletList": "https://api.juejin.cn/booklet_api/v1/booklet/listbybuyer",
    "booklet": "https://api.juejin.cn/booklet_api/v1/booklet/get",
    "section": "https://api.juejin.cn/booklet_api/v1/section/get"
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

cookie = ''

def setCookie(cookieStr):
    global cookie
    cookie = cookieStr
    headers["cookie"] = cookieStr

def getCookie():
    return cookie

def getBookletList(uid):
    data = {
        "cursor": "0",
        "limit": 100,
        "user_id": uid
    }
    res = requests.post(URL.get("bookletList"),
                        headers=headers, data=json.dumps(data))
    return res.json()

def getBooklet(id):
    data = {
        "booklet_id": id,
    }
    res = requests.post(URL.get("booklet"), headers=headers,
                        data=json.dumps(data))
    return res.json()


def getSection(id):
    data = {
        "section_id": id,
    }
    res = requests.post(URL.get("section"),
                        data=json.dumps(data), headers=headers)
    return res.json()


def ensureDir(dir):
    os.makedirs(dir, mode=0o777, exist_ok=True)


def saveBooklet(bid, content):
    folder = "./datas/%s" % bid
    file = "%s/%s.json" % (folder, "booklet")
    ensureDir(folder)
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)


def saveSectionList(bid, content):
    folder = "./datas/%s" % bid
    file = "%s/%s.json" % (folder, "sections")
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)


def saveSectionContent(bid, aid, content):
    folder = "./datas/%s" % bid
    file = "%s/%s.json" % (folder, aid)
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)


def downloadBooklet(bid):

    booklet = getBooklet(bid)
    print("booklet", booklet);
    print("获取小册信息成功，小册名称：", booklet["data"]["booklet"]["base_info"]["title"])
    saveBooklet(bid, json.dumps(booklet["data"]))

    sectionList = booklet["data"]["sections"]
    print("sections 长度：", len(sectionList))

    saveSectionList(bid, json.dumps(sectionList));
    sectionIds = list(
        map(lambda item: item["section_id"], sectionList))
    print("获取小册章节列表成功：", sectionIds)

    for sid in sectionIds:
        seContent = getSection(sid)
        saveSectionContent(bid, sid, json.dumps(seContent["data"]))
        print("Section ID为 %s 的章节下载完毕" % sid)
