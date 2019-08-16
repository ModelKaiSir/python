import win32api
import win32con
import win32clipboard as clip
import menu


class Util:

    def __init__(self):
        pass

    @staticmethod
    def send_ClipBoard(text):
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardText(text)
        clip.CloseClipboard()

    @staticmethod
    def sendFile_ClipBoard(file):
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardData(win32con.CF_DIF, file)
        clip.CloseClipboard()

    @staticmethod
    def get_desktop_path():
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0,
                                  win32con.KEY_READ)
        return win32api.RegQueryValueEx(key, 'Desktop')[0]

    @staticmethod
    def cmd_wait():
        # 阻塞界面 用户输入回车关闭
        while True:
            input("回车关闭：")
            break


class UtilContext:
    def __init__(self):
        self.MENU_MAX_LENGTH = 60
        self.MENU_SPE_LENGTH = 60
        self.menuMap = None
        self.SELECT_MENU = "选择菜单："
        self.INVALID_INPUT = "无效的输入"
        self.PUT_LINE = "* {menuContext:<" + str(self.MENU_SPE_LENGTH) + "}"
        self.menuKeyIter = UtilContext.generateId()
        pass

    def __formatLine(self, string):
        return self.PUT_LINE.format(menuContext=string)
        pass

    def printMenu(self, _menu):
        print(self.__formatLine(("[{}]:{}".format(_menu.key, _menu.menuContent))))

    def printText(self, text):
        if len(text) > self.MENU_SPE_LENGTH:
            _a, _b = text[0:self.MENU_SPE_LENGTH], text[self.MENU_SPE_LENGTH:]
            self.printText(_a)
            self.printText(_b)
            pass
        else:
            print(self.__formatLine(text))
        pass

    def placeHolder(self):
        print(self.__formatLine("　"))

    def __registerMenu(self, menus):
        self.menuMap = {str(m.key): m for m in menus}

    def initMenu(self, menu_es, reset=False):
        if reset:
            self.printText(self.INVALID_INPUT)

        print("".join(['*' for i in range(self.MENU_MAX_LENGTH)]))
        self.placeHolder()
        for _menu in menu_es:
            self.printMenu(_menu)
        self.placeHolder()
        print("".join(['*' for i in range(self.MENU_MAX_LENGTH)]))

    def doMain(self, menus):
        self.initMenu(menus)
        self.__registerMenu(menus)
        obj = lambda: self.initMenu(menus, False)
        self.inputListener(lambda k: k.run(obj) if k is not None else self.initMenu(menus, True))
        pass

    def inputListener(self, fn):
        while True:
            fn(self.menuMap.get(input(self.SELECT_MENU)))
            pass

    # menuId生成器
    @staticmethod
    def generateId():
        _id = 1
        while True:
            yield _id
            _id += 1
        pass


context = UtilContext()
components = [menu.FindClassToZip(context), menu.SqlHandle(context), menu.ImportDmp(context),
              menu.CreateQrCode(context), menu.ImportDmpGlobal(context), menu.AddOracleTns(context),
              menu.GenerateScriptDataSetColumnXml(context), menu.GenerateMD5(context)]

try:
    context.doMain(components)
except BaseException as e:
    print(e)
    context.doMain(components)

