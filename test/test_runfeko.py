#!/bin/env python
import sys, os
sys.path.append('./bin/')
import runfeko

task = runfeko.Runfeko()
print('====_select_files====')
print(task.files)
print('====command generate 1====')
print(task._generate(task.files[0]))
print('====command generate all====')
print(task._command_list_gen(task.files))
print('====send mail====')
print(task.mailing_list('./ini/file.log'))
print('====run====')
print(task._main())
