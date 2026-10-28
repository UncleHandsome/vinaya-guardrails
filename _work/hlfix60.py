# -*- coding: utf-8 -*-
"""第 60 輪・刀：外路第二十三報之真病五事（P0 二・P1 二・P2 一）。
逐條先向本地語料（_tk.VINAYA・漢譯《四分律》六十卷）求證，凡新掛「**…**」之句必證連寫，無據即不刀。
  一.1 第十六章 L6206『此句漢譯《四分律》無文』——**失考為真**：卷五十四·五百集法毘尼白紙黑字記阿難自陳
      「我親從佛聞，憶持佛語，自今已去，為諸比丘捨雜碎戒」，迦葉問「何者是雜碎戒」遂成諍，乃立「隨佛所制而學」之限。
      （外路所引「小隨小戒」乃南傳之譯名，此律作「雜碎戒」，不從其文。）
  一.2 第十章案例四 L4031 把如草覆地之適用**說反**：律作「犯諍以三滅滅：現前毘尼、自言治、草覆地」，
      別有一類「犯諍以二滅滅…不用如草覆地」，而「言諍以二滅滅：以現前毘尼、用多人語」本不用草覆地——
      書中恰倒為『只用於言諍、犯諍不用』，且與本章第三節『言諍以二滅滅…用多人語』自相踢。今依律文兩層重寫。
  一.4 『大師母』→『大愛道』（2 處：目錄 L171・標題 L2109；主角即摩訶波闍波提，L2114 律文自稱瞿曇彌）。
  二.1 第十一章第二節『（上篇）』之闌尾（全書『下篇』0 見）→ 改『二、 深度案例解碼：四大樞紐與二十七場制度現場』
      （樞紐 H3 實數 4・案例實數 27，先數後改）。
  三   十線地圖三行短報：案例十八補 90、91、116（「共臥」之題眼恰在漏中）・案例六補 94・案例八補 129～131、168。
擯回（偽病灶）：一.3 如來衣量——本地《四分律》卷二十作「**長佛十搩手、廣六搩手**」（三見俱同），
      九搩手乃南傳巴利之數，本書法源既為漢譯，『十搩手』不誤；四.1 案例二十一之【條文】欄本已並制五條；
      四.2 案例十一之 136／137 本已分置兩行（L6046・L6047）。
"""
import hashlib
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "_work"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk                                            # noqa: E402

BOOK = os.path.join(HERE, [f for f in os.listdir(HERE)
                           if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0])
BAK = BOOK + u".bak60a"
NV = re.sub(u"[^一-鿿]", u"", _tk.norm(_tk.VINAYA))


def claimed(s):
    """新文內凡『「**…**」』者皆逐字之宣稱，須於語料連寫（去標點比對）。"""
    bad = []
    for q in re.findall(u"「\\*\\*(.+?)\\*\\*」", s):
        t = re.sub(u"[^一-鿿]", u"", _tk.norm(q))
        if len(t) >= 6 and t not in NV:
            bad.append(q[:30])
    return bad


raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n")
L = raw.split(u"\r\n")
log = []


def rowof(sub, frm=0, to=None, want=1):
    to = to or len(L)
    ns = [i for i in range(frm, min(to, len(L))) if sub in L[i]]
    assert len(ns) == want, u"靶『%s』命中 %d 處（須 %d）：%s" % (sub, len(ns), want, [n + 1 for n in ns][:6])
    return ns


def rep(tag, sub, old, new, frm=0, to=None, want=1):
    ns = rowof(sub, frm, to, want)
    for n in ns:
        assert L[n].count(old) == 1, u"%s L%d：old 命中 %d（須 1）" % (tag, n + 1, L[n].count(old))
        bad = claimed(new)
        assert not bad, u"%s：新掛宣稱而語料無據 %s" % (tag, bad)
        L[n] = L[n].replace(old, new)
        log.append(u"%-14s L%-5d｜%s" % (tag, n + 1, L[n][:60]))


# ── 一.1 第十六章・『漢譯無文』之失考 ────────────────────────────────────
F1_OLD = (u"——南傳《長部·大般涅槃經》。此句漢譯《四分律》無文；本律唯於卷第五十四·五百集法毘尼，"
          u"記大迦葉之嘆：「**今者眾人言各不定，不知何者是雜碎戒。**」")
F1_NEW = (u"——南傳《長部·大般涅槃經》。漢譯《四分律》無此臨終之敘，而同樣之開許存於卷第五十四·五百集法毘尼："
          u"阿難自陳「**我親從佛聞，憶持佛語，自今已去，為諸比丘捨雜碎戒**」——所許捨者，此律作『雜碎戒』。"
          u"迦葉隨問他何不問世尊何者是雜碎戒，大眾遂各說不一（有言除四波羅夷，有言除四波羅夷十三事，乃至除九十事），"
          u"大迦葉乃嘆「**今者眾人言各不定，不知何者是雜碎戒**」，共立制限「**若佛先所不制，今不應制；"
          u"佛先所制，今不應却，應隨佛所制而學**」。阿難亦以此未問一事，於結集中被判突吉羅。")
rep(u"捨戒之文", u"此句漢譯《四分律》無文", F1_OLD, F1_NEW)

# ── 一.2 第十章案例四・如草覆地之兩層 ───────────────────────────────────
F2_OLD = (u"律文明白規定：**「犯諍以二滅滅，現前毘尼、自言治，不用如草覆地。」** 如草覆地只適用於「言諍」"
          u"過程中相互犯下的微細口過；真正的犯戒（重罪）絕不能藉大和解一筆抹除。")
F2_NEW = (u"律文分兩層說。犯諍本以三滅滅：**「犯諍以三滅滅，現前毘尼、自言治、草覆地。」**"
          u"——如草覆地正是為犯諍而設，覆的是大諍之中彼此攪出的無邊輕垢。另有一種犯諍不許用它："
          u"**「犯諍以二滅滅，現前毘尼、自言治，不用如草覆地。」**（罪相分明、一人前即可懺盡者，不借大和解抹去）。"
          u"至於言諍，律但說**「言諍以二滅滅，以現前毘尼、用多人語」**，本來就不在草覆地之內。")
rep(u"草覆地兩層", u"如草覆地只適用於「言諍」", F2_OLD, F2_NEW)

# ── 一.4 大師母 → 大愛道（目錄＋標題）───────────────────────────────────
rep(u"名形·大愛道", u"大師母手上的顏色", u"大師母手上的顏色", u"大愛道手上的顏色", want=2)

# ── 二.1 『（上篇）』之闌尾（先數後改）──────────────────────────────────
nk = len([x for x in L if x.startswith(u"### 【第") and u"樞紐" in x])
nc = len([x for i, x in enumerate(L) if x.startswith(u"#### 案例") and 4165 < i < 4712])
assert (nk, nc) == (4, 27), u"新題之數不可自證：%d 樞紐・%d 案例" % (nk, nc)
rep(u"標題·去上篇", u"深度案例解碼（上篇）", u"深度案例解碼（上篇）",
    u"深度案例解碼：四大樞紐與二十七場制度現場", want=2)
assert not [x for x in L if u"上篇" in x], u"『上篇』仍有殘留"

# ── 三・十線地圖三行補條號 ──────────────────────────────────────────────
for tag, old, new in [(u"地圖·共臥", u"| 第十四章案例十八 | 尼單提第84、115條 |",
                       u"| 第十四章案例十八 | 尼單提第84、90、91、115、116條 |"),
                      (u"地圖·瞻病", u"| 第十四章案例六 | 尼單提第93條 |",
                       u"| 第十四章案例六 | 尼單提第93、94條 |"),
                      (u"地圖·考核", u"| 第十五章案例八 | 尼單提第121～127條 |",
                       u"| 第十五章案例八 | 尼單提第121～127、129～131、168條 |")]:
    rep(tag, old.split(u"|")[2].strip(), old, new)

# ── 寫檔與自證 ──────────────────────────────────────────────────────────
new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔）"
assert chk.count(u"\r") == chk.count(u"\n") == len(L) - 1, u"CRLF 之計異"
print(u"行數：%d（不變）・字數：%d → %d（%+d）" % (len(L), len(raw), len(new_raw), len(new_raw) - len(raw)))
for z in log:
    print(u"  " + z)
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
print(u"新掛宣稱俱已向語料證連寫 ✓（每刀皆先證後改）")
