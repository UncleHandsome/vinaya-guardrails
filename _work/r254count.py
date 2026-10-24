# -*- coding: utf-8 -*-
"""第 254 輪・刀十四：全書『99』之計數宣稱隨動為 102（含圍欄圖之等寬護持）。

围欄內之圖以半形格計寬（與 build39._cw 同口徑）：『99』→『102』多佔一格，
故同格內須削一空格以護框線對齊——改畢斷言該行半形寬不變、且框線『│』之列位不變。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')


def cw(s):                                    # 半形格數（全形與 CJK 佔二）
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


SITES = [
    (u'99 個判例單元於此全數圓滿', u'102 個判例單元於此全數圓滿'),
    (u'翻過這 99 個跌倒又爬起', u'翻過這 102 個跌倒又爬起'),
    (u'六十卷律典、99 則判例', u'六十卷律典、102 則判例'),
    (u'第六章 99 則活生生的判例法典', u'第六章 102 則活生生的判例法典'),
    (u'本表今全章 99 案', u'本表今全章 102 案'),
    (u'第六章 99 則判例依', u'第六章 102 則判例依'),
]
FENCE = u'99 片法相之葉（古典判例法典）'


def main():
    apply = u'apply' in sys.argv[1:]
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
    text = u'\n'.join(lines)
    for old, new in SITES:
        c = text.count(old)
        print(u'%s %d 處｜%s' % (u'中' if c else u'✗未中', c, old[:26]))
        text = text.replace(old, new)
    # 圍欄圖之等寬改寫
    n_f = 0
    out = []
    for l in text.split(u'\n'):
        if FENCE in l:
            w0 = cw(l)
            k = l.index(FENCE) + len(FENCE)
            tail = l[k:]
            if tail.startswith(u' │'):
                cand = l[:k + len(u' ')] + tail[1:]      # 補一格即削一格
            else:
                cand = re.sub(u'\\s+│', u'│', l, count=1)
            l2 = re.sub(u'99 片', u'102 片', cand)
            w1 = cw(l2)
            if w1 != w0:
                raise SystemExit(u'圍欄寬變：%d→%d，須人工重排' % (w0, w1))
            pos0 = [i for i, c in enumerate(l) if c == u'│']
            pos1 = [i for i, c in enumerate(l2) if c == u'│']
            if pos0 != pos1:
                raise SystemExit(u'框線列位移動：%s vs %s' % (pos0, pos1))
            out.append(l2)
            n_f += 1
            print(u'圍欄等寬護持：寬 %d 不变、框位 %s' % (w1, pos1))
            continue
        out.append(l)
    text = u'\n'.join(out)
    print(u'圍欄圖隨動 %d 行' % n_f)
    left = [(i + 1, l.strip()[:60]) for i, l in enumerate(text.split(u'\n'))
            if re.search(u'(?<!〔案例 )99(?= 則| 個| 片| 案)', l)]
    print(u'殘留『99』計數宣稱：%d' % len(left))
    for i, s in left[:6]:
        print(u'   L%-5d %s' % (i, s))
    if apply:
        io.open(SRC, 'w', encoding=u'utf-8').write(text)
        print(u'已落檔')
    else:
        print(u'（dry-run）')


main()
