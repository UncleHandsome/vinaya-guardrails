# -*- coding: utf-8 -*-
"""277 輪・刀：第七章第二節『處分階梯軸』與『四諍軸』之歸位（第十尺 v39ladder 逮得之錯列）。

病：『迎回補丁』以分號把未入軸之案塞進最相近的一行以湊數，遂有『落水救拔・師徒瞻視・安隱尼問倒・
    目連緘默』同列『不可懺·極刑滅擯』之荒謬（報告所指，量而俱實）。
治（一物一據，皆自本案之載體行與附錄四行取其律刑）：
    13 落水救拔 ➔ 宣告無犯 ➔ 第七階      20 異分取片 ➔ 反坐第九僧殘 ➔ 第二階
    51 私度關逃稅 ➔ 波逸提六七 ➔ 第四階   72 兵象猛獸 ➔ 不應食（教誡）➔ 第六階
    75 師徒瞻視 ➔ 聽立瞻視責任（開許）➔ 第七階   92 安隱尼問倒 ➔ 比丘尼波逸提 ➔ 第四階
    93 目連緘默 ➔ 第七階已有，第一階除其重出
    101 僧地入己 ➔ 應語令起（教誡）➔ 第六階       102 安居聞利 ➔ 失歲結違要（突吉羅）➔ 第五階
    35 蓮華色覺醒 ➔ 因緣敘事（非波逸提犯）➔ 第六階  89 新堂初坐 ➔ 瞋嫌慢爭（非波逸提）➔ 第六階
    88 跋難陀自在 ➔ 『是應是不應』教誡之鏡 ➔ 第六階  99 難民借衣 ➔ 急難開許 ➔ 第七階
    四諍：言諍除 94・96・35・53（皆非教義之爭）；覓諍除 60・06；事諍除 51。
    第六・七階之自報『31／34』乃補丁时代之虛數，一律按實列之唯一案號改齊。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r277ladder.py [apply]
"""
import hashlib
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
L0 = io.open(SRC, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').split(u'\n')

MOVES = [  # (案號, 源軸行首, 目軸行首)
    (13, u'第一階', u'第七階'), (20, u'第一階', u'第二階'), (51, u'第一階', u'第四階'),
    (72, u'第一階', u'第六階'), (75, u'第一階', u'第七階'), (92, u'第一階', u'第四階'),
    (101, u'第二階', u'第六階'), (102, u'第二階', u'第五階'),
    (35, u'第四階', u'第六階'), (89, u'第四階', u'第六階'),
    (88, u'第五階', u'第六階'), (99, u'第六階', u'第七階'),
]
DUPS = [(93, u'第一階', u'第七階')]                      # 目階已有，源階除其重出
DROPS = [(94, u'言諍'), (96, u'言諍'), (35, u'言諍'), (53, u'言諍'),
         (60, u'覓諍'), (6, u'覓諍'), (51, u'事諍')]

HEAD = re.compile(r'^\* \*\*(.+?)，?共 (\d+) 案')


def axis_key(name):
    m = re.match(u'第([一二三四五六七])階', name)
    if m:
        return u'第' + m.group(1) + u'階'
    m = re.search(u'([言覓犯事]諍)', name)
    return m.group(1) if m else None


def rows(lines):
    """回傳 {軸鍵: (標題行, [名單行…])}——名單行＝至下一軸標題或更高層級題前、含〔案例』之諸行。"""
    out = {}
    heads = [(i, axis_key(HEAD.match(lines[i]).group(1))) for i in range(len(lines)) if HEAD.match(lines[i])]
    for k, (i, key) in enumerate(heads):
        stop = heads[k + 1][0] if k + 1 < len(heads) else next(
            (j for j in range(i + 1, len(lines)) if lines[j].startswith(u'#')), len(lines))
        items = [j for j in range(i + 1, stop) if u'〔案例' in lines[j]]
        if items:
            out[key] = (i, items)
    return out


def item_span(line, n):
    """取该案在名單行之完整片語（自〔案例NN〕起，至下一個『、』或『；』或行末句號前）。"""
    m = re.search(u'〔案例 ?0*%d〕' % n, line)
    if not m:
        return None
    a = m.start()
    b = a
    while b < len(line) and line[b] not in u'、；。':
        b += 1
    while b < len(line) and line[b] == u'。':
        break
    return line[a:b]


def grab(line, n):
    """取該案在此名單行之完整片語（自〔案例NN〕起，至『、』『；』或『。』前止）。"""
    m = re.search(u'〔案例 ?0*%d〕' % n, line)
    if not m:
        return None
    a = m.start()
    b = a
    while b < len(line) and line[b] not in u'、；。':
        b += 1
    return line[a:b]


def clean(line):
    line = re.sub(u'；+。', u'。', line)
    line = re.sub(u'、+。', u'。', line)
    line = re.sub(u'；+', u'；', line)
    line = re.sub(u'、+', u'、', line)
    line = re.sub(u'。$', u'。', line)
    return line


def pull(lines, r, n):
    """自某軸之諸名單行中摘出该案片語；返回（片語, 行號）。"""
    for j in r[1]:
        frag = grab(lines[j], n)
        if frag:
            if (frag + u'、') in lines[j]:
                lines[j] = lines[j].replace(frag + u'、', u'')
            elif (u'、' + frag) in lines[j]:
                lines[j] = lines[j].replace(u'、' + frag, u'')
            else:
                lines[j] = lines[j].replace(frag, u'')
            lines[j] = clean(lines[j])
            return frag, j
    return None, None


def move(lines, src, dst, n, drop_only=False):
    R = rows(lines)
    frag, j = pull(lines, R[src], n)
    if not frag:
        raise AssertionError(u'%s 名單內查無案例 %03d' % (src, n))
    if drop_only:
        print(u'    除：%s｜%s' % (src, frag[:36]))
        return
    tail = lines[R[dst][1][-1]].rstrip()
    if not tail.endswith(u'。'):
        raise AssertionError(u'目標軸 %s 之行非句號結：%s' % (dst, tail[-14:]))
    lines[R[dst][1][-1]] = tail[:-1] + u'、' + frag + u'。'
    print(u'    移：%s ➔ %s｜%s' % (src, dst, frag[:36]))


def recount(lines, skip=(u'犯諍',)):
    R = rows(lines)
    for key, (hi, items) in R.items():
        if key in skip:
            print(u'  %-6s 依例不重計（分群之列，其數由人工守）' % key)
            continue
        body = chr(10).join(lines[j] for j in items)
        nums = [int(x) for x in re.findall(r'〔案例 ?0*(\d+)〕', body)]
        u = len(set(nums))
        lines[hi] = re.sub(r'共 \d+ 案', u'共 %d 案' % u, lines[hi], count=1)
        print(u'  %-6s 宣稱 ➔ %d（唯一案號・出現 %d 枚）' % (key, u, len(nums)))


def main():
    apply = u'apply' in sys.argv
    raw = io.open(SRC, encoding=u'utf-8-sig').read()
    L = list(L0)
    print(u'正本｜%d 行・sha256 %s' % (len(L), hashlib.sha256(raw.encode(u'utf-8')).hexdigest()[:12]))
    for n, s, d in MOVES:
        move(L, s, d, n)
    for n, s, d in DUPS:
        move(L, s, d, n, drop_only=True)
    for n, s in DROPS:
        if s not in rows(L):
            raise AssertionError(u'軸 %s 不可見' % s)
        move(L, s, s, n, drop_only=True)
    recount(L)
    bad = [(k, j) for k, (_h, items) in rows(L).items() for j in items
           if any(s in L[j] for s in (u'；。', u'、。', u'、、', u'；、'))]
    print(u'覆核｜名單行殘留串點 %d 處' % len(bad))
    if bad:
        return 1
    txt = u'\n'.join(L)
    if not apply:
        print(u'———— 乾跑畢（加 apply 方落刀）・字數 %+d・行數 %+d' % (len(txt) - len(raw), len(L) - len(L0)))
        return 0
    shutil.copyfile(SRC, os.path.join(WORK, u'r277ladder.bak'))
    io.open(SRC, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    new = io.open(SRC, encoding=u'utf-8').read()
    print(u'落刀｜備份 r277ladder.bak｜%d 行・%d B・sha256 %s' % (
        new.count(u'\n') + 1, len(new.encode(u'utf-8')), hashlib.sha256(new.encode(u'utf-8')).hexdigest()[:12]))
    return 0 if new == txt else 2


if __name__ == u'__main__':
    sys.exit(main())
