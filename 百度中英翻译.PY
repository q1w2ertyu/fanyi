import requests
import json
import TEST
def main():
    while True:
        key = input("翻译(自动检测语言):")
        if len(key) == 0:
            print("退出翻译系统")
            break
        fanyi(key)
        TEST.fanyi(key)

def fanyi(key):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Mobile Safari/537.36"
    }
    data = {"query": key
            }
    a = requests.post("https://fanyi.baidu.com/langdetect", headers=headers, data=data)
    c = json.loads(a.content.decode())
    l = c["lan"]
    if l =="zh":
        to = "en"
    else:
        to ="zh"

    data_new ={"query": key,
            "from":l,
            "to":to
            }
    d = requests.post("https://fanyi.baidu.com/basetrans", headers=headers, data=data_new)
    f = json.loads(d.content.decode())["trans"][0]["dst"]
    print("百度翻译:",f)

if __name__== "__main__":
    main()
