# -*- coding: utf-8 -*-
"""第 75 輪・十線地圖之更新入冊（自裁定奪；指針與宣稱俱由尺之法源自算，不手填）。
甲・五枚新行：第十二章案例三／五／六・第十三章案例四／六——尼部兩章向不入十線（今涉章九，十二・十三不在內），
    依附錄倒排先證其條號與落點，而後落刀；插入一依章次 ascending，免破該線之序。
乙・指針形制歸一：「第六章第三節附論」非書中指針之形（附錄作「第六章第三節」），改歸正形，【過渡專題／附論】移入描述欄。
丙・宣稱歸實：導言增「十線共X行，點名Y案」（自算）；「第五至第九章與第十三至第十五章…四章合計逾百案」乃誤
    （四章實 71 案，且第十一章最密 28 案未被點名），改如實；第十四・十五章之案數與第二節之矩陣亦按實有陳之。
丁・形制補齊：第六線補導引段（十線唯此無導引）；《附記》以第四線（醫療照護）錯入「公共形象」一栏，今歸七，第四線另立一行。
戊・一枚簡形：「强制」➔「強制」（全書 56:1 之成例；`_simpmap.MAP` 不收『强』形，故刀自設盯形之閘）。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402
import mapchk as MC  # noqa: E402
import _simpmap  # noqa: E402

GO = u"--go" in sys.argv
# 兩級盯形：簡形之無可辯解者（硬退）；兩形同城者（如『回』『面』『干』之正字亦常用此形，只報不退，由目視定）
DING_ERR = [u"后", u"台", u"据", u"毁", u"与", u"强", u"办", u"关", u"乐", u"个", u"让", u"从",
            u"众", u"优", u"万", u"征", u"会", u"长", u"阳", u"云", u"叶", u"苏", u"卫"]
DING_EYE = [u"干", u"里", u"面", u"服", u"沉", u"回", u"余", u"艺", u"郁", u"适"]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
BEFORE = list(L)
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
touched = set()
NEWTEXT = []          # 本器實際落檔之新文（逐條存其形，寫檔前印碼目視）
errs = []

FORM = [(7, u"七"), (10, u"十"), (11, u"十一"), (14, u"十四"), (15, u"十五"), (20, u"二十"),
        (28, u"二十八"), (56, u"五十六"), (71, u"七十一"), (80, u"八十"), (103, u"一百零三"),
        (115, u"一百一十五"), (483, u"四百八十三")]
for x, want in FORM:
    got = MC._cn(x)
    if got != want or MC.cn2int(got) != x:
        errs.append(u"數詞之形不合：%d➔『%s』（期望『%s』）" % (x, got, want))


def find(sub, note=u""):
    hit = [i for i, s in enumerate(L) if sub in s]
    if len(hit) != 1:
        errs.append(u"錨命中 %d（%s）：%s" % (len(hit), note, sub[:26]))
        return None
    return hit[0]


def rep(sub, old, new, note=u""):
    i = find(sub, note)
    if i is None or L[i].count(old) != 1:
        if i is not None:
            errs.append(u"靶非唯一（%s）：%s" % (note, old[:18]))
        return
    L[i] = L[i].replace(old, new)
    touched.add(i)
    NEWTEXT.append((note, new))


def ins_after(sub, add, note=u""):
    i = find(sub, note)
    if i is None:
        return
    L[i + 1:i + 1] = add
    touched.update(range(i + 1, i + 1 + len(add)))
    NEWTEXT.extend((note, s) for s in add if s.strip())


def ins_before(sub, add, note=u""):
    i = find(sub, note)
    if i is None:
        return
    L[i:i] = add
    touched.update(range(i, i + len(add)))
    NEWTEXT.extend((note, s) for s in add if s.strip())


BR = chr(0x3010) + u"過渡專題" + chr(0xFF0F) + u"附論" + chr(0x3011)      # 【過渡專題／附論】
print(u"括號自構：%s｜碼位 %s" % (BR, u" ".join(u"U+%04X" % ord(c) for c in BR if ord(c) > 0x2000)))

# ── 乙・指針形制
rep(u"| 第六章第三節附論 |", u"| 第六章第三節附論 | 二不定法第1、2條 | 獨處屏處",
    u"| 第六章第三節 | 二不定法第1、2條 | " + BR + u"獨處屏處", u"指針形制")
# ── 丁・附記之錯配
rep(u"| 公共形象與信任資產 | 四、七 |", u"四、七", u"七", u"附記歸七")
ins_after(u"| 財務、消費與投機心態 | 一 |",
          [u"| 身體、照護與制度之溫厚 | 四 |"], u"附記補四")
# ── 丁・第六線導引
ins_after(u"## 六、語言的冷暴力——貶損、挑撥、恐嚇與失真的一字之差",
          [u"", u"這一線的案件全由一句話說完：罵人、傳話、嚇人、藏衣鉢、聽錯了再傳。"
                u"這些都不見血，也不犯重，合起來卻足以拆掉一座僧團的互信。"
                u"律的辦法不是勸人少說話，而是把話釘回說者身上——出口即算，不許推給一時失言。"],
          u"六線導引")
# ── 甲・五枚新行（先證後插：落點須與附錄同一，否則擲）
NEW = [
    (u"| 第十四章案例三 | 尼單提第82條 |",
     u"| 第十二章案例三 | 尼僧殘第7、8、9條 | 獨行四事與染心受食——落單的每一步先被堵住，不等出事才追 |",
     u"線三・第十二章案例三", [(u"尼", u"僧殘", 7), (u"尼", u"僧殘", 8), (u"尼", u"僧殘", 9)]),
    (u"| 第十一章案例九 | 羯磨矩陣 |",
     u"| 第十二章案例六 | 尼僧殘第14、15條 | 共住覆罪與教莫別住——同伴的包庇與拒絕隔離，是司法的第二道破口 |",
     u"線五・第十二章案例六", [(u"尼", u"僧殘", 14), (u"尼", u"僧殘", 15)]),
    (u"| 第十四章案例六 | 尼單提第78條 |",
     u"| 第十三章案例四 | 尼捨墮第24、25條 | 多畜好色器與畜長鉢——寺院陳設近似市肆，供養心先退一步 |",
     u"線七・第十三章案例四", [(u"尼", u"捨墮", 24), (u"尼", u"捨墮", 25)]),
    (u"| 第十四章案例六 | 尼單提第78條 |",
     u"| 第十三章案例六 | 尼捨墮第20～23條 | 四條迴物戒——把施主的指定撥回自己，是最難自察的微型權術 |",
     u"線七・第十三章案例六", [(u"尼", u"捨墮", n) for n in (20, 21, 22, 23)]),
    (u"| 第十五章案例二 | 尼單提第121",
     u"| 第十二章案例五 | 尼僧殘第5條 | 度賊女出家——准入之一漏，可引來滅僧之危 |",
     u"線八・第十二章案例五", [(u"尼", u"僧殘", 5)]),
]
_mlo, _mhi, _apx, _lines, _cases, _secs, _inv = MC.structure(BEFORE)


def apx_pos(who, key, n):
    out = set()
    for (w, p, k2), v in _inv.items():
        if w == who and key in p and k2 == n:
            out |= set(v)
    return out


for anc, row, note, proof in NEW:
    pos = row.split(u"|")[1].strip()
    for who, key, n in proof:
        hs = apx_pos(who, key, n)
        if pos not in hs:
            errs.append(u"%s：附錄指 %s 而非 %s" % (note, u"／".join(sorted(hs)) or u"查無", pos))
    cells = [x.strip() for x in row.strip().strip(u"|").split(u"|")]
    if len(cells) != 3 or not cells[2]:
        errs.append(u"%s：表格行須三欄且描述欄非空（今 %d 欄）" % (note, len(cells)))
for anc, row, note, proof in NEW:
    ins_before(anc, [row], note)
# ── 戊・簡形
rep(u"設强制考核期", u"强制", u"強制", u"强制歸強製")
# ── 自算（刀後之形）
mlo, mhi, apx, lines, cases, secs, inv = MC.structure(L)
xian = [x for x in lines if not x["title"].startswith(u"附記")]
data = [r for x in xian for r in x["rows"]]
ncase = len({r[1] for r in data if MC.MPCASE.match(r[1])})
per = {}
for (c, _k) in cases:
    per[c] = per.get(c, 0) + 1
l7 = next(x for x in xian if x["title"].startswith(u"七、"))
n7 = len(l7["rows"])
print(u"自算｜資料行 %d・點名 %d 案・第七線 %d 行｜各章案例 11:%d 7:%d 9:%d 8:%d 14:%d 15:%d" % (
    len(data), ncase, n7, per.get(11, 0), per.get(7, 0), per.get(9, 0), per.get(8, 0),
    per.get(14, 0), per.get(15, 0)))
# ── 丙・計數與宣稱（全取上算之數）
rep(u"九場公關災難", u"九場", u"%s場" % MC._cn(n7), u"七線標題場數")
rep(u"九樁「小事」", u"九樁", u"%s樁" % MC._cn(n7), u"七線導引樁數")
rep(u"這一段不新增論證，只做一件事",
    u"把全書一百一十五則案例按「同一種動作」重排十遍，每一線都標明書中今制的位置",
    u"把全書一百一十五則案例中最可通貫的一部分按「同一種動作」重排十遍："
    u"十線共%s行，點名%s案，每一行都標明書中今制的位置" % (MC._cn(len(data)), MC._cn(ncase)),
    u"導言行案宣稱")
dense = [11, 7, 9, 8]
ssum = sum(per[c] for c in dense)
rep(u"第五至第九章與第十三至第十五章是案例最密之處",
    u"第五至第九章與第十三至第十五章是案例最密之處，四章合計逾百案，不必一口氣讀盡。",
    u"案例最密之處是%s，%s章合計%s案，於全書一百一十五則案例中已過其半，不必一口氣讀盡。" % (
        u"、".join(u"第%s章（%s案）" % (MC._cn(c), MC._cn(per[c])) for c in dense),
        MC._cn(len(dense)), MC._cn(ssum)), u"節讀宣稱")
# 第十四・十五章之宣稱須實有其表
chk = {}
for c in (14, 15):
    lo = next(i for i, s in enumerate(L) if s.startswith(u"# 第%s章" % MC._cn(c)))
    seg = u"".join(L[lo:lo + 120])
    chk[c] = (u"板塊" in seg) or (u"矩陣" in seg)
    if not chk[c]:
        errs.append(u"第十五章宣稱有表而實無" if c == 15 else u"第十四章宣稱有表而實無")
rep(u"再回頭讀該章的矩陣圖**；其餘條目",
    u"再回頭讀該章的矩陣圖**；其餘條目",
    u"再回頭讀該章的矩陣圖**；第十四章（%s案）與第十五章（%s案）乃比丘尼不共單提，兩章第二節各立四大防護之矩陣表，"
    u"可先讀表再挑案例；其餘條目" % (MC._cn(per[14]), MC._cn(per[15])), u"十四十五節讀")
# ── 自查一：尺之法源（非另抄一份）
rp = MC.row_problems(L)
print(u"刀後行數 %d→%d｜row_problems %d 條" % (len(BEFORE), len(L), len(rp)))
for x in rp[:12]:
    print(u"   L%-5d %s｜%s" % (x[0], x[1], x[2]))
if rp:
    errs.append(u"指針未清：%d 條" % len(rp))
if len(cases) != 115:
    errs.append(u"案例戶口漂移：%d" % len(cases))
if len(inv) != 483:
    errs.append(u"附錄鍵數漂移：%d" % len(inv))
# ── 自查二：所觸行之簡形（MAP∪盯形）・標點之制・引號之衡
sm, ding, eye = set(), set(), set()
allnew = u"".join(s for _n, s in NEWTEXT)
for c in set(allnew):
    if c in _simpmap.MAP:
        sm.add(u"%s➔%s" % (c, _simpmap.MAP[c]))
    if c in DING_ERR:
        ding.add(u"%s(U+%04X)" % (c, ord(c)))
    if c in DING_EYE:
        eye.add(u"%s(U+%04X)" % (c, ord(c)))
print(u"新文 %d 段｜MAP 之簡形：%s｜硬盯：%s｜目視：%s" % (
    len(NEWTEXT), u"、".join(sorted(sm)) or u"0", u"、".join(sorted(ding)) or u"0",
    u"、".join(sorted(eye)) or u"0"))
if sm or ding:
    errs.append(u"新文帶簡形")
for i in sorted(touched):
    s = L[i]
    if chr(0x30FB) in s:
        errs.append(u"L%d 带中圓點（本書之制：圍欄外須 0）" % (i + 1))
    if u"/" in s:
        errs.append(u"L%d 帶半形斜線" % (i + 1))
now = u"\n".join(L)
for a, b in ((u"「", u"」"), (u"『", u"』"), (chr(0x3010), chr(0x3011))):
    d0 = raw.count(a) - raw.count(b)
    d1 = now.count(a) - now.count(b)
    if d0 != d1:
        errs.append(u"全書引號之衡已變：%s%s %+d→%+d" % (a, b, d0, d1))
    print(u"  引號衡 %s%s：%+d（原 %+d）" % (a, b, d1, d0))
print(u"新文逐條（全文目視）：")
for note, s in NEWTEXT:
    print(u"  [%s] %s" % (note, s))

if errs:
    print(u"✗ 擲不寫：")
    for e in errs:
        print(u"   " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
out = u"\r\n".join(L)
BK = HP.bakpath("75a")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk2 = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk2.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk2 == out else u"不等!", os.path.relpath(BK, ROOT)))
