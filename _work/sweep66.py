# -*- coding: utf-8 -*-
"""第六十六輪探測：歷輪改名與削欄之後，全書殘留之舊稱、舊序、舊欄指涉。"""
import io
import re

import _tk as t

L = io.open(t.SRC, encoding='utf-8').read().split('\n')
out = []

# 一、章序實況
heads = [(i + 1, l) for i, l in enumerate(L) if re.match(r'^# 第[^章]*章', l) or re.match(r'^# 附錄', l) or l.startswith('# 結語')]
out.append('=== 一、H1 章序 ===')
for n, l in heads:
    out.append('L%-6d %s' % (n, l[:46]))

# 二、所有「通往第N章」／引橋／指針式標題與框
out.append('')
out.append('=== 二、引橋式標題與框（通往／引橋／交接／指針）===')
for i, l in enumerate(L):
    if re.search(r'(通往第|引橋|交接|之指針|檢索引橋|下一章|上章|承章)', l) and (
            l.startswith('#') or l.startswith('>') or l.startswith('**') or l.startswith('*')):
        out.append('L%-6d %s' % (i + 1, l[:120]))

# 三、舊稱清單（歷輪已改名者）
out.append('')
out.append('=== 三、舊稱殘留 ===')
OLD = {
    '三十格立體矩陣': '第55/63輪改為「三十格檢索總表」',
    '終審十維': '第58輪改為「十維驗收覆核報告」',
    '驗收認證報告': '第58輪改為「驗收覆核報告」',
    '終審法相台帳': '第58輪改為「法相台帳核定卡」',
    '終審核定卡': '第58輪',
    '終審消磁令': '第58輪改為「結案消磁令」',
    '無懈可擊': '第58輪削自誇',
    '萬古界碑': '第58輪削自誇',
    '十六觀心問與動態決策樹': '第60輪章題已改',
    '行者觀心專用': '第60輪保留但須與夜半四問並稱',
    '事相簡述': '第56輪削欄，只應剩第六章與說明',
    '主題概括': '第56輪削欄',
    '完全平帳': '第55輪降溫',
    '差額為零': '第55輪降溫',
    '平帳': '第55輪降溫（日誌引述除外）',
}
for k, why in OLD.items():
    hits = [i + 1 for i, l in enumerate(L) if k in l]
    out.append('%-22s %-16s %d 見 %s' % (k, why[:16], len(hits), hits[:14]))
io.open('_work/sweep66.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(out))
