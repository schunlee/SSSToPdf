from os import error
import download
import mdToHtml
import subprocess
import json
import sys
import uutils


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
    booklet = download.downloadBooklet(bid)

    # 判断是否已经生成功过
    title = booklet["booklet"]["base_info"]["title"]
    fname = "%s.pdf" % title
    print("检查%s是否存在" % fname)
    if(uutils.isFileExisted("./pdfs/%s" % fname) == True):
        return print("%s.pdf已存在，跳过" % fname)

    download.downloadSections(bid, booklet["sections"])
    print("开始生成html文件")
    mdToHtml.mdToHtml(bid, title)
    print("生成html文件完毕")
    print("开始生成%s.pdf" % title)
    genPdf(title)
    print("%s.pdf生成完毕" % title)


def downloadAllAndGenPdf(uid):
    res = download.getBookletList(uid)
    bIds = list(map(lambda b: b["booklet_id"], res["data"]))
    for bid in bIds:
        try:
            downloadAndGenPdf(bid)
        except Exception as err:
            print("download error:", err)
            print("download Booklet %s failed, continue next one" % bid)


def setCookie():
    cookieArr = json.loads(mdToHtml.readFile("./cookie.json"))

    if len(cookieArr) <= 0 or type(cookieArr) == str:
        return False

    cookieStr = " ;".join(
        list(map(lambda item: item.get("name") + "=" + item.get("value"), cookieArr)))
    download.setCookie(cookieStr)
    return True


def run():
    if len(sys.argv) < 2:
        return print("please input booklet")

    id= sys.argv[1];
    choice = '';
    if len(sys.argv) >= 3:
        choice = sys.argv[2]

    print(id, choice);
    success = setCookie()
    if success == False:
        return print("请检查cookie是否正确设置, 必须是有效的对象列表")
    if choice != 'u':
        print("booklet id:%s" % (id))
        downloadAndGenPdf(id)
    else:
        print("user id:%s" % (id))
        downloadAllAndGenPdf(id)


run()


# downloadAllAndGenPdf("131597122679661")
# downloadAndGenPdf("6901095904892321800")
