# -*- coding: utf-8 -*-
"""第八十八輪之字頻軸：印面「詞 N 見」式宣稱逐筆復算（口徑＝_tk.VINAYA 六檔本律）。

只掃印面篇（編纂底冊 C／K／L／M 不入軸，其日誌敘事多引舊稱）。所報不中者須人工
斷其為捕詞假象（如「各 1 見」「皆 0 見」「尼戒卷段佔 166 見」）或真虛頻。
罕字一律從書中取字，不手打 escape。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
BOTTOM = _tk.bottom_lines()   # 第 143 輪：舊以篇名关键字劃區，附錄M 改名後即靜默失效
PAT = re.compile(u"[、，；：（(｜|*\\s]*([\\u4e00-\\u9fff]{1,8})"
                 u"(?:[」』])?\\s*(?:凡|共|僅|計)?\\s*(\\d{1,4})\\s*見")

rows = []
for i, l in enumerate(LINES):
    if i in BOTTOM or u"見" not in l:
        continue
    for m in PAT.finditer(l):
        rows.append((i + 1, m.group(1), int(m.group(2)), l))

out = [u"##### 緊排式字頻宣稱 %d 筆（口徑 _tk.VINAYA）#####" % len(rows)]
bad = 0
for ln, term, num, src in rows:
    act = _tk.term_count(term)
    if act != num:
        bad += 1
        out.append(u"  ≠ L%-6d %-10s 載 %4d 實 %4d | %s" % (ln, term, num, act, src[:78]))
out.insert(1, u"  —— 不中 %d 筆（須逐筆人工斷其假象與真誤）——" % bad)
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "freq88.txt"),
        "w", encoding="utf-8").write(u"\n".join(out) + u"\n")
sys.stdout.write(u"rows %d mismatch %d\n" % (len(rows), bad))
