# -*- coding: utf-8 -*-
"""第 253 輪・刀一：三十九版全書舊案號〔遮N／開N／僧N〕之死鏈改鏈。

三十九版第六章已改號為〔案例 01〕～〔案例 100〕，而第一～五章與第七章之 87 處指針
猶呼叫舊帳法相分類號（56 個不同舊號），讀者按號求案而不得——其害同於死鏈。

對照之法源：以 ver38 舊卡（號＋題＋內文人名）對 ver39 新卡（案例號＋題＋內文），
由 `_work/r253map.py` 出候選，再逐條親裁如下表。舊號乃**分類**，一類可含新制數案，
故兩案同舉者列雙號；確無對應卡者（11 號）不虛指，逕削其號而留原句之事相描述。

用法：python -X utf8 _work/r253relink.py         # dry-run（印每行之前後對照）
      python -X utf8 _work/r253relink.py apply
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

MAP = {
    u'僧1': u'案例 83', u'僧2': u'案例 84', u'僧3': u'案例 85', u'僧7': u'案例 88',
    u'僧9': u'案例 49',
    u'僧10': u'案例 90', u'僧11': u'案例 91', u'僧17': u'案例 96', u'僧18': u'案例 97',
    u'僧19': u'案例 98', u'僧20': u'案例 62', u'僧22': u'案例 63', u'僧26': u'案例 80',
    u'僧30': u'案例 09',
    u'遮1': u'案例 32', u'遮4': u'案例 41', u'遮5': u'案例 42', u'遮6': u'案例 70',
    u'遮7': None, u'遮8': None, u'遮9': u'案例 77', u'遮10': u'案例 79',
    u'遮12': u'案例 97', u'遮13': u'案例 47', u'遮16': None, u'遮17': u'案例 28',
    u'遮19': u'案例 24', u'遮20': u'案例 26', u'遮21': u'案例 27', u'遮22': None,
    u'遮23': u'案例 60', u'遮26': u'案例 20', u'遮29': u'案例 46', u'遮31': u'案例 53',
    u'遮32': u'案例 58', u'遮33': None, u'遮34': u'案例 29', u'遮35': u'案例 56',
    u'遮36': u'案例 68', u'遮37': None, u'遮38': u'案例 34', u'遮39': u'案例 67',
    u'遮40': u'案例 35', u'遮41': u'案例 72', u'遮42': None,
    u'遮44': u'案例 05〕〔案例 06',
    u'開2': None, u'開3': None, u'開9': u'案例 44', u'開10': None,
    u'開11': u'案例 13〕〔案例 14', u'開12': u'案例 78', u'開14': None,
    u'開18': u'案例 15', u'開20': u'案例 40', u'開21': u'案例 76',
}
RX = re.compile(u'〔(遮|開|僧)\\s*(\\d+)〕')
DROPED = sorted([k for k, v in MAP.items() if v is None])


def relink_line(line):
    hits = list(RX.finditer(line))
    if not hits:
        return line, 0, 0
    n_map = sum(1 for m in hits if MAP.get(m.group(1) + m.group(2)))
    n_drop = len(hits) - n_map
    out = RX.sub(lambda m: u'〔%s〕' % MAP[m.group(1) + m.group(2)]
                 if MAP.get(m.group(1) + m.group(2)) else u'§§', line)
    # 削號之後之空殼：『（）』、『（、）』、『（§§，〔案例 x〕）』之类先清分隔再拋空括
    out = re.sub(u'§§\\s*[、，；]\\s*', u'', out)
    out = re.sub(u'[、，；]\\s*§§', u'', out)
    out = out.replace(u'§§', u'')
    out = re.sub(u'（\\s*[、，；]?\\s*）', u'（', out) if False else out
    out = re.sub(u'（\\s*）', u'', out)
    out = re.sub(u'[（（]〔', u'（〔', out)
    out = re.sub(u'〔([^〕]*)〕[、，]\\s*）', u'〔\\1〕）', out)
    out = re.sub(u'  +', u' ', out) if u'§§' in line else out
    return out, n_map, n_drop


def main():
    apply = u'apply' in sys.argv[1:]
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
    seen = set()
    for l in lines:
        for m in RX.finditer(l):
            seen.add(m.group(1) + m.group(2))
    miss = sorted(seen - set(MAP))
    if miss:
        raise SystemExit(u'對照表未蓋到之舊號 %d 個：%s —— 未斷言即不落刀'
                         u'（防『表外之號被當作死號偷偷削去』）' % (len(miss), u' '.join(miss)))
    print(u'書中實引用之舊號 %d 個｜對照表 %d 條俱有歸屬（改鏈 %d、削號 %d）'
          % (len(seen), len(MAP), len([v for v in MAP.values() if v]),
             len([v for v in MAP.values() if v is None])))
    changed, tot_map, tot_drop = [], 0, 0
    for i, l in enumerate(lines):
        nl, a, b = relink_line(l)
        if nl != l:
            changed.append((i + 1, l, nl))
            tot_map += a
            tot_drop += b
    print(u'受刀之行 %d｜改鏈 %d 處｜削死號 %d 處（11 舊號確無新卡）'
          % (len(changed), tot_map, tot_drop))
    for i, a, b in changed:
        print(u'-- L%d\n   前 %.105s\n   後 %.105s' % (i, a.strip(), b.strip()))
    left = [(i + 1, l.strip()[:80]) for i, l in enumerate(lines)
            if RX.search(relink_line(l)[0])]
    print(u'\n殘留舊號（須為 0）：%d' % len(left))
    for i, s in left[:8]:
        print(u'   L%-6d %s' % (i, s))
    print(u'削號之 11 舊帳：%s' % u' '.join(DROPED))
    if not apply:
        print(u'（dry-run，未落檔）')
        return
    out = []
    for l in lines:
        nl, _a, _b = relink_line(l)
        out.append(nl)
    io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(out))
    print(u'已落檔｜行數 %d' % len(out))


main()
