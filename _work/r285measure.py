# -*- coding: utf-8 -*-
"""285・候裁清冊之復量：逐項向今檔取證（只量不刀）。"""
import io
import re

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
T = io.open(P, encoding=u'utf-8').read().replace(u'\r\n', u'\n')
L = T.split(u'\n')


def n(s, pat):
    print(u'%s：%s' % (s, pat))


# #1 一章兩 H1
h1 = [x for x in L if re.match(u'^# ', x)]
updown = [x for x in h1 if u'（上）' in x or u'（下）' in x]
n(u'#1 一章兩 H1（上／下）', u'H1 共 %d・其中（上）（下）%d 條 ➔ %s' % (
    len(h1), len(updown), u'／'.join(x[2:22] for x in updown)))

# #3 附錄六編序之形
n(u'#3 附錄六之編號形制', u'『〔補遺 NN〕』%d 見・漢字編次（卅五〜卅七）%d 見・『調部深描』%d 見' % (
    len(re.findall(u'〔補遺', T)), len(re.findall(u'卅[五七]', T)), T.count(u'調部深描')))

# #10 終卷括註
n(u'#10 終卷『不隨冊』', [m.group(0) for m in re.finditer(u'終卷[^\\n]{0,28}', T)][:6])

# #33 卷欠／卷次未細核
n(u'#33 卷次未細核・未證之自標', u'『卷次未細核』%d 見・『未證』%d 見・『本地未收』%d 見' % (
    T.count(u'卷次未細核'), T.count(u'未證'), T.count(u'本地未收')))

# #37 全屬攝述之卡：欄題【律典原典】之數
n(u'#37 欄題之數', u'【律典原典】%d 見・【律典攝要】%d 見・【原典法意】%d 見' % (
    T.count(u'【律典原典】'), T.count(u'【律典攝要】'), T.count(u'【原典法意】')))

# #39 凡例『今十四欄』
n(u'#39 凡例欄數之自稱', [m.group(0) for m in re.finditer(u'[^\\n]{0,18}(十四欄|回查欄)[^\\n]{0,18}', T)])

# #41 附錄三巴利
n(u'#41 附錄三之巴利形', u'Abbhāna %d・Parivāsa %d・Mānatta %d・梵巴分流之凡例條 %d・象力行舍羅自言治 %s' % (
    T.count(u'Abbhāna'), T.count(u'Parivāsa'), T.count(u'Mānatta'),
    T.count(u'外語轉寫體例'), [k for k in (u'象力', u'行舍羅', u'自言治') if k in T]))

# #42 消磁
n(u'#42 『消磁』', u'%d 見（含章題 %d・目錄 %d）' % (
    T.count(u'消磁'), len([x for x in L if x.startswith(u'#') and u'消磁' in x]),
    len([x for x in L if u'消磁' in x and u'|' not in x and x.startswith(u'- ')])))

# #43 非法足數
n(u'#43 『非法足數』', u'%d 見 ➔ %s' % (
    T.count(u'非法足數'), [x.strip()[:60] for x in L if u'非法足數' in x]))

# #44 案名小異（今冊口徑：附錄四與正文長名之異）——量附錄四行數與正文載體數
n(u'#44 案名之兩載體', u'附錄四表列 %d・正文定義載體 %d' % (
    len(re.findall(u'^\\| \\*\\*〔案例', T, re.M)),
    len(re.findall(u'^\\* \\*\\*案號\\*\\*：〔案例', T, re.M))))

# #45 次碼
n(u'#45 次碼〔案例 NN / XMM〕', u'%d 見（遮・僧・開・性之正次碼另由 r285measure3 細分）' % len(
    re.findall(u'〔案例[^〕]{0,10}/[^〕]{1,8}〕', T)))

# #46 阿[少/兔]樓陀
n(u'#46 合字', [m.group(0) for m in re.finditer(u'阿\\[[^\\]]{1,8}\\][^\\n]{0,6}', T)][:4])

# #49 短「」（語料無據者之粗量：全書「」對數）
n(u'#49 引號之量', u'「 共 %d 枚・『 共 %d 枚' % (T.count(u'「'), T.count(u'『')))

# #51 句讀：≥20 字而全無標點之逐字段（第 32 目之口徑外延）
NOPUNCT = re.compile(u'^[^，。；：、！？“”「」『』（）《》>\\-|*# \\t]{20,}$')
cnt = 0
for x in L:
    s = x.strip()
    if s.startswith(u'>'):
        s = s[1:].strip()
    if NOPUNCT.match(s):
        cnt += 1
n(u'#51 ≥20 字無標點之行', u'%d 行（含非引文之表行標題，僅供參考；尺之正式口徑在第 32 目）' % cnt)

# #52 附錄四行數
n(u'#52 附錄四', u'表列 %d 行' % len(re.findall(u'^\\| \\*\\*〔案例', T, re.M)))

# #6/#7/#8 落點存在與否
for k in (u'視訊會議', u'數位資產', u'寺產借名代持', u'醫療', u'第五組', u'四大板塊'):
    n(u'落點『%s』' % k, u'%d 見' % T.count(k))

# #2 第七章四軸之行數
i0 = next(i for i, x in enumerate(L) if x.startswith(u'# 第七章'))
i1 = next((i for i in range(i0 + 1, len(L)) if L[i].startswith(u'# 第')), len(L))
ax = [i for i in range(i0, i1) if L[i].startswith(u'## ') and u'軸' in L[i]]
n(u'#2 第七章', u'章範圍 L%d〜L%d（%d 行）・含『軸』之 H2 %d 個' % (
    i0 + 1, i1, i1 - i0, len(ax)))

# 本冊之外：25 行 ghost-writing 之覆核標記今在否
n(u'276 債③・矩陣代筆之自標', [m.group(0) for m in re.finditer(u'[^\\n]{0,20}(代筆|本書之解)[^\\n]{0,26}', T)][:8])
