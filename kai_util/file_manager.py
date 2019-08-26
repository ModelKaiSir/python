import pathlib
import time
import subprocess
import sys
import file_generate
import lrc_util
import curses


# 文件管理工具
class CopyFileSystem:
    MODE_COPYFILE = "COPY_FILE"
    MODE_DOWNLOAD_LRC = "DOWNLOAD_LRC"

    def __init__(self, mode):
        self.mode = mode
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
        self.finish_shutdown_switch = 'N'
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
        self.mode = input("输入模式({} {}) :".format(CopyFileSystem.MODE_COPYFILE,CopyFileSystem.MODE_DOWNLOAD_LRC))
        self.finish_shutdown_switch = input("要在任务完成后关闭计算机吗？ Y/N")

        if self.mode == CopyFileSystem.MODE_COPYFILE:
            self.copy_files()
        elif self.mode == CopyFileSystem.MODE_DOWNLOAD_LRC:
            # 下载歌词
            download_lrc(input("输入目录："))
            pass
        pass

    pass

    @staticmethod
    def finish_shutdown():
        subprocess.Popen("shutdown -s -t 60", shell=True,
                         stdin=subprocess.PIPE,
                         encoding="GBK", stdout=sys.stdout)
        pass

    def copy_files(self):

        source_dir = input(self.input_source_msg)
        target_dir = input(self.input_target_msg)

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
        pg_iter = file_generate.progress_tag()
        try:
            for _path, _target_path in file_generate.generate_not_exists_file(space, source_dir, target_dir, tag, source):

                self.add_info(self.tips_point, "> source_dir {} target_dir {}".format(_path, _target_path))
                # 创建不存在的目录 并将文件复制到目标目录
                if not _target_path.exists():
                    self.add_info(self.tips_point, "--> create dir {}".format(_target_path.parent))
                    create_dir(_target_path)

                max_size = _path.stat().st_size

                self.add_info(self.tips_point, "正在复制中。。。")
                with _path.open(mode='rb') as _file, _target_path.open('wb') as _write:
                    cache_size = 0
                    while True:
                        _byte_data = _file.read(self.read_size)
                        if not _byte_data:
                            break
                        # 显示进度(%)
                        cache_size += len(_byte_data)
                        # info = "{} {:0.4%}".format(next(pg_iter), (cache_size / max_size))
                        # self.add_info(self.progress_point, info)
                        _write.write(_byte_data)
                    pass
                self.add_info(self.tips_point, "复制完成。。。")
            pass
            end_time = time.time()
            self.add_info(self.tips_point, "copy file success in Time：{}".format(end_time - start_time))
            # 任务完成自动关机
            if self.finish_shutdown_switch.upper() == 'N':
                self.finish_shutdown()

        except BaseException as e:
            self.add_info(self.error_msg_point, "Error {}".format(str(e)))

    pass


def download_lrc(source_dir):
    for _path in file_generate.generate_not_exists_lrc_sound(source_dir):
        try:
            d = lrc_util.LrcDownload(_path)
            d.download_lrc()
            time.sleep(0.2)
        except BaseException as e:
            print("网络出错！Error{}".format(str(e)))
        pass
    pass


system = CopyFileSystem(CopyFileSystem.MODE_DOWNLOAD_LRC)
# system.main(source_dir=input("输入源目录："), target_dir=input("输入吗目标目录："))
system.start(None)
# curses.wrapper(system.main)
# curses.wrapper(system.start)
