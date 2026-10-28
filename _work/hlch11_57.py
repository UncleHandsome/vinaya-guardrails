# -*- coding: utf-8 -*-
"""第 57 輪・甲：以作者新稿換入第十一章，並先將稿中『掛了逐字式樣而語料無據』之引文歸真。
法據：卷首【凡例】款①（引號與粗體相合之文必是漢譯《四分律》原句）＋款②（案例【律制】欄同此）。
口徑：①案例卡【律制】欄（形制即宣稱）②粗體與引號相合者；未掛式樣之敘事引語屬『本書今語』，不在此刀。
工序：讀稿→逐條歸真（行號＋子串雙錨，命中數須為 1）→語料閘複核（須 0）→查簡形→插入正本→量行量尾。
用法：python -X utf8 _work/hlch11_57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = HP.SRC
_c = glob.glob(os.path.join(os.path.expanduser(u"~"), u".qoder", u"tmp", u"*",
                            u"attachments", u"bfc14756-*", u"8e641a59-*.txt"))
assert len(_c) == 1, u"新稿附件定位失敗：%s" % _c
DRAFT = _c[0]

# ── 歸真名單（稿內行號 1 起；子串须於該行唯一）────────────────────────
FIX = [
    (26, u"**「法定人數差序體系」**", u"**法定人數差序體系**"),
    (118, u"說戒。此如來最後說戒", u"說戒。……此如來最後說戒"),
    (170, u"**「行舍羅（籌籤表決）」**", u"**行舍羅（籌籤表決）**"),
    (187, u"不應作非法別眾、非法和合、法別眾、法相似別眾、法相似和合、作呵不止羯磨。",
          u"不應作非法別眾羯磨、不應作非法和合羯磨、不應作法別眾羯磨、"
          u"不應作法相似別眾羯磨、不應作法相似和合羯磨、不應作呵不止羯磨。"),
    (212, u"**制定了一整套精密無比的「緊急狀態逐級降級應變預案」**",
          u"**制定了一整套精密無比的緊急狀態逐級降級應變預案**"),
    (330, u"隨所取令彼歡喜。如此親友應取。", u"隨所取令彼歡喜。……如此親友應取。"),
    (345, u"有如是因緣聽受。凡我所遮", u"有如是因緣聽受。……是我所遮"),
    (360, u"世尊未聽我曹受黑石蜜。聽受黑石蜜，隨所餘處分。",
           u"如來未聽比丘受黑石蜜。……自今已去，聽諸比丘受黑石蜜。……汝今持此殘石蜜，著淨地無虫水中。"),
    (364, u"「以殘石蜜著淨地、若無蟲水中。」", u"「汝今持此殘石蜜，著淨地無虫水中。」"),
    (378, u"**為期數月的「集體法規豁免總包」**", u"**為期數月的集體法規豁免總包**"),
    (380, u"過去已滅、未來未至，唯以當下現在三句正式生效！",
           u"過去已滅、未來未至，是故以現在三句受功德衣。"),
    (397, u"令斷命。佛問：『汝以何心？』答：『殺心。』",
           u"令斷命。疑，佛問言：『汝以何心？』答言：『殺心。』"),
    (412, u"周竟不得非是藥者，知所用處無非藥者。醫道以成。",
           u"周竟不得非是藥者，……知所用處無非藥者。……醫道以成。"),
    (427, u"終不傷肉。借衣，勿令露形來見我。", u"終不傷肉。……借衣，勿令露形來見我。"),
    (443, u"不應取病人衣物。若能極上瞻病", u"不應取病人衣物。……若能極上瞻病"),
    (447, u"**「照護行為五法鑑定標準」**", u"**照護行為五法鑑定標準**"),
    (461, u"不應作是！不應作是！當作如是施", u"不應作是！不應作是！蘇卑優婆私！當作如是施"),
    (465, u"不應作是！不應作是！當作如是施", u"不應作是！不應作是！蘇卑優婆私！當作如是施"),
    (476, u"今何得便斷？布施應與一切。", u"今何得便斷？"),
    (480, u"開示：**「彼尼揵外道", u"開示：「彼尼揵外道"),
    (480, u"皆有福德，何況於人！」**", u"皆有福德，何況於人！」"),
    (491, u"王瓶沙聞已慚愧。汝不得治餘人病", u"王瓶沙聞已慚愧。……汝不得治餘人病"),
    (491, u"唯治我病……耆婆白王：是故不能", u"唯治我病。……是故不能"),
]

d = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert d.count(u"\r\n") == d.count(u"\n") and d.count(u"\r") == d.count(u"\n"), u"新稿行尾混雜"
DL = d.replace(u"\r\n", u"\n").rstrip(u"\n").split(u"\n")
assert DL[0] == u"---" and DL[2].startswith(u"# 第十一章"), u"新稿首三行形制不如期：%r" % DL[:3]
assert DL[-1].strip(), u"新稿末行須為內容行"

for n, old, new in FIX:
    l = DL[n - 1]
    c = l.count(old)
    assert c == 1, u"歸真錨非唯一（稿 L%d，命中 %d）：%s" % (n, c, old[:24])
    DL[n - 1] = l.replace(old, new)
    print(u"  歸真 稿L%-4d %s → %s" % (n, old[:34], new[:34]))
print(u"歸真 %d 條已施" % len(FIX))

CN = u"零一二三四五六七八九十"


def cn2int(s):
    if s == u"十":
        return 10
    if len(s) == 1:
        return CN.index(s)
    if s.startswith(u"十"):
        return 10 + CN.index(s[1])
    if len(s) == 3 and s[1] == u"十":
        return CN.index(s[0]) * 10 + CN.index(s[2])
    return CN.index(s[0]) * 10


cs = [cn2int(m.group(1)) for m in
      (re.match(u"^#### 案例([一二三四五六七八九十]+)：", l) for l in DL) if m]
assert cs == list(range(1, 28)), u"新稿案例非一至二十七之連號：%s" % cs
assert len([l for l in DL if re.match(u"^### [一二三四]、", l)]) == 4, u"新稿節題數 ≠ 4"
assert len([l for l in DL if re.match(u"^### 【第[一二三四]樞紐", l)]) == 4, u"新稿樞紐題數 ≠ 4"
assert sum(1 for l in DL if l.startswith(u"# ")) == 1, u"新稿 H1 數 ≠ 1"

# ── 語料閘（歸真後須全綠）：①【律制】欄 ②粗體＋引號相合者───────────
sys.path.insert(0, ROOT)
import _tk  # noqa: E402
from _work._simpdict import MAP as SIMP  # noqa: E402
V = _tk.VINAYA
PUN = re.compile(u"[「『」。；、：？！，\\s]")


def segs(txt):
    out = []
    for g in re.split(u"…+", PUN.sub(u"", txt)):
        for h in re.split(u"』|『", g):
            if len(h) >= 6:
                out.append(h)
    return out


bad = []
for k, l in enumerate(DL):
    claims = []
    if l.startswith(u"> **【律制】：**"):
        claims += re.findall(u"『?「([^」]+)」", l) or [l.split(u"：", 1)[1]]
    claims += [m.group(1) for m in re.finditer(u"\\*\\*「([^」]+)」\\*\\*", l)]
    claims += [m.group(1) for m in re.finditer(u"「([^」]+)」\\*\\*", l)]
    for c in claims:
        bad += [(k + 1, c[:30], x) for x in segs(c) if V.find(_tk.norm(x)) < 0]
print(u"語料閘：逐字宣稱之無據片段 **%d**" % len(bad))
for n, c, x in bad:
    print(u"  稿L%-4d %s｜無據：%s" % (n, c, x[:44]))
assert not bad, u"歸真未盡，不敢入冊"

# 簡形之口徑須與 _work/simp_sweep.py 全等：語料自有此形者（如『虫』），只在引號外追查。
spans = [(m.start(), m.end()) for m in re.finditer(u"「[^」\n]*」", u"\n".join(DL))]
inq = lambda i: any(a <= i < b for a, b in spans)
flat = u"\n".join(DL)
flag = [c for i, c in enumerate(flat)
        if c in SIMP and not (V.find(_tk.norm(c)) >= 0 and inq(i))]
print(u"簡形掃描（引號內之語料舊形豁免）：%s" % (u"無" if not flag else u"有 → %s" % u"".join(sorted(set(flag)))))
assert not flag, u"新稿帶簡形入冊"

# ── 入冊──────────────────────────────────────────────────────────────
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, B0 = len(L), len(raw.encode(u"utf-8"))
A_OLD = u"# 第十一章 二十犍度"
A_END = u"# 【第三部：比丘尼戒的精密護網】"
assert L.count(A_OLD) == 1 and L.count(A_END) == 1, u"錨不唯一"
i0, i1 = L.index(A_OLD), L.index(A_END)
j0 = i0 - 1
while j0 > 0 and not L[j0].strip():
    j0 -= 1
assert L[j0] == u"---", u"章前分隔線定位失敗：%r" % L[j0]
OLD = L[j0:i1]
print(u"舊區 %d 行（正本 L%d–L%d，連章前分隔線）｜新區 %d 行＋1 空行" % (len(OLD), j0 + 1, i1, len(DL)))
print(u"舊區字數 %d｜新區字數 %d｜差 %+d" % (sum(map(len, OLD)), sum(map(len, DL)),
                                            sum(map(len, DL)) - sum(map(len, OLD))))
if u"--go" in sys.argv:
    txt = u"\r\n".join(L[:j0] + DL + [u""] + L[i1:])
    assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔｜行數 %d→%d｜位元組 %d→%d" % (N0, len(L[:j0] + DL + [u""] + L[i1:]),
                                                B0, len(txt.encode("utf-8"))))
else:
    print(u"（乾跑：加 --go 始寫）")
