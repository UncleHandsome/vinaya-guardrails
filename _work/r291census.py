# -*- coding: utf-8 -*-
r"""291・外路『七大刀口』之今冊實量（唯讀）。

只數事實：各工具之見數與落點、次碼之數與載體、附錄六與第六章之關係句、J 案載體、
出堂洗心三事之重複度、臨濟四奪在判準表內之現制。
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
L = TXT.replace('\r\n', '\n').split('\n')

# 章／節索引
CH = [(i, l) for i, l in enumerate(L) if re.match(u'^# 第[一二三四五六七八九十]+章|^# 附錄|^# 結語|^# 終卷', l)]


def zone(i):
    cur = u'卷首'
    for j, h in CH:
        if j <= i:
            cur = h.replace(u'# ', u'')[:12]
        else:
            break
    return cur


print(u'【一・觀心工具之密度與落點】')
for p in [u'三環', u'隨身三鏡', u'三鏡', u'夜半四照', u'四照', u'六重閘門', u'六重心智閘門', u'閘門', u'隨身三印', u'三印卡']:
    hits = [i + 1 for i, l in enumerate(L) if p in l]
    zs = {}
    for i in hits:
        z = zone(i - 1)
        zs[z] = zs.get(z, 0) + 1
    print(u'  %-12s %3d 見｜%s' % (p, len(hits), u'、'.join(u'%s:%d' % kv for kv in sorted(zs.items()))))

print(u'\n【二・斜線次碼】')
sub = re.findall(u'〔案例 ?\d{1,3} ?/ ?[遮僧開]\d{1,3}(?:[、／/][遮僧開]\d{1,3})*〕', TXT)
print(u'  次碼形：%d 枚' % len(sub))
cnt = {}
for i, l in enumerate(L):
    n = len(re.findall(u'[遮僧開]\d{1,3}〕', l))
    if n:
        cnt[zone(i)] = cnt.get(zone(i), 0) + n
print(u'  落點：%s' % u'、'.join(u'%s:%d' % kv for kv in sorted(cnt.items())))

print(u'\n【三・附錄六與第六章之關係句】')
for i, l in enumerate(L):
    if u'不計入' in l or (u'地標' in l and u'重疊' in l) or u'既證' in l and u'推演' in l:
        print(u'  L%-5d［%s］%s' % (i + 1, zone(i), l.strip()[:170]))

print(u'\n【四・J 案之載體】')
js = [(i + 1, zone(i)) for i, l in enumerate(L) if re.search(u'J-\d', l)]
print(u'  J-# 見數：%d｜落點：%s' % (len(js), u'、'.join(sorted({z for _i, z in js}))))

print(u'\n【五・出堂洗心三事之重复度】')
occ = [(i + 1, zone(i), len(l)) for i, l in enumerate(L) if u'出堂洗心' in l or u'洗心三事' in l]
for a, b, c in occ:
    print(u'  L%-5d［%s］長 %d' % (a, b, c))

print(u'\n【六・臨濟四奪現制（判準表內之自標）】')
for i, l in enumerate(L):
    if u'臨濟四奪' in l:
        print(u'  L%-5d［%s］%s' % (i + 1, zone(i), l.strip()[:150]))
