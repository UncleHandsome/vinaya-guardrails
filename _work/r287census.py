# -*- coding: utf-8 -*-
r"""287 候裁清單・實測（唯讀）。

對兩冊（ver38 與 ver39 正本）逐件量出：迎回之體量、今冊之缺口、舊債之現形。
只印數，不改檔。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V39 = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
V38 = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')


def load(p):
    return io.open(p, encoding='utf-8').read().replace('\r\n', '\n')


T39, T38 = load(V39), load(V38)
L39, L38 = T39.split('\n'), T38.split('\n')
print(u'冊：ver39 %d 行・%d 字｜ver38 %d 行・%d 字' % (len(L39), len(T39), len(L38), len(T38)))


def heads(L, pat):
    return [(i + 1, l) for i, l in enumerate(L) if re.search(pat, l)]


def show(tag, L, pat, n=12, cap=76):
    hs = heads(L, pat)
    print(u'  %-22s %3d 見｜%s' % (tag, len(hs), u' / '.join(h[1].strip()[:cap] for h in hs[:n])))
    return hs


print(u'\n【一・133 綁定台帳】')
show(u'v38『台帳』', L38, u'台帳')
show(u'v38『133』', L38, u'133')
show(u'v39『台帳』', L39, u'台帳')
show(u'v39『133』', L39, u'133')

print(u'\n【二・29 則稱重法式】')
show(u'v38『稱重』', L38, u'稱重')
show(u'v39『稱重』', L39, u'稱重')

print(u'\n【三・附錄B 壓力測試】')
h = show(u'v38 附錄B 題', L38, u'^# 附錄B|^#### .*壓力測試|^### .*壓力測試')
v38B = [l for l in L38 if re.search(u'^# 附錄B', l)]
# 附錄B 之體量：自其 H1 至下一個 H1
if v38B:
    i = L38.index(v38B[0])
    j = next((k for k in range(i + 1, len(L38)) if L38[k].startswith(u'# ')), len(L38))
    blk = L38[i:j]
    print(u'  v38 附錄B 區間 L%d〜L%d＝%d 行・%d 字' % (i + 1, j, len(blk), sum(len(x) for x in blk)))
    print(u'  其中『測試』條目：%d 條' % len([x for x in blk if re.search(u'^\*\*?測試|^\d+\. |^### ', x)]))
show(u'v39『壓力測試』', L39, u'壓力測試')

print(u'\n【四・五大世俗法務 SOP／防線】')
show(u'v38『世俗法務』', L38, u'世俗法務|五大世俗')
show(u'v39『世俗法務』', L39, u'世俗法務|五大世俗')

print(u'\n【五・F-2 查無清單】')
show(u'v38『F-2』', L38, u'F-2')
show(u'v39『F-2』', L39, u'F-2')

print(u'\n【六・舊債現形（今冊）】')
ci = len(re.findall(u'〔案例 \d{1,3} / [遮僧開]\d+〕', T39))
print(u'  次碼〔NN／遮僧開MM〕：%d 枚（284 帳作 62，285・286 之後須以今量為準）' % ci)
claim = re.findall(u'(?:共|\uff08)(\d+) 案', T39)
print(u'  『N 案』宣稱：%d 枚（尺十口徑五俱校）' % len(claim))
d = len(re.findall(u'卷次未細核', T39))
print(u'  卷次未細核：%d 見（核卷尺之未證 18 條屬此族）' % d)
print(u'  句讀：無標點長段≥40 字者由第 32 目校（今 0 紅）；20〜39 字之段今另量 ➔', end=u'')
STOP = u'，。、；：！？・『』「”（）《》…—'
segs = [s for s in re.findall(u'「([^」]+)」', T39) if len(s) >= 20 and not any(c in STOP for c in s)]
print(u' %d 段' % len(segs))
print(u'  第九章／第九章字面：%d 見｜『補遺』：%d 見｜『範本待議』：%d 見'
      % (T39.count(u'第九章'), T39.count(u'補遺'), T39.count(u'範本待議')))
h5 = heads(L39, u'^# 第[一二三四五六七八九十]+章')
print(u'  章級 H1：%d 條 ➔ %s' % (len(h5), u'、'.join(x[1][2:14] for x in h5)))

print(u'\n【七・精簡本（slim）之制】')
sys.path.insert(0, os.path.join(ROOT, u'_print'))
try:
    S = io.open(os.path.join(ROOT, u'_print', u'build39.py'), encoding='utf-8').read()
    m = re.search(u'SLIM[^=\n]*=', S)
    print(u'  build39 之 slim 攔：%s' % (u'有（run slim 即擲回）' if u'slim' in S else u'無'))
    print(u'  SLIM_BLOCKS 之元素數：%s' % (len(re.findall(u'^\s*[\'\"]', m.group(0), re.M)) if m else u'未見'))
except Exception as e:
    print(u'  讀產器失敗：%s' % e)
