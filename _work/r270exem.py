# -*- coding: utf-8 -*-
"""270 輪・量三：『例示之詞須見於冊』——凡以『如…之屬／之類／（如：A、B、C）』舉例者，
   其所舉之每一項應在冊內別有出處；若舉一例而全書唯此一句，即屬**空头例示**。
口徑：① 鑰句式而非欄目名（宣稱之範圍按句式劃，267 輪之誡）；
      ② 項以『、・，』切，去動語（之屬／等／之類），norm ≥3；
      ③ 他处須見（排除本行）；專名性不足者（含『之』『與』『或』者）擲之不判，免以散文為病。
用法：python -X utf8 _work/r270exem.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
PU = re.compile(u'[\\s\\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·／/]')


def norm(s):
    return PU.sub(u'', s)


B = norm(u'\n'.join(L))
PAT = re.compile(u'(?:如|例如|譬如|如：)[『「【（]?([^』」】）；。\\n]{3,80}?)(?:之屬|之類|等[？。、）】』」]?|：)')
hit = 0
missing = 0
for i, l in enumerate(L):
    for m in PAT.finditer(l):
        for item in re.split(u'[、・，]', m.group(1)):
            it = re.sub(u'^(?:此等|諸|如|即)', u'', item.strip())
            n = norm(it)
            if len(n) < 3 or re.search(u'[之與或而於其]', n):        # 散文語擲之
                continue
            hit += 1
            if B.count(n) <= 1:                                       # 唯見於本處
                missing += 1
                print(u'  空頭例示 L%-5d ｜例：『%s』｜原句：%s'
                      % (i + 1, it[:22], l.strip()[:78]))
print(u'——— 可判之例示項 %d・其中全書唯此一見者 %d' % (hit, missing))
