# -*- coding: utf-8 -*-
"""284・清場（一）：列舉候刪之暫存檔，逐檔印【大小・是否被腳本引用・是否已入庫・日誌有無提及】。
   本器只報不刪。"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, u'_work')

CAND = [u'_a.txt', u'_b.txt', u'_e3.txt', u'_e4.txt', u'_u.txt', u'_v.txt', u'_w.txt', u'_z.txt',
        u'_zw.txt', u'_zz.txt', u'_neg39.md', u'_r204base.md', u'_r224neg.md', u'_r226neg.md',
        u'_r227neg.md', u'_case_remap.json', u'_topics.txt', u'_axes.txt', u'_tmp270.py',
        u'_tmp_clean2.py', u'_tmp_tocpair.py', u'_tmp_tocprobe.py', u'appendix_jieben.md',
        u'appxd74.txt', u'appxtag89.txt', u'b.log', u'sig_map.py']
CAND += [f for f in sorted(os.listdir(W)) if f.startswith(u'ver39.pre') and f.endswith(u'.md')]

py = [os.path.join(W, f) for f in os.listdir(W) if f.endswith(u'.py')]
py += [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.endswith(u'.md')]
py += [os.path.join(ROOT, u'_print', f) for f in os.listdir(os.path.join(ROOT, u'_print'))
       if f.endswith(u'.py')]
TXTS = {}
for p in py:
    try:
        TXTS[p] = io.open(p, encoding=u'utf-8-sig', errors=u'ignore').read()
    except OSError:
        TXTS[p] = u''
LOG = io.open(os.path.join(ROOT, u'_archive', u'編年工程日誌.md'), encoding=u'utf-8-sig',
              errors=u'ignore').read()
tracked = set(subprocess.run([u'git', u'ls-files', u'--', u'_work'], capture_output=True,
                             text=True, cwd=ROOT).stdout.split(u'\n'))

print(u'%-26s %10s %8s %8s %10s' % (u'檔案', u'大小 B', u'引用', u'入庫', u'日誌'))
for f in CAND:
    p = os.path.join(W, f)
    if not os.path.exists(p):
        print(u'%-26s  （不存在）' % f)
        continue
    refs = [k for k, v in TXTS.items() if f in v]
    print(u'%-26s %10d %8s %8s %10s  %s' % (f, os.path.getsize(p), len(refs),
                                             (u'_work/' + f) in tracked, f in LOG,
                                             (u'← ' + os.path.basename(refs[0])) if refs else u''))
