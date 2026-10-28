# -*- coding: utf-8 -*-
"""第 70 輪・甲：新第十三章草稿之預修刀＋入冊（法度同 hlfix69）。
刀序：草稿先行（逐條命中斷言）→ 形制（表格縮排・數字板式・斜體・條文欄序號）→ 款①歸真／降式樣
      → 指針歸位（第七章案例之錯指）→ 迎回舊章考訂（厥修羅・十八條之號次與連誦三則）→ 刪補最後
      → 圍欄重鑄 → 自證四閘（逐字・條文欄序號對勘・簡形・形制＋負測）→ 行錨入冊。
用法：python -X utf8 _work/hlfix70.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import _tk
import lane
from _simpdict import MAP as SIMP

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\00bfabe8-3a8f-4f54-9e66-19f223805657.txt"
BOOK = HP.SRC
BAK = HP.bakpath("70a")
GO = u"--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")
LABR = re.compile(u"^>\\s*\\*\\*【第([^】]*?)條?\\s*條文】：\\*\\*\\s*(.+)$")


def nm(s):
    return _tk.norm(PUNC.sub(u"", s))


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


dr_raw = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert dr_raw.count(u"\r") == dr_raw.count(u"\n") == dr_raw.count(u"\r\n"), u"草稿 CRLF 異常"
D = dr_raw.split(u"\r\n")
assert D[0] == u"---" and D[1] == u"", u"草稿首兩行非『---＋空行』：%r" % D[:2]
assert D[2].startswith(u"# 第十三章"), u"稿L3 非 H1：%r" % D[2][:30]
# 全稿行號一律照附件原號（章界之『---』留於列首，入冊時才削，免諸刀之號漂移）
N0 = len(D)
print(u"草稿 %d 行（末行『%s』）" % (N0, D[-1][:24]))

book_raw0 = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert book_raw0.count(u"\r") == book_raw0.count(u"\n"), u"正本入口 CRLF 已傷"
B0 = book_raw0.split(u"\r\n")


def harvest(snip, start=None, endsnip=None):
    hits = [l for l in B0 if snip in l]
    assert len(hits) == 1, u"迎回錨在正本見 %d 處（欲 1）：%s" % (len(hits), snip[:18])
    l = hits[0]
    if start is None:
        return l
    a = l.index(start)
    return l[a:] if endsnip is None else l[a:l.index(endsnip) + len(endsnip)]


# 附錄之尼三十捨墮各行律文（條文欄序號對勘之法源）
APXN = {}
_sec = u""
for l in B0[next(i for i, x in enumerate(B0) if x.startswith(u"# 附錄")):]:
    if l.startswith(u"## "):
        _sec = l[3:]
        continue
    m = re.match(u"^(\\d+)\\. 「(.+?)」　｜書中：", l)
    if m and u"尼" in _sec and u"三十捨墮" in _sec:
        APXN[int(m.group(1))] = m.group(2)
assert len(APXN) == 30, u"附錄尼三十捨墮取 %d 行（欲 30）" % len(APXN)


def do(tag, ln, old, new, want=1):
    i = ln - 1
    c = D[i].count(old)
    assert c == want, u"%s｜稿L%d 命中 %d（欲 %d）：%s" % (tag, ln, c, want, old[:26])
    assert old != new, u"%s｜舊新同形" % tag
    D[i] = D[i].replace(old, new)
    print(u"  %s 稿L%-4d ✓×%d" % (tag, ln, want))


print(u"\n―― 甲・形制與交付殘跡 ――")
# 表格須出格（全書 115 枚表行俱在縮排 0，本稿縮二則可能被 pandoc 併入上一列表項而不成表）
tb = [i for i, l in enumerate(D) if l.startswith(u"  |")]
assert len(tb) == 6, u"縮排表格行 %d 枚（欲 6）" % len(tb)
for i in tb:
    D[i] = D[i][2:]
print(u"  甲1 表格出格 ✓×%d（稿L%d..L%d）" % (len(tb), tb[0] + 1, tb[-1] + 1))
# 數字板式：全書成例『第24條』無空格（737 見），本稿帶空格者 14 見
sp = [i for i, l in enumerate(D) if re.search(u"第 \\d", l) or re.search(u"\\d 條", l)]
nsp = 0
for i in sp:
    D[i], k = re.subn(u"(第) (\\d)", u"\\1\\2", D[i])
    D[i], k2 = re.subn(u"(\\d) (條)", u"\\1\\2", D[i])
    nsp += k + k2
print(u"  甲2 數字板式歸成例：『第 N 條』去空格 %d 枚（涉 %d 行）" % (nsp, len(sp)))
# 斜體（Markdown emphasis）非本書之形：削其例如从句，細目改由（三）款之連誦清單任之
IT = [i for i, l in enumerate(D) if re.search(u"(?<!\\*)\\*[^*\\s][^*]*\\*(?!\\*)", l) and not l.startswith(u"* ")]
assert len(IT) == 1, u"斜體行 %d 枚（欲 1）：%s" % (len(IT), [x + 1 for x in IT])
i = IT[0]
m = re.match(u"^(\\s*)\\*例如：[^*]*\\*\\s*(.*)$", D[i])
assert m, u"斜體行形不认得：%r" % D[i][:60]
D[i] = m.group(1) + m.group(2)
print(u"  甲3 削斜體之『例如』从句（稿L%d・星號落入印面之危既除，細目由（三）款之連誦清單任之）" % (i + 1))
# 未序號之條文欄補號（俾序號對勘有靶）
do(u"甲4", 81, u"**【條文】：**", u"**【第2條 條文】：**")
do(u"甲5", 169, u"**【條文】：**", u"**【第19條 條文】：**")

print(u"\n―― 乙・款①之歸真（律語回原形）――")
do(u"乙1", 120, u"**「常望此衣，更不自辦」**", u"**「常望此衣，更不辦衣」**")
do(u"乙2", 146, u"我知正法，如是有何正法？多畜好色鉢，故鉢狼藉在地，與瓦肆（碗盤雜貨鋪）無異！",
   u"我知正法，如是何有正法？多畜好色鉢，故鉢狼藉在地，與瓦肆無異！")
do(u"乙3", 146, u"無異！」** 佛陀嚴詞呵責", u"無異！」**（瓦肆者，碗盤雜貨鋪也。）佛陀嚴詞呵責")
def sub_all(tag, old, new, want):
    n = sum(l.count(old) for l in D)
    assert n == want, u"%s｜全稿命中 %d（欲 %d）：%s" % (tag, n, want, old[:20])
    for i, l in enumerate(D):
        if old in l:
            D[i] = l.replace(old, new)
    print(u"  %s 全稿 ✓×%d" % (tag, n))


sub_all(u"乙4", u"偷蘭難陀", u"偷羅難陀", 7)

print(u"\n―― 丙・款①之降式樣（今語與本書術語，去其自稱逐字之形）――")
for t, ln, k in [(u"丙1", 22, 1), (u"丙2", 23, 1), (u"丙3", 24, 2), (u"丙4", 25, 2), (u"丙5", 26, 1),
                 (u"丙6", 27, 1), (u"丙7", 110, 1), (u"丙8", 127, 1), (u"丙9", 130, 1), (u"丙10", 131, 1),
                 (u"丙11", 132, 1), (u"丙13", 179, 1), (u"丙14", 198, 1), (u"丙15", 204, 1)]:
    i = ln - 1
    hits = [m.group(1) or m.group(2) for m in PAT1.finditer(D[i])]
    assert len(hits) == k, u"%s｜稿L%d 款① %d 枚（欲 %d）：%s" % (t, ln, len(hits), k, D[i][:60])
    D[i] = PAT1.sub(lambda m: u"「%s」" % (m.group(1) or m.group(2)), D[i])
    print(u"  %s 稿L%-4d 降 ✓ %s" % (t, ln, u"｜".join(x[:22] for x in hits)))
# 丙12：粗體包著兩支引號（『**「甲」與「乙」**』）非款①之形，PAT1 抓不到，逐枚削其星號
do(u"丙12a", 153, u"心理學上的**「築巢本能", u"心理學上的「築巢本能")
do(u"丙12b", 153, u"美學自戀」**。", u"美學自戀」。")

print(u"\n―― 丁・指針歸位（第七章之案例序，依條號對實題）――")
do(u"丁1", 92, u"這與本書第七章案例十三（比丘離三衣宿戒）", u"這與本書第七章案例二（比丘離三衣宿戒）")
do(u"丁2", 123, u"【第七章案例十三：比丘第2條離三衣宿", u"【第七章案例二：比丘第2條離三衣宿")
do(u"丁3", 149, u"【第七章案例十一：比丘第21條畜長鉢", u"【第七章案例十六：比丘第21條畜長鉢")
do(u"丁4", 155, u"本書第七章案例十一（比丘第21條·畜長鉢過十日戒）",
   u"本書第七章案例十六（比丘第21條·畜長鉢過十日戒）")
do(u"丁5", 105, u"【第156條著襯體衣戒之前哨】", u"【尼單提第156條著襯體衣戒之前哨，見第十四章案例二】")

print(u"\n―― 戊・迎回舊章之考訂與連誦三則（長句俱自正本 harvest，不假重打）――")
JUE = harvest(u"漢傳律家釋五衣別出", u"漢傳律家釋五衣別出", u"故書中不敢託為律說")
assert JUE.startswith(u"漢傳律家") and JUE.endswith(u"律說"), u"厥修羅考訂之形異：%r" % JUE[:20]
do(u"戊1", 85, u"與原本的三衣合為『五衣』。", u"與原本的三衣合為『五衣』；%s。" % JUE)
print(u"  戊1 迎回『厥修羅』之失考（此名本律無文，故書中不敢託為律說）")

print(u"\n―― 己・圍欄之重鑄（舊稿三欄溢框 94 格）――")
FENCE = [
    u"【比丘尼三十捨墮法（30條）之三重閘門】",
    u"├─ 第一重：五衣與服裝防線（管穿著與身體防暴）",
    u"│    第1～8條（五衣、長衣、乞衣）、第13～15條（織衣、贈與奪衣）",
    u"│    第26條（生理期病衣）、第28條（貿易奪衣）",
    u"│    第29～30條（重衣、輕衣價格上限）",
    u"├─ 第二重：生活器物與金融絕緣（管器具玩好與資產管理）",
    u"│    第9～12條（金銀、寶物買賣、販賣、減五綴鉢）",
    u"│    第24條（畜長鉢）、第25條（多畜好色器皿）",
    u"└─ 第三重：信施公義與專款信託（管索求倫理與組織權術）",
    u"     第16條（七日藥）、第17條（急施衣）、第18條（自求入己）",
    u"     第19條（欲索是更索彼）、第20～23條（四條迴物戒）",
    u"     第27條（非時衣）",
    u"（三重同歸）拔除「生活品味、特權私蓄與利益輸送」——守護第二根本盜戒",
]
marks = [i for i, l in enumerate(D) if l.startswith(u"```")]
assert len(marks) == 2, u"圍欄標記 %d 枚（欲 2）" % len(marks)
a, b = marks[0], marks[1]
old_w = max(cw(x) for x in D[a + 1:b])
w = max(cw(x) for x in FENCE)
assert w <= 72, u"新圍欄仍寬 %d 格" % w
D[a + 1:b] = FENCE
print(u"  圍欄重鑄：%d 行・%d 格 → %d 行・%d 格" % (b - a - 1, old_w, len(FENCE), w))

print(u"\n―― 庚・刪補（以內容錨定位，免行號漂移）――")
k = [i for i, l in enumerate(D) if l.startswith(u"   這十二條法規")]
assert len(k) == 1, u"（三）款插入點見 %d 處" % len(k)
OLD_H = harvest(u"#### 1. 十八條只在戒本裡連誦一遍")
OLD_A = harvest(u"第十三章前面七案所解剖的")
OLD_B = harvest(u"十一條如次，各附其與甲部同制之條與本書位置")
OLD_C = harvest(u"**讀法有三。**")
assert OLD_H.startswith(u"#### 1. "), u"舊款題之形異：%r" % OLD_H[:14]
assert OLD_A.startswith(u"第十三章前面七案"), u"連誦首行之形異：%r" % OLD_A[:16]
HEAD3 = OLD_H.replace(u"#### 1. ", u"#### （三） ", 1)
BLK = [u"", HEAD3, u"", OLD_A.replace(u"第十三章前面七案", u"第十三章前面六案", 1),
       u"", OLD_B, u"", OLD_C]
D[k[0] + 1:k[0] + 1] = BLK
print(u"  庚1 迎回舊章『十八條連誦』一款（款題＋三則＋甲部同制之號與第七章指針）共 %d 行，"
      u"改列為（三）款・『七案』已改『六案』（附錄乙部十八行之『書中』指針自此有錨）" % len(BLK))
D += [u"", u"---"]
print(u"  庚2 章末補『空行＋---』（草稿原以過渡句作結，無章界）")

print(u"\n―― 辛・自證四閘（寫檔前必過）――")
txt = u"\r\n".join(D)
bad, tiao, nclaim = [], {}, 0
for i, l in enumerate(D):
    cands = [m.group(1) or m.group(2) for m in PAT1.finditer(l)]
    if l.startswith(u">") and (u"律制" in l[:16] or u"律文" in l[:16]):
        cands += [m.group(1) for m in re.finditer(u"「([^「」]+?)」", l)]
    m = LABR.match(l)
    if m:
        cands.append(m.group(2))
        tiao[i] = (m.start(2), m.end(2), m.group(1))
    nclaim += len(cands)
    for s in cands:
        for frag in re.split(u"……|…", s.strip()):
            nb = nm(frag)
            if len(nb) >= 4 and nb not in _tk.VINAYA:
                bad.append((i + 1, frag[:44]))
print(u"  逐字閘：管轄 %d 枚（條文欄 %d 行）・無據 %d 枚" % (nclaim, len(tiao), len(bad)))
for i, f in bad:
    print(u"    × 稿L%-4d %s" % (i, f))
assert not bad, u"逐字閘未過"
assert len(tiao) == 12, u"條文欄 %d 行（稿實 12 行，尺少覆便是空尺）" % len(tiao)
mis = []
for i, (a_, b_, lab) in tiao.items():
    mm = re.search(u"(\\d+)", lab)
    if not mm:
        mis.append((i + 1, lab, u"無號"))
        continue
    n = int(mm.group(1))
    body = nm(D[i][a_:b_])
    ref = nm(APXN.get(n, u""))
    if not ref or body != ref:
        mis.append((i + 1, u"標籤『%s』" % lab[:16], APXN.get(n, u"未取此號")[:26]))
print(u"  條文欄序號對勘（欄文须與附錄該號之律文全等）：管 %d 行・不合 %d 行" % (len(tiao), len(mis)))
for i, lab, ref in mis:
    print(u"    × 稿L%-4d %s｜附錄作：%s" % (i, lab, ref))
assert not mis, u"條文欄序號對勘未過"
CORPF = set(_tk.VINAYA)
simp = []
for i, l in enumerate(D):
    ex = [(m.start(), m.end()) for m in re.finditer(u"「[^」]*」", l)]
    if i in tiao:
        ex.append(tiao[i][:2])
    for ch in SIMP:
        for m in re.finditer(re.escape(ch), l):
            if ch in CORPF and any(a_ <= m.start() < b_ for a_, b_ in ex):
                continue
            simp.append((ch, i + 1, l[max(0, m.start() - 10):m.start() + 10]))
print(u"  簡形：%d 枚" % len(simp))
for ch, i, ctx in simp:
    print(u"    × 稿L%-4d 『%s』%s" % (i, ch, ctx))
assert not simp, u"簡形殘留"
assert u"・" not in txt, u"稿內有 U+30FB『・』"
NEG = sum(1 for i, (a_, b_, _l) in tiao.items()
          if nm(D[i][:a_] + u"假" + D[i][a_ + 1:]) not in _tk.VINAYA)
print(u"  負測（條文欄亂改一字須全逮）：%d／%d" % (NEG, len(tiao)))
assert NEG == len(tiao), u"對勘之尺為空尺"
NCASE = sum(1 for l in D if l.startswith(u"#### 案例"))
NH1 = sum(1 for l in D if l.startswith(u"# 第"))
assert NCASE == 6 and NH1 == 1, u"案例 %d・H1 %d" % (NCASE, NH1)
print(u"  形制：案例 %d 則・H1 %d・圍欄 1 段・行數 %d→%d" % (NCASE, NH1, N0, len(D)))

if not GO:
    print(u"\n（乾跑：加 --go 始入冊）")
    sys.exit(0)

print(u"\n―― 壬・入冊（取代舊第十三章）――")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"正本入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
i13 = next(i for i, l in enumerate(L) if l == u"# 第十三章 比丘尼三十捨墮")
i14 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十四章"))
assert L[i13 - 1] == u"" and L[i13 - 2] == u"---", u"上章界非『---＋空行』"
assert L[i14 - 1] == u"" and L[i14 - 2] == u"---", u"下章界非『---＋空行』"
NEWL = L[:i13] + D[2:] + L[i14 - 1:]
print(u"  舊章 %d 行 → 新章 %d 行｜全書 %d → %d 行" % (i14 - 1 - i13, len(D) - 2, len(L), len(NEWL)))
out = u"\r\n".join(NEWL)
assert out.count(u"\r") == out.count(u"\n") == len(NEWL) - 1, u"CRLF 變形"
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(out.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == out, u"回讀不符"
back = chk.split(u"\r\n")
j = next(i for i, l in enumerate(back) if l == u"# 第十三章 比丘尼三十捨墮")
assert back[j:j + len(D) - 2] == D[2:], u"回讀块體不等"
print(u"  已寫檔｜sha %s→%s｜備份 %s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                                        os.path.basename(BAK)))
print(u"  全書 %d 行｜案例 %d 則｜H1 %d 個｜圍欄 %d 段" % (
    len(back), sum(1 for l in back if re.match(u"^#### (?:★ )?案例", l)),
    sum(1 for l in back if re.match(u"^# 第[一二三四五六七八九十]+章", l)),
    sum(1 for l in back if l == u"```") // 2))
