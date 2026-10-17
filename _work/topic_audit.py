# -*- coding: utf-8 -*-
"""合併專題清單之查證尺（第卅三輪立）：外部（人或 AI）整理之「跨章專題」清單，逐條過三關——
   甲｜落點：該條號在書中之指針（法源＝gen_appendix.book_index，與附錄所標全等）是否即清單所稱之章與案。
   乙｜歸因：清單所稱人物是否真見於該條之「因緣段」＝前一條戒文之終 至 本條戒文之起（整段敘事）。
   丙｜犍度之案（無條號可據）：查書中該案塊有無此名，報丙級，與甲乙不同等。
   兩度自查之教：① 旧版以最後一個「爾時」截段，遇細判相連之篇便把因緣切掉大半，虛報『歸因無據』；
   ② 篇之第一條若以 0 為起点，窗會吞入前一整篇，任何名字都能在別篇敘事裡蒙中——兩病俱已修。
用法：python -X utf8 _work/topic_audit.py [清單檔]
清單每行：專題|篇|號|章|案序|人物1、人物2（篇＝gen_appendix 之 stem；犍度案篇位填「犍度」）
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import gen_appendix as G  # noqa: E402

LIST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, u"_topics.txt")
IDX, _, IDXR = G.book_index()
# 篇名在两部之中會撞名（比丘・尼各有「三十捨墮法」），故以 (部, stem) 為鍵；部由所稱之章推得
PLAN = {}
for q in G.PLAN:
    PLAN[(u"尼" if q[0].startswith(u"乙") else u"比", q[1])] = q
NICH = (u"十二", u"十三", u"十四", u"十五")
BK = io.open(G.BOOK, encoding="utf-8", newline="").read().split(u"\r\n")
CORP = {}


def corpus(tag):
    if tag not in CORP:
        CORP[tag] = G.corpus(tag)
    return CORP[tag]


def origin(fam, stem, num):
    """該條之因緣段。回傳 (段文, 有戒文?)。"""
    _, _, _, cat, exp, tag = PLAN[(fam, stem)]
    s = corpus(tag)
    rs = G.rules_of(s, stem, cat, exp)
    d = dict(rs)
    txt = d.get(num)
    if not txt:
        return u"", False
    j = s.find(txt)
    if j < 0:
        return u"", False
    k = [i for i, (n, _) in enumerate(rs) if n == num][0]
    if k == 0:
        p = s.rfind(stem, 0, j)              # 篇之第一條：起點取最近之篇題，勿從檔頭算起
        lo = p if p >= 0 else max(0, j - 3000)
    else:
        lo = s.find(d[rs[k - 1][0]]) + len(d[rs[k - 1][0]])
    return s[max(lo, j - 9000):j], True


def book_case(ch, cs):
    st = [i for i, l in enumerate(BK) if re.match(u"^# 第%s章" % ch, l)]
    if not st:
        return u""
    a = st[0]
    z = next((i for i in range(a + 1, len(BK)) if re.match(u"^# 第", BK[i])), len(BK))
    ci = [i for i in range(a, z) if BK[i].startswith(u"#### 案例%s：" % cs)]
    if not ci:
        return u""
    b = ci[0]
    e = next((i for i in range(b + 1, z) if re.match(u"^#{1,4} ", BK[i]) and i > b), z)
    return u"\n".join(BK[b:e])


def callers(seg):
    return sorted(set(re.findall(u"[\\u4e00-\\u9fff]{2,6}(?=白佛|白世尊|語諸比丘|往白佛|念言|作是念)", seg)))[:8]


rows = [x for x in io.open(LIST, encoding="utf-8").read().split(u"\n") if x.strip() and not x.startswith(u"//")]
res, bad_a, bad_b = {}, [], []
for r in rows:
    tp, stem, num, ch, cs, ppl = (r.split(u"|") + [u""])[:6]
    who = [w for w in re.split(u"[、,，]", ppl) if w.strip()]
    if stem == u"犍度":
        blk = book_case(ch, cs)
        a1 = u"✓" if blk else u"✗"
        bad = [w for w in who if w not in blk]
        a2 = u"○" if not who else (u"✓" if not bad else u"✗")
        note = u"丙級｜書中案塊 %d 字%s" % (len(blk), (u"｜無據：" + u"、".join(bad)) if bad else u"")
    else:
        n = int(num)
        fam = u"尼" if ch in NICH else u"比"
        cat = PLAN[(fam, stem)][3]
        hit = IDX.get((fam, cat, n)) or IDXR.get((fam, cat, n))
        a1 = u"✓" if hit and hit.split(u"案例")[0] == u"第%s章" % ch and (not cs or hit.endswith(u"案例" + cs)) else u"✗"
        seg, ex = origin(fam, stem, n)
        bad = [w for w in who if w not in seg]
        a2 = u"○" if not who else (u"✓" if not bad else u"✗")
        note = u"指針=%s｜因緣段 %d 字%s" % (hit or u"查無", len(seg), (u"｜無據：" + u"、".join(bad)) if bad else u"")
        if bad:
            note += u"\n      └ 段首：%s…\n      └ 段內呼名：%s" % (
                seg[:130].replace(u"\n", u""), u"、".join(callers(seg)) or u"無")
        if a1 == u"✗":
            note += u"\n      └ 書中今制之落點：%s" % (hit or u"（此號書中無指針）")
    tag2 = u"%s %s｜%s %s%s" % (a1, a2, ch, cs, (u"（第%s條）" % num) if num != u"-" else u"")
    print(u"%s %s｜%s" % (tag2, tp, note))
    res.setdefault(tp, []).append((a1, a2, tag2))
    if a1 == u"✗":
        bad_a.append(tag2 + u" " + tp)
    if a2 == u"✗":
        bad_b.append(tag2 + u" " + tp)

print(u"\n── 依專題統計（甲＝落點、乙＝歸因）──")
for tp, ls in res.items():
    print(u"專題%s：%d 筆｜落點有誤 %d｜歸因有誤 %d" % (
        tp, len(ls), sum(1 for x in ls if x[0] == u"✗"), sum(1 for x in ls if x[1] == u"✗")))
print(u"── 總 %d 筆｜落點有誤 %d｜歸因有誤 %d ──" % (len(rows), len(bad_a), len(bad_b)))
