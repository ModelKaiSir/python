from kai_util.main import UtilContext
import pys_util
import qrcode
import subprocess


'''加载Json配置文件'''


class Config:
    pass


def main():
    text = input("输入文本")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    url = text
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('二维码.png')

    subprocess.Popen("D:\JavaFxProject\python\kai_util\二维码.png", shell=True, stdin=subprocess.PIPE, encoding="GBK")
    '''
    ERROR_CORRECT_L：大约7%或更少的错误能被纠正。
    ERROR_CORRECT_M（默认）：大约15%或更少的错误能被纠正。
    ROR_CORRECT_H：大约30%或更少的错误能被纠正。
    '''
