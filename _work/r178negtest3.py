# -*- coding: utf-8 -*-
# 第 178 輪負測丙：新入單之 15 簡形須『植之能報』（前測植錯字，故重做），並證基態仍淨。
import hashlib, io, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
A = u'六閘門是給審理者的詳圖'
PLANTS = [(u'甲 植『码』', u'——植碼码'),
          (u'乙 植『图』', u'——植圖图'),
          (u'丙 植『语』', u'——植語语')]
orig = io.open(BOOK, encoding='utf-8').read()
assert orig.count(A) == 1
h0 = hashlib.sha256(io.open(BOOK, 'rb').read()).hexdigest()


def rc():
    return subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode


print(u'基態 rc=%d（須 0）' % rc())
for tag, add in PLANTS:
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(A, A + add))
    r = rc()
    rep = io.open(u'_work/check.txt', encoding='utf-8').read()
    got = [c for c in u'码图语' if c in rep]
    print(u'%s → rc=%d（須非零）｜報中所含：%s' % (tag, r, got))
    io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
    assert hashlib.sha256(io.open(BOOK, 'rb').read()).hexdigest() == h0, u'還原失敗'
print(u'終態 rc=%d｜雜湊已復原：%s' % (rc(), hashlib.sha256(io.open(BOOK, 'rb').read()).hexdigest() == h0))
