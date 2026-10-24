# -*- coding: utf-8 -*-
"""284・清場（二）：逐名列檔——大塊快照與備檔『移』入 gitignore 之 _archive/備份/，0 byte 與一次性雜檔『刪』。
   先試跑印名（不動作），加 --apply 方動。禁用前綴通配（名單在檔，逐一核在否）。"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, u'_work')
DST = os.path.join(ROOT, u'_archive', u'備份')
APPLY = u'--apply' in sys.argv

MOVE = [u'_neg39.md', u'_r204base.md', u'_r224neg.md', u'_r226neg.md', u'_r227neg.md',
        u'ver39.pre278.md', u'ver39.pre278b.md', u'ver39.pre279.md', u'ver39.pre279b.md',
        u'ver39.pre280.md', u'ver39.pre281.md', u'ver39.pre281b.md', u'ver39.pre282.md',
        u'ver39.pre282b.md', u'ver39.pre283.md', u'ver39.pre284.md',
        u'r273mutant.pdf', u'r273diary.bak', u'r274swap.bak', u'r274toc.bak', u'r275toc.bak',
        u'r276verb3.bak', u'r276word.bak', u'r276word2.bak', u'r277fix.bak', u'r277fix2.bak',
        u'r277ladder.bak']
MOVE_ROOT = [u'_r219work.md']
DEL = [u'_a.txt', u'_b.txt', u'_e3.txt', u'_e4.txt', u'_u.txt', u'_v.txt', u'_w.txt', u'_z.txt',
       u'_zw.txt', u'_zz.txt', u'_tmp270.py', u'_tmp_clean2.py', u'_tmp_tocpair.py',
       u'_tmp_tocprobe.py', u'b.log']

moved = deleted = 0
mb = 0.0
if APPLY:
    if not os.path.isdir(DST):
        os.makedirs(DST)
for f in MOVE:
    p = os.path.join(W, f)
    if not os.path.exists(p):
        print(u'  移・不存在：%s' % f)
        continue
    sz = os.path.getsize(p)
    mb += sz / 1048576.0
    tgt = os.path.join(DST, f)
    if os.path.exists(tgt):
        print(u'  移・目標已存在，跳過：%s' % f)
        continue
    print(u'  移 %9d ➜ _archive/備份/%s' % (sz, f))
    if APPLY:
        shutil.move(p, tgt)
    moved += 1
for f in MOVE_ROOT:
    p = os.path.join(ROOT, f)
    if not os.path.exists(p):
        print(u'  移根・不存在：%s' % f)
        continue
    sz = os.path.getsize(p)
    mb += sz / 1048576.0
    tgt = os.path.join(DST, f)
    print(u'  移根 %9d ➜ _archive/備份/%s' % (sz, f))
    if APPLY and not os.path.exists(tgt):
        shutil.move(p, tgt)
    moved += 1
for f in DEL:
    p = os.path.join(W, f)
    if not os.path.exists(p):
        print(u'  刪・不存在：%s' % f)
        continue
    print(u'  刪 %9d  %s' % (os.path.getsize(p), f))
    if APPLY:
        os.remove(p)
    deleted += 1
print(u'—— 移 %d 檔・刪 %d 檔・讓出工作區 %.1f MB・%s' % (
    moved, deleted, mb, u'已落' if APPLY else u'試跑（未動）'))
