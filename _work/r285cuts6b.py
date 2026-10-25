# -*- coding: utf-8 -*-
"""285・批六乙：#59 之第五段——第五章「定罪判決生效」之四列大圖（寬 120）重排為兩部直列（≤ 85）。
   保義之法：舊圖每一【】〔〕（）之名相須在新圖中逐字再現，缺一即不寫檔。
   用法：python -X utf8 _work/r285cuts6b.py [--apply]"""
import io
import re
import sys
import unicodedata

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
L = S.replace(u'\r\n', u'\n').split(u'\n')


def w(s):
    return sum(2 if unicodedata.east_asian_width(c) in u'WF' else 1 for c in s)


st = next(i for i, x in enumerate(L) if x.startswith(u'```') and u'【定罪判決生效' in L[i + 1])
en = next(k for k in range(st + 1, len(L)) if L[k].strip() == u'```')
OLD = u'\n'.join(L[st:en + 1])
NEW = u'\n'.join([
    u'```text',
    u'【定罪判決生效（篇聚分流處置）】',
    u'      │',
    u'      ├─► 甲部・重罪二聚',
    u'      │     【四波羅夷（極刑滅擯）】（戒體伏滅，不可復起）',
    u'      │        ├─► 〔性侵殺盜〕【終身永擯】（移送國法）',
    u'      │        │       └─► 終端終止・絕不下接（移送司法）',
    u'      │        └─► 〔合意婬無覆〕【留寺與學】（空間隔離）',
    u'      │                └─► 終端終止・結小界（不入出罪）',
    u'      │     【僧殘（重度可懺）】（殘破戒體，行治修復）',
    u'      │        ├─► 〔當日自首〕【直入六夜】（意喜勞役）',
    u'      │        └─► 〔隔夜覆藏〕【隨日別住】（時間對沖）',
    u'      │',
    u'      └─► 乙部・中輕二聚',
    u'            【中罪偷蘭遮（中度可懺）】（重罪未遂前方便／中罪）',
    u'               ├─► 〔上品偷蘭遮〕【四人眾法發露】（公堂眾法結清）',
    u'               └─► 〔中下品偷蘭遮〕【對首稱名發露】（清淨同修發露）',
    u'            【輕微四聚（輕度可懺）】（波逸提/捨墮/提舍尼/突吉羅）',
    u'               ├─► 〔捨墮先捨後懺〕【當眾沒入公產】（換賜下鉢/棄金銀）',
    u'               └─► 〔對首/責心即淨〕【稱名發露說悔已】（無作戒體復圓滿）',
    u'',
    u'【僧殘行治之階】',
    u'   行治中 ─┬─► 〔再犯新罪〕→【本日治】（計時清零）→（重起別住）',
    u'           └─► 〔清淨服滿〕→【六夜意喜】（去慢勞役）',
    u'                    │',
    u'                    ▼',
    u'           〔六夜摩那埵服滿〕',
    u'              ├─► 〔人數不足二十〕→【滿摩那埵位】',
    u'              │                      · 時效凍結，勞役終止',
    u'              │                      · 小道場持牒赴大叢林出罪',
    u'              └─► 〔滿二十位清淨大僧〕→【阿浮呵那出罪大會】',
    u'                                        （比丘20人／尼二部各20人，',
    u'                                          排除15類非法足數）',
    u'                    │',
    u'                    ▼',
    u'   【出罪還淨四事（復權）】',
    u'      1. 庭宣除罪（法權歸零）    2. 戒臘復舊（年資通算）',
    u'      3. 空間儀禮（執手復座）    4. 檔案熔封（案卷落鎖）',
    u'                    │',
    u'                    ▼',
    u'   【防衛性任職排他原則】',
    u'      （性犯罪禁任教誡尼眾；重大侵吞禁任財務簽核）',
    u'                    │',
    u'                    ▼',
    u'   【解縛還淨·回歸無事】',
    u'   （洗鉢經行，走出急診，天下太平）',
    u'```',
])

toks = set(re.findall(u'[【〔（][^】〕）\n]{2,16}[】〕）]', OLD))
miss = [t for t in sorted(toks) if t not in NEW]
print(u'舊圖名相 %d 種・新圖未見 %d ➔ %s' % (len(toks), len(miss), miss))
print(u'舊寬 %d・新寬 %d・行 %d➔%d' % (max(w(x) for x in OLD.split(u'\n')[1:-1]),
                                      max(w(x) for x in NEW.split(u'\n')[1:-1]),
                                      len(OLD.split(u'\n')), len(NEW.split(u'\n'))))
assert not miss, u'新圖失落名相，不寫檔'
if APPLY:
    L[st:en + 1] = NEW.split(u'\n')
    io.open(u'_archive/備份/ver39.pre285j.md', 'w', encoding=u'utf-8', newline=u'\n').write(S)
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(u'\n'.join(L))
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
