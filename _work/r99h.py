# -*- coding: utf-8 -*-
"""第 98 輪收尾：底冊（附錄C／M）不預本輪之改，逐行還原；兩處「對」字_CHAIN 修整。"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
PRE = os.path.join(ROOT, "_work", "round96_pre.md")
cur = io.open(MD, encoding="utf-8").read().split("\n")
pre = io.open(PRE, encoding="utf-8").read().split("\n")
assert len(cur) == len(pre), (len(cur), len(pre))

def rng(start):
    i = next(k for k, l in enumerate(cur) if l.startswith(start))
    j = i + 1
    while j < len(cur) and not cur[j].startswith("# "):
        j += 1
    return i, j

log = []
for tag in ("# 附錄C", "# 附錄K", "# 附錄L", "# 附錄M", "# 終卷"):
    a, b = rng(tag)
    for i in range(a, b):
        if cur[i] != pre[i]:
            log.append("還原 %s L%d：%s" % (tag[2:5], i + 1, cur[i].strip()[:40]))
            cur[i] = pre[i]
s = "\n".join(cur)

def rep(old, new, t):
    global s
    k = s.count(old)
    log.append("%s %s（命中 %d）" % ("OK  " if k == 1 else ("MULT" if k > 1 else "MISS"), t, k))
    if k == 1:
        s = s.replace(old, new, 1)

rep("##### 3. 自然犯 對 法定犯 對 聲聞性戒不開之出世絕對要求",
    "##### 3. 自然犯、法定犯與聲聞性戒不開之出世絕對要求", "1 三項比較之語式")
rep("> **〔案例數 對 落點次數對齊公約〕**", "> **〔案例數與落點次數對齊公約〕**", "2 對齊公約標題")

io.open(MD, "w", encoding="utf-8").write(s)
sys.stdout.write("\n".join(log) + "\n")
