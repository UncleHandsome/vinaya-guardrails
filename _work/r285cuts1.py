# -*- coding: utf-8 -*-
"""285・批一之刀（形制）：#1 一章一 H1（七・八章合併上下）＋#10 除『；不隨冊』。
用法：python -X utf8 _work/r285cuts1.py         ＝試跑（印命中數，不寫檔）
     python -X utf8 _work/r285cuts1.py --apply ＝落刀（先備份於 _archive/備份/）"""
import io
import os
import shutil
import sys

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
T = S.replace(u'\r\n', u'\n')

LOG = []


def rep(old, new, label, x=1, y=None):
    if isinstance(x, int):
        lab2, n = (y or label), x
    else:
        lab2, n = x, y or 1
    c = T.count(old)
    assert c == n, u'【%s】命中 %d 見・期 %d 見' % (lab2, c, n)
    LOG.append(u'%-26s 命中 %d' % (lab2, c))
    return T.replace(old, new, n)


# ── #1 第七章：去（上）・併副題・刪（下）之 H1 塊
T = rep(u'# 第七章　總攝指針與隨身行法（上）',
        u'# 第七章　總攝指針與隨身行法', u'第七章 H1 去（上）')
T = rep(u'**——生命之樹生態全景與四維極速檢索矩陣**',
        u'**——生命之樹生態全景與四維極速檢索矩陣・夜半四照與公堂審計手冊**',
        u'第七章副題併吞（下）')
T = rep(u'# 第七章　總攝指針與隨身行法（下）\n\n'
        u'**——夜半四照、公堂審計與法庭消磁操作手冊**\n\n---\n\n',
        u'', u'第七章（下）之 H1 塊除')

# ── #1 第八章：同法
T = rep(u'# 第八章　現代治理會通與法域邊界（上）',
        u'# 第八章　現代治理會通與法域邊界', u'第八章 H1 去（上）')
T = rep(u'**——宏觀三線治理、調查實務與反靈性操縱防護**',
        u'**——宏觀三線治理、調查實務、人事勞動與寺產信託之現代防護**',
        u'第八章副題改鑄')
T = rep(u'# 第八章　現代治理會通與法域邊界（下）\n\n'
        u'**——雙軌人事分立、寺產信託防禦、數位資產與深水案例實戰**\n\n---\n\n',
        u'', u'第八章（下）之 H1 塊除')

# ── #10 目錄之『；不隨冊』除
T = rep(u'終卷　全書竣工呈辭與終局迴向偈（在結語之後、附錄之前；不隨冊）',
        u'終卷　全書竣工呈辭與終局迴向偈（在結語之後、附錄之前）', u'目錄除『；不隨冊』')

print(u'\n'.join(LOG))
print(u'行數 %d ➔ %d（淨 %+d）' % (len(S.split(u'\n')), len(T.split(u'\n')),
                                 len(T.split(u'\n')) - len(S.split(u'\n'))))
print(u'校：（上）餘 %d・（下）餘 %d・不隨冊餘 %d' % (
    T.count(u'（上）'), T.count(u'（下）'), T.count(u'不隨冊')))
assert T.count(u'（上）') == 0 and T.count(u'（下）') == 0 and T.count(u'不隨冊') == 0
assert T.count(u'\n# 第') == 8, u'章級 H1 今應八條，量得 %d' % T.count(u'\n# 第')

if APPLY:
    import hashlib
    BK = u'_archive/備份/ver39.pre285a.md'
    if not os.path.exists(BK):
        shutil.copyfile(P, BK)
    print(u'備份 ➔ %s・起點 sha256 前 12 ＝ %s' % (
        BK, hashlib.sha256(S.encode(u'utf-8')).hexdigest()[:12]))
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
