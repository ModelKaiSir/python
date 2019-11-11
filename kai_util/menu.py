import pathlib
import hashlib
import os
import zipfile
import qrcode
import subprocess
import re
import sys
import json
from itertools import takewhile


def log(lev):
    def warpper(fn):
        def call(*args, **kwargs):
            print("日志等级 {}".format(lev))
            fn(*args, **kwargs)
            print("end")
            pass

        return call

    return warpper


# 程序的配置 json格式
class Config:
    PATH_MAP = "pathMap"

    def __init__(self):

        # 从目录下面找config.json文件 找不到则生成一个默认的
        _path = pathlib.Path.cwd().joinpath("config.json")

        def parse_data(_content):
            if _content.startswith(u'\ufeff'):
                return _content.encode('utf8')[3:].decode('utf8')
            else:
                return _content

        # 存在文件 解析config
        if pathlib.Path.is_file(_path):
            with open(_path, mode='r', encoding='UTF-8') as f:
                try:
                    self.config = json.loads(parse_data(f.read()))
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    # json文件为空 初始化config
                    self.initConfig()
                pass
        else:
            # 没有就创建
            with open(_path, 'a+'):
                pass

        pass

    def initConfig(self):
        print("初始化配置")
        self.config = {"pathMap": {}}
        pass

    def getConfig(self):
        return self.config

    pass


class Menu:
    def __init__(self, context, text, tips):
        self.context = context
        self.menuContent = text
        self.key = next(self.context.menuKeyIter)
        self.tips = tips
        self.util = context.util

        pass

    def beforeRun(self):
        self.context.placeHolder()
        self.context.printText(self.tips)
        self.context.placeHolder()
        pass

    def afterRun(self):
        pass

    def currentRun(self):
        pass

    def run(self, fn):
        self.beforeRun()
        self.currentRun()

        self.util.cmd_wait()
        fn()
        self.afterRun()

    pass


'''查找文件并打包'''


class FindClassToZip(Menu):

    def __init__(self, context):

        text = r"""生成class替换文件"""
        tips = r"""格式[pathTag]:[包名] 会自动根据配置的pathTag找到对应的目录，并自动转换包名如[POS61]:com.qiuKai.test"""
        Menu.__init__(self, context, text, tips)

        self.CONFIG_FIND_CLASS = "findClassConfig"
        self.CONFIG_ZIP_PATH = "zipPath"
        self.CONFIG_ZIP_ROOT_PATH = "zipRootPath"
        self.CONFIG_README = "readMe"
        self.INPUT_MSG = "请输入需要处理的路径："
        self.readme_filename = "path.txt"
        self.def_suffix = "class"
        self.more_pack = False
        self.init_pack = True
        self.pack_length = 1

        self.config = Config().getConfig()
        self.pathMap = self.config[Config.PATH_MAP]
        self.README_TEXT = self.config[self.CONFIG_FIND_CLASS][self.CONFIG_README]
        self.PACK_PATH = self.config[self.CONFIG_FIND_CLASS][self.CONFIG_ZIP_PATH]
        self.PACK_ROOT_PATH = self.config[self.CONFIG_FIND_CLASS][self.CONFIG_ZIP_ROOT_PATH]
        self.README_PATH = "{}\\{}".format(self.util.get_desktop_path(), self.readme_filename)

        pass

    def currentRun(self):
        input_string = input(self.INPUT_MSG)
        parameter = input_string.split("|")
        self.pack_length = len(parameter)
        self.more_pack = self.pack_length > 1
        zip_file_it = self.generate_pack_name(self.pack_length)
        for p in parameter:
            self.start_find(p.split(":"), zip_file_it)
        pass

    def start_find(self, parameter, zip_file_it):

        result = []

        if len(parameter) > 0:
            tag, package_name, suffix = parameter[0], parameter[1], parameter[2] if len(
                parameter) > 2 else self.def_suffix
            # 根据tag找根目录
            root_path = self.pathMap.get(tag)

            # com.a.b.c.a,b,c => com/a/b/c/a,b,c
            root_path_temp = "{}{}".format(root_path, "\\".join(i for i in package_name.split(".")))

            if os.path.isfile("{}.{}".format(root_path_temp, suffix)):
                # 具体目录
                detail_path, last_name = "\\".join(i for i in package_name.split(".")[:-1]), package_name.split(".")[
                                                                                             -1:]
                # 如果整个目录不是一个文件夹则lastName就是要查找的文件名
                path = "{}{}".format(root_path, detail_path)
                self.findFile(path, last_name[0], suffix, result=result)
            else:
                # 查找所有文件
                self.context.printText(root_path_temp)
                detail_path = "\\".join(i for i in package_name.split(".")[:-1])
                last_name = "".join(package_name.split(".")[-1:])

                # 检查是否带有文件名列表
                if last_name.find(",") != -1:
                    path = "{}{}".format(root_path, detail_path)
                    self.findFile(path, file_name=last_name.replace(',', '|'),
                                  suffix=suffix, result=result)
                else:
                    path = root_path_temp
                    self.findFile(path, suffix=suffix, no_check=True, result=result)
                pass

            self.packFiles(path, result, zip_file_it)

        pass

    def findFile(self, root_path, file_name="*", suffix="class", no_check=False, result=[]):
        regex = r'(' + file_name + ').*(\.' + suffix + ')$'

        # 读取path下面所有文件，并进行正则过滤
        for file_item in os.listdir(root_path):
            self.checkAndSetFile(file_item, regex, result, no_check)

        pass

    # 检查文件并放入集合
    def checkAndSetFile(self, file_path, regex, result, no_check=False):
        if os.path.isdir(file_path):
            for file_item in os.listdir(file_path):
                self.checkAndSetFile(file_item, regex, result)
        else:
            if no_check:
                result.append(file_path)
            elif re.match(regex, file_path) is not None:
                result.append(file_path)

        pass

    def generate_pack_name(self, pack_length):
        while pack_length >= 1:
            result = "替换{}.zip".format(pack_length)
            pack_length -= 1
            yield result
        pass

    # 打包并写入ReadeMe
    def packFiles(self, path, result, zip_file_it=None):

        # 创建ReadMe
        def writeReadMe(source, _path):
            with open(source.README_PATH, 'a', encoding='utf-8') as file:
                file.writelines(source.README_TEXT.format(path=_path[_path.find("classes"):]))
            pass

        # 打包zip
        def pack(source, _folder, _result, fit):

            zip_file_path = "{}/{}".format(source.PACK_ROOT_PATH,
                                           next(fit)) if source.more_pack else source.PACK_PATH

            with zipfile.ZipFile(zip_file_path, "a") as z:
                for r in _result:
                    _F = "{}/{}".format(path, r[r.rfind("\\") + 1:])
                    print("{}\\{}".format(_folder, r))
                    z.write(_F, "{}\\{}".format(_folder, r), compress_type=zipfile.ZIP_DEFLATED)

            with zipfile.ZipFile(zip_file_path, "a") as z2:
                z2.write(source.README_PATH, "path.txt", compress_type=zipfile.ZIP_DEFLATED)
                pass
            os.remove(source.README_PATH)
            pass

        def delete_file(file_path):
            if pathlib.Path(file_path).is_file():
                os.remove(file_path)
            pass

        # 打包之前初始化 只初始化一次
        def init(source):
            if source.init_pack:
                if source.more_pack:
                    for v in source.generate_pack_name(source.pack_length):
                        delete_file("{}/{}".format(source.PACK_ROOT_PATH, v))
                else:
                    delete_file(source.PACK_PATH)

                source.init_pack = False

        try:
            init(self)
            #
            writeReadMe(self, path)
            pack(self, path.split("\\")[-1:][0], result, zip_file_it)
            self.context.printText("job Done")
        except Exception as e:
            self.context.printText(str(e))
        pass

    pass


'''处理sql'''


class SqlHandle(Menu):

    def __init__(self, context):

        text = r"""Sql处理"""
        tips = r"""对sql进行批量处理,加入/*<SQL>*//*</SQL>*/标签 以空行为分割符"""
        Menu.__init__(self, context, text, tips)

        self.CONFIG_SQL_HANDLE = "sqlHandle"
        self.CONFIG_DATA_PATH = "sqlDataHandlePath"
        self.config = Config().getConfig()

        self.SQL_DATA_PATH = self.config[self.CONFIG_SQL_HANDLE][self.CONFIG_DATA_PATH]

        self.sql_temp = "/*<SQL>*/{a}{sql}{b}/*</SQL>*/"
        self.sql_text = ""

    pass

    def currentRun(self):

        with open(self.SQL_DATA_PATH, mode='r', encoding='utf-8') as f:
            # 读取所有sql
            for line in f.readlines():
                self.sql_text += line
            pass

        regex = r"(\n)(\n)"

        _cache = ""
        for sql in re.split(regex, self.sql_text):
            if sql != '\n':
                obj = lambda string: '' if string == '\n' else '\n'
                a, b = obj(sql[0]), obj(sql[-1])

                _cache += self.sql_temp.format(a=a, sql=sql, b=b) + "\n"
                self.context.printText(_cache)
            pass
        pass
        # send cache to ClipBard
        self.context.printText("Copy for ClipBoard is Success")
        self.util.send_ClipBoard(_cache)

    pass


'''导库工具'''


class ImportDmp(Menu):

    def __init__(self, context):
        text = r"""Oracle导库"""
        tips = r"""根据配置导入数据库,导库配置信息放在{configPath}格式为 
                        [TITLE] [DMP_PATH] [TO_DATABASE_NAME] [FORM_DATABASE_NAME]"""
        self._init(context, text, tips)
        pass

    def _init(self, context, text, tips):
        self.CONFIG_IMPORT_DMP = "ImportDmp"
        self.CONFIG_DATA_PATH = "configPath"
        self.IMP_SHELL = "impShell"
        self.CONFIG_DATA_BEFORE_SQL_LIST = "beforeSqlList"
        self.config = Config().getConfig()

        self.CONFIG_PATH = self.config[self.CONFIG_IMPORT_DMP][self.CONFIG_DATA_PATH]
        self.BEFORE_SQL_LIST = self.config[self.CONFIG_IMPORT_DMP][self.CONFIG_DATA_BEFORE_SQL_LIST]
        self.before_tip = "准备工作SQL已生成，请先执行SQL.(已复制到粘贴板)"
        self.ready = "准备好,按回车开始导库："
        self.finish = "导库{title}完毕！"
        # 导库语句
        self.import_shell = self.config[self.CONFIG_IMPORT_DMP][self.IMP_SHELL]

        Menu.__init__(self, context, text, tips.format(
            configPath=self.CONFIG_PATH))
        pass

    def currentRun(self):

        def run(source, _info):
            self.util.send_ClipBoard(source.generateBeforeImpSql(_info[1], _info[2], _info[3]))
            source.context.printText(source.before_tip)
            input(source.ready)
            source.importDmp(_info[1], _info[2], _info[3])
            source.context.printText(source.finish.format(title=_info[0]))
            pass

        try:

            def isNone(_line):
                return _line is None
                pass

            no_config = True
            with open(self.CONFIG_PATH, "r") as file:
                for line in takewhile(isNone, file.readlines()):
                    if line[0] == '#':
                        continue
                    # 读取配置
                    no_config = False
                    info = line.replace("\n", "").split(" ")
                    run(self, info)
                    break
            if no_config:
                info = input("手动输入导库信息：")
                if info is not None:
                    run(self, info.split(" "))
                else:
                    self.context.printText("取消操作")
            pass
        except BaseException as e:
            self.context.printText("Error({})".format(str(e)))
        pass

    # 生成准备sql
    def generateBeforeImpSql(self, dmp_path, to_user, form_user):
        result = ""
        for sql in self.BEFORE_SQL_LIST:
            result += sql.format(DMP_PATH=dmp_path, FORM_DATABASE_NAME=form_user, TO_DATABASE_NAME=to_user) + "\n"
        return result
        pass

    # 执行导库脚本
    def importDmp(self, dmp_path, to_user, form_user):

        self.beforeImpDmp()
        cmd = subprocess.Popen(self.import_shell.format(DMP_PATH=dmp_path, FORM_DATABASE_NAME=form_user,
                                                        TO_DATABASE_NAME=to_user), shell=True, stdin=subprocess.PIPE,
                               encoding="GBK", stdout=sys.stdout)
        cmd.wait()
        self.afterImpDmp()
        pass

    def beforeImpDmp(self):
        pass

    def afterImpDmp(self):
        pass

    pass


'''导入数据库文件 指定表'''


class ImportDmpGlobal(ImportDmp):

    def __init__(self, context):
        ImportDmp.__init__(self, context)
        self.import_shell += " TABLES=({tables:})"

        pass

    def _init(self, context, text, tips):

        text += "(导入表)"
        tips += "(导入表)"
        ImportDmp._init(self, context, text, tips)
        pass

    def importDmp(self, dmp_path, to_user, form_user):
        tables = input("输入导入的表名：")
        if tables is not None and tables != '':
            cmd = subprocess.Popen(self.import_shell.format(DMP_PATH=dmp_path, FORM_DATABASE_NAME=form_user,
                                                            TO_DATABASE_NAME=to_user, tables=tables), shell=True,
                                   stdin=subprocess.PIPE,
                                   encoding="GBK", stdout=sys.stdout)
            cmd.wait()
        else:
            self.context.printText("取消导入")
        self.afterImpDmp()
        pass


'''重设数据库管理员密码 TechTranDataBase'''


class UpdateDataBase(Menu):

    def __init__(self, context):
        self.CONFIG_UPDATE_DB = "updateDb"

        text = r"""Oracle导库"""
        tips = r"""重置数据库ADMIN账号密码为123 输入数据库账号密码即可(逗号分割,只输入账号则默认账号密码相同,数据库连接地址在config中配置)"""
        Menu.__init__(self, context, text, tips)
        pass


'''根据文本创建二维码'''


class CreateQrCode(Menu):

    def __init__(self, context):
        self.INPUT_TEXT = "请输入文本："
        self.qr_code_filename = "二维码.png"
        self.cache_image = None
        text = "生成二维码"
        tips = "输入字符串生成一张二维码，字符串不能太长"
        Menu.__init__(self, context, text, tips)
        pass

    def currentRun(self):
        string = input(self.INPUT_TEXT)
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        qr.add_data(string)
        qr.make(fit=True)
        self.cache_image = qr.make_image()
        self.cache_image.save(self.qr_code_filename)
        # 显示图片
        subprocess.Popen(str(pathlib.Path.cwd().joinpath(self.qr_code_filename)), shell=True, stdin=subprocess.PIPE,
                         encoding="GBK")
        pass

    def afterRun(self):
        # 删除图片
        print(os.remove(str(pathlib.Path.cwd().joinpath(self.qr_code_filename))))
        pass


class AddOracleTns(Menu):

    def __init__(self, context):

        text = "添加Oracle TNS 配置"
        tips = "快捷添加OracleTns,格式数据库名 ip地址 数据库实例 端口(默认1521可不输),空格分隔"
        Menu.__init__(self, context, text, tips)

        self.CONFIG_ADD_ORACLE_TNS = "AddOracleTns"
        self.CONFIG_TNS_PATH = "tnsPath"
        self.config = Config().getConfig()

        self.temp = "\n{TNSNAME:} = "
        self.temp += "\n  (DESCRIPTION ="
        self.temp += "\n    (ADDRESS_LIST ="
        self.temp += "\n      (ADDRESS = (PROTOCOL = TCP)(HOST = {IP:})(PORT = {PORT:}))"
        self.temp += "\n    )"
        self.temp += "\n    (CONNECT_DATA ="
        self.temp += "\n      (SERVICE_NAME = {SERVICE_NAME:})"
        self.temp += "\n    )\n  )"

        self.INPUT_MSG = "请输入tns信息："
        self.def_port = "1521"

        self.tns_config_path = self.config[self.CONFIG_ADD_ORACLE_TNS][self.CONFIG_TNS_PATH]
        pass

    def currentRun(self):

        def write(file_path, _data):
            with open(file_path, 'a') as file:
                file.writelines(_data)
            pass

        tns = input(self.INPUT_MSG)
        if tns is not None and tns != '':
            info = tns.split(" ")
            if len(info) <= 3:
                write(self.tns_config_path,
                      self.temp.format(TNSNAME=info[0], IP=info[1], PORT=self.def_port, SERVICE_NAME=info[3]))
                pass
            elif len(info) >= 4:
                write(self.tns_config_path,
                      self.temp.format(TNSNAME=info[0], IP=info[1], PORT=info[4], SERVICE_NAME=info[3]))
                pass

            self.context.printText("job Done")
            pass
        pass


pass

'''快捷生成ScriptDataSet字段 xml'''


class GenerateScriptDataSetColumnXml(Menu):

    def __init__(self, context):
        text = "生成ScriptDataSet字段"
        tips = "快捷生成ScriptDataSet字段的xml,直接贴到对应位置 格式字段名空格分割"
        Menu.__init__(self, context, text, tips)

        self.INPUT_MSG = "请输入字段信息："

        self.resultSetHints = '''<list-property name="resultSetHints">
                                {structure}
                            </list-property>'''
        self.columnHints = '''
                        <list-property name="columnHints">
                                {structure}
                            </list-property>'''
        self.cachedMetaData = '''<structure name="cachedMetaData">
                                <list-property name="resultSet">
                                    {structure}
                                </list-property>
                            </structure>'''
        self.defDataType = "javaObject"
        self.structure = """<structure>
                                        <property name="position">{position}</property>
                                        <property name="name">{name}</property>
                                        <property name="dataType">{dataType}</property>
                                        </structure>"""
        self.structureProperty = '''<structure>
                                    <property name="columnName">{columnName}</property>
                                    <text-property name="displayName" key="{key}">{displayName}</text-property>
                                </structure>'''
        pass

    def currentRun(self):
        cols = input(self.INPUT_MSG)
        if cols is not None and cols != '':
            self.util.send_ClipBoard(self.getData(cols.split(" ")))
            self.context.printText("job Done")
            pass
        pass

    def createResultSetHints(self, structures: list):
        return self.resultSetHints.format(structure="\n".join(s for s in structures))
        pass

    def createColumnHints(self, structures_pro: list):
        return self.columnHints.format(structure="\n".join(s for s in structures_pro))
        pass

    def createCachedMetaData(self, structures: list):
        return self.cachedMetaData.format(structure="\n".join(s for s in structures))
        pass

    def createStructure(self, index, name):
        return self.structure.format(position=index, name=name, dataType=self.defDataType)
        pass

    def createStructureProperty(self, name):
        return self.structureProperty.format(columnName=name, key=name, displayName=name)
        pass

    def getData(self, cols: list):
        structures = []
        structures_pro = []
        for index, col in enumerate(cols):
            structures.append(self.createStructure(index + 1, col))
            structures_pro.append(self.createStructureProperty(col))

        _cache = self.createResultSetHints(structures)
        _cache += self.createColumnHints(structures_pro)
        _cache += self.createCachedMetaData(structures)

        print(_cache)
        return _cache
        pass


pass

'''计算文件md5'''


class GenerateMD5(Menu):

    def __init__(self, context):
        text = "计算md5"
        tips = "根据输入的信息计算md5值 如果是一个文件地址则计算文件的md5"
        Menu.__init__(self, context, text, tips)
        self.INPUT_MSG = "输入内容或文件路径："
        self.RESULT_MSG = "计算结果 第{index:}个 {MD5:} (已复制)"
        pass

    def currentRun(self):
        msg = input(self.INPUT_MSG)
        _result = []
        if msg is not None and msg != '':
            for _index, _msg in enumerate(msg.split(":")):
                _md5 = self.getMD5(_msg)
                self.context.printText(self.RESULT_MSG.format(index=_index + 1, MD5=_md5))
                _result.append(_md5)
                pass
            self.util.send_ClipBoard(":".join(_r for _r in _result))
            self.context.printText("job Done")
            pass
        pass

    def getMD5(self, source):

        def cal(obj):
            _generate = hashlib.md5()
            _generate.update(obj)
            return _generate.hexdigest()
            pass

        _path = pathlib.Path(source)
        if _path.is_file():
            with _path.open(mode='rb') as f:

                generate = hashlib.md5()
                for line in f:
                    generate.update(line)
                return generate.hexdigest()

            pass
        else:
            return cal(source.encode('UTF-8'))
            pass
        pass

# POS61:com.techtrans.vaadin.espos61.mis.mall.ec.smsc.make.MakeTicke4DepositFunctionMain,MakeTickePrintFunctionMain
# POS61:com.techtrans.vaadin.espos61.mis.mall.ec.smsc.make.MakeTicke4DepositFunctionMain|POS61:com.techtrans.vaadin.espos61.mis.mall.ec.smsc.make.MakeTickePrintFunctionMain
