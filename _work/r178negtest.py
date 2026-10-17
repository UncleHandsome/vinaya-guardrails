# -*- coding: utf-8 -*-
# 第 178 輪負測：二條新閘（83 表必帶分隔行・84 標題不無端跨級）須植病能報、底冊不報，還原核雜湊。
import hashlib, io, re, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
K1 = u'印面表格必帶分隔行'
K2 = u'印面標題不無端跨級'
A = u'六閘門是給審理者的詳圖'       # 印面（第三章）
B = u'### 第一節　歷史現場與立法本懷'   # 印面（第一章章首之節題）
C = u'母數 13,355 行（本條入檔另計）。'  # 底冊（附錄M）
TAB = u'\n\n| 植甲 | 植乙 |\n| 丙 | 丁 |'      # 無分隔行之假表
HEAD = u'\n##### 植碼跨兩級'                  # H3→H5 之跨級


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).read().hexdigest() if False else hashlib.sha256(t.encode('utf-8')).hexdigest()


def measure():
    out = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                         capture_output=True).stdout.decode('utf-8', 'replace')
    g = {}
    for k in (K1, K2):
        m = re.search(u'^(PASS|FAIL)\\s*' + k + u'.*$', out, re.M)
        g[k] = m.group(0)[:118] if m else u'（未見此檢！）'
    return g


orig = io.open(BOOK, encoding='utf-8').read()
for s in (A, B, C):
    assert orig.count(s) == 1, u'錨點命中 %d，未動檔' % orig.count(s)
h0 = sha(orig)
g = measure()
print(u'基態｜%s' % g[K1])
print(u'基態｜%s' % g[K2])
for tag, anchor, extra, key in (
        (u'甲 印面植無分隔之表', A, TAB, K1),
        (u'乙 印面植跨兩級之題', B, HEAD, K2),
        (u'丙 底冊植無分隔之表', C, TAB, K1),
        (u'丁 底冊植跨兩級之題', C, HEAD, K2)):
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(anchor, anchor + extra))
    print(u'%s → %s' % (tag, measure()[key]))
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    print(u'    還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
print(u'終態==初態：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
