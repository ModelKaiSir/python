import pathlib
import re


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
    source_dir = pathlib.Path("G:\MUSIC\华语")
    child_dirs = [path for path in source_dir.iterdir() if path.exists() and path.is_dir()]

    result_flac = [[_path for _path in path.glob("**/*.flac") if len(_path.name.split(" - ")) <= 1] for path in
                   child_dirs]
    result_mp3 = [[_path for _path in path.glob("**/*.mp3") if len(_path.name.split(" - ")) <= 1] for path in
                  child_dirs]

    for result_flac_item in result_flac:
        rename(result_flac_item)

    for result_mp3_item in result_mp3:
        rename(result_mp3_item)


pass

# for item in pathlib.Path("G:\MUSIC\华语").glob("**/*.flac"):
#     try:
#         suffix = item.suffix
#         new_name = re.sub("(.*[0-9]|-|\+|\.)+?", "", str(item.stem)).strip()
#         print(new_name)
#         item.rename(item.with_name("{}{}".format(new_name, suffix)))
#     except FileExistsError:
#         print("文件名相同")

rename_not_author()
