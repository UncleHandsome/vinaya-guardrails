# -*- coding: utf-8 -*-
"""因緣全文器：以關鍵字定錨，吐出該條之完整段（自前一個卷尾標 (N) 至該條之尾標止）。
   條內含制戒因緣、嫌責、呵責、初制／重制、細判、開緣——撰稿取材之唯一來源。
用法：python -X utf8 _work/passage.py <檔序 如 11-21|01-10|22-30> 詞1 [詞2…]
     詞為該條戒文或其因緣之獨字串；多詞則逐一取段。
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = sys.argv[1]
FILES = [p for p in glob.glob(os.path.join(ROOT, "原文", "*.txt")) if TAG in os.path.basename(p)]
assert FILES, u"無原文檔 %s" % TAG
S = io.open(FILES[0], encoding="utf-8").read().replace("\r\n", "\n")
TAIL = re.compile(u"[(（]([〇零一二三四五六七八九十百]{1,5})竟?[)）]")
MARKS = [(m.start(), m.group(1), m.end()) for m in TAIL.finditer(S)]


def show(w):
    i = S.find(w)
    if i < 0:
        print(u"（語料無『%s』）" % w)
        return
    prev = [m for m in MARKS if m[2] <= i]
    a = prev[-1][2] if prev else 0
    nxt = [m for m in MARKS if m[0] >= i]
    b = nxt[0][2] if nxt else len(S)
    tail = nxt[0][1] if nxt else u"?"
    seg = S[a:b].strip()
    print(u"@@@@@ 『%s』｜條尾標 (%s)｜%d 字" % (w, tail, len(seg)))
    print(seg.replace(u"\n\n", u"\n"))
    print(u"")


for w in sys.argv[2:]:
    show(w)
