# -*- coding: utf-8 -*-
"""281・尾句之補齊：標點重敷之後，四段引文皆截止於語料句中（如『長者牛不如』），讀來如斷句。
   此刀把每段末片延展至語料之下一個『。』（含），一字不臆造；無可補者不動。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r281tail.py [--apply]
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')
Q = re.compile(u'「([^「」]+)」')
ELL = re.compile(u'\\u2026+')


def last_piece(inner):
    ps = [p for p in ELL.split(inner) if len(_tk.norm(p)) >= 6]
    return ps[-1] if ps else None


def extend(inner):
    lp = last_piece(inner)
    if lp is None:
        return inner, None
    pn = _tk.norm(lp)
    for _fn, raw, nt, nm in v39align.CORPUS:
        pos = nt.find(pn)
        if pos < 0:
            continue
        b = nm[pos + len(pn) - 1]
        nxt = raw.find(u'。', b)
        if nxt < 0 or nxt - b > 12:
            continue
        tail = raw[b + 1:nxt + 1]
        if not tail or tail in inner:
            continue
        return inner + tail, tail
    return inner, None


for ln in (4980, 4981, 5326, 5327):
    line = LINES[ln - 1]
    m = Q.search(line)
    if not m:
        continue
    inner = m.group(1)
    new, tail = extend(inner)
    if not tail:
        print(u'L%-5d 末片已合句或無可補（不動）｜尾 …%s' % (ln, inner[-20:]))
        continue
    assert _tk.norm(new).startswith(_tk.norm(inner)), u'只可延展，不得改字'
    LINES[ln - 1] = line[:m.start(1)] + new + line[m.end(1):]
    print(u'L%-5d 補尾 %2d 字 ➔ …%s' % (ln, len(tail), new[-30:]))

out = u'\n'.join(LINES)
print(u'改後 %d 行・sha %s' % (len(LINES), hashlib.sha256(out.encode(u'utf-8')).hexdigest()[:12]))
if not APPLY:
    print(u'（乾跑）')
    sys.exit(0)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
print(u'落盤訖')
