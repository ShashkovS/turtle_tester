#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ast import literal_eval
import sys, codecs
sys.stdout, sys.stderr = codecs.getwriter("utf-8")(sys.stdout.detach()), codecs.getwriter("utf-8")(sys.stderr.detach())
OK=0; PE=4; WA=5; CF=6

def error(*args, sep=' '): sys.stderr.write(args[0].format(*args[1:])); sys.exit(WA)
def ok(*args, sep=' '): sys.stdout.write(args[0].format(*args[1:])); sys.exit(OK)

try:
    test = open(sys.argv[1], encoding='utf-8').read().strip()
    cor_ans = open(sys.argv[3], encoding='utf-8').read().strip()
    pup_ans = open(sys.argv[2], encoding='utf-8').read().strip()
except ZeroDivisionError:
    sys.exit(PE)

ok('Настоящая проверка будет чуть позже')
