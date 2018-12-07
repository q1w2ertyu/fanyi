import requests
import re


def main():
    while True:
        key = input("有道翻译:")
        if len(key) == 0:
            print("退出翻译系统")
            break
        fanyi(key)


def fanyi(key):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Mobile Safari/537.36"
    }

    data = {"inputtext": key,
            "type": "AUTO"
            }
    a = requests.post("http://m.youdao.com/translate", headers=headers, data=data)
    c = re.findall(r"translateResult[\d\D]+?/ul>", a.content.decode())
    d = re.findall(r"<li>([\d\D]+?)</li>",c[0])[0]
    print("有道翻译：",d,"\n")


if __name__== "__main__":
    main()
