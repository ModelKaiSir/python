import pathlib
import string
import urllib.request as request
import urllib.parse as parse
import json
import time
import re


class LrcDownload:

    @staticmethod
    def generate_lrc(author, json_object):
        for detail in json_object["data"]["song"]["list"]:
            # 优先排除伴奏和作者不对的歌词
            if detail["singer"][0]["name"].find(author) != -1 and detail["title"].find("伴奏") == -1:
                print("info {mid:}:{name:}:{title:}:{signer:}".format(mid=detail["mid"], name=detail["name"], title=detail["title"], signer=detail["singer"][0]["name"]))
                yield detail
        pass

    def __init__(self, source_path: pathlib.Path):
        # 解析qq音乐歌曲
        self.api_url = "http://www.douqq.com/qqmusic/qqapi.php"
        # 通过qq音乐获取歌曲信息
        self.qq_music_api_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid={timetamp:}&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={sound:}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"

        self.source_path = source_path
        self.suffix = source_path.suffix
        file_name = re.sub(r"[0-9(.lrc)_]+", "", self.source_path.name)
        file_name = file_name.split("-")
        if len(file_name) > 1 :
            self.author, self.sound = file_name[0].strip(), file_name[1].strip()
        else:
            self.author, self.sound = "", file_name[0].strip()
        pass

    def download_lrc(self):

        mid = self.get_sound_mid()
        if mid is None:
            print("{} 沒有找到歌词！".format(self.source_path))
            return
        parameter = {"mid": mid}
        lrc_obj = LrcDownload.send_request(self.api_url, data=parse.urlencode(parameter).encode("UTF-8"))
        _lrc_obj = json.loads(json.load(lrc_obj))

        with open(self.source_path, 'wb') as file:
            file.write(_lrc_obj["lrc"].encode('utf-8'))

    def get_sound_mid(self):

        print("{} : {} ".format(self.author, self.sound))

        result_json = LrcDownload.send_request(
            self.qq_music_api_url.format(timetamp=int(float(time.time())), sound=self.sound))
        if result_json is not None:
            mid = self.parse_song(json.load(result_json))
            return mid
        else:
            return None

    pass

    def parse_song(self, json_obj):
        print(json_obj["data"]["song"]["list"])
        for detail in LrcDownload.generate_lrc(self.author, json_obj):
            # 排除伴奏和作者不对的歌曲
            return detail["mid"]

    @staticmethod
    def send_request(url, data=None):

        _url = parse.quote(url, safe=string.printable)

        try:
            response = request.urlopen(_url, data)
            return response
        except BaseException as e:
            print(e)
        pass
