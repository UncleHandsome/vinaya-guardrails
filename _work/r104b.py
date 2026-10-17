# -*- coding: utf-8 -*-
"""第 104 輪探針二：引號內出現、而語料全書無此形之字（逐字宣稱之殘留風險，『缽』即此式）。"""
import io, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tk

L = _tk.DOC.split("\n")
def skip(i):
    for tag in ("# 附錄C", "# 附錄K", "# 附錄L", "# 附錄M", "# 終卷"):
        pass
    return None

DROP = set()
cur = None
for i, l in enumerate(L):
    if l.startswith("# "):
        cur = l[2:8]
    if cur in (u"附錄C　", u"附錄K　", u"附錄L　", u"附錄M　") or u"修訂誌" in l or u"全書校勘記" in l or u"跨章款級" in l or u"十維驗收" in l or u"終卷" in l:
        DROP.add(i)
CORP = _tk.VINAYA + "".join(_tk.OTHER.values())
cnt = collections.Counter(); where = {}
for i, l in enumerate(L):
    if i in DROP:
        continue
    for m in re.finditer(u'「([^」]{1,60})」', l):
        for ch in set(m.group(1)):
            if u'\u4e00' <= ch <= u'\u9fff' and CORP.count(ch) == 0:
                cnt[ch] += 1
                where.setdefault(ch, (i + 1, m.group(0)[:26]))
for ch, n in cnt.most_common(40):
    ln, seg = where[ch]
    print("  %s(U+%04X) %2d 處  L%-6d %s" % (ch, ord(ch), n, ln, seg))
print("共 %d 形" % len(cnt))
