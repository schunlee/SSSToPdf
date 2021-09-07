import download
import mdToHtml
import subprocess
import json
import sys


def genPdf(title):
    # TODO:: 需要配置全局路径
    exePath = "wkhtmltopdf.exe"
    sourcePath = "./htmls/%s.html" % title
    targetPath = "./pdfs/%s.pdf" % title
    cmd = '"%s" --outline-depth 2 --footer-center [page] "%s" "%s"' % (
        exePath, sourcePath, targetPath)
    print(cmd)
    subprocess.call(cmd)


def downloadAndGenPdf(bid):
    download.downloadBooklet(bid)
    booklet = mdToHtml.getJSONData("./datas/%s/booklet.json" % bid)
    title = booklet["booklet"]["base_info"]["title"]
    print("开始生成html文件")
    mdToHtml.mdToHtml(bid, title)
    print("生成html文件完毕")
    print("开始生成%s.pdf" % title)
    genPdf(title)
    print("%s.pdf生成完毕" % title)


# downloadAndGenPdf("6901095904892321800")


def setCookie():
    cookieArr = json.loads(mdToHtml.readFile("./cookie.json"))
    cookieStr = " ;".join(
    list(map(lambda item: item.get("name") + "=" + item.get("value"), cookieArr)))
    download.setCookie(cookieStr)


def run():
    if len(sys.argv) < 2:
        return print("please input booklet")
    bid = sys.argv[1]
    print("booklet:%s" % (bid))
    setCookie();
    downloadAndGenPdf(bid)


run()
