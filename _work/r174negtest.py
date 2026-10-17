# -*- coding: utf-8 -*-
# 第 174 輪收尾之負測（三植三證，植畢俱還原並核雜湊）：
#   甲 正文植『第八章第五節第一款』 → 附錄K 回指檢須報（器有牙）
#   乙 底冊植同語                → 該檢須不報（證源新界生效）
#   丙 印面植簡形『两』於引號外    → 簡形檢須報（名單新字有牙）
import hashlib, io, re, subprocess, sys

BOOK = 'ver38四分律_起心動念心智分析框架_修正版.md'
KKEY = u'附錄K 回指狀態＝實測'
SKEY = u'引號外無簡體孤立字'
A = u'前後相續，非一次儀禮做兩遍。'
B = u'母數 13,355 行（本條入檔另計）。'
C = u'業道成立依境想思相；'

def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()

def measure():
    out = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                         capture_output=True).stdout.decode('utf-8', 'replace')
    g = {}
    for key in (KKEY, SKEY):
        m = re.search(r'^(PASS|FAIL)\s*' + key + u'.*$', out, re.M)
        g[key] = m.group(0)[:110] if m else u'（未見此檢！）'
    return g

def report(tag, g, key):
    print(u'%s ｜ %s' % (tag, g[key]))

orig = io.open(BOOK, encoding='utf-8').read()
for nm, s in ((u'甲', A), (u'乙', B), (u'丙', C)):
    assert orig.count(s) == 1, u'%s 錨點命中 %d，未動檔' % (nm, orig.count(s))
h0 = sha(orig)

g = measure()
report(u'基態', g, KKEY)
report(u'基態', g, SKEY)

for tag, anchor, extra, key in (
        (u'甲 正文植指針', A, u'（復測植碼：詳第八章第五節第一款之但書）', KKEY),
        (u'乙 底冊植指針', B, u'（復測植碼：詳第八章第五節第一款之但書）', KKEY),
        (u'丙 印面植簡形', C, u'此論两款俱通。', SKEY)):
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(anchor, anchor + extra))
    g = measure()
    report(tag, g, key)
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    print(u'   還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))

print(u'終態雜湊==初態：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
