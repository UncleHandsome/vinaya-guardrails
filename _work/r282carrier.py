# -*- coding: utf-8 -*-
"""282・量：套語行處斷欄所貼之經文，其『逐字串』在全書是否有其他載體？
   口徑：取該欄『<br>』之後之文字，先剝去粗體與括注，切成 14 字之切片，
        統計每片在全書其他行之出現；印出『唯一／有他體』與他體所在之章。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')
TPL = u'犯緣與開緣之界如何判？'
CASE = re.compile(u'〔案例 ?0*(\\d+)([^〕]*)〕')
HEAD = re.compile(u'^(#{1,3}) *(第[一二三四五六七八九十]+章|附錄[一二三四五六七八九十]|【?全書|上篇|下篇|結語|導讀|自序)')

# 章名索引
ch = {}
cur = u'卷首'
for i, l in enumerate(LINES):
    m = HEAD.match(l)
    if m:
        cur = m.group(2).strip()
    ch[i + 1] = cur

def frags(s):
    s = re.sub(u'\\*\\*', u'', s)
    s = re.sub(u'（[^）]{0,24}）', u'', s)
    s = re.sub(u'[^\\u4e00-\\u9fff]', u'', s)
    return [s[i:i + 14] for i in range(0, max(0, len(s) - 13), 14)]

for i, l in enumerate(LINES):
    if TPL not in l:
        continue
    m = CASE.search(l)
    cells = [c.strip() for c in l.split(u'|')]
    body = cells[4].split(u'<br>')[-1]
    fs = [f for f in frags(body) if len(f) >= 14]
    others = set()
    for f in fs:
        for j, o in enumerate(LINES):
            if j == i or f not in o:
                continue
            others.add((j + 1, ch[j + 1]))
    print(u'L%d 案%-3s 切片 %d ・他體 %d 處 %s' % (
        i + 1, m.group(1), len(fs), len(others),
        u'' if not others else sorted(others)[:4]))
