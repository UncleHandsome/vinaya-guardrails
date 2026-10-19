# -*- coding: utf-8 -*-
import io, os, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
inc=False
for i,l in enumerate(L,1):
    if l.startswith(u"### 案例"): inc=True
    if re.match(u"^#{1,2} ",l): inc=False
    for k in [u"心相照鏡",u"事相經過",u"法相剖析",u"佛陀處斷",u"人間智慧與行持",u"律文出處",u"此戒所護",u"現代對讀",u"六欄",u"六段",u"戒本次第"]:
        if k in l and not l.startswith(u"#### ") and not l.startswith(u"> 《"):
            print(u"L%-6d｜%s" % (i, l.strip()[:130])); break
