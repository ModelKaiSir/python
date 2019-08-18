import pathlib
import urllib.request as request
import json

lrc_api_url = "http://api.dagoogle.cn/music/lrc?filename={name:}"
# 返回需要下载歌词的歌曲
for sound in pathlib.Path("E:\MUSIC\华语").glob("**/*.flac"):
    result = str(sound).replace(str(sound.suffix), '.lrc')
    _result_path = pathlib.Path(result)
    if not _result_path.exists():
        _name = _result_path.name.strip(".lrc")
        print(_name)
        response = request.urlopen(lrc_api_url.format(name=_name))
        _json = json.dump(response)
        print(_json)
