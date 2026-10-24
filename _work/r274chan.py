# -*- coding: utf-8 -*-
"""274 輪・器・四尺加「試跑通道」：換冊之前，先讓尺量**假冊**（未入正本之新稿）。

改法一律：`LINES = _tk.MAIN_LINES` 之下插入三行——有非旗參數則改讀該檔。
    不帶參時與舊完全相同（此即負測之道一：無參之輸出必與歷輪一致）。
適用：v39quote2／v39volchk／v39volrange／v39secref。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274chan.py
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
BLOCK = [u'SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)'
         u'          # 274 輪・試跑通道：量假冊而不動正本',
         u'if SRC_PATH:',
         u'    LINES = io.open(SRC_PATH, encoding=u"utf-8-sig").read().split(u"\\n")']
import ast
for f in (u'v39quote2.py', u'v39volchk.py', u'v39volrange.py'):
    p = os.path.join(WORK, f)
    L = io.open(p, encoding=u'utf-8').read().split(u'\n')
    if any('SRC_PATH' in l for l in L):
        print(u'%s 已有通道，略' % f)
        continue
    i = next(k for k, l in enumerate(L) if l.startswith(u'LINES = _tk.MAIN_LINES'))
    L[i:i] = BLOCK
    t = u'\n'.join(L)
    ast.parse(t)
    io.open(p, 'w', encoding=u'utf-8').write(t)
    print(u'%s｜通道插入於原 LINES 行前' % f)

p = os.path.join(WORK, u'v39secref.py')
L = io.open(p, encoding=u'utf-8').read().split(u'\n')
if not any('SRC_PATH' in l for l in L):
    i = next(k for k, l in enumerate(L) if l.startswith(u'L = io.open('))
    L[i:i] = [u'SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)'
              u'          # 274 輪・試跑通道',
              u'if SRC_PATH:',
              u'    NAME = SRC_PATH']
    t = u'\n'.join(L)
    ast.parse(t)
    io.open(p, 'w', encoding=u'utf-8').write(t)
    print(u'v39secref.py｜通道以改 NAME 之形插入')
print(u'———— 四尺試跑通道立訖')
