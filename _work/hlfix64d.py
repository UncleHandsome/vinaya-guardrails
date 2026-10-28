# -*- coding: utf-8 -*-
"""第 64 輪・丁：段一圍欄之防線名畫一（我鑄時為省格把「第四防線」「第五防線」縮成「四」「五」，
   與同段之「第一／第二／第三防線」不一，形制之尺雖不報，目視即見——補齊並復量其格。）"""
import io
import os
import re

BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
raw = io.open(BOOK, "rb").read()
L = raw.decode("utf-8").split(u"\r\n")
MID = chr(0xB7)
PAIR = [(u"├─ 四" + MID + u"組織撕裂與世俗寄生（10～12）",
         u"├─ 第四防線" + MID + u"組織撕裂與世俗寄生（10～12）"),
        (u"└─ 五" + MID + u"系統最後總閘（13）",
         u"└─ 第五防線" + MID + u"系統最後總閘（13）")]
cw = lambda s: sum(2 if ord(c) > 0x2E80 else 1 for c in s)
for old, new in PAIR:
    assert L.count(old) == 1, u"錨命中 %d：%s" % (L.count(old), old[:22])
    L[L.index(old)] = new
    print(u"  改：%s｜%d 格 → %d 格" % (new[:26], cw(old), cw(new)))
seg = L[1496:1516]
assert seg[0].startswith(u"【十三僧殘"), u"段一之界已動"
print(u"  段一最寬 %d 格｜名目：%s" % (
    max(cw(x) for x in seg),
    u"／".join(sorted(set(re.findall(u"第.防線", u"\n".join(seg)))))))
out = u"\r\n".join(L)
assert out.count(u"\r") == out.count(u"\n") == len(L) - 1, u"CRLF 變形"
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(out)
chk = io.open(BOOK, "rb").read().decode("utf-8").split(u"\r\n")
for _o, n in PAIR:
    assert chk.count(n) == 1, u"覆讀不合：%s" % n[:20]
print(u"已寫檔｜%d B｜%d 行" % (len(io.open(BOOK, 'rb').read()), len(chk)))
