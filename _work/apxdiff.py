# -*- coding: utf-8 -*-
"""附錄之對單：產生器草稿 vs 書中現附錄，逐行示異（apxchk 之漂移檢只報「有無不合」，
   此器報「不合者何行」——凡動過 gen_appendix 或 append_appendix，先跑此器再寫檔。
用法：python -X utf8 _work/apxdiff.py"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import difflib
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
import os
NEW = os.path.join(os.path.dirname(os.path.abspath(__file__)), u"appendix_jieben.md")
L = io.open(BOOK, encoding="utf-8", newline=u"").read().split(u"\r\n")
a = [i for i, s in enumerate(L) if s.startswith(u"# 附錄")]
assert len(a) == 1, u"附錄起點 %d 處" % len(a)
nl = io.open(NEW, encoding="utf-8", newline=u"").read().replace(u"\r\n", u"\n").split(u"\n")
ol = [x.rstrip() for x in L[a[0]:] if x.strip()]
nn = [x.rstrip() for x in nl if x.strip()]
print(u"書中附錄非空行 %d｜草稿非空行 %d｜差 %+d" % (len(ol), len(nn), len(nn) - len(ol)))
k = 0
for line in difflib.unified_diff(ol, nn, u"書中", u"草稿", lineterm=u"", n=1):
    k += 1
    if k <= 60:
        print(line)
print(u"異動 %d 处（含題頭與節記；0 即兩處純相同）" % max(k - 2, 0))
