# -*- coding: utf-8 -*-
"""r161sent2.py —— 第 161 輪・句級梳理乙批：自動尋得『長句而含分枝標記者』就地斷拍。

甲批以人列之 11 行斷 18 拍，最長句由 295 降 171。本批改由器自尋：
  候選＝印面散文或列條之內，單句 ≥150 字而句中另有『；**』（粗體分枝）或『；①～⑦』（序號分枝）者；
  手法＝唯將該分枝前之分號升為句號——一字不易，只易一標點；
  口徑剔案例代碼之清冊（〔…〕八枚以上）與引言塊、表格（同 readchk 第九目）。
用法：DRY=1 只報不寫。
"""
import io, os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

SRC = [f for f in os.listdir('.') if f.startswith('ver38') and f.endswith('.md')][0]
D = 'DRY' in os.environ
L = t.LINES
N = len(L)
BOT = set(t.bottom_lines())
FEN = [False] * N
_in = False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        _in = not _in
        FEN[i] = True
        continue
    FEN[i] = _in
PRINT = [i for i in range(N) if i not in BOT and not FEN[i]]


def kind(i):
    s = L[i].strip()
    if s == u'':
        return u'空'
    if s.startswith(u'|'):
        return u'表'
    if s.startswith(u'#'):
        return u'題'
    if s.startswith(u'>'):
        return u'引'
    if re.match(u'^([-*]\\s|\\d+[.)、]\\s|[（(][一二三四五六七八九十]+[）)])', s):
        return u'列'
    if s in (u'---', u'***'):
        return u'線'
    return u'文'


SENT = re.compile(u'[^。！？]*[。！？]')
CODE = re.compile(u'〔[^〕]{1,6}〕')
BRANCH = re.compile(u'；(?=[①②③④⑤⑥⑦*])')
LIM = 150
rows = []
for i in PRINT:
    if kind(i) not in (u'文', u'列') or len(CODE.findall(L[i])) >= 8:
        continue
    s = L[i]
    if not BRANCH.search(s):
        continue
    mx = max([len([c for c in seg if not c.isspace()]) for seg in SENT.findall(s)] or [0])
    if mx >= LIM:
        rows.append((mx, i, s.count(u'；**') + len(re.findall(u'；[①②③④⑤⑥⑦]', s))))
rows.sort(key=lambda x: -x[0])
print(u'候選：%d 行（單句 ≥%d 字且含分枝標記）' % (len(rows), LIM))
lines = io.open(SRC, encoding='utf-8').read().split(u'\n')
for mx, i, cnt in sorted(rows, key=lambda x: -x[0]):
    s2 = BRANCH.sub(u'。', lines[i])
    assert s2 != lines[i]
    after = max([len([c for c in seg if not c.isspace()]) for seg in SENT.findall(s2)] or [0])
    print(u'  L%-6d 最長句 %3d → %3d｜斷 %d 拍｜%s' % (i + 1, mx, after, cnt, lines[i].strip()[:24]))
    lines[i] = s2
print(u'共 %d 行、%d 拍' % (len(rows), sum(c for _, _, c in rows)))
if D:
    sys.exit(0)
shutil.copy(SRC, '_work/r161bak2.md')
io.open(SRC, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(lines))
print(u'已落刀。')
