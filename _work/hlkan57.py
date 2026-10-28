# -*- coding: utf-8 -*-
"""第 57 輪・己佐證：第十一章各案例之『案發現場（X犍度）』標籤，逐一向本地語料求其實位。
法：取該案例【律制】欄第一條可定位之律文片段 → 在 `原文/*.txt` 找其行 → 取其上最近之篇題行（本地檔僅存部分篇題）
    → 若檔內無篇題（如 31-37 檔全無），則改以『該片段之上文內所提之犍度名』與『說戒／受戒等語之密度』佐證。
只報不判：報『標籤所云』vs『語料所居』，供人工裁。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = re.compile(u"^[◎\\s]*([一-龥]{1,8}[揵犍]度)(之[一二三四五六七八九十]*)?[◎\\s]*$")
PROSE = re.compile(u"([一-龥]{1,7})[揵犍]度")

FILES = []
for f in sorted(glob.glob(os.path.join(ROOT, u"原文", u"*.txt"))):
    txt = io.open(f, encoding="utf-8", errors="ignore").read().replace(u"\r\n", u"\n")
    lines = txt.split(u"\n")
    acc, pos = [], []
    for n, l in enumerate(lines):
        pos.append((len(acc), n + 1))
        acc.extend(re.sub(u"[^一-龥]", u"", l))
    FILES.append((os.path.basename(f), lines, u"".join(acc), pos))

raw = io.open(HP.SRC, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
i0 = L.index(u"# 第十一章 犍度精要")
i1 = L.index(u"# 【第三部：比丘尼戒的精密護網】")
cur = None
cases = []
for i in range(i0, i1):
    if L[i].startswith(u"#### 案例"):
        cur = [i + 1, L[i][5:33], None, []]
        cases.append(cur)
        continue
    if cur is None:
        continue
    m = re.match(u"^> \\*\\*【律制】：\\*\\* (.*)$", L[i])
    if m:
        cur[3] = [q for q in re.findall(u"『?「([^」]+)」", m.group(1))]
    m = re.match(u"^\\s*\\* \\*\\*【案發現場（(.+?)）】", L[i])
    if m:
        cur[2] = m.group(1)


def locate(frag):
    """片段（只留漢字）於各檔之所在行＋其上最近篇題＋上文所提之犍度名。"""
    key = re.sub(u"[^一-龥]", u"", frag)
    if len(key) < 8:
        return None
    for name, lines, s, pos in FILES:
        p = s.find(key)
        if p < 0:
            continue
        ln = max([q for a, q in pos if a <= p])
        heads = []
        for j in range(ln - 1, -1, -1):
            m = HEAD.match(lines[j].strip())
            if m:
                heads.append(m.group(1) + (m.group(2) or u""))
                break
        prose = [m.group(1) for m in PROSE.finditer(u"\n".join(lines[max(0, ln - 400):ln]))]
        tail = [x for x in prose if x not in u"如上下為第"][-2:]
        return u"%s L%d｜上篇題：%s｜上文所提：%s" % (name, ln, heads[0] if heads else u"（檔內無）",
                                              u"、".join(tail) or u"（無）")
    return u"✗ 全語料無從定位"


for a, t, lab, frs in cases:
    print(u"L%-5d %-30s 標籤【%s】" % (a, t[:28], lab or u"（無）"))
    got = 0
    for q in frs:
        for seg in re.split(u"…+", q):
            if len(re.sub(u"[^一-龥]", u"", seg)) < 8:
                continue
            got += 1
            print(u"        律制片段：%s" % seg[:30])
            print(u"        實位：%s" % (locate(seg) or u"（片段過短）"))
            if got >= 2:
                break
        if got >= 2:
            break
    if not got:
        print(u"        （無 ≥8 字之片段可定位）")
