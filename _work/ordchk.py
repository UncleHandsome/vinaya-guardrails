# -*- coding: utf-8 -*-
"""ordchk.py —— 序數歸一尺（第 44 輪立）。

緣起：refchk 之甲乙丙丁皆不問「第N僧殘／第N波羅夷」與其後所系之罪名是否同指一條。
      此族之錯植歷輪四次由外審或人工逮得（「第四重僧殘：與白衣往還」應作第十二僧殘、
      「摩觸八事誤作初一二波羅夷」等），第 44 輪自查又逮三處——本尺補此缺口。

法源三層（皆非本書自述）：
 ① 附錄該序之戒文：`gen_appendix` 自語料逐字取出，故「序↔戒文」之配對已由語料閘守住；
 ② 該號在書中的落點：附錄『書中：』指針若作『第X章案例Y』，反查該案例題（含小節題）；
 ③ ALIAS 律家簡名：後世律家之罪名、本律無此語者，放行並記其據——免把簡名讀成錯植。
判準：取宣稱之名的二字窗（摺異體、去標點、去泛字），任一窗落於①或②即成立；皆不落者查③；
      三者皆空報「序數錯植」。範圍式（「第六、第七」「第十至第十三」）先展開，任一序合格即過。
      標題行（# 開頭）與目錄案例題只作池、不被檢，免自證。
用法：python -X utf8 _work/ordchk.py [-v] [--book=副本]（副本供負測植病）
退出碼：錯植數（0 即無病）。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk                                            # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
for a in sys.argv:
    if a.startswith(u"--book="):
        BOOK = a[7:]
NUM = {u"一": 1, u"二": 2, u"三": 3, u"四": 4, u"五": 5, u"六": 6, u"七": 7, u"八": 8, u"九": 9,
       u"十": 10, u"十一": 11, u"十二": 12, u"十三": 13, u"十四": 14, u"十五": 15, u"十六": 16,
       u"十七": 17}
KINDS = [u"波羅夷", u"僧殘", u"捨墮", u"提舍尼"]
DROP = set(u"之與及以而於所者了中此第")
# ③ 兩類放行，皆須写明其據（不得 silently 豁免）：
#   ALIAS＝律家／本書之罪名簡寫，序位本對，唯字形與律文異；
#   GLOSS＝靶點以序系「本書評語」而非罪名（如「第十、十一僧殘：滅諍之責」），不比字。
ALIAS = [(u"僧殘", u"甲", 11, u"朋黨", u"律文作「有餘伴黨」，書中另作「群黨」——今語之系，序位無誤"),
         (u"僧殘", u"甲", 12, u"污家", u"律文作「污他家、行惡行」，本書簡作「污家」"),
         (u"僧殘", u"乙", 12, u"污家", u"尼端律文亦作「污他家」，同上")]
# ⑤ 欄位標籤非罪名：第 69 輪新第十二章作「**【第七僧殘·條文】：** 律文」之形——
#   『條文』二字自不成罪名之窗，舊尺遂誤報錯植。此欄實帶整段戒文，故不只能放行，
#   還可比舊題更進一步：拿欄內之文與該序之附錄律文對勘，序與文不合者即病。
LANE = (u"條文", u"律文", u"戒文")
TIAO = re.compile(u"^(?:>\\s*)?\\*\\*【第[^】]*】：\\*\\*\\s*(.+?)\\s*$")
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
CHNUM = re.compile(u"^#\\s*第([一二三四五六七八九十]{1,3})章")
GLOSS = [(u"僧殘", (10, 11), u"朋黨惡行", u"以二序合系一評，非罪名"),
         (u"僧殘", (10, 11), u"滅諍之責", u"同上"),
         (u"僧殘", (10, 11), u"隔離之效應", u"同上"),
         (u"僧殘", (10, 11), u"暴力與分裂之尼僧版", u"同上"),
         (u"僧殘", (6, 7), u"身語洗淨之拖遲", u"尼端第六隨舉・第七獨行，本書合系一評")]
CLAIM_T = (u"第([一二三四五六七八九十]{1,3})(?:至第([一二三四五六七八九十]{1,3}))?"
           u"([、，]?第?([一二三四五六七八九十]{1,3}))?"
           u"%s(?:戒|法)?[：:·]{1,2}([^】，。；、）)\\n]{2,16})")
_c = {}


def claim(kind):
    if kind not in _c:
        _c[kind] = re.compile(CLAIM_T % kind)
    return _c[kind]


L = io.open(BOOK, encoding="utf-8", newline=u"").read().split(u"\r\n")
ai = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
rule = {}                                            # (篇, 序) →（戒文, 書中指針）
sec = None
for s in L[ai:]:
    if s.startswith(u"## "):
        sec = s[3:].strip()
        continue
    m = re.match(u"^(\\d+)(?:～(\\d+))?\\. (.+?)　｜書中：(.*)$", s)
    if not (m and sec):
        continue
    for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
        rule[(sec, k)] = (m.group(3), m.group(4))
secs = sorted(set(k[0] for k in rule))
head_t = {}                                          # 章序 → 該章各標題（節題・案例題）
ch = 0
for i in range(ai):
    m = re.match(u"^# 第(.+?)章", L[i])
    if m:
        ch = NUM.get(m.group(1), ch)
        continue
    if L[i].startswith(u"####") and ch:
        head_t.setdefault(ch, []).append(L[i][4:].strip())
HEAD = re.compile(u"^#")
TOCLINE = re.compile(u"^\\*\\s*案例")


def pools(kind, n):
    out = []
    for s in [x for x in secs if kind in x]:
        if (s, n) in rule:
            out.append((u"乙" if u"比丘尼" in s else u"甲", rule[(s, n)][0], rule[(s, n)][1]))
    return out


def wins(t):
    t = _tk.norm(t)
    return set(t[x:x + 2] for x in range(len(t) - 1))


titles = {}                                      # 池②（序號限定）：標題與目錄案例題把 (類,序) 系於何名
for i in range(ai):
    s = L[i]
    if not (HEAD.match(s) or TOCLINE.match(s)):
        continue
    for kind in KINDS:
        for m in claim(kind).finditer(s):
            a = NUM.get(m.group(1))
            b = NUM.get(m.group(2) or m.group(1))
            e = NUM.get(m.group(4)) if m.group(4) else None
            ns = list(range(a, b + 1)) if (a and b) else []
            if e:
                ns.append(e)
            for n in ns:
                titles[(kind, n)] = titles.get((kind, n), u"") + m.group(5) + u"　"


def loc_heads(kind, n):
    return titles.get((kind, n), u"")


verbose = u"-v" in sys.argv
SK = u"--skip" in sys.argv
bad = tot = nalias = n5 = 0
title_only = []
cuch = None
for i in range(ai):
    s = L[i]
    mc = CHNUM.match(s)
    if mc:
        cuch = mc.group(1)
        continue
    if HEAD.match(s) or TOCLINE.match(s):
        continue
    for kind in KINDS:
        for m in claim(kind).finditer(s):
            a = NUM.get(m.group(1))
            b = NUM.get(m.group(2) or m.group(1))
            e = NUM.get(m.group(4)) if m.group(4) else None
            ns = list(range(a, b + 1)) if (a and b) else []
            if e:
                ns.append(e)
            nm = m.group(5).strip()
            mt = TIAO.match(s)
            if nm in LANE and mt:                   # ⑤ 條文欄：以欄內戒文直對該序之律文
                # 欄文常以「……」節去中間之諫辭（三諫之文最長），故須分段依序對位，
                # 不可整段求前後綴——求前後綴者五條俱亡（第 69 輪首版之教）。
                frags = [_tk.norm(PUNC.sub(u"", x)) for x in re.split(u"……|…", mt.group(1))
                         if len(_tk.norm(PUNC.sub(u"", x))) >= 4]
                hit = None
                for n in ns:
                    for side, txt, loc in pools(kind, n):
                        t = _tk.norm(PUNC.sub(u"", txt))
                        pos, good = 0, bool(frags) and len(t) >= 10
                        for f in frags:
                            q = t.find(f, pos)
                            if q < 0:
                                good = False
                                break
                            pos = q + len(f)
                        if not good:
                            continue
                        home = cuch is not None and (u"第" + cuch + u"章") in loc
                        if hit is None or home:
                            hit = (n, side, u"⑤條文欄對勘" + (u"・本章指針合" if home else u"・指針他章"))
                if hit:
                    n5 += 1
                    tot += 1
                    if verbose:
                        print(u"✓ L%d｜%s＝序%s（%s・%d 段）" % (
                            i + 1, m.group(0)[:22], hit[0], hit[2], len(frags)))
                    continue
                bad += 1
                print(u"✗ L%d｜…%s…｜條文欄之文與此序之律文不合（序 %s・欄段 %s）" % (
                    i + 1, s[max(0, m.start() - 16):m.end() + 4], ns,
                    u"∥".join(f[:14] for f in frags)[:70]))
                continue
            w = set(x for x in wins(nm) if kind not in x and not (x[0] in DROP or x[1] in DROP))
            if not ns or not w:
                if SK and ns and nm:
                    print(u"s L%d｜跳｜%s｜名『%s』窗=%s" % (i + 1, m.group(0)[:20], nm[:16], u"/".join(sorted(w))[:40]))
                continue
            tot += 1
            ok = None
            for n in ns:
                for side, txt, loc in pools(kind, n):
                    hay = _tk.norm(txt + u"　" + loc_heads(kind, n))
                    if any(x in hay for x in w):
                        inrule = any(x in _tk.norm(txt) for x in w)
                        if not inrule:
                            title_only.append(u"L%d %s" % (i + 1, m.group(0)[:18]))
                        ok = (n, side, u"①戒文" if inrule else u"②僅據標題")
                        break
                if ok:
                    break
            if not ok:
                for (k2, side, q, word, why) in ALIAS:
                    if k2 == kind and q in ns and word in nm and any(side == p[0] for p in pools(kind, q)):
                        ok = (q, side, u"③律家簡名")
                        nalias += 1
                        if verbose:
                            print(u"  ○ 放行｜%s｜『%s』——%s" % (m.group(0)[:20], word, why))
                        break
            if not ok:
                for (k2, q, word, why) in GLOSS:
                    if k2 == kind and word in nm and set(ns) <= set(q):
                        ok = (q[0], u"－", u"④本書評語")
                        nalias += 1
                        if verbose:
                            print(u"  ○ 放行｜%s｜『%s』——%s" % (m.group(0)[:20], word, why))
                        break
            if ok:
                if verbose:
                    print(u"✓ L%d｜%s＝序%s（%s）" % (i + 1, m.group(0)[:22], ok[0], ok[2]))
            else:
                bad += 1
                cand = u"｜".join(u"%s端%d：%s" % (sd, n, tx[:14])
                                  for n in ns for sd, tx, lc in pools(kind, n))
                print(u"✗ L%d｜…%s…｜名『%s』無一窗配得着此序｜律文今注：%s" % (
                    i + 1, s[max(0, m.start() - 16):m.end() + 4], nm[:16], cand[:120]))
# ⑥ 條文欄之『攔腰截斷』（第 77 輪立・外路第廿八報之線索）：全書 244 支條文欄以「……」省中段者凡 18 支，
#    省三諫之諫辭乃舊例（長文難排，前後段俱存）；惟省至**只餘結罪詞**者，等於把該戒的要件整段抹去而不成句
#    （今逮兩處：九十單提第34條・第73條——後者並省去『更重增無知罪』一句，正是此戒所以立義之處）。
#    結罪詞之集不手打，自附錄各條之末句實算（附錄乃產生器所出之逐字法源）。
APX0 = next((n for n, t in enumerate(L) if t.startswith(u"# 附錄")), len(L))
VERD = set()
for t in L[APX0:]:
    m = re.match(u"^\\d+(?:～\\d+)?\\. .*，([^，。]{2,12})。」", t)
    if m:
        VERD.add(_tk.norm(m.group(1)))
cut6 = []
for n, t in enumerate(L[:APX0]):
    if u"條文】：" not in t or u"……" not in t:
        continue
    core = _tk.norm(PUNC.sub(u"", t.rsplit(u"……", 1)[-1]))
    if core and core in VERD:
        cut6.append((n + 1, core, t[:70]))
print(u"⑥條文欄以『……』省至只餘結罪詞（結罪詞集自附錄末句，%d 形）：%d 處" % (len(VERD), len(cut6)))
for n, core, t in cut6:
    print(u"✗ L%d｜『……%s』省成爛尾（要件佚）｜…%s…" % (n, core, t[-52:]))

# ⑦ 合併號標籤之殘留（第 81 輪立・外路第三十報之線索）：「【第A、B條 條文】」若其下所宣唯首條之文，
#    而 B 於同案之內另有單條標籤，則此合併號領不動它所宣的號——讀者見「第A、B條」而只得 A，B 在別處。
#    判式：合併號之餘號與同案稍後之單條標籤有交即紅。此形多生於「先合併、後又拆開」之改稿殘跡。
LBL = re.compile(u"【第([^】]{1,24})條 條文】")


def _labels(lines, a, b):
    out = []
    for k in range(a, b):
        for m in LBL.finditer(lines[k]):
            out.append((k, m.group(1).strip()))
    return out


def _case_end(lines, n, lim):
    for k in range(n + 1, lim):
        if lines[k].startswith(u"#### 案例") or (lines[k].startswith(u"# ") and u"章" in lines[k][:10]) \
           or lines[k].startswith(u"# 附錄"):
            return k
    return lim


dbl = []
for _n in range(APX0):
    for _k, spec in _labels(L, _n, _n + 1):
        if u"、" not in spec and u"～" not in spec:
            continue
        nums = [x.strip() for x in re.split(u"[、～]", spec) if x.strip()]
        later = {s for _k2, s in _labels(L, _n + 1, _case_end(L, _n, APX0))}
        dup = [x for x in nums[1:] if x in later]
        if dup:
            dbl.append((_n + 1, spec, u"、".join(dup)))
print(u"⑦合併號之條文標籤而其餘各號另立單條者：%d 處" % len(dbl))
for _n, spec, dup in dbl:
    print(u"✗ L%d｜『第%s條』之下唯首條之文，另見『第%s條』單標" % (_n, spec, dup))
_pl = [u"#### 案例X", u"> **【第97、98條 條文】：** 甲", u"> **【第98條 條文】：** 乙"]
_nh = 0
for _n, s in enumerate(_pl):
    for _k, spec in _labels(_pl, _n, _n + 1):
        if u"、" in spec:
            nums = [x.strip() for x in re.split(u"[、～]", spec)]
            later = {y for _k2, y in _labels(_pl, _n + 1, len(_pl))}
            _nh += 1 if [x for x in nums[1:] if x in later] else 0
print(u"  ⑦之負測｜植『第97、98條→第98條』逮 %d（宜 1）" % _nh)

print(u"== 核 %d 處序數↔罪名宣稱｜放行律家簡名 %d 處｜條文欄對勘 %d 處｜序數錯植 %d 處" % (
    tot, nalias, n5, bad))
print(u"僅據標題（戒文無此語，須於新寫標題時以 -v 複看）：%d 處｜%s" % (
    len(title_only), u"、".join(title_only[:14])))
sys.exit(1 if (bad or cut6 or dbl or _nh != 1) else 0)
