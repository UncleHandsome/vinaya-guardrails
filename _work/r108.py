# -*- coding: utf-8 -*-
"""第 108 輪探針：括弧嵌套、標點相重、標點前後之空白。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
drop, cur = set(), None
for i, l in enumerate(L):
    if l.startswith("# "):
        cur = None
        for t in (u"修訂誌", u"跨章款級", u"十維驗收", u"全書校勘記"):
            if t in l:
                cur = 1
    if cur:
        drop.add(i)
pats = [(u"嵌套圓括", r"（（|））"), (u"括弧相貼", r"）（"), (u"逗號相重", r"，，|、、"),
        (u"句點相重", r"。。"), (u"驚問混排", r"？！|！？"), (u"標點前有空白", r" [，。；：]"),
        (u"標點後空白", r"[，。；：] (?=[一-鿿])"), (u"引號內句末點", r"。[」』]"),
        (u"半形括弧包漢字", r"\([^)]{1,30}[一-鿿]")]
for name, p in pats:
    out = []
    for i, l in enumerate(L):
        if i in drop:
            continue
        for m in re.finditer(p, l):
            out.append((i + 1, l[max(0, m.start() - 16):m.end() + 14]))
    print("%-14s %3d 見" % (name, len(out)))
    for n, seg in out[:5]:
        print("      L%-6d …%s…" % (n, seg))
