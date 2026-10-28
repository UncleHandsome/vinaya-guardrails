# -*- coding: utf-8 -*-
r"""290 補・帳之自清：日誌還 CRLF、索引去重、狀態檔覆核。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
b = io.open(D, 'rb').read()
print(u'修復前：CRLF %d｜LF %d' % (b.count(b'\r\n'), b.count(b'\n')))
t = b.decode('utf-8').replace('\r\n', '\n')          # 一律先歸 LF
out = t.replace('\n', '\r\n').encode('utf-8')        # 一次轉 CRLF（單地換行）
io.open(D, 'wb').write(out)
b2 = io.open(D, 'rb').read()
print(u'修復後：CRLF %d｜LF %d｜CR %d｜裸 CR %d' % (b2.count(b'\r\n'), b2.count(b'\n'),
      b2.count(b'\r'), b2.count(b'\r') - b2.count(b'\r\n')))
L = b2.decode('utf-8').split('\r\n')
print(u'日誌：%d 行｜尾：%s' % (len(L), L[-2][:104]))

MEM = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory'
Q = io.open(os.path.join(MEM, u'MEMORY.md'), encoding='utf-8').read()
A = u'大綱 146＝目錄 146・大綱 146＝目錄 146・9pt 以下 0 段'
assert Q.count(A) == 1, u'重覆錨：%d' % Q.count(A)
Q = Q.replace(A, u'大綱 146＝目錄 146・9pt 以下 0 段')
B = u'。印面：262 頁・五量全中。290 收外路第十七報告'
if Q.count(B) == 1:
    Q = Q.replace(B, u'。290 收外路第十七報告')
io.open(os.path.join(MEM, u'MEMORY.md'), 'wb').write(Q.encode('utf-8'))
print(u'索引：重覆已除（殘 %d）' % Q.count(u'大綱 146＝目錄 146・大綱'))

P = io.open(os.path.join(MEM, u'project-round31-state.md'), encoding='utf-8').read()
import re
dups = [m.group(0) for m in re.finditer(u'(\S{6,24})\1', P)]
print(u'狀態檔疑似重覆：%s' % (dups[:3] or u'無'))
i = P.find(u'積輪 0（290 奉令重建')
print(u'狀態檔印面句：%s' % P[i:i + 96])
