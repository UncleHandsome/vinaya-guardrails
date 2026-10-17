# -*- coding: utf-8 -*-
# 第 176 輪負測：二條新閘須以植病證其能報，且底冊同形不報（歸零非消音），植畢俱還原核雜湊。
import hashlib, io, re, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
K1 = u'印面粗體記號段內成對'
K2 = u'印面六族括號段內平衡'
A = u'三禁既守，正理八方還其本懷'          # 印面（第一章）
B = u'母數 13,355 行（本條入檔另計）。'      # 底冊（附錄M）


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def measure():
    out = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                         capture_output=True).stdout.decode('utf-8', 'replace')
    g = {}
    for key in (K1, K2):
        m = re.search(u'^(PASS|FAIL)\\s*' + key + u'.*$', out, re.M)
        g[key] = m.group(0)[:112] if m else u'（未見此檢！）'
    return g


orig = io.open(BOOK, encoding='utf-8').read()
assert orig.count(A) == 1 and orig.count(B) == 1, u'錨點命中數不符，未動檔'
h0 = sha(orig)
g = measure()
print(u'基態｜%s' % g[K1])
print(u'基態｜%s' % g[K2])

CASES = [(u'甲 印面植落單星號', A, u'——**植碼未閉', K1),
         (u'乙 印面植單邊括號', A, u'（另植〔单边括', K2),
         (u'丙 底冊植落單星號', B, u'**植碼未閉', K1),
         (u'丁 底冊植單邊括號', B, u'〔植碼未閉', K2)]
for tag, anchor, extra, key in CASES:
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(anchor, anchor + extra))
    g = measure()
    print(u'%s → %s' % (tag, g[key]))
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    print(u'    還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
print(u'終態==初態：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
