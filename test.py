import mdToHtml;
import download
import json

cookieArr =  json.loads(mdToHtml.readFile("./cookie.json"))
cookieStr = " ;".join(list(map(lambda item: item.get("name") + "=" + item.get("value") , cookieArr)));

download.setCookie(cookieStr)

download.downloadBooklet("6901095904892321800")