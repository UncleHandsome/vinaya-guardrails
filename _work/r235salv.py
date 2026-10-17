# -*- coding: utf-8 -*-
"""第 235 輪自救：重建被誤截之 `_work/readchk.py`。
   三源拼合——今檔首 129 行（未傷）＋235 碼內註（未傷）＋233 塊（取自本輪 Read 之原始輸出）
   ＋碼體 294 行（取自 Qoder 檔史 403 行版之 L110..end，行數與首尾俱合前帳）。
   成則以 `compile` 與『跑畢覆核 readchk.txt 一字不易』雙證之。"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, u'_work')
LIVE = os.path.join(W, 'readchk.py')
SNAP = os.path.join(W, u'_snap403.py')
OUT = os.path.join(W, u'_readout.txt')
TXT = os.path.join(W, 'readchk.txt')

live = io.open(LIVE, encoding='utf-8').read().split(u'\n')
snap = io.open(SNAP, encoding='utf-8').read().split(u'\n')
raw = io.open(OUT, encoding='utf-8').read().split(u'\n')

assert len(live) == 134, u'今檔 %d 行（須 134）' % len(live)
assert snap[109].rstrip() == u'"""', u'快照閉引號不在 L110：%r' % snap[109]

# 233 塊：Read 輸出中 130..134 五行，去其「行號\t」前綴
blk = []
for k in range(130, 135):
    hit = [l for l in raw if l.startswith(u'%d\t' % k)]
    assert len(hit) == 1, u'Read 輸出缺行 %d' % k
    blk.append(hit[0].split(u'\t', 1)[1])
assert blk[0].startswith(u'量訖而不立之維（第 233 輪'), u'塊首不合：%r' % blk[0][:24]
assert len(blk) == 5

note = live[129:134]                                    # 235 塊（含尾隨空行）
assert note[0].startswith(u'量訖而不立之維（第 235 輪'), u'235 塊位不合'
head = live[:129]
tail = snap[109:]                                       # 自 """ 起之碼體
recon = head + note + blk + tail

# 結構自證
for h in (u'218', u'219', u'220', u'221', u'222', u'229', u'230', u'231', u'232', u'234', u'235', u'233'):
    n = sum(1 for l in recon if l.startswith(u'量訖而不立之維（第 %s 輪' % h))
    assert n == 1, u'第 %s 輪之組見 %d 次（須恰一）' % (h, n)
assert recon[128].startswith(u' ③ **新增指針之副作用在證源之範圍**'), u'頭尾不合'
assert recon[133] == u'' and recon[134].startswith(u'量訖而不立之維（第 233 輪')
i3 = next(i for i, l in enumerate(recon) if l.rstrip() == u'"""')
assert recon[i3 + 1] == u'import io, os, re, sys', u'碼體起點不合：%r' % recon[i3 + 1]
assert recon[-2].startswith(u"print(u'written"), u'碼體終點不合：%r' % recon[-2]
compile(u'\n'.join(recon), 'readchk.py', 'exec')
print(u'拼合 ✓ %d 行・docstring 閉 L%d・compile 可編' % (len(recon), i3 + 1))

before = io.open(TXT, encoding='utf-8').read() if os.path.exists(TXT) else u''
io.open(LIVE, 'w', encoding='utf-8', newline=u'\n').write(u'\n'.join(recon))

env = dict(os.environ, PYTHONPATH=ROOT, PYTHONIOENCODING='utf-8')
r = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(u'_work', 'readchk.py')],
                   cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
print(u'複跑 rc=%d｜%s' % (r.returncode, (r.stdout or u'').strip()[:60]))
after = io.open(TXT, encoding='utf-8').read()
if before:
    same = before == after
    print(u'覆核輸出與傷前一字不易：%s（%d 行）' % (u'✓' if same else u'✗', len(after.split(u'\n'))))
    if not same:
        b, a = before.split(u'\n'), after.split(u'\n')
        for k in range(min(len(b), len(a))):
            if b[k] != a[k]:
                print(u'  首異 L%d 前=%r 後=%r' % (k + 1, b[k][:60], a[k][:60]))
                break
    sys.exit(0 if same else 1)
