import pathlib
import string
import urllib.request as request
import urllib.parse as parse
import json
import pathlib


def download_file(url, rename, suffix="lrc"):
    response = request.urlopen(url)
    _data = response.read()

    with open(pathlib.Path.cwd().joinpath(rename + "." + suffix), 'wb') as file:
        file.write(_data)
    pass


lrc_api_url = "http://www.douqq.com/qqmusic/qqapi.php"


# 返回需要下载歌词的歌曲
# for sound in pathlib.Path("E:\MUSIC\华语").glob("**/*.flac"):
#     result = str(sound).replace(str(sound.suffix), '.lrc')
#     _result_path = pathlib.Path(result)
#     if not _result_path.exists():
#         _name = _result_path.name.strip(".lrc")
#         print(_name)
#         response = request.urlopen(lrc_api_url.format(name=_name))
#         _json = json.dump(response)
#         print(_json)


def main():
    _lrc_api_url = lrc_api_url  # Artist="周杰伦"
    # 千古
    parameter = {"mid": "https://y.qq.com/n/yqq/song/003HBeLJ1q4Pao.html"}
    # get请求 处理中文
    _lrc_api_url = parse.quote(_lrc_api_url, safe=string.printable)
    print(_lrc_api_url)
    # post请求要将data参数转码
    response = request.urlopen(_lrc_api_url, data=parse.urlencode(parameter).encode('UTF-8'))

    _json = json.load(response)
    json_obj = json.loads(_json)

    print(json_obj["lrc"])
    with open("D:/TEST.lrc", 'wb') as file:
        file.write(json_obj["lrc"].encode('utf-8'))
    # download_file(_json['result'][0]['lrc'], "周杰伦-枫")


main()
