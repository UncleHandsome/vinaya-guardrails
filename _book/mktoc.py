# -*- coding: utf-8 -*-
"""卷首【本書總目錄】重生器——目錄唯據冊身實題自算，不手打、不殘留舊稱。
   用法：python -X utf8 _book/mktoc.py"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
txt = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n")
toc = [u"## 【本書總目錄】", u""]
for line in txt.split(u"\n"):
    if line.startswith(u"# 【卷末"):
        toc += [u"**卷末・工具與附錄**", u""]
        continue
    m = re.match(u"^# 【(.+?)】.*$", line)
    if m:
        toc += [u"**%s**" % m.group(1), u""]
        continue
    m = re.match(u"^# (第[一二三四五六七八九十]+章　.+)$", line)
    if m:
        toc.append(u"- %s" % m.group(1))
        continue
    m = re.match(u"^## (第[一二三四五六七八九十]+節　.+)$", line)
    if m:
        toc.append(u"    - %s" % m.group(1))
        continue
    m = re.match(u"^## (附錄[一二三四五]　.+)$", line)
    if m:
        toc.append(u"- %s" % m.group(1))
i0 = txt.index(u"## 【本書總目錄】")
i1 = txt.index(u"\n# ", i0)
out = txt[:i0] + u"\n".join(toc) + txt[i1:]
io.open(SRC, "w", encoding="utf-8", newline="\n").write(out)
print(u"目錄重生：%d 條" % (len(toc) - 2))
