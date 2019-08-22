import pathlib
import string
import urllib.request as request
import urllib.parse as parse
import json
import time
import re
import math
import jieba
import wordcloud as wc
import numpy
from PIL import Image


class LrcDownload:

    @staticmethod
    def generate_mid(author, json_object):

        def checking(singer_author, _title, compare_author):


            # 不要伴奏
            if _title.find("伴奏") != -1:
                return False
            # 如果歌曲没有作者信息则不判断作者
            if not bool(compare_author and compare_author.strip()):
                return True
            elif re.match(".*({})+?".format(compare_author), singer_author) is not None:
                return True

            return False

        pass

        def log(_mid, _name, _title, singer):
            msg = "info {mid:}:{name:}:{title:}:{signer:}"
            print(msg.format(mid=_mid, name=_name, title=_title, signer=singer))

        pass

        for detail in json_object["data"]["song"]["list"]:

            signer = detail["singer"][0]
            mid = detail["mid"]
            name, title = detail["name"], detail["title"]
            # 优先排除伴奏和作者不对的歌词
            if checking(signer["name"], title, author):
                log(mid, name, title, signer["name"])
                yield detail
        pass

    def __init__(self, source_path: pathlib.Path):
        # 解析qq音乐歌曲
        self.api_url = "http://www.douqq.com/qqmusic/qqapi.php"
        # 通过qq音乐获取歌曲信息
        self.qq_music_api_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid={timetamp:}&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={sound:}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
        # 通过qq音乐获取歌曲评论
        self.qq_music_comment_cfg_url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid={timetamp:}&reqtype=1&biztype=1&topid={id:}&cmd=4&needmusiccrit=0&pagenum=0&pagesize=0&lasthotcommentid=&domain=qq.com"
        self.qq_music_comment_url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid={timetamp:}&reqtype=2&biztype=1&topid={id:}&cmd=8&needmusiccrit=0&pagenum={pagenum:}&pagesize={pagesize:}&lasthotcommentid=&domain=qq.com&ct=24&cv=10101010"

        self.source_path = source_path
        self.suffix = source_path.suffix
        file_name = re.sub(r"[0-9(.lrc)_]+", "", self.source_path.name)
        file_name = file_name.split("-")
        if len(file_name) > 1:
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

    pass

    def get_sound_info(self, mode="DEF"):
        print("{} : {} ".format(self.author, self.sound))

        result_json = LrcDownload.send_request(
            self.qq_music_api_url.format(timetamp=int(float(time.time())), sound=self.sound))

        if result_json is not None:
            try:
                if mode == "DEF":
                    return self.parse_song(json.load(result_json))
                else:
                    # 尝试将返回的数据解析成字符串
                    json_text = result_json.read().decode("utf-8")
                    json_text = json_text[json_text.find("{"):json_text.rfind("}") + 1]
                    if bool(json_text and json_text.strip()):
                        return self.parse_song(json.loads(json_text))
                    else:
                        return None
            except BaseException as e:
                print(e)
                return self.get_sound_info(mode="OTHER")
        else:
            return None
        pass

    def get_sound_mid(self):

        sound = self.get_sound_info()
        return sound["mid"]

    pass

    # 数据分析 分析歌曲下面的评论
    def load_comment(self):

        # 获取评论的相关信息（评论条数等信息）
        def get_comment_cfg(url):
            rep = LrcDownload.send_request(url)
            return json.load(rep)
            pass

        def get_comments(url):
            rep = LrcDownload.send_request(url)
            return json.load(rep)
            pass

        def save_data(comment_text):
            path = pathlib.Path("D:/comments.txt")
            with path.open(mode='ab+') as text:
                insert = comment_text + "\n"
                text.write(insert.encode('utf-8'))

            pass

        # 先获取到id 再获取歌曲评论id 再获取评论信息 保存到txt中
        sound_id = self.get_sound_info()
        if sound_id is not None:
            sound_id = sound_id["id"]
            url_get_comment_cfg = self.qq_music_comment_cfg_url.format(timetamp=int(float(time.time())), id=sound_id)
            comment_cfg = get_comment_cfg(url_get_comment_cfg)

            split_size = 25
            comment_total = comment_cfg["commenttotal"]
            for num in range(math.ceil(comment_total / split_size)):
                url_get_comments = self.qq_music_comment_url.format(timetamp=int(float(time.time())), id=sound_id,
                                                                    pagenum=num,
                                                                    pagesize=split_size)
                comment = get_comments(url_get_comments)
                for _comment in comment["comment"]["commentlist"]:
                    try:
                        print("写入评论中。。。")
                        if _comment is not None:
                            save_data(_comment["rootcommentcontent"])
                    except KeyError as e:
                        print("没有评论 error{}".format(str(e)))

                pass

            pass
        pass

    pass

    def analysis_comment(self):
        # 打开文件
        path = pathlib.Path("D:/comments.txt")
        with path.open(mode='r', encoding='utf-8') as text:

            comments = "".join(text.read())
            comments = comments.replace("\n", "")
            comments = comments.replace("该评论已经被删除", "")

            comments = re.sub(r"[\[em\]].*[/\[em\]]", "", comments)

            jieba.add_word("白子画")
            jieba.add_word("少了些")
            jieba.add_word("糖宝")
            jieba.add_word("单春秋")
            jieba.add_word("洪荒之力")

            seg_list = jieba.cut(comments, cut_all=False)
            result = " ".join(seg_list)
            bg = numpy.array(Image.open("D:/bg.png"))
            wc_instance = wc.WordCloud(background_color="white", mask=bg, max_words=600, max_font_size=50,
                                       random_state=42
                                       , font_path="C:\WINDOWS\Fonts\simhei.ttf").generate(result)
            image = wc_instance.to_image()
            image.show()

    def parse_song(self, json_obj):
        for detail in LrcDownload.generate_mid(self.author, json_obj):
            # 排除伴奏和作者不对的歌曲
            return detail

    @staticmethod
    def send_request(url, data=None):

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://y.qq.com/portal/search.html",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }

        _url = parse.quote(url, safe=string.printable)

        req = request.Request(url=_url, headers=headers)

        try:
            response = request.urlopen(req, data)
            return response
        except BaseException as e:
            print(e)
        pass

json_text = ""
print(bool(json_text and json_text.strip()))