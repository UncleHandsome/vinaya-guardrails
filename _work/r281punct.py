# -*- coding: utf-8 -*-
"""281・生肉引文之標點重敷：把無句讀之逐字段，自本地語料之**原始檔**依碼位回圖重切片取回（帶標點），
   內層 「」 轉 『』（本書之式：外層 「」 掛逐字、內層 『』 為引中之引）。

口徑（四則）：
  （一）只治『印面逐字引號內最長無標點串 >= 40 字』者（量尺見 _work/v39chk.py 第 33 目）；
  （二）以刪節號 …… 分片，逐片歸一後於語料求其落檔，回圖取原始檔之切片（含標點）；
        一片不中即整段不動（不臆造標點）；
  （三）取回之片段須仍與語料逐字相合（norm 覆核），否則擲棄；
  （四）內層引號不平衡者，去其邊角之孤號，必使 『 與 』 成對（否則形制尺第 9 目即紅）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r281punct.py [--apply] [--lines 5326,5327,4980,4981]
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
BAK = os.path.join(ROOT, u'_work', u'ver39.pre281.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')
PUNCT = u'，。；：、！？「」‘’（）《》【】…—‧'
ELL = re.compile(u'\\u2026+')
Q = re.compile(u'\\u300c([^\\u300c\\u300d]+)\\u300d')


def longest_run(s):
    best = cur = 0
    for ch in s:
        if ch in PUNCT or ch.isspace():
            cur = 0
        else:
            cur += 1
            best = max(best, cur)
    return best


def raw_slice(pn):
    """歸一片段 ➔ 原始檔之帶標點切片（取首見者）。"""
    for fn, raw, nt, nm in v39align.CORPUS:
        pos = nt.find(pn)
        if pos < 0:
            continue
        a = nm[pos]
        b = nm[pos + len(pn) - 1] + 1
        return raw[a:b]
    return None


COMP = {u'[貝*為]': u'為'}   # CBETA 組字碼 ➔ 本書既定之通行字（276 舊文已作『為』）


def unbignify(s):
    for k, v in COMP.items():
        s = s.replace(k, v)
    assert not re.search(u'\[[^\]\s]{1,3}[*\/][^\]\s]{1,3}\]', s), s[:80]
    return s


def rebalance(s):
    s = s.replace(u'「', u'『').replace(u'」', u'』')
    while s.count(u'『') != s.count(u'』'):
        if s.startswith(u'』'):
            s = s[1:]
        elif s.endswith(u'』'):
            s = s[:-1]
        elif s.count(u'『') > s.count(u'』'):
            i = s.rfind(u'『')
            s = s[:i] + s[i + 1:]
        else:
            i = s.find(u'』')
            s = s[:i] + s[i + 1:]
    return s


targets = [int(x) for x in (sys.argv[[i for i, a in enumerate(sys.argv) if a == '--lines'][0] + 1].split(u',')
                            if '--lines' in sys.argv else [4980, 4981, 5326, 5327])]
print(u'正本 %d 行・sha %s' % (len(LINES), hashlib.sha256(TXT.encode(u'utf-8')).hexdigest()[:12]))
for ln in targets:
    line = LINES[ln - 1]
    m = Q.search(line)
    if not m:
        print(u'L%d 無逐字引號，擲過' % ln)
        continue
    inner = m.group(1)
    if longest_run(inner) < 40:
        print(u'L%d 最長無標點 %d 字，未達閾，擲過' % (ln, longest_run(inner)))
        continue
    parts = [p for p in ELL.split(inner) if len(_tk.norm(p)) >= 6]
    got, bad = [], []
    for p in parts:
        pn = _tk.norm(p)
        r = raw_slice(pn)
        if r is None:
            bad.append(p[:24])
            continue
        got.append(rebalance(unbignify(r)))
    if bad:
        print(u'L%d ✗ 有 %d 片不可求，整段不動：%s' % (ln, len(bad), bad[:2]))
        continue
    new_inner = u'……'.join(got)
    assert _tk.norm(new_inner).replace(u'……', u'') and True
    for p in parts:                                     # 覆核：新文之逐片仍須見於語料
        if _tk.norm(p) not in u''.join(_tk.norm(g) for g in got):
            print(u'L%d ✗ 覆核不合格：%s' % (ln, p[:20]))
            new_inner = None
            break
    if not new_inner:
        continue
    newline = line[:m.start(1)] + new_inner + line[m.end(1):]
    print(u'==== L%d｜舊最長無標點 %d 字 ➔ 新 %d 字（引文 %d ➔ %d 字）' % (
        ln, longest_run(inner), longest_run(new_inner), len(inner), len(new_inner)))
    print(u'   新：' + new_inner[:150])
    LINES[ln - 1] = newline

out = u'\n'.join(LINES)
left = [(i + 1, longest_run(m.group(1))) for i, l in enumerate(LINES) for m in Q.finditer(l)
        if longest_run(m.group(1)) >= 40]
print(u'全書仍有無標點長段：%d 段 %s' % (len(left), left[:6]))
print(u'改後 %d 行・sha %s' % (len(LINES), hashlib.sha256(out.encode(u'utf-8')).hexdigest()[:12]))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(TXT)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
print(u'落盤訖')
