# -*- coding: utf-8 -*-
"""第 77 輪・第廿八報之入冊五刀（自裁定奪；數與文俱自算自取，不手打）。
甲・凡例款③之內部工作註記「（第 56 輪再定）」刪去（全書『第 N 輪』唯此一见，屬交付殘跡）。
乙・第一章「本律也不記他們曾為佛營造講堂」一說與律文相反——語料明記「六群比丘與佛修治講堂，遶堂周匝自掘地」
    （4 見俱此一事，因結自手掘地戒，書中第八章案例十即其事）➔ 改為如實，並引該句為款①（先自證連寫）。
丙・第九章案例七【第73條 條文】以「……」省至只餘「波逸提」，且佚去此戒立義之「更重增無知罪」➔ 依附錄補足。
丁・第八章案例一【第34條 條文】同病➔ 同法補足。
戊・第十四章案例五【第85條 條文】末作「波逸提。。」➔ 削一枚。
"""
import hashlib
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402
import lane  # noqa: E402
import _simpmap  # noqa: E402
import _tk  # noqa: E402

GO = u"--go" in sys.argv
DING_ERR = [u"后", u"台", u"据", u"毁", u"与", u"强", u"办", u"关", u"个", u"让", u"从", u"众", u"万",
            u"实", u"写", u"栏", u"征", u"会", u"优", u"卫"]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
BEFORE = list(L)
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []
touched = set()
NEWTEXT = []
CF = lane.corpus_flat()


def find(sub, note=u""):
    hit = [i for i, s in enumerate(L) if sub in s]
    if len(hit) != 1:
        errs.append(u"%s｜靶命中 %d：%s" % (note, len(hit), sub[:26]))
        return None
    touched.add(hit[0])
    return hit[0]


def rep(sub, old, new, note=u""):
    i = find(sub, note)
    if i is None or L[i].count(old) != 1:
        if i is not None:
            errs.append(u"%s｜靶非唯一：%s" % (note, old[:18]))
        return
    L[i] = L[i].replace(old, new)
    touched.add(i)
    NEWTEXT.append((note, new))


APX = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))


def rule_text(pian, num):
    """取附錄某篇某號之戒文（附錄乃產生器所出之逐字法源），『』改「」以從書中引號之成例。"""
    st = None
    for i in range(APX, len(L)):
        if L[i].startswith(u"## ") and pian in L[i]:
            st = i
        elif st is not None and L[i].startswith(u"## "):
            break
        elif st is not None:
            m = re.match(u"^%d\\. 「(.+?)」\\s*｜書中：" % num, L[i])
            if m:
                return m.group(1).replace(chr(0x300E), chr(0x300C)).replace(chr(0x300F), chr(0x300D))
    return None


# ── 甲・內部註記
rep(u"（第 56 輪再定）", u"**形制亦是聲明之一半**（第 56 輪再定）：", u"**形制亦是聲明之一半**：", u"甲・刪內部註記")
# ── 乙・「不記營造講堂」之如實
Q = u"時六群比丘與佛修治講堂，遶堂周匝自掘地"
print(u"乙・款①自證：『%s』連寫於語料 = %s" % (Q, lane.flat(Q) in CF))
if lane.flat(Q) not in CF:
    errs.append(u"乙・引語未中語料，不可掛款①")
n_jt = _tk.VINAYA.count(u"講堂")
n_gd = _tk.VINAYA.count(u"作功德")
n_xz = _tk.VINAYA.count(u"修治講堂")
print(u"乙・數自證：講堂 %d｜作功德 %d｜修治講堂 %d" % (n_jt, n_gd, n_xz))
for kw, want in ((u"『講堂』32 見", n_jt), (u"『作功德』12 見", n_gd)):
    if str(want) not in kw:
        errs.append(u"%s 之數不合（語料實 %d）" % (kw, want))
rep(u"本律也不記他們曾為佛營造講堂",
    u"本律也不記他們曾為佛營造講堂、積集功德（『講堂』%d 見皆屬佛所居之說處，『作功德』%d 見皆屬功德衣與自陳之語）" % (n_jt, n_gd),
    u"本律記他們為佛修治講堂——而正是為此犯戒：**「%s」**（『修治講堂』%d 見俱此一事，因結自手掘地戒，即第八章案例十之所據）"
    u"；營造於此不是功德，是被呵責的現場。『講堂』%d 見皆屬佛所居之說處，『作功德』%d 見皆屬功德衣與自陳之語" % (Q, n_xz, n_jt, n_gd),
    u"乙・講堂之說歸實")
# ── 丙丁・條文欄之攔腰截斷
for pian, num, mark, note in ((u"九十單提", 73, u"**【第73條 條文】：** 若比丘說戒時", u"丙・第73條補足"),
                              (u"九十單提", 34, u"**【第34條 條文】：** 若比丘至白衣家", u"丁・第34條補足")):
    rt = rule_text(pian, num)
    if not rt:
        errs.append(u"%s｜附錄查無該號戒文" % note)
        continue
    print(u"%s｜附錄全文（%d 字）：%s" % (note, len(rt), rt[:96]))
    if lane.flat(rt) not in CF:
        errs.append(u"%s｜補入之文非語料連寫，不可掛逐字" % note)
        continue
    i4 = find(mark, note)
    if i4 is None:
        continue
    old4 = L[i4]
    if u"……" not in old4:
        errs.append(u"%s｜今行本無『……』，所報已非今形" % note)
        continue
    tail4 = old4[len(old4.rstrip()):]                     # markdown 之硬換行（行尾兩空白）須一仍其舊
    new4 = old4.split(u"：**")[0] + u"：** " + rt + tail4
    L[i4] = new4
    touched.add(i4)
    NEWTEXT.append((note, new4))
# ── 戊・疊句號
rep(u"不語主人輒自敷座宿者，波逸提。。", u"波逸提。。", u"波逸提。", u"戊・削疊句號")

# ── 自查
print(u"刀後：%s" % u"・".join(n for n, _s in NEWTEXT))
sm = sorted({u"%s➔%s" % (c, _simpmap.MAP[c]) for c in set(u"".join(x for _n, x in NEWTEXT)) if c in _simpmap.MAP})
ding = sorted({c for c in set(u"".join(x for _n, x in NEWTEXT)) if c in DING_ERR})
print(u"新文簡形：MAP %s｜硬盯 %s" % (u"、".join(sm) or u"0", u"、".join(ding) or u"0"))
if sm or ding:
    errs.append(u"新文帶簡形")
for n2, t2 in enumerate(L):
    for dd in [u"。。", u"，，", u"：："]:
        if dd in t2 and t2.strip() != u"```":
            errs.append(u"L%d 仍帶疊標點 %s" % (n2 + 1, dd))
now = u"\r\n".join(L)
for a, b in ((u"「", u"」"), (u"『", u"』"), (chr(0x3010), chr(0x3011))):
    if now.count(a) - now.count(b) != raw.count(a) - raw.count(b):
        errs.append(u"引號之衡已變：%s%s" % (a, b))
for n3, t3 in [(i, L[i]) for i in sorted(touched)]:
    if chr(0x30FB) in t3 and not t3.startswith(u"|"):
        errs.append(u"L%d 帶中圓點" % (n3 + 1))
print(u"行數 %d ➔ %d" % (len(BEFORE), len(L)))
if len(L) != len(BEFORE):
    errs.append(u"本刀只改字句，不應增損行數")
print(u"新文逐條（目視）：")
for note, s in NEWTEXT:
    print(u"  [%s] %s" % (note, s[:168]))

if errs:
    print(u"✗ 擲不寫：")
    for e in errs:
        print(u"   " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
out = u"\r\n".join(L)
BK = HP.bakpath("77a")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
