# -*- coding: utf-8 -*-
"""第五十七輪・⑤：六欄卡熔為四步散文（241 案）。

指南之請：『這不是搬移或刪削，是把 241 案逐案重寫：事相、心相、法相、處斷、人間、律文六節，
熔成臨場還原→心智透視→金剛護欄→人間迴響四段，出處縮為末尾一行。』

今依呈裁已准之起承轉合四名落刀，一字不刪、只熔其欄：
  起·案發現場  ＝ 戒文（戒本次第）＋事相經過        （臨場還原）
  承·照妖鏡下  ＝ 心相照鏡＋法相剖析                （心智透視）
  轉·金剛斷腕  ＝ 佛陀處斷＋此戒所護                （金剛護欄）
  合·清涼轉身  ＝ 人間智慧與行持＋現代對讀          （人間迴響）
  末行：出處：《四分律》…（律文出處之引文折為一行，自掛欄名之式樣裏解出）
欄名既廢，鏡位清冊與『六段齊』之尺隨之入帳（歸⑥改口徑）。
用法：python -X utf8 _work/r57four.py [--go]
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
BAK = os.path.join(ROOT, u"_work", u"r57_六欄前.md")
GO = u"--go" in sys.argv
CASE = re.compile(u"^### 案例([一二三四五六七八九十百]+)：(.*)$")
MAP = {u"事相經過": u"起", u"戒文（戒本次第）": u"起", u"戒文": u"起",
       u"心相照鏡": u"承", u"法相剖析": u"承",
       u"佛陀處斷": u"轉", u"此戒所護": u"轉",
       u"人間智慧與行持": u"合", u"現代對讀": u"合", u"人間與行持": u"合"}
HEAD = {u"起": u"#### 起·案發現場", u"承": u"#### 承·照妖鏡下",
        u"轉": u"#### 轉·金剛斷腕", u"合": u"#### 合·清涼轉身"}
ORD = [u"起", u"承", u"轉", u"合"]

L = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
io.open(BAK, "w", encoding="utf-8", newline="\n").write(u"\n".join(L))
out = []
i = 0
n_case = 0
odd = Counter()
lost = []
while i < len(L):
    l = L[i]
    m = CASE.match(l)
    if not m:
        out.append(l)
        i += 1
        continue
    # ── 收本案區塊（至下一個 H1/H2/H3）
    j = i + 1
    while j < len(L) and not re.match(u"^#{1,3} ", L[j]):
        j += 1
    block = L[i + 1:j]
    # 依 #### 欄名切段
    segs, cur, buf = [], None, []
    for x in block:
        h = re.match(u"^#### (.+?)\s*$", x)
        if h:
            if cur is not None or buf:
                segs.append((cur, buf))
            cur, buf = h.group(1).strip(), []
        else:
            buf.append(x)
    if cur is not None or buf:
        segs.append((cur, buf))
    fields = {}
    extras = []
    prelude = []
    for name, body in segs:
        if name is None:
            if [x for x in body if x.strip()]:
                prelude += [x for x in body if x.strip() != u"---"]
            continue
        elif name in MAP:
            fields.setdefault(MAP[name], []).append((name, body))
        elif name == u"律文出處":
            fields[u"_cite"] = body
        else:
            odd[name] += 1
            extras.append((name, body))
    n_case += 1
    if prelude:
        fields.setdefault(u"起", []).insert(0, (u"__pre__", prelude))
    out.append(l)
    for k in ORD:
        chunks = fields.get(k, [])
        if not chunks:
            if k != u"起":
                continue
        out.append(u"")
        out.append(HEAD[k])
        for name, body in chunks:                        # 依原序接排，欄名不落紙面
            for x in body:
                if x.strip() == u"---":
                    continue
                out.append(x)
        while out and out[-1].strip() in (u"", u"---"):
            out.pop()
        out.append(u"")
    if extras:
        for name, body in extras:
            odd[u"隨案附出：" + name] += 1
            out.append(u"")
            out.append(u"#### %s" % name)
            out.extend(body)
    cite = [x.strip() for x in fields.get(u"_cite", []) if x.strip()]
    if cite:
        one = u"；".join(x.lstrip(u">").strip() for x in cite)
        one = re.sub(u"^出處[：:]", u"", one)
        out.append(u"")
        out.append(u"出處：%s" % one)
    while out and out[-1].strip() in (u"", u"---"):
        out.pop()
    out.append(u"")
    out.append(u"---")
    i = j

txt = u"\n".join(out)
txt = txt.replace(u"判見下面『佛陀處斷』欄", u"判見下文『轉·金剛斷腕』")
print(u"案 %d｜陌生欄名 %s" % (n_case, dict(odd)))
A = [x for x in L if x.startswith(u"#### ")]
B = [x for x in txt.split(u"\n") if x.startswith(u"#### ")]
print(u"H4 前 %d｜後 %d（四步 %d）" % (len(A), len(B),
      sum(1 for x in B if x.startswith((u"#### 起·", u"#### 承·", u"#### 轉·", u"#### 合·")))))
for k in [u"#### 事相經過", u"#### 心相照鏡", u"#### 法相剖析", u"#### 佛陀處斷",
          u"#### 人間智慧與行持", u"#### 律文出處", u"#### 此戒所護", u"#### 戒文（戒本次第）",
          u"#### 現代對讀"]:
    if txt.count(k):
        print(u"  未熔：%s 餘 %d" % (k, txt.count(k)))
print(u"行 %d（前 %d）｜字 %d（前 %d）" % (txt.count(u"\n") + 1, len(L), len(txt),
                                          sum(len(x) + 1 for x in L)))
if GO:
    io.open(SRC, "w", encoding="utf-8", newline="\n").write(txt)
    print(u"已落盤")
else:
    print(u"試跑")
