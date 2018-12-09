import requests
import re
from multiprocessing import Pool,Manager
import os


def inputurl():
    sitename = input("SITE NAME(Http Encode):")
    print("Got the sitename!")
    print("-"*100)
    m3u8url = input("M3U8 URL:")
    print("Got the m3u8!")
    print("-" * 100)
    saveurl= input("Save in local path:")
    print("Got the path!")
    print("-" * 100)
    return sitename,m3u8url,saveurl


def judgesaveurl(root):
    if root =="":
        root = r"G:\movie"
        if not os.path.exists(root):
            os.makedirs(root)
    if not os.path.exists(root):
        os.makedirs(root)


def m3u8url(m3u8urls):
    with open(r"{}".format(m3u8urls),"r+") as c:
        m3u8content = c.read()
        urllist = re.findall(r"(https:[\D\d]+?.ts)",m3u8content)
        length =len(urllist)
    print("m3u8解析完毕，需要下载{}个链接".format(length))
    return urllist,length


def getts(sitename,array,len,saveurl):
    listid = len - array.qsize()
    url= array.get()
    headers = {
     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36",
     "referer": sitename,
    }
    a = requests.get(url,headers=headers)
    d = a.content
    with open(r"{}".format(saveurl)+"\\{}.ts".format(listid), "wb+") as e :
        e.write(d)
    print("成功写入第{}个文件".format(listid))
    print("-"*100)


def save(saveurl):
    root = saveurl
    list = os.listdir(path=root)
    writer = open(r"{}".format(root)+"\\all.ts","ab+")
    for thing in range(0,len(list)):
        with open(r"{}".format(root)+"\\{}.ts".format(thing),"rb") as tschunk:
            writer.write(tschunk.read())
        os.remove(r"{}".format(root)+"\\{}.ts".format(thing))
        print("完成分卷{}的拷贝".format(thing))
    writer.close()


def main():
    # inputurls函数得到网站引用，和M3U8本地地址，以及保存的本机根目录
    sitename,m3u8urls,saveurl = inputurl() 
    judgesaveurl(saveurl)
    # m3u8url函数得到m3u8的所有链接地址列表，以及链接的个数
    urllist,len = m3u8url(m3u8urls)
    # 创建以M3U8个数为大小的进程队列
    array = Manager().Queue(len)
    # 将M3U8链接列表中的元素加入进程队列
    for a in urllist: 
        array.put(a)
    # 创建进程池，进程最大5个进程
    pool = Pool(5)
    # 循环链接个数次，每一次循环开启进程，保持进程个数为5
    for NUM in range(0,len):
        # 每个进程必须要传入进程队列array！
        pool.apply_async(getts,(sitename,array,len,saveurl))
    # 固定进程池，等待所有进程终止
    pool.close()    
    pool.join()
    #将所有ts分段整合为1个大ts文件
    save(saveurl)
    print("-" * 100)
    print("Done!")
    print("-"*100)


if __name__ == "__main__":
    main()

