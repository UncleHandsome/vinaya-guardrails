# -*- coding: utf-8 -*-
"""第七十二輪軸三：書中「『某語』N 見」「全書 N 處／凡 N 條」式自稱之復算。
產出為待診清單（口径不同須人工斷），非缺陷清單。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(ROOT, 'ver38四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
VIN = ''
for f in sorted(os.listdir(os.path.join(ROOT, '原文'))):
    if f.endswith('.txt'):
        VIN += open(os.path.join(ROOT, '原文', f), encoding='utf-8', errors='replace').read()

FOLD = [('恒', '恆'), ('净', '淨'), ('净', '凈'), ('却', '卻'), ('里', '裏'), ('众', '眾'), ('与', '與')]


def vc(term):
    cands = {term}
    for a, b in FOLD:
        if a in term:
            cands.add(term.replace(a, b))
        if b in term:
            cands.add(term.replace(b, a))
    return max(VIN.count(c) for c in cands)


out = []
pat = re.compile('[「『]([^」』]{2,14})[」』][^。「；，\n]{0,10}?(\\d{1,5})\\s*(見|處|次|條|項)')
seen = set()
bad = []
tot = 0
for m in pat.finditer(DOC):
    term, num, unit = m.group(1), int(m.group(2)), m.group(3)
    if unit != '見' or term in seen:
        continue
    seen.add(term)
    tot += 1
    ln = DOC[:m.start()].count('\n') + 1
    act = vc(term)
    if act != num:
        bad.append((ln, term, num, act))
out.append('=== 一、語料字頻宣稱（『X』N 見）：可測 %d 筆，不符 %d 筆 ===' % (tot, len(bad)))
for ln, term, num, act in bad:
    out.append('  L%-6d %-16s 載 %4d 實 %4d' % (ln, term, num, act))

out.append('')
out.append('=== 二、本書自我計數宣稱（全書／凡／共／計 ＋ 數字 ＋ 處·條·項·則·個）===')
pat2 = re.compile('(全書|本書|凡|共|計)\\s*(?:所載|所收)?\\s*(?:其他)?[^。；\n]{0,8}?(\\d{1,4})\\s*(處|條|項|則|個|款|篇|章|節)')
rows = []
for m in pat2.finditer(DOC):
    rows.append((DOC[:m.start()].count('\n') + 1, m.group(0).strip(), int(m.group(2)), m.group(3)))
out.append('  共 %d 筆，逐筆須人工斷其母數與口径；列前 60 筆：' % len(rows))
for ln, s, num, unit in rows[:60]:
    out.append('  L%-6d %-52s %d %s' % (ln, s.replace('\n', ''), num, unit))
open(os.path.join(HERE, 'selfcount.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('terms', tot, 'mismatch', len(bad), 'selfclaims', len(rows))
