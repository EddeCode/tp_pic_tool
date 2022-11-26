from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk


def select_file(init_dir=None):
    # 弹出文件选择对话框
    path_ = filedialog.askopenfile(initialdir=init_dir)
    return path_.name


def confirm_gui():
    confirm = messagebox.askyesno("提示", "图片存在失效情况，是否继续？")
    return confirm
