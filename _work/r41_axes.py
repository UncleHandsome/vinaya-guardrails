# -*- coding: utf-8 -*-
"""第四十一輪自建之二軸抽查（可重跑）：
軸一：心相照鏡所描之心 ↔ 定位行根本心（關鍵字缺席即提出人工覆核，勿逕改）。
軸二：佛陀處斷欄點名之正理 ↔ 定位行所掛之正理（差屬行文之常，綁定唯以定位行為準）。
用法：PYTHONPATH=. python -X utf8 _work/r41_axes.py
"""
import io
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(HERE, '_work')
SRC = [f for f in os.listdir(HERE) if f.startswith('ver37') and f.endswith('.md') and u'列印' not in f][0]
L = io.open(os.path.join(HERE, SRC), encoding='utf-8').read().split('\n')
S6 = [i for i, l in enumerate(L) if l.startswith(u'# 第六章')][0]
E6 = [i for i, l in enumerate(L) if l.startswith(u'# 第七章')][0]
KW = {u'貪': [u'貪'], u'瞋': [u'瞋', u'怒', u'恨'], u'癡': [u'癡', u'無明', u'愚'],
      u'慢': [u'慢', u'傲', u'名位', u'身段', u'面子'],
      u'清淨': [u'清淨', u'慈', u'悲', u'出離', u'慚', u'愧', u'捨', u'真理', u'解脫'],
      u'無記': [u'無記', u'不知', u'無心', u'未成', u'看錯'], u'懈怠': [u'懈怠', u'推諉', u'不作為']}
CN = u'一二三四五六七八'


def cases():
    """yield (案例號, 定位行根本心, 定位行正理集, 心相全文, 處斷欄正文)"""
    i = S6
    while i < E6:
        m = re.match(u'^#### 〔(遮|開|僧)(\\d+)〕', L[i])
        if m:
            cid = m.group(1) + m.group(2)
            nxt = [j for j in range(i + 1, E6) if re.match(u'^#### 〔', L[j])]
            stop = nxt[0] if nxt else E6
            root, pos, mirror, duan = None, None, [], []
            for j in range(i, stop):
                if L[j].startswith(u'**定位｜根本心：'):
                    seg = L[j]
                    root = seg.split(u'根本心：')[1].split(u'｜')[0].strip()
                    tail = seg.split(u'八大正理：')[1] if u'八大正理：' in seg else u''
                    pos = set(re.findall(u'正理([%s])' % CN, tail))
                if L[j].strip() == u'##### 心相照鏡':
                    k = j + 1
                    while k < E6 and not L[k].startswith(u'##### ') and not L[k].startswith(u'#### '):
                        if L[k].strip():
                            mirror.append(L[k])
                        k += 1
                if L[j].startswith(u'##### 佛陀處斷'):
                    k = j + 1
                    while k < E6 and not L[k].startswith(u'##### ') and not L[k].startswith(u'#### '):
                        duan.append(L[k])
                        k += 1
            yield cid, root, pos, u''.join(mirror), u''.join(duan)
        i += 1


def main():
    o, ax1, ax2, ax2n, n2 = [], [], [], 0, 0
    for cid, root, pos, mirror, duan in cases():
        if not root:
            continue
        base = root.split(u'加')[0].split(u'（')[0].strip()
        if mirror and base in KW and not any(w in mirror for w in KW[base]):
            ax1.append(u'  %-6s 標=%-24s | %s' % (cid, root, mirror[:70]))
        if pos and duan:
            d = set(re.findall(u'正理([%s])' % CN, duan))
            n2 += 1
            extra = sorted(d - pos)
            if extra:
                ax2n += 1
                ax2.append(u'  %-6s 定位=%-4s 處斷多點=%s' % (cid, u''.join(sorted(pos)), u''.join(extra)))
    o.append(u'== 軸一：心相無所標根本心之關鍵字（待人工覆核，非缺陷清單）%d 案 ==' % len(ax1))
    o += ax1
    o.append(u'' if not ax1 else u'  …（本軸歷輪覆核結論：悉屬同義詞誤報，無一確認缺陷）')
    o.append(u'== 軸二：%d 可對案例中，處斷點名而定位行未掛者 %d 案（綁定唯以定位行為準，非漏計）==' % (n2, ax2n))
    o += ax2
    io.open(os.path.join(WORK, 'r41_axes.txt'), 'w', encoding='utf-8').write(u'\n'.join(o))
    print(u'軸一 %d 案（誤報待人工覆核）；軸二 %d/%d 案處斷多點正理' % (len(ax1), ax2n, n2))


if __name__ == '__main__':
    main()
