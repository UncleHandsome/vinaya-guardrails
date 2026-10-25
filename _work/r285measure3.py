# -*- coding: utf-8 -*-
"""285・候裁清冊復量 第三波（定數：次碼・附錄三・第七章・補遺編序・非法足數）"""
import io
import re

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
T = io.open(P, encoding=u'utf-8').read().replace(u'\r\n', u'\n')
L = T.split(u'\n')

# 次碼：嚴格式〔案例 NN / XMM〕
zc = re.findall(u'〔案例\\s*[0-9]{1,3}\\s*/\\s*[^〕]{1,8}〕', T)
print(u'次碼（含號帶斜線者）共 %d 枚；其樣本：%s' % (len(zc), zc[:4]))
kind = {}
for z in zc:
    k = z.split(u'/')[1].strip()[:1]
    kind[k] = kind.get(k, 0) + 1
print(u'次碼大類分布：%s' % kind)
print(u'『原編』殘留 %d・J 錄之形 %d' % (T.count(u'原編'),
      len(re.findall(u'〔案例\\s*J', T))))

# 附錄三兩表分行
j0 = next(i for i, x in enumerate(L) if x.startswith(u'# 附錄三'))
j1 = next((i for i in range(j0 + 1, len(L)) if L[i].startswith(u'# ')), len(L))
sec = L[j0:j1]
cur = None
cnt = {}
for x in sec:
    if x.startswith(u'###'):
        cur = x[4:24]
        cnt[cur] = 0
    elif x.startswith(u'| ') and cur and not re.match(u'^\\|[: \\-|]+$', x):
        cnt[cur] += 1
print(u'附錄三各節表行：%s' % cnt)

# 第七章上下兩 H1 之合計行數與『軸』節
h = [i for i, x in enumerate(L) if x.startswith(u'# 第') or x.startswith(u'# 附錄') or x.startswith(u'# 結語')]
a7 = [i for i in h if L[i].startswith(u'# 第七章')]
nxt = [i for i in h if i > a7[-1]][0]
seg = L[a7[0]:nxt]
print(u'第七章（上＋下）L%d〜L%d 共 %d 行・其中含『軸』之 H3/H4 %d 條' % (
    a7[0] + 1, nxt, len(seg),
    len([x for x in seg if (x.startswith(u'###') or x.startswith(u'####')) and u'軸' in x])))
k = [i for i, x in enumerate(seg) if u'軸' in x and x.startswith(u'#')]
if k:
    print(u'    軸節題：%s' % [seg[i][:40] for i in k])

# 補遺編序今形
nums = sorted(set(int(m.group(1)) for m in re.finditer(u'〔補遺\\s*0?([0-9]{1,2})〕', T)))
print(u'補遺編號實見：%s（缺 %s）' % (nums, [i for i in range(min(nums), max(nums) + 1) if i not in nums]))
print(u'漢字編次（卅〜四十N）見數：%d' % len(re.findall(u'[卅]?[一二三四五六七八九十]五?', T)) and T.count(u'卅'))

# 非法足數・消磁（見／行）
print(u'非法足數：%d 見／%d 行' % (T.count(u'非法足數'), len([x for x in L if u'非法足數' in x])))
print(u'消磁：%d 見／%d 行（其中 H1 章題 %d 條）' % (
    T.count(u'消磁'), len([x for x in L if u'消磁' in x]),
    len([x for x in L if x.startswith(u'#') and u'消磁' in x])))
