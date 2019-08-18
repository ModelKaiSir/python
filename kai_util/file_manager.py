import pathlib
import time
import subprocess
import sys
import curses


# 文件管理工具
class CopyFileSystem:
    def __init__(self):
        self.title = "复制文件工具"
        self.tips = "检查输入的source_dir目录下所有文件与target_dir目录对比，将不存在于target_dir目录的文件复制过来到" \
                    "target_dir"

        # 终端模式
        self.curses_mode = False
        self.window = None
        self.tips_point = 0
        self.error_msg_point = 30
        self.progress_point = 10

        self.read_size = 4096

        self.input_source_msg = "输入源目录："
        self.input_target_msg = "输入目标目录："

        pass

    def add_info(self, x, string):
        if self.curses_mode:
            self.window.addstr(x, len(string), string)
        else:
            print(string)

    def start(self, window):
        self.window = window
        while True:
            self.main()
        pass
    pass

    def main(self):

        source_dir = "G:\MUSIC\华语"#input(self.input_source_msg)
        target_dir = "E:\MUSIC"#input(self.input_target_msg)

        # 依次从目录的最上级往下 创建不存在的目录
        def create_dir(path: pathlib.Path):
            parents = list(path.parents)
            parents.reverse()
            for _PATH in parents:
                if not _PATH.exists():
                    _PATH.mkdir()
        pass

        self.add_info(self.tips_point, "Start Running")
        space = ""
        source = pathlib.Path(source_dir)
        tag = str(source.parts[-1])

        start_time = time.time()
        pg_iter = progress_tag()
        try:
            for _path, _target_path in generate_file(space, source_dir, target_dir, tag, source):

                self.add_info(self.tips_point, "> source_dir {} target_dir {}".format(_path, _target_path))
                # 创建不存在的目录 并将文件复制到目标目录
                if not _target_path.exists():
                    self.add_info(self.tips_point, "--> mkdir {}".format(_target_path.parent))
                    create_dir(_target_path)

                max_size = _path.stat().st_size
                with _path.open(mode='rb') as _file, _target_path.open('wb') as _write:
                    cache_size = 0
                    while True:
                        _byte_data = _file.read(self.read_size)
                        if not _byte_data:
                            break
                        # 显示进度(%)
                        cache_size += len(_byte_data)
                        info = "{} {:0.4%}".format(next(pg_iter), (cache_size / max_size))
                        self.add_info(self.progress_point, info)
                        _write.write(_byte_data)
                    pass
            end_time = time.time()
            self.add_info(self.tips_point, "copy file success in Time：{}".format(end_time - start_time))
            # subprocess.Popen("shutdown -s -t 60", shell=True,
            #                  stdin=subprocess.PIPE,
            #                  encoding="GBK", stdout=sys.stdout)
        except BaseException as e:
            self.add_info(self.error_msg_point, "Error {}".format(str(e)))

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


def generate_file(space, source_dir, target_dir, tag, path: pathlib.Path):
    if path.is_dir():
        space += ' '
        for _p in path.iterdir():
            for _result in generate_file(space, source_dir, target_dir, tag, _p):
                yield _result
            pass
    elif path.is_file():
        target_path = pathlib.Path(str(path.absolute()).replace(source_dir, target_dir + "\\" + tag))
        if not target_path.exists():
            yield path, target_path
    pass
    pass


system = CopyFileSystem()
# system.main(source_dir=input("输入源目录："), target_dir=input("输入吗目标目录："))
system.main()
# curses.wrapper(system.main)
# curses.wrapper(system.start)