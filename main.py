# -*- coding:utf-8 -*-
"""
@author: chengyijun
@contact: cyjmmy@foxmail.com
@file: 操作剪贴板.py
@time: 2020/12/21 11:41
@desc:
"""
import os
import time

import requests
import win32clipboard as wc
import win32con
from PIL import ImageGrab
from PIL.BmpImagePlugin import DibImageFile


class SMMS:
    def __init__(self):
        # 参数设置
        self.url = 'https://sm.ms/api/v2/upload'
        self.authorization = 'wZqSFbPiynsmUxGs3zFl7Jmu7Cj5SQXR'
        self.file_name_without_path = f'{int(time.time())}.jpg'
        self.file_name = os.path.join(os.getcwd(), self.file_name_without_path)

    def upload(self):
        """
        上传图片到smms服务器
        :return:
        """
        # 从剪贴板获取图片并保存到本地
        if self.__save_img_from_clipboard():
            # 从本地上传图片到smms,得到md链接
            md_link = self.__upload()
            # 将得到的markdown图片链接 写入到系统剪贴板
            self.__set_clip(md_link)

    @staticmethod
    def __get_clip():
        """
        从剪贴板获取数据
        :return:
        """
        wc.OpenClipboard()
        t = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        wc.CloseClipboard()
        return t

    @staticmethod
    def __set_clip(msg):
        """
        给剪贴板设置数据
        :param msg:
        :return:
        """
        if not msg:
            return
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(win32con.CF_UNICODETEXT, msg)
        wc.CloseClipboard()

    def __save_img_from_clipboard(self) -> bool:
        """
        从剪贴板读取图片数据，并保存到本地
        :return:
        """
        image = ImageGrab.grabclipboard()
        if image and isinstance(image, DibImageFile):
            image.save(self.file_name)
            return True
        return False

    def __upload(self) -> str:
        """
        上传图片到smms服务器，并得到md链接
        :return:
        """
        headers = {
            'Authorization': self.authorization,
        }

        try:
            with open(self.file_name, 'rb') as f:
                files = {
                    'smfile': f,
                }
                res = requests.post(url=self.url, headers=headers, files=files).json()
        except:
            return ''

        if all([res, res.get('code') == 'image_repeated']):
            return f'![{self.file_name_without_path}]({res.get("images")})'
        if all([res, res.get('code') == 'success']):
            return f'![{self.file_name_without_path}]({res.get("data").get("url")})'
        return ''

    def __del__(self):
        """
        销毁本地图片
        :return:
        """
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


if __name__ == '__main__':
    smms = SMMS()
    smms.upload()
