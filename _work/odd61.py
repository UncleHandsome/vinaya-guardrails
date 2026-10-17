# -*- coding: utf-8 -*-
"""第六十一輪前哨：掃描全書非常規碼位（韓日假名、異形空格、控制字元）。"""
import io, os, sys, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(ROOT, u'ver38\u56db\u5206\u5f8b_\u8d77\u5fc3\u52d5\u5ff5\u5fc3\u667a\u5206\u6790\u6846\u67b6_\u4fee\u6b63\u7248.md'),
           encoding='utf-8').read()

bad = {}
for i, ch in enumerate(DOC):
    o = ord(ch)
    if o < 128 or ch in '\n\r':
        continue
    if 0x4E00 <= o <= 0x9FFF or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF:
        continue
    if 0x2000 <= o <= 0x2BFF:
        continue
    if 0x00C0 <= o <= 0x024F:
        continue
    if 0x0370 <= o <= 0x3FF:      # 希臘
        continue
    bad.setdefault(ch, []).append(DOC[:i].count('\n') + 1)

out = []
for ch, v in sorted(bad.items()):
    try:
        nm = unicodedata.name(ch)
    except Exception:
        nm = '?'
    out.append('U+%04X | %s | %s | %d | %s' % (ord(ch), nm, ch, len(v), v[:6]))
open(os.path.join(HERE, 'odd61.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('kinds', len(bad))
