# -*- coding: utf-8 -*-
"""279・外路第七報告（論第一〜三章）十五案之逐條量今檔（量而不刀）。

口徑：每案印【鍵・命中數・首見行之行號與節題】；命中 0 者須以異鍵覆核（防傳遞層歸簡致偽幽靈）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r279probe.py [-v]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
verbose = u'-v' in sys.argv

H1 = [(k, l.strip()[:20]) for k, l in enumerate(LINES) if l.startswith(u'# ')]
H3 = [(k, l.strip()[:34]) for k, l in enumerate(LINES) if l.startswith(u'### ')]


def region(idx):
    cur = u'卷首'
    for k, h in H1:
        if k <= idx:
            cur = h
    return cur


def node(idx):
    cur = region(idx)
    for k, h in H3:
        if k <= idx:
            cur = cur[:8] + u'｜' + h
        else:
            break
    return cur


KEYS = [
    (u'A1 暫取想', u'暫取想'), (u'A1 借用想', u'借用想'), (u'A1 親厚', u'親厚'),
    (u'A2 止犯不坐別住', u'止犯不坐別住'), (u'A2 不作為', u'不作為'),
    (u'A2 惡意不給', u'不與飲食'), (u'A2 保證人', u'保證人'),
    (u'B 五遍行', u'五遍行'), (u'B 俱時', u'俱時'), (u'B 剎那', u'剎那'),
    (u'C1 年少受具', u'年未滿二十'), (u'C1 重新受戒', u'重新如法'),
    (u'C1 信賴保護', u'信賴保護'), (u'C1 既判力', u'既判力'),
    (u'D 正理一定文', u'心淨則開'), (u'D 除不可逆', u'除不可逆'),
    (u'E 出時樂', u'出時'), (u'E 他心智', u'他心智'), (u'E 不可反駁', u'不可反駁'),
    (u'F 臨濟四奪', u'臨濟四奪'), (u'F 判準層級', u'判準層級'), (u'F 除偏鏡', u'除偏鏡'),
    (u'G1 罪疑唯輕', u'罪疑唯輕'), (u'G1 疑罪唯輕', u'疑罪唯輕'), (u'G1 勝解', u'勝解'),
    (u'G2 越濟人', u'越濟人'), (u'G2 破內外道', u'破內外道'),
    (u'G3 波逸提第六十九', u'第六十九'), (u'G3 五如法', u'五如法'),
    (u'G3 四瑕疵', u'四瑕疵'), (u'G3 非法羯磨', u'非法羯磨'),
    (u'G4 阿難自誓', u'大悲自誓'), (u'G4 違心自誣', u'違心自誣'),
    (u'G5 破法輪僧', u'破法輪僧'), (u'G5 破羯磨僧', u'破羯磨僧'), (u'G5 賊住', u'賊住'),
    (u'H1 不害特權', u'不害'), (u'H1 法理特權', u'法理特權'), (u'H1 行捨', u'行捨'),
    (u'H2 惡作', u'惡作'), (u'H2 染污惡作', u'染污惡作'),
    (u'I 言聲離處', u'言聲'), (u'I 斷彼心', u'斷彼心'), (u'I 寄託', u'寄託'),
    (u'J 正理八三禁', u'三禁'), (u'J 斷漏為的', u'斷漏為的'),
    (u'K 數位管轄', u'管轄'), (u'K 遙舉', u'遙舉'), (u'K 跨界聯合', u'跨界聯合'),
]

for tag, key in KEYS:
    hits = [i for i, l in enumerate(LINES) if key in l]
    mark = u'0 見' if not hits else u'%3d 見' % len(hits)
    print(u'%-16s %-8s｜%s%s' % (tag, key.encode('unicode_escape')[:0] or key, mark,
                                 u'' if not hits else u'｜首 L%d %s' % (hits[0] + 1, node(hits[0]))))
    if verbose:
        for i in hits[:6]:
            j = LINES[i].find(key)
            print(u'      L%-5d …%s…' % (i + 1, LINES[i][max(0, j - 26):j + 44].replace(u'\n', u'')))
