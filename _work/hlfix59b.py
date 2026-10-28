# -*- coding: utf-8 -*-
"""第 59 輪・刀二：外路第二十二報之『自裁』諸項（標點・名相・條文欄・編號）。
護三道（老誡『文字換文字之器須護三道』）：① 每靶先試跑、印命中數，非 1（或宣告數）即停；
   ② 名相之換只動引號外（「」『』之內乃律文原字，一仍其舊）；③ 備份＋SHA 一步回退，
   並逐項印出改動行，事後以 hlbattery 全尺覆核。
名相之向（依語料與本書 53 輪『名形歸律文常用形』之成例）：
   偷羅難陀 172 見 ≫ 偷蘭難陀 32 見 ⇒ 自敘歸『偷羅難陀』（與外路所建議者相反）；
   以手搏 7 見・以手摶 0 見 ⇒ 歸『搏』；
   讖摩／差摩 語料各 11 見（差摩乃人名、讖摩另有布名），讖摩為通行之名 ⇒ 自敘歸『讖摩』。
"""
import hashlib
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOOK = os.path.join(HERE, [f for f in os.listdir(HERE)
                           if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0])
BAK = BOOK + u".bak59b"
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n"), u"CR/LF 不等，先清換行"
L = raw.split(u"\r\n")
Q = re.compile(u"[「『][^」』]*[」』]")


def sub_outside(line, old, new):
    """只在引號之外替換（引號內乃律文原字）。回 (新行, 次數)。"""
    spans = [(m.start(), m.end()) for m in Q.finditer(line)]

    def inq(i):
        return any(a <= i < b for a, b in spans)
    n, out, i = 0, [], 0
    while i < len(line):
        if line.startswith(old, i) and not inq(i):
            out.append(new)
            i += len(old)
            n += 1
        else:
            out.append(line[i])
            i += 1
    return u"".join(out), n


log = []


def cut(tag, idx, old, new, want=1, outside_only=False):
    """在指定行 idx（0 起）替換 old→new，命中須＝want；outside_only 則只動引號外。"""
    line = L[idx]
    if outside_only:
        got = [k for k in range(len(L)) if old in L[k]]
        new_line, c = sub_outside(line, old, new)
        assert c == want, u"%s：引號外命中 %d（須 %d）｜L%d" % (tag, c, want, idx + 1)
    else:
        c = line.count(old)
        assert c == want, u"%s：命中 %d（須 %d）｜L%d" % (tag, c, want, idx + 1)
        new_line = line.replace(old, new)
    assert new_line != line
    L[idx] = new_line
    log.append(u"%-22s L%-5d ×%d｜%s" % (tag, idx + 1, c, new_line[:64]))


def rowof(sub, frm=0):
    ns = [n for n in range(frm, len(L)) if sub in L[n]]
    assert len(ns) == 1, u"定位『%s』命中 %d 處（須唯一）" % (sub, len(ns))
    return ns[0]


# ── 1・【條文（第N條）： 缺右括號（三.1，並掃全書同形）────────────────────
pat = re.compile(u"【條文（第(\\d+)條）：")
hits = [(n, m.group(1)) for n, x in enumerate(L) for m in [pat.search(x)] if m]
assert hits, u"未見『【條文（第N條）：』之形，靶失"
for n, num in hits:
    cut(u"標點·括號歸位", n, u"【條文（第%s條）：" % num, u"【第%s條 條文】：" % num)
print(u"掃得『【條文（第N條）：』同形 %d 處，俱歸位" % len(hits))

# ── 2・（，波逸提） 逗號入括（三.2）─────────────────────────────────────
n2 = rowof(u"不語主人捨去者（，波逸提）")
cut(u"標點·逗號出括", n2, u"不語主人捨去者（，波逸提）。", u"不語主人捨去者，波逸提。")
assert not [x for x in L if u"（，" in x], u"仍有『（，』殘留"

# ── 3・須提那子：破折號後之律文補主詞（三.4）────────────────────────────
n3 = rowof(u"此事甚易，我能為之。**」——「便捉婦臂")
cut(u"敘事·律續寫", n3,
    u"此事甚易，我能為之。**」——「便捉婦臂將至園中屏處三行不淨」。",
    u"此事甚易，我能為之。**」律又續寫：「**便捉婦臂將至園中屏處三行不淨**」。")

# ── 4・二不定法：目擊者先點名再引律文（三.5）────────────────────────────
n4 = rowof(u"即就倚壁而聽")
cut(u"敘事·主詞前置", n4,
    u"。**「即就倚壁而聽，但聞說非法語聲。」**",
    u"。目擊者毘舍佉母來這戶人家本有小事，先以為聽見的是說法，**「即就倚壁而聽，但聞說非法語聲。」**", 1)
cut(u"敘事·尾句收攏", n4,
    u"——目擊者是毘舍佉母，她來這戶人家本有小事，先以為聽見的是說法，靠牆聽了一陣才知道不是。",
    u"——她靠牆聽了一陣，才知道說的不是法。", 1)

# ── 5・名相統一（引號外）────────────────────────────────────────────────
c1 = 0
for n in range(len(L)):
    if u"偷蘭難陀" in L[n]:
        new, c = sub_outside(L[n], u"偷蘭難陀", u"偷羅難陀")
        if c:
            L[n] = new
            c1 += c
            log.append(u"%-22s L%-5d ×%d｜%s" % (u"名相·偷羅難陀", n + 1, c, new[:56]))
c2 = 0
for n in range(len(L)):
    if u"差摩" in L[n]:
        new, c = sub_outside(L[n], u"差摩", u"讖摩")
        if c:
            L[n] = new
            c2 += c
            log.append(u"%-22s L%-5d ×%d｜%s" % (u"名相·讖摩", n + 1, c, new[:56]))
B79 = [(u"以手摶比丘戒", u"以手搏比丘戒"), (u"打摶同一族", u"打搏同一族"),
       (u"以手摶、", u"以手搏、"), (u"故以手摶比丘者", u"故以手搏比丘者"),
       (u"撲打（摶）", u"撲打（搏）")]
c3 = 0
for old, new in B79:
    for n in range(len(L)):
        while old in L[n]:
            L[n] = L[n].replace(old, new, 1)
            c3 += 1
            log.append(u"%-22s L%-5d %s→%s" % (u"名相·搏（第79條）", n + 1, old, new))
print(u"名相：偷羅難陀 %d 處・讖摩 %d 處・搏 %d 處" % (c1, c2, c3))
assert not [n for n, x in enumerate(L) if u"以手摶" in x], u"『以手摶』仍有殘留"
assert u"大摶飯食" in u"".join(L), u"誤傷：『大摶飯食』被動"

# ── 6・附錄凡例：初制／重制之約（一.2 之補）─────────────────────────────
n6 = rowof(u"戒文一律取該條")
cut(u"凡例·初制之約", n6,
    u"（無別宣者取其結戒句或犯相句）",
    u"（無別宣者取其結戒句或犯相句）；其後經佛重制者，正文另標【重制戒文】以列定本，本表但錄初制原句，兩不相代")

# ── 7・案例十四補第44條・案例十八補第29條（二.2）─────────────────────────
n7 = rowof(u"【第43條 條文】")
assert L[n7 + 1].strip() == u"", u"第43條行之下非空行，插入點變"
L.insert(n7 + 1, u"> **【第44條 條文】：** 若比丘食家中有寶在屏處坐者，波逸提。")
log.append(u"%-22s L%-5d 補一行" % (u"條文欄·第44條", n7 + 2))
n8 = rowof(u"同篇並制：「**若比丘十日未竟夏三月")
L[n8] = L[n8].rstrip()
assert L[n8].endswith(u"」）"), u"並制行尾形制變：%r" % L[n8][-8:]
L[n8] = (L[n8][:-2] + u"」「**若比丘夏三月竟，後迦提一月滿，在阿蘭若有疑恐懼處住，"
         u"比丘在如是處住，三衣中欲留一一衣置舍內。諸比丘有因緣，離衣宿乃至六夜。若過者，尼薩耆波逸提。**」）")
log.append(u"%-22s L%-5d 補第29條" % (u"條文欄·第29條", n8 + 1))

# ── 8・案例十五：標題條次依引文之序（二.2・正文＋目錄兩處）──────────────
OLD_T = u"（第148、149、165、166、167、169、170條）"
NEW_T = u"（第165、166、167、169、170、148、149條）"
nt = [n for n, x in enumerate(L) if OLD_T in x]
assert len(nt) == 2, u"案例十五標題命中 %d 處（須正文＋目錄＝2）：%s" % (len(nt), [z + 1 for z in nt])
for n in nt:
    cut(u"標題·條次依序", n, OLD_T, NEW_T)

# ── 9・七滅諍 H4：拆 2 為 2・3，後續順延（二.1）──────────────────────────
n9 = rowof(u"#### 2. 憶念毘尼")
assert L[n9 + 1].startswith(u"* **法理：**"), u"其下非『法理』行：%r" % L[n9 + 1][:20]
assert L[n9 + 2].strip().startswith(u"* 當一位已經證得阿羅漢果"), u"第一子項非憶念之例"
assert L[n9 + 3].strip().startswith(u"* 當一個人在精神發狂"), u"第二子項非不癡之例"
b1 = L[n9 + 2].strip()
b2 = L[n9 + 3].strip()
b1 = b1[2:] if b1.startswith(u"* ") else b1
b2 = b2[2:] if b2.startswith(u"* ") else b2
b1 = re.sub(u"；\\s*$", u"。", b1)
head2 = u"#### 2. 憶念毘尼（Sati-vinaya）：聖者清白之永久終審"
head3 = u"#### 3. 不癡毘尼（Amūḷha-vinaya）：精神失常者之免責"
BLOCK = [head2, u"* **法理：** " + b1, u"", head3, u"* **法理：** " + b2]
assert len([z for z in BLOCK if z.strip()]) == 4
L[n9:n9 + 4] = BLOCK
log.append(u"%-22s L%-5d 拆為 2・3 兩節（%d 行→%d 行）" % (u"編號·七滅諍", n9 + 1, 4, len(BLOCK)))
for old, new in [(u"#### 3. 自言治", u"#### 4. 自言治"),
                 (u"#### 4. 覓罪相", u"#### 5. 覓罪相"),
                 (u"#### 5. 多人覓罪", u"#### 6. 多人覓罪"),
                 (u"#### 6. 如草覆地", u"#### 7. 如草覆地")]:
    ns = [n for n, x in enumerate(L) if x.startswith(old)]
    assert len(ns) == 1, u"『%s』命中 %d（須 1）" % (old, len(ns))
    L[ns[0]] = new + L[ns[0]][len(old):]
    log.append(u"%-22s L%-5d %s" % (u"編號·順延", ns[0] + 1, new))
seq = [x for x in L if re.match(u"^#### \\d+\\. ", x)]
print(u"第十章第三節 H4 序：%s" % [x[:14] for x in seq if 3900 < L.index(x) < 3960])

# ── 寫檔與自證 ──────────────────────────────────────────────────────────
new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔）"
assert chk.count(u"\r") == chk.count(u"\n") == len(L) - 1, u"CRLF 之計異"
cn = re.compile(u"[^一-鿿]")
print(u"行數：%d → %d（%+d）・字數：%d → %d（%+d）" % (
    len(raw.split(u"\r\n")), len(L), len(L) - len(raw.split(u"\r\n")), len(raw), len(new_raw),
    len(new_raw) - len(raw)))
print(u"漢字數：%d → %d" % (len(cn.sub(u"", raw)), len(cn.sub(u"", new_raw))))
for z in log:
    print(u"  " + z)
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
