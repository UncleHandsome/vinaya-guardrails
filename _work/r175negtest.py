# -*- coding: utf-8 -*-
# 第 175 輪負測：兩條新閘須以原病回植證其能報，且植畢必還原、雜湊必相符。
#   甲 撤附錄D 前之分隔線 → 『篇題之前一律有分隔線』須報（回植 173 前之原病）
#   乙 印面散文行加野縮排   → 『印面無野縮排』須報
#   丙 底冊同處加野縮排     → 須不報（豁免之界生效）
import hashlib, io, re, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
K = [u'篇題之前一律有分隔線', u'印面無野縮排', u'印面無野縮排']
A_OLD = u'仍依前輪紅線不動。\n\n---\n\n# 附錄D'
A_NEW = u'仍依前輪紅線不動。\n\n# 附錄D'
B_ANCHOR = u'三十二字憲綱，於行者提純之際層層剝落'
C_ANCHOR = u'母數 13,355 行（本條入檔另計）。'


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def measure():
    out = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                         capture_output=True).stdout.decode('utf-8', 'replace')
    g = {}
    for key in set(K):
        m = re.search(u'^(PASS|FAIL)\\s*' + key + u'.*$', out, re.M)
        g[key] = m.group(0)[:104] if m else u'（未見此檢！）'
    return g


orig = io.open(BOOK, encoding='utf-8').read()
assert orig.count(A_OLD) == 1 and orig.count(B_ANCHOR) == 1 and orig.count(C_ANCHOR) == 1
h0 = sha(orig)
print(u'基態｜%s' % measure()[K[0]])

for tag, old, new, key in (
        (u'甲 撤分隔線', A_OLD, A_NEW, K[0]),
        (u'乙 印面植野縮', B_ANCHOR, u'  ' + B_ANCHOR, K[1]),
        (u'丙 底冊植野縮', C_ANCHOR, u'  ' + C_ANCHOR, K[2])):
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(old, new))
    g = measure()
    print(u'%s → %s' % (tag, g[key]))
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    print(u'    還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
print(u'終態==初態：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
