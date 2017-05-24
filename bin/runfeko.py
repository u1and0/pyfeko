#!/bin/env python3
"""FEKOの逐次実行スケジューラ
# USAGE
## @Windows env
* Click `runfeko.bat`
* Select files

## @Linux env
```
$ cd 
$ ,/runfeko
```

# FUNCTION
"""
import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()


def select_files(filetypes, initialdir):
    filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
    return filenames


class Runfeko:
    """docstring for Runfeko"""
    FILETYPES = [('テキストファイルとExcelファイル', '*.txt;*.csv')]
    ROOT = os.getcwd()

    def __init__(self):
        self.files = select_files(Runfeko.FILETYPES, Runfeko.ROOT)

    def generate(self):
        pass

    def execute(self):
        pass

    def mail(self):
        pass


if __name__ == '__main__':
    task = Runfeko()
    print(task.files)
