import pathlib
import re
import sys
import lrc_util

class ExitError(Exception):

    pass


def rename(sounds):
    if len(sounds) > 0:
        print(sounds)
        author = input("为该文件夹下的所有歌曲添加作者：")
        for _sound in sounds:
            if not bool(author and author.strip()):
                continue
            name = _sound.name
            name = name.replace(author, "").strip()
            new_name = "{} - {}".format(author, name)
            print(new_name)
            new_item = _sound.with_name(new_name)
            _sound.rename(new_item)
    pass


pass


def rename_not_author():
    # 检查哪些歌曲没有作者信息 正确的歌曲名称为 作者 - 歌名
    source_dir = pathlib.Path("E:\MUSIC\华语")
    child_dirs = [path for path in source_dir.iterdir() if path.exists() and path.is_dir()]

    result_flac = [[_path for _path in path.glob("**/*.flac") if len(_path.name.split(" - ")) <= 1] for path in
                   child_dirs]
    result_mp3 = [[_path for _path in path.glob("**/*.mp3") if len(_path.name.split(" - ")) <= 1] for path in
                  child_dirs]

    result_m4a = [[_path for _path in path.glob("**/*.mp3") if len(_path.name.split(" - ")) <= 1] for path in
                  child_dirs]

    for result_flac_item in result_flac:
        rename(result_flac_item)

    for result_mp3_item in result_mp3:
        rename(result_mp3_item)

    for result_m4a_item in result_m4a:
        rename(result_m4a_item)


pass


def reset_file_name():

    while True:
        source_dir = input("输入要处理的目录：")
        if source_dir == "DONE":
            raise ExitError("Done")

        for item in pathlib.Path(source_dir).glob("**/*.flac"):
            try:
                suffix = item.suffix
                new_name = re.sub("[0-9]+.?(-)?", "", str(item.stem)).strip()
                print(new_name)
                item.rename(item.with_name("{}{}".format(new_name, suffix)))
            except FileExistsError:
                print("文件名相同")
            except ExitError:
                print("操作完成")
                sys.exit()
    pass


#rename_not_author()
#reset_file_name()

#string = "02 -我不會愛"
#print(re.sub("[0-9]+.?(-)?","",string))
lrc_util.LrcDownload(pathlib.Path("E:\MUSIC\华语\其他\花粥 - 出山.lrc")).download_lrc()