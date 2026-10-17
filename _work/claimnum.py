# -*- coding: utf-8 -*-
"""claimnum.py —— 宣稱『N＋量詞』是否如其實列之數（第 151 輪立，**待診軸**：恆退 0）。

緣起：書中向有『N大道岔』之特例檢與『篇題之數＝篇內實列』一條，然散文領句之
『恪守三項禁戒：』『七階所存皆實體量刑清冊：』一类自報項數者，歷輪無器一問。
第 151 輪以此徑通掃，得可校 48 筆、數不符 9 筆，**逐筆分診俱屬設計或反證**：
或三禁戒之外別列一中斷令（其數已明宣於領句），或八事以四目分承（目內具註第几事），
或七階之外另附〔案外如實〕一則，或律列兩項而本書益以第三項且自陳其所以然。
是故不升不變量（升之則每有 grouped list 即假陽性，反成死法），只留此軸如實報差，
**新報之差不即改文——先問是數不符，還是列法分組／另有附目。**

窄口徑三則（寬一級即淹於假陽性）：
  ① 序數前不接『第』與他數（免「四十五則」誤讀為「五則」）；
  ② 唯取**行尾以冒號收**之領句；
  ③ 其後第一非空行須即為列舉，全串同式（同 1.／同 *／同 一、），中途換式即擱置不判。
數法以縮排定同組：首項縮排為準，更深者屬其下屬（標『有子層』），更浅者屬另組即止。
退出碼：恆 0（待診）；`argv[1]` 可注副本以供負測。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t
if len(sys.argv) > 1:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    L = io.open(sys.argv[1], encoding='utf-8').read().split('\n')
    # 副本須與正路徑同享底冊豁免（第 150 輪之教）：自掃 H1 篇界，名屬底冊者整段免校。
    BOT, inb = set(), False
    for i, l in enumerate(L):
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7,
      u'八': 8, u'九': 9, u'十': 10, u'兩': 2}
QTY = u'項事條目階層類款端種則'
CLAIM = re.compile(u'(?<![第%s\\d])([一兩二三四五六七八九十]|\\d{1,2})([%s])'
                   % (u''.join(CN.keys()), QTY))
MARK = [re.compile(u'^\\s*\\d+[.)、]\\s'), re.compile(u'^\\s*[-*]\\s'),
        re.compile(u'^\\s*[%s][.)、]' % u''.join(CN.keys())),
        re.compile(u'^\\s*[（(]\\s*[%s\\d]+\\s*[）)]' % u''.join(CN.keys())),
        re.compile(u'^\\s*[①-⑳]')]


def marker(s):
    for k, rx in enumerate(MARK):
        if rx.match(s):
            return k
    return None


def indent(s):
    return len(s) - len(s.lstrip())


def is_bottom(i):
    return i in BOT


rows = []
for i, line in enumerate(L):
    if is_bottom(i) or not line.rstrip().endswith((u'：', u':')):
        continue
    ms = list(CLAIM.finditer(line))
    if not ms:
        continue
    k = i + 1
    while k < len(L) and L[k].strip() == u'' and k - i < 4:
        k += 1
    if k >= len(L) or is_bottom(k):
        continue
    kind = marker(L[k])
    if kind is None:
        continue
    lvl = indent(L[k])
    n, j, sub = 0, k, False
    while j < len(L) and j - i <= 40:
        s = L[j]
        if s.strip() == u'':
            j += 1
            continue
        if indent(s) < lvl:
            break
        if indent(s) > lvl:
            sub = True
            j += 1
            continue
        if marker(s) == kind:
            n += 1
            j += 1
        else:
            break
    if n == 0:
        continue
    for m in ms:
        num = CN.get(m.group(1))
        if num is None:
            try:
                num = int(m.group(1))
            except ValueError:
                continue
        if 1 < num <= 16:
            rows.append((i + 1, m.group(0), num, n, sub, line.rstrip()[-42:]))

diff = [r for r in rows if r[2] != r[3]]
print(u'宣稱數對實列（待診，不為閘）：可校 %d 筆｜數不符 %d 筆' % (len(rows), len(diff)))
for ln, claim, num, n, sub, tail in diff:
    print(u'  L%-6d 宣%2d 實%2d%s 【%s】…%s' % (ln, num, n, u'(有子層)' if sub else u'', claim, tail))
sys.exit(0)
