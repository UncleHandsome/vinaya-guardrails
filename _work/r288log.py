# -*- coding: utf-8 -*-
r"""288・日誌入帳：正哈希・掃簡形・併入編年日誌（寫檔換行只在一處）。"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
DIARY = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
PARA = os.path.join(ROOT, u'_work', u'r288para.txt')

sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402

BOOK_SHA = hashlib.sha256(io.open(BOOK, 'rb').read()
                          .replace(b'\r\n', b'\n')).hexdigest()[:12]
para = io.open(PARA, encoding='utf-8').read()
para = para.replace(u'cf60bb7d5f2c', BOOK_SHA)
print(u'哈希已正：今冊 sha256(LF) %s' % BOOK_SHA)

SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
book = io.open(BOOK, encoding='utf-8').read()
bad = sorted({c for c in para if c in SIMPS and c not in book})
print(u'簡形（冊中所無者）：%s' % (u''.join(bad) or u'無'))
for c in bad:
    j = para.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), para[max(0, j - 24):j + 18].replace(u'\n', u'')))

raw = io.open(DIARY, 'rb').read().decode('utf-8').replace('\r\n', '\n')
out = (raw.rstrip('\n') + '\n' + para).replace('\n', '\r\n').encode('utf-8')
io.open(DIARY, 'wb').write(out)
L = out.decode('utf-8').split('\r\n')
print(u'日誌：%d 行・%dB｜尾：%s' % (len(L), len(out), L[-4][:36]))
