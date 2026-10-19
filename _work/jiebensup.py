# -*- coding: utf-8 -*-
"""證『新冊⊇舊本之兩部戒本』：逐行比舊附錄之每一條目，是否原樣在新冊附錄三內。
   口徑：以『組頭＋號＋戒文前 24 字』為鑰；戒文之『｜書中：…』指針允許改號（relink 所為）。"""
import io
import re

HL = u'_archive/舊本/佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt'
BK = u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md'


def appx(path, start_key, end_key=None):
    t = io.open(path, encoding='utf-8-sig').read().replace(u'\r\n', u'\n')
    L = t.split(u'\n')
    i = next(k for k, l in enumerate(L) if start_key in l)
    j = next((k for k in range(i + 1, len(L)) if end_key and L[k].startswith(end_key)), len(L))
    return L[i:j]


def rows(seg):
    out = []
    grp = u'?'
    for l in seg:
        m = re.match(r'^#{2,4}\s*([甲乙]、[^（]*)', l)
        if m:
            grp = m.group(1).strip()
            continue
        m = re.match(u'^\\s*(\\d+)(?:[～~](\\d+))?\\.\\s*(.*)$', l)
        if m:
            txt = m.group(3).split(u'｜書中')[0].strip()
            out.append((grp, m.group(1), m.group(2) or u'', txt))
    return out


a = rows(appx(HL, u'附錄　全戒本歷條總表', u'# '))
b = rows(appx(BK, u'附錄三　全戒本歷條總對照表', u'## 附錄四'))
print(u'舊本之條目 %d・新冊之條目 %d' % (len(a), len(b)))

bkey = {}
for g, n, n2, txt in b:
    bkey.setdefault((g, n), []).append(txt)

lost = []
for g, n, n2, txt in a:
    cands = bkey.get((g, n), [])
    if not cands:
        lost.append((g, n, txt[:40]))
        continue
    head = txt[:24]
    if not any(head[:12] in c or c.startswith(head[:12]) for c in cands):
        lost.append((g, n, txt[:40]))
print(u'舊本有而新冊不合者：%d' % len(lost))
for g, n, t in lost[:20]:
    print(u'   %s 第%s號｜%s' % (g[:14], n, t))

extra = [(g, n, t[:34]) for g, n, n2, t in b if (g, n) not in
         {(x[0], x[1]) for x in a}]
print(u'新冊多出者（本輪自律藏補登）：%d 條' % len(extra))
seen = set()
for g, n, t in extra:
    if g not in seen:
        seen.add(g)
        print(u'   %s：%d 條（首：%s）' % (g[:26], len([1 for x in extra if x[0] == g]), t))
