#!/bin/env python
from tkinter import filedialog
import os


def _select_files(filetypes, initialdir):
    filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
    return filenames


if __name__ == '__main__':
    filetypes = [('テキストファイルとExcelファイル', '*.txt;*.csv')]
    root = os.getcwd()
    print(_select_files(filetypes, root))
