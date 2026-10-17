# -*- coding: utf-8 -*-
r"""印面三數之計器（第 244 輪立・向來逐輪手算，今歸一器）。

口徑（與歷輪終測同）：
  · 印面＝全檔剔**編纂底冊四篇**（附錄C 修訂誌・K 款級台帳・L 十維驗收・M 校勘記——不入印本）；
  · 含圍欄＝印面一切漢字（含 ``` 圍欄內）；
  · 剔圍欄＝印面圍欄外之漢字；圍欄內＝兩者之差。
  · 第 250 輪起底冊另檔，故另報主檔與備檔之各行數（母數＝兩者之和，與歷帳可比）。
用法：python -X utf8 _work/facecount.py    （只讀不寫，exit 0）
"""
import os
import re
import sys

sys.path.insert(0, "_work")
sys.path.insert(0, ".")
import _tk as t

CJK = re.compile(u"[一-鿿]")
L = t.LINES
BOT = t.bottom_lines()
in_fence = set()
run = False
for i, l in enumerate(L):
    if l.startswith(u"```"):
        run = not run
        continue
    if run:
        in_fence.add(i)

face = [i for i in range(len(L)) if i not in BOT]
inc = sum(len(CJK.findall(L[i])) for i in face)
exc = sum(len(CJK.findall(L[i])) for i in face if i not in in_fence)
n_main = len(t.DOC_MAIN.split(u"\n"))
n_bot = len(t.DOC_BOTTOM.split(u"\n")) if t.DOC_BOTTOM else 0
tail = (u"｜主檔 %d 行＋底冊備檔 %d 行" % (n_main, n_bot)) if n_bot else u"｜（底冊未另檔）"
print(u"母數 %d 行%s｜印面含圍欄 %d｜剔圍欄 %d｜圍欄內 %d（含 − 剔 = %d ✓）"
      % (len(L), tail, inc, exc, inc - exc, inc - exc))
sys.exit(0)
