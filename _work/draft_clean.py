# -*- coding: utf-8 -*-
"""草稿清理：以 `_simpdict.MAP`（與全書尺 simp_sweep 同一法源）歸形，並保護逐字引文區
   （`**「…」**`、`「**…**」`、以及 `> **【…】：` 整行之戒文行）與語料自有之舊形。
   保護區必先去重疊：一行戒文常同時被「整行式」與「粗體引號式」兩樣命中，
   兩段若相交，掩蓋時前段之内又插入後段之佔位符，還原便把該段寫兩次（舊版之病，已以最小病例復現）。
用法：python -X utf8 _work/draft_clean.py <草稿檔> [--go]
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _simpdict import MAP  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = sys.argv[1]
GO = "--go" in sys.argv
t = io.open(D, encoding="utf-8", newline="").read()

PATS = [u"\\*\\*「[^」\n]*」\\*\\*", u"「\\*\\*[^」\n]*\\*\\*」", u"(?m)^> \\*\\*【[^】\n]*】：[^\\n]*"]
raw = [m.span() for p in PATS for m in re.finditer(p, t)]
spans, drops = [], 0
for a, b in sorted(raw, key=lambda x: (x[0], -(x[1] - x[0]))):
    if spans and a < spans[-1][1]:          # 與已取者重疊（含同段之較小命中）→ 棄
        drops += 1
        continue
    spans.append((a, b))
print(u"保護區 %d 段（去其重疊 %d 段）" % (len(spans), drops))

slots, out, pos = {}, [], 0
for i, (a, b) in enumerate(spans):
    slots[u"\x02%d\x02" % i] = t[a:b]
    out.append(t[pos:a])
    out.append(u"\x02%d\x02" % i)
    pos = b
out.append(t[pos:])
body = u"".join(out)

rep = []
for a in sorted(MAP):
    n = body.count(a)
    if n:
        body = body.replace(a, MAP[a])
        rep.append(u"%s→%s×%d" % (a, MAP[a], n))
left = [c for c in MAP if c in body]      # 先於掩蓋態覆核：此時佔位符尚在，受保護區不算殘留
for k, v in slots.items():
    body = body.replace(k, v)
print(u"歸形 %d 種：%s" % (len(rep), u"、".join(rep) or u"無"))
kept = u"".join(slots.values())
surv = u"".join(c for c in sorted(set(kept)) if c in MAP)
print(u"引號區保留之舊形（語料自有或逐字須原樣）：%s" % (u"、".join(
    u"%s×%d" % (c, kept.count(c)) for c in surv) or u"無"))
assert not left, u"覆核仍有簡形殘留（引號外）：%s" % left
print(u"覆核殘留：0 枚｜行數 %d→%d" % (len(t.split(u"\r\n")), len(body.split(u"\r\n"))))
if GO:
    io.open(D, "w", encoding="utf-8", newline="").write(body)
    back = io.open(D, encoding="utf-8", newline="").read()
    assert back == body, u"寫後覆核不符"
    print(u"已寫草稿")
else:
    print(u"（覆核模式，未寫檔）")
