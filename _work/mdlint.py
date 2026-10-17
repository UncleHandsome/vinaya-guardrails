# -*- coding: utf-8 -*-
"""機械式 Markdown／體例健檢（唯讀，輸出 _work/mdlint.txt）。"""
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import _tk as t

L = t.LINES
FENCE = '`' * 3
CODE_RE = re.compile(r'`[^`]*`')
o = []


def out(s):
    o.append(s)
    print(s)


f = [i + 1 for i, l in enumerate(L) if l.strip().startswith(FENCE)]
out('``` 圍欄 %d 個（%s）首筆 %s' % (len(f), '偶數·成對' if len(f) % 2 == 0 else '★奇數不成對', f[:10]))

# 底冊區（附錄C 修訂誌・K 台帳・L 驗收・M 校勘記・終卷）不印，且其文慣以反引號直呼腳本與符號
# （一行之內奇數枚 ` 與字面「**」俱常見），故粗體成對之檢唯及印面。
# 第 250 輪：底冊四篇已另檔，界標一律向 `_tk.bottom_lines()` 取（單一法源），勿再以篇名手搭區間。
_BOT = t.bottom_lines()


def _printable(i):
    return i not in _BOT


odd = [(i + 1, l) for i, l in enumerate(L)
       if _printable(i) and CODE_RE.sub('', l).count('**') % 2
       and not l.strip().startswith(FENCE)]
out('** 數為奇數之行：%d 筆（唯計印面；行內反引號跨度先剔，字面 `**` 非粗體 delimit）' % len(odd))
for i, l in odd[:14]:
    out('   L%-6d %s' % (i, l[:110]))

out('--- 表格欄數與表頭不合 ---')
i = 0
nbad = 0
while i < len(L):
    if L[i].lstrip().startswith('|') and i + 1 < len(L) and re.match(r'^\|[\s:|-]+\|$', L[i + 1].strip()):
        ncol = L[i].count('|')
        j = i + 2
        while j < len(L) and L[j].lstrip().startswith('|'):
            if L[j].count('|') != ncol:
                nbad += 1
                if nbad < 16:
                    out('   L%-6d 欄%d≠表頭%d :: %s' % (j + 1, L[j].count('|'), ncol, L[j][:80]))
            j += 1
        i = j
    else:
        i += 1
out('   合計 %d 列' % nbad)

bad = [(i + 1, l) for i, l in enumerate(L) if l.startswith('## ') and not re.match(r'^## 【', l)]
out('--- H2 未以【】起者（凡例：H2 限卷首與附錄存目）：%d ---' % len(bad))
for i, l in bad[:8]:
    out('   L%-6d %s' % (i, l[:80]))

SIMPLE = '与么为观记设话语书务团学习国实对经关闭问题样种术职允许实现达变历产从优会传伤体亚亲仅俩价众伞伟图无数档录让们这没来断应净准备养兽释马驾'
out('--- 疑似簡體字殘留 ---')
hits = {}
for i, l in enumerate(L):
    for ch in l:
        if ch in SIMPLE:
            hits.setdefault(ch, []).append(i + 1)
for ch, v in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:14]:
    out('   %r ×%-3d L%s' % (ch, len(v), v[:6]))

out('--- CJK 間半形標點 ---')
pat = re.compile(r'[一-鿿][,.;:?!][一-鿿]')
n = 0
for i, l in enumerate(L):
    if pat.search(l) and not l.strip().startswith(FENCE):
        n += 1
        if n < 10:
            out('   L%-6d %s' % (i + 1, l[:80]))
out('   合計 %d 行' % n)

out('--- 行尾孤立半形空格（md 硬換行须雙空格）：單一尾空格行 ---')
one = [i + 1 for i, l in enumerate(L) if _printable(i) and re.search(r'[^ ] $', l)]
out('   %d 行：%s' % (len(one), one[:10]))

open('_work/mdlint.txt', 'w', encoding='utf-8').write('\n'.join(o))
