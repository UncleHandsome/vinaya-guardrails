# -*- coding: utf-8 -*-
# 第 177 輪負測：不變量 82（四制括號各司其形）須三植有牙、底冊不報，植畢還原核雜湊。
import hashlib, io, re, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
K = u'印面四制括號各司其形'
A = u'六閘門是給審理者的詳圖'          # 印面（第三章）
B = u'母數 13,355 行（本條入檔另計）。'  # 底冊（附錄M）


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def measure():
    out = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                         capture_output=True).stdout.decode('utf-8', 'replace')
    m = re.search(u'^(PASS|FAIL)\\s*' + K + u'.*$', out, re.M)
    return m.group(0)[:118] if m else u'（未見此檢！）'


orig = io.open(BOOK, encoding='utf-8').read()
for s in (A, B):
    assert orig.count(s) == 1, u'錨點命中 %d，未動檔' % orig.count(s)
h0 = sha(orig)
print(u'基態｜%s' % measure())
for tag, anchor, extra in ((u'甲 印面植問序六角', A, u'（植碼：第〔7〕問）'),
                           (u'乙 底冊植問序六角', B, u'（植碼：第〔8〕問）'),
                           (u'丙 印面植案號半形', A, u'（植碼：[遮9]）')):
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(anchor, anchor + extra))
    print(u'%s → %s' % (tag, measure()))
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    print(u'    還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
print(u'終態==初態：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
