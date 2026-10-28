# -*- coding: utf-8 -*-
"""標點之制尺（punctchk・第 50 輪立）：全書標點形制之一致性。

書中之制（歷輪所定）：
  ・（U+30FB 日式中黑）── 一律不用，並列歸全形頓號「、」（印面「應無」清單亦查此形）。
  ／（U+FF0F 全形斜線）── 散文之並列用全形。
  /（U+002F 半形斜線）── **只准出現在圍欄圖內**（框線以 1 格計，半形是排版所需），散文須為 0。
  ·（U+00B7）── 案例標題之分隔（「第一波羅夷·婬戒」）與人名・經名（「喬治·凱林」「《中阿含經·七法經》」）用之，屬自制。
  組字碼（如『[真/心]』）內之斜線是構形之一部，動之即毀可回溯性，故一律豁免。
  「「／」」── 重引號必誤（此書以「」為外層， nesting 用『』）；第 74 輪立此目，
        因降式樣之刀在內層已含「」而外層又包一次，遂成「「…」」——尺當場接住。
        『『／』』不判：律文引中之引之雙收（『…『…。』』）乃合法。
  疊標點（。。・，，・：：・？？・！！・、。・；；）── 須為 0；第 77 輪立此目，
        因第十四章案例五之條文欄末作「波逸提。。」（录入時連引號內之句號一并抄入）。
        「）。」「）」之連用乃括號收束，合法，不在此列。
用法：python -X utf8 _work/punctchk.py
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = os.environ.get("HULAN_SRC") or (
    HP.SRC)
L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
APX = next((n for n, t in enumerate(L) if t.startswith(u"# 附錄")), len(L))
MID, SL, FS, DOT = chr(0x30FB), chr(0x2F), chr(0xFF0F), chr(0xB7)

inf = False
bad = []
dbl = []                       # 重引號之目（第 74 輪立：74a 降式樣時外層多包一次「」即此病）
dup = []                       # 疊標點之目（第 77 輪立：第十四章案例五之條文欄末作「波逸提。。」）
DUPS = [u"。。", u"，，", u"：：", u"？？", u"！！", u"、。", u"；；"]
Q1, Q2 = chr(0x300C) * 2, chr(0x300D) * 2     # 「「 ／ 」」（『』之雙收乃引中之引，合法，不判）
cnt = {MID: 0, SL: 0, FS: 0, DOT: 0}
inb = {SL: 0}
for n, t in enumerate(L):
    if t.strip() == u"```":
        inf = not inf
        continue
    for c in cnt:
        cnt[c] += t.count(c)
    if inf:
        inb[SL] += t.count(SL)
        continue
    for q in (Q1, Q2):
        if q in t:
            dbl.append((n + 1, q, t[:60]))
    for dd in DUPS:
        if dd in t:
            dup.append((n + 1, dd, t[:60]))
    if n >= APX:                                   # 附錄唯產生器是法源，此尺不判
        continue
    if MID in t:
        bad.append((n + 1, u"日式中黑", t[:60]))
    if SL in t and chr(0x5B) not in t:             # 組字碼行豁免
        bad.append((n + 1, u"散文半形斜線", t[:60]))

print(u"標點之制（punctchk）｜全書計：・%d ／%d ·%d｜斜線 半%d（其中圍欄內 %d）・全%d"
      % (cnt[MID], cnt[FS], cnt[DOT], cnt[SL], inb[SL], cnt[FS]))
print(u"判：圍欄外之『・』與半形『/』須為 0（附錄與組字碼豁免）｜今 %d 處" % len(bad))
for n, k, t in bad[:20]:
    print(u"  L%-5d %s ｜ %s" % (n, k, t))
print(u"判：重引號『「「』『」』』須為 0（附錄亦判；『』之雙收屬引中之引，不在此列）｜今 %d 處" % len(dbl))
for n, q, t in dbl[:12]:
    print(u"  L%-5d %s ｜ %s" % (n, q, t))
print(u"判：疊標點%s須為 0（圍欄內豁免，附錄亦判）｜今 %d 處" % (u"".join(DUPS), len(dup)))
for n, dd, t in dup[:12]:
    print(u"  L%-5d %s ｜ %s" % (n, dd, t))
sys.exit(1 if (bad or dbl or dup) else 0)
