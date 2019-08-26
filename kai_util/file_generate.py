import pathlib
import itertools
# 文件路径生成器

'''返回对应source_dir在target_dir目录下不存在或大小不一致的文件'''


def generate_not_exists_file(space, source_dir, target_dir, tag, path: pathlib.Path):
    # 返回需要复制的文件
    if path.is_dir():
        space += ' '
        for _p in path.iterdir():
            for _result in generate_not_exists_file(space, source_dir, target_dir, tag, _p):
                yield _result
            pass
    elif path.is_file():
        target_path = pathlib.Path(str(path.absolute()).replace(source_dir, target_dir + "\\" + tag))

        # 不存在的文件和大小不一致的文件
        if not target_path.exists():
            yield path, target_path
        else:
            a = target_path.stat().st_size
            b = path.stat().st_size
            if a != b:
                target_path.unlink()
            yield path, target_path
    pass
    pass


'''返回没有歌词的歌曲的路径'''


def generate_not_exists_lrc_sound(source_dir):

    def glob_file(_result, _source, _pattern):
        for _file in _source.glob(_pattern):
            _file_lrc = _file.with_suffix(".lrc")
            if not _file_lrc.exists():
                _result.append(_file_lrc)

    source_path = pathlib.Path(source_dir)
    if source_path.exists():
        # 同目录下对应的歌词文件
        result = []
        patterns = ["**/*.flac", "**/*.mp3"]
        for pattern in patterns:
            glob_file(result, source_path, pattern)

        for r in result:
            yield r

    pass


# 制造一个旋转的线的效果
def progress_tag():
    tags = ["\\", "|", "/", "—"]
    i = -1
    while True:
        i += 1
        if i >= len(tags):
            i = 0
        yield tags[i]
