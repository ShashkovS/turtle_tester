#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.extend(['/usr/lib64/python35.zip', '/usr/lib64/python3.5', '/usr/lib64/python3.5/plat-linux', '/usr/lib64/python3.5/lib-dynload', '/usr/lib64/python3/site-packages', '/usr/lib64/python3/site-packages/PIL', '/usr/lib/python3/site-packages'])
user_pgm = sys.argv[1]
with open(user_pgm, 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('import turtle', 'import turtle_tester')
code = code.replace('turtle import', 'turtle_tester import')

code = '\n'.join(code)
exec(code)
