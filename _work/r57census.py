# -*- coding: utf-8 -*-
"""第五十七輪・②之先：案例歸位清冊。

一口徑：案之篇聚『唯據其律文出處之卷段與戒篇』，不以節次臆推（前令「指針落點唯據源節實文」之例）。
出處取「#### 律文出處」下之引文，若無引文則退取案例題與所屬節題之 keyword；三者皆無者列入待判。
"""
import io
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
OUT = os.path.join(ROOT, u"_book", u"歸位清冊.tsv")

lines = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")

# 章・節・案 之位
CH = re.compile(u"^# (?:【(.+?)】|第([一二三四五六七八九十]+)章　(.+))$")
SEC = re.compile(u"^## (?:【(.+)】|第([一二三四五六七八九十]+)節　?(.*))$")
CASE = re.compile(u"^### 案例([一二三四五六七八九十百零〇]+)：(.+)$")

# 篇聚之鑰（依戒篇順序，長者先判）
KEYS = [
    (u"比丘尼", u"尼"),
    (u"波羅夷法", u"波羅夷"),
    (u"僧伽婆尸沙", u"僧殘"),
    (u"僧殘", u"僧殘"),
    (u"捨墮", u"捨墮"),
    (u"尼薩耆", u"捨墮"),
    (u"波逸提", u"單提"),
    (u"單提", u"單提"),
    (u"提舍尼", u"提舍尼"),
    (u"眾學", u"眾學"),
    (u"七滅諍", u"滅諍"),
    (u"滅諍", u"滅諍"),
    (u"犍度", u"犍度"),
    (u"揵度", u"犍度"),
    (u"調部", u"調部"),
]
PIN_ORDER = [u"波羅夷", u"僧殘", u"捨墮", u"單提", u"提舍尼", u"眾學", u"滅諍", u"犍度", u"調部", u"尼"]

rows = []
cur_ch = cur_sec = None
i = 0
while i < len(lines):
    l = lines[i]
    m = CH.match(l)
    if m:
        cur_ch = (m.group(2) or u"") and u"第%s章" % m.group(2) or l[2:].strip()
    elif l.startswith(u"## ") and not l.startswith(u"## 【卷末"):
        s = SEC.match(l)
        if s:
            cur_sec = (s.group(2) and u"第%s節" % s.group(2) or u"") + u" " + (s.group(3) or s.group(1) or u"")
    c = CASE.match(l)
    if c:
        # 向後搜本案區塊內之「律文出處」引文
        j, cite, block = i + 1, u"", []
        while j < len(lines) and not re.match(u"^#{2,3} ", lines[j]):
            block.append(lines[j])
            j += 1
        btxt = u"\n".join(block)
        mm = re.search(u"#### 律文出處\s*\n+> ?(.+)", btxt)
        if mm:
            cite = mm.group(1).strip()
        pins = []
        for k, p in KEYS:
            if k in cite:
                pins.append(p)
        src = u"出處"
        if not pins:
            for k, p in KEYS:
                if k in c.group(2):
                    pins.append(p)
            src = u"案題"
        if not pins:
            for k, p in KEYS:
                if k in cur_sec:
                    pins.append(p)
            src = u"節題" if pins else u"待判"
        pins = [p for p in dict.fromkeys(pins) if p]
        rows.append({
            u"章": cur_ch, u"節": cur_sec.strip(), u"號": c.group(1), u"題": c.group(2)[:40],
            u"聚": u"/".join(pins) or u"?", u"據": src, u"卷": u"",
        })
        vm = re.search(u"《四分律》卷([一二三四五六七八九十百零〇\d]+)", cite)
        if vm:
            rows[-1][u"卷"] = vm.group(1)
        i = j
        continue
    i += 1

CN = {u"一":1,u"二":2,u"三":3,u"四":4,u"五":5,u"六":6,u"七":7,u"八":8,u"九":9,u"十":10,
      u"十一":11,u"十二":12,u"十三":13,u"十四":14,u"十五":15,u"十六":16,u"十七":17,u"十八":18,u"十九":19,u"二十":20}
out = io.open(OUT, "w", encoding="utf-8", newline="\n")
out.write(u"\t".join([u"章", u"節", u"案號", u"案題", u"篇聚", u"判據", u"律卷"]) + u"\n")
for r in rows:
    out.write(u"\t".join([r[u"章"], r[u"節"], r[u"號"], r[u"題"], r[u"聚"], r[u"據"], r[u"卷"]]) + u"\n")
out.close()

print(u"案數：%d｜清冊：%s" % (len(rows), os.path.basename(OUT)))
print(u"判據來源：%s" % dict(Counter(r[u"據"] for r in rows)))
print(u"篇聚計數：%s" % dict(Counter(r[u"聚"] for r in rows)))
print(u"\n=== 章 × 篇聚 ===")
mat = defaultdict(Counter)
for r in rows:
    mat[r[u"章"]][r[u"聚"]] += 1
for ch in sorted(mat, key=lambda s: CN.get(s.replace(u"第", u"").replace(u"章", u""), 99)):
    print(u"%s（%d 案）：%s" % (ch, sum(mat[ch].values()), dict(mat[ch])))
print(u"\n=== 待判案 ===")
for r in rows:
    if r[u"據"] == u"待判":
        print(u"%s %s｜案%s %s" % (r[u"章"], r[u"節"], r[u"號"], r[u"題"]))
