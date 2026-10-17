# -*- coding: utf-8 -*-
"""第 89 輪乙批：標題與緊接其下之「同文粗體框／引言」回音之探測。

只把 Markdown 記號與括弧「符號」去掉（留其內容），再比兩句之包含關係。
本軸報候刪之單，斷之在人。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
BR = u"（）()「」『』【】〈》《〉“”‘’"
MD = u"#*>-| \t`　"


def core(s):
    s = re.sub(r"(?s)<[^>]+>", "", s)
    return "".join(ch for ch in s if ch not in BR and ch not in MD)


out, n = [], 0
for i, l in enumerate(LINES):
    m = re.match(r"^(#{2,5})\s+(.+)", l)
    if not m:
        continue
    h = core(m.group(2))
    if len(h) < 8:
        continue
    for j in range(i + 1, min(i + 6, len(LINES))):
        nxt = LINES[j]
        if not nxt.strip():
            continue
        c = core(nxt)
        if len(c) >= 8 and (h in c or c in h):
            n += 1
            out.append(u"L%-6d 標｜%s" % (i + 1, m.group(2)[:60]))
            out.append(u"       回｜%s" % nxt.strip()[:60])
        break

io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "echo89.txt"),
        "w", encoding="utf-8").write(
    u"##### 標題下之同文回音 %d 處 #####\n" % n + u"\n".join(out) + u"\n")
sys.stdout.write(u"hits %d\n" % n)
