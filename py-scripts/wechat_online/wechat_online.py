#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import random
import time
import tkinter as tk
from multiprocessing import Process

import pyautogui

pyautogui.FAILSAFE = False
import win32api
import win32con
import win32gui
from loguru import logger
from PIL import Image, ImageTk


def run_wechat():
    logger.info("打开企业微信")
    hwnd = win32gui.FindWindow(None, "企业微信")
    if hwnd != 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
    else:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32api.SetCursorPos([left + 34, top + 42])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
    )
    time.sleep(3)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


class RandomMouseMove:
    def __init__(self):
        self.random_x = None
        self.random_y = None
        self.last_x = None
        self.last_y = None
        self.currnet_x = None
        self.current_y = None

    def _random_move(self):
        self.random_x, self.random_y = (
            random.randint(0, pyautogui.size().width),
            random.randint(0, pyautogui.size().height),
        )
        pyautogui.moveTo(self.random_x, self.random_y, 1)

    def move(self, forever=False):
        self.current_x, self.current_y = pyautogui.position()
        if forever:
            logger.info("forever模式，一直都会随机移动鼠标，开始移动")
            self._random_move()
            return
        if self.current_x == self.last_x and self.current_y == self.last_y:
            logger.info(
                f"开始随机移动鼠标, 原来的鼠标位置 x:{self.last_x}, y:{self.last_y}, 现在的鼠标位置 x:{self.random_x}, y:{self.random_y}"
            )
            self._random_move()
            self.last_x, self.last_y = self.random_x, self.random_y
            return
        elif (None, None) == (self.last_x, self.last_y):
            logger.info(
                f"初始运行, 原来的鼠标位置 x:{self.last_x}, y:{self.last_y}, 现在的鼠标位置 x:{self.random_x}, y:{self.random_y}"
            )
            self._random_move()
            self.last_x, self.last_y = self.random_x, self.random_y
            return
        logger.info(
            f"不需要移动鼠标, 原来的鼠标位置 x:{self.last_x}, y:{self.last_y}, 现在的鼠标位置 x:{self.random_x}, y:{self.random_y}"
        )
        self.last_x, self.last_y = self.current_x, self.current_y


def lock_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.90)
    root.bind_all("<Control-z>", lambda event: root.destroy())
    photo = ImageTk.PhotoImage(
        file=r"D:\备份资料\个人资料\Python\Python小工具\wechat_online\lock.png"
    )
    tk.Label(root, image=photo).pack()
    root.mainloop()


def all_start(sec=15):
    random_mouse_move = RandomMouseMove()
    while True:
        run_wechat()
        random_mouse_move.move(forever=True)
        time.sleep(sec)


def main():
    p = Process(target=all_start, args=(10,))
    p.daemon = True
    p.start()
    lock_screen()


if __name__ == "__main__":
    main()
