# -*- coding: utf-8 -*-
"""第 89 輪探針：套語之出處分布（按章／節列出），與印面冗語之候削清單。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split(u"\n")
MOTIFS = [u"洗缽", u"獵巫", u"法架自捨", u"卡尺", u"良知過載", u"天下太平",
          u"重甲", u"經架", u"熔封", u"消磁", u"高舉", u"向內一問"]

# 章／節定位
heads = []
for i, l in enumerate(LINES):
    m = re.match(r"^(#|##|###) (.+)", l)
    if m:
        heads.append((i + 1, m.group(2).strip()))


def where(ln):
    ch = sec = sub = u"-"
    for h, t in heads:
        if h > ln:
            break
        # 章以「# 第X章」或「# 附錄X」為層
        pass
    return ch, sec


BOTTOM = _tk.bottom_lines()
out = []
for w in MOTIFS:
    hits = [i + 1 for i, l in enumerate(LINES) if w in l]
    # 排除編纂底冊
    drop = [i + 1 for i, l in enumerate(LINES) if i in BOTTOM and w in l]
    keep = [h for h in hits if h not in drop]
    out.append(u"### %-6s 全書 %2d 行｜印面 %2d 行（底冊 %d）" %
               (w, len(hits), len(keep), len(drop)))
    # 依章分計
    cur = u"？"
    dist = {}
    for i, l in enumerate(LINES):
        m = re.match(r"^# (第[一二三四五六七八九]章|附錄[A-M]|卷首|結語|終卷)", l)
        if m:
            cur = m.group(1)
        if i + 1 in keep:
            dist[cur] = dist.get(cur, 0) + 1
    out.append(u"   按章：%s" % (dist,))
    out.append(u"   行：%s" % keep[:40])

io.open(u"_work/motif89.txt", "w", encoding="utf-8").write(u"\n".join(out) + u"\n")
sys.stdout.write(u"ok\n")
