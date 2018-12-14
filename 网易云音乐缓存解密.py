import os
import re
import struct
from pymediainfo import MediaInfo
import json
import sys
from time import sleep

# 输入缓存目录，不输则采用默认目录
inputdir = input("请输入加密歌曲的目录位置（没有在客户端更改过缓存目录则不用输入，回车即可）：")
if inputdir != "":
    temprootpath = inputdir
else:
    os.getenv("LOCALAPPDATA")
    temprootpath = os.getenv("LOCALAPPDATA") + r"\Netease\CloudMusic\Cache\Cache" + "\\"
print("加密歌曲缓存目录为：", temprootpath)
print("-" * 100)

# 设置歌曲转换地址，没有则设置默认目录为D:\1A
inputaimdir = input("请输入解密歌曲保存的目录（默认设置为D:\\1A）：")
if inputaimdir == "":
    inputaimdir = r"D:\1A"
if not os.path.exists(inputaimdir):
    os.mkdir(inputaimdir)
print("保存目录为：", inputaimdir)
print("-" * 100)

print("关于命名：如果歌曲内有名称信息，则自动命名。")
print("         如找不到名称信息，则需要手动命名。")
print("-" * 100)

# 获取.UC文件的列表
a = os.listdir(temprootpath)
songtemplist = ""
# 将名称加入字符串
for thing in a:
    songtemplist = songtemplist + thing + "\n"

# Re找到歌曲名单，生成文件位置
allsongs = re.findall(r".+?.uc", songtemplist, 0)

# 目录下找不到歌曲则退出
if allsongs == []:
    print("该目录下找不到任何加密的音乐，请确认！")
    sleep(2)
    sys.exit()

# 对列表中的所有单个歌曲，取每个字节与163做异或，写入新文件
num = 1
for song in allsongs:
    tempfile = temprootpath + song
    file = open(tempfile, "rb")
    path_aim = inputaimdir + "\\"
    song_file = path_aim + ".{}.mp3".format(num)
    new_file = open(song_file, "ab+")
    try:
        while True:
            a = file.read(1)
            b = struct.unpack('<B', a)
            c = b[0] ^ 163
            d = struct.pack('<B', c)
            new_file.write(d)
    except struct.error:
        pass
    file.close()
    new_file.close()

    # 获取歌曲的媒体信息字符串，用json导入生成字典。以字典中的名称信息命名歌曲。
    media_info = MediaInfo.parse(song_file)
    c = json.loads(media_info.to_json())
    if "track_name" in c["tracks"][0]:
        name = (c["tracks"][0]["track_name"])
        song_new_name = path_aim + name + ".mp3"
        if not os.path.exists(song_new_name):
            try:
                os.rename(song_file, song_new_name)
            except:
                pass
        else:
            print("歌曲{}存在,默认替换".format(name))
            os.remove(song_new_name)
            os.rename(song_file, song_new_name)
        print(song_new_name + " COMPLETED!!!")
        print("-" * 100)
    else:
        print(song_file + " COMPLETED!!!")
        print("-" * 100)
    # 删除缓存歌曲，防止未来重新下载

    num += 1
