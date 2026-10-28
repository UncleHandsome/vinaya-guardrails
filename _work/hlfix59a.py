# -*- coding: utf-8 -*-
"""第 59 輪・刀一：第六章第四節【按：微型道場之困】人數四級之精確化（外路第二十一報第 5 項，判真）。
病：原括號「（四人、五人、十人、二十人，邊地別開減省）」未分所減者為何——律文實唯『受大戒』於邊地得開五人，
    『出罪』則四人／五人／十人僧俱除之，唯二十人僧得作（無邊地之減）。含混則成律學硬傷。
據（本地語料・四分律，皆連寫可檢）：
    是中四人僧者除自恣受大戒出罪餘一切如法羯磨應作
    是中五人僧者在中國除受大戒出罪餘一切如法羯磨應作
    是中十人僧者除出罪餘一切如法羯磨應作
    是中二十人僧者一切羯磨應作況復過二十
自證：① 四條律據先向語料求連寫（無據即不刀）；② 點唯一；③ 新句內不掛「」（免生逐字之宣稱）；
      ④ 除本行外全檔一字不動；⑤ CRLF 等式・回讀合・備份 .bak59a＋SHA 可回退。
"""
import hashlib
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "_work"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk                                            # noqa: E402

BOOK = [f for f in os.listdir(HERE) if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0]
BOOK = os.path.join(HERE, BOOK)
BAK = BOOK + u".bak59a"
V = _tk.norm(_tk.VINAYA)
EVID = [u"是中四人僧者除自恣受大戒出罪餘一切如法羯磨應作",
        u"是中五人僧者在中國除受大戒出罪餘一切如法羯磨應作",
        u"是中十人僧者除出罪餘一切如法羯磨應作",
        u"是中二十人僧者一切羯磨應作況復過二十"]
OLD = (u"律於人數本有四級之判（四人、五人、十人、二十人，邊地別開減省），其意一貫：法權隨人而存，"
       u"不隨地理而絕。")
NEW = (u"律於人數本有四級之判（四人、五人、十人、二十人），四級各有開除：四人僧除自恣、受大戒、出罪；"
       u"五人僧於中國亦除受大戒與出罪（邊地於受戒得開）；十人僧除出罪；二十人僧則一切羯磨應作。"
       u"其意一貫：法權隨人而存，不隨地理而絕——然所開者唯受戒之緣，出罪一法必滿二十，無得而減。")

for z in EVID:
    assert _tk.norm(z) in V, u"律據無據（不刀）：%s" % z[:24]
print(u"律據四條俱連寫於本地語料 ✓")
assert u"「" not in NEW and u"”" not in NEW, u"新句掛引號即成逐字之宣稱"

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n")
L = raw.split(u"\r\n")
hit = [n for n, x in enumerate(L) if OLD in x]
assert len(hit) == 1, u"錨命中 %d 處（須唯一）：%s" % (len(hit), [n + 1 for n in hit])
n = hit[0]
assert L[n].startswith(u"**按：微型道場之困"), u"錨所落非按語之行：%s" % L[n][:24]
line = L[n].replace(OLD, NEW)
assert L[n].count(OLD) == 1 and line != L[n]
for frag in [u"故僧數不具之處", u"此係本書據律意之推衍，非律之明文"]:
    assert frag in line and frag in L[n], u"按語之下半被牽動：%s" % frag
out = list(L)
out[n] = line
assert sum(1 for a, b in zip(out, L) if a != b) == 1, u"改動非僅一行"
new_raw = u"\r\n".join(out)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔）"
assert chk.count(u"\r") == chk.count(u"\n") == len(out) - 1
print(u"L%d｜字數 %d → %d（%+d）・全檔 %d → %d（%+d）" % (
    n + 1, len(L[n]), len(line), len(line) - len(L[n]), len(raw), len(new_raw), len(new_raw) - len(raw)))
print(u"行數：%d（不變）・CRLF：%d/%d" % (len(out), chk.count(u"\r"), chk.count(u"\n")))
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
print(u"新句：%s" % line[:150])
