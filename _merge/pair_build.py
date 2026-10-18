# -*- coding: utf-8 -*-
"""對位表產器：由 `_merge/掛載表.tsv` 抽『護欄 Ch.N 案M ↔ 框架母案碼』，
寫成 `_merge/對位表.tsv`（骨肉合流之 join 法源），並印涵蓋率。

用法：python -X utf8 _merge/pair_build.py
指南對位經第五輪機核『Ch/案指針零失指』，故可用其表、不以其表為骨。
"""
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_merge"))
import refnum as RN

TSV = os.path.join(ROOT, u"_merge", u"掛載表.tsv")
OUT = os.path.join(ROOT, u"_merge", u"對位表.tsv")
OLD = os.path.join(ROOT, "_archive", u"舊本")
H = io.open(glob.glob(os.path.join(OLD, u"佛陀的護欄*.txt"))[0], encoding="utf-8").read()

rows, cur = [], u""
for l in io.open(TSV, encoding="utf-8").read().split("\n"):
    if not l.strip().startswith(u"|"):
        continue
    cs = [c.strip() for c in l.strip().strip(u"|").split(u"|")]
    if len(cs) < 4:
        continue
    m = re.match(u"第([一二三四五六七八九十]+)章", cs[0])
    if m and u"同上" not in cs[0]:
        cur = u"第%s章" % m.group(1)
    codes = re.findall(u"〔(?:遮|開|僧)\\d+〕", cs[2])
    if not codes:
        continue
    for _hc, an in re.findall(u"Ch\\.?(\\d+)\\s*案([一二三四五六七八九十]+)", cs[1] + u" " + cs[3]):
        rows.append((u"第%s章" % RN.cn_num(int(_hc)), an, codes[0], cur,
                     cs[4] if len(cs) > 4 else u""))

seen, uniq = set(), []
for r in rows:
    if (r[0], r[1]) in seen:
        continue
    seen.add((r[0], r[1]))
    uniq.append(r)

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(u"# 由 掛載表.tsv 經 pair_build.py 產｜護欄原章\t案序\t框架母案\t指南所派本冊章\t正理\n")
    for r in uniq:
        f.write(u"\t".join(r) + u"\n")


def chap_body(hc):
    seg = H.split(u"# " + hc, 1)
    if len(seg) < 2:
        return u""
    return seg[1].split(u"\n# ")[0]


n_all = 0
got_all = 0
by = {}
for hc, an, *_ in uniq:
    by.setdefault(hc, set()).add(an)
print(u"對位表：%d 條｜寫入 %s" % (len(uniq), os.path.basename(OUT)))
for hc in [u"第%s章" % RN.cn_num(i) for i in range(1, 21)]:
    n = len(re.findall(u"^#### 案例", chap_body(hc), re.M))
    if not n:
        continue
    got = len(by.get(hc, ()))
    n_all += n
    got_all += got
    if got < n:
        print(u"   %-7s 卡 %2d／對位 %2d（未對位 %d）" % (hc, n, got, n - got))
print(u"涵蓋：%d／%d＝%d%%｜未對位 %d 張（此些須立子案碼或另裁）" % (
    got_all, n_all, got_all * 100 // n_all, n_all - got_all))
