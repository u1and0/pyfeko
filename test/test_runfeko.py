#!/bin/env python3
import sys
sys.path.append('./bin/')
from runfeko import *

# =================_select_files==================
print('-------------------')
task = Runfeko()
print('files\n', task.files)
print('-------------------')
print('command\n', task._generate(task.files[0]))
