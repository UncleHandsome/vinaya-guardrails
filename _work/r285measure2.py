# -*- coding: utf-8 -*-
"""285・候裁清冊復量 第二波（修 v1 之破 regex，並補未量諸目）"""
import io
import os
import re
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, u'_work'))
P = u'ver39四分律_起心動念心智分析框架_修正版.md'
T = io.open(P, encoding=u'utf-8').read().replace(u'\r\n', u'\n')
L = T.split(u'\n')

# #45 次碼
ZC = re.findall(u'〔案例[^〕]{0,10}/\\s*[遮僧開性][0-9]{1,3}〕', T)
print(u'#45 次碼 %d 枚・其大類 %s' % (
    len(ZC), sorted(set(x.split(u'/')[1].strip()[0] for x in ZC))))

# #49 引號與『』
print(u'#49 「 %d・」 %d・『 %d・』 %d' % (
    T.count(u'「'), T.count(u'」'), T.count(u'『'), T.count(u'』')))

# #4 行動卡之形
print(u'#4 ==== 框卡 %d 處・```markdown 圍欄 %d 處・```text %d 處・``` 計 %d 對' % (
    len(re.findall(u'^={4,}', T, re.M)), T.count(u'```markdown'),
    T.count(u'```text'), T.count(u'```') // 2))

# #5 五階心印
for m in re.finditer(u'[^\\n]{0,26}(?:32\\s*字|五階|心印)[^\\n]{0,26}', T):
    print(u'#5 ▸ %s' % m.group(0).replace(u'\n', u''))

# #2 第七章四軸
i0 = next(i for i, x in enumerate(L) if x.startswith(u'# 第七章'))
i1 = next((i for i in range(i0 + 1, len(L)) if L[i].startswith(u'# 第')), len(L))
seg = L[i0:i1]
ax = [(i + i0 + 1, x[:44]) for i, x in enumerate(seg) if x.startswith(u'## ')]
print(u'#2 第七章 L%d〜L%d 共 %d 行・H2 %d 個' % (i0 + 1, i1, i1 - i0, len(ax)))
for a in ax:
    print(u'    %d| %s' % a)

# #8 附錄三・#41 巴利
j0 = next(i for i, x in enumerate(L) if x.startswith(u'# 附錄三'))
j1 = next((i for i in range(j0 + 1, len(L)) if L[i].startswith(u'# ')), len(L))
rows = [x for x in L[j0:j1] if x.startswith(u'| ') and not x.startswith(u'|:')]
print(u'#8 附錄三 L%d〜L%d・表行 %d・H2/H3 小標 %d' % (
    j0 + 1, j1, len(rows),
    len([x for x in L[j0:j1] if x.startswith(u'##')])))
for x in L[j0:j1]:
    if x.startswith(u'##'):
        print(u'#8   %s' % x[:60])

# 25 行 ghost-writing 之今況（276 債③）
print(u'債③ 卷首代筆之自標 %d 見・『本書之解』%d 見・『本書之推』%d 見' % (
    T.count(u'代筆'), T.count(u'本書之解'), T.count(u'本書之推')))

# 未證／卷欠／粒度（#33・#36・債②）
print(u'#33/#36 『卷次未細核』%d・『檔段』%d・『分段檔』%d・『未證』%d' % (
    T.count(u'卷次未細核'), T.count(u'檔段'), T.count(u'分段檔'), T.count(u'未證')))

# 非法足數正用逐行（#43）
print(u'#43 非法足數逐行定位：%s' % [i + 1 for i, x in enumerate(L) if u'非法足數' in x])

# 消磁逐行（#42・帳稱 18 見）
print(u'#42 消磁逐行定位：%s' % [i + 1 for i, x in enumerate(L) if u'消磁' in x])
