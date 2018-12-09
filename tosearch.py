import re
import json
import requests
from lxml import etree

def getresponse(serachname):
    site = "https://sukebei.nyaa.si/"
    append ="?f=0&c=0_0&q={}".format(serachname)
    url =site+append
    data= {"f": "0",
    "c": "0_0",
    "q": serachname}
    response = requests.get(url,data=data).content.decode()
    html = etree.HTML(response)
    titles = html.xpath("//td[@colspan=2]/a/@title")
    sizes =  html.xpath("//td[@colspan=2]/../td[4]/text()")
    magnets= html.xpath("//i[@class=\"fa fa-fw fa-magnet\"]/../@href")
    content=[]
    contentslist=[]
    for a in range(len(titles)):
        content.append(titles[a])
        content.append(sizes[a])
        content.append(magnets[a])
        contentslist.append(content)
        content=[]
    for a in contentslist:
        for b in a:
            print(b,"\n")
        print("\n")

def main():
    while 1:
        search = input("Search:")
        if search:
            getresponse(search)
        else:
            break

if __name__=="__main__":
    main()
