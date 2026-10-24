# -*- coding: utf-8 -*-
"""273 輪・印面覆核器（`r273face.py`）之負測：證其四量真有牙，非以 rc=0 自賣。

兩道（各證一枝）：① **移大綱一條於不載其題之頁** → 甲須報『未中 1』並點名該題，退 1；
                  ② **冊首插一空白頁**（頁腳遂全體偏移一格）→ 乙須報『不合 ≥1』，退 1。
判式：**因判決而紅，非因崩而紅**——stderr 必空・目數（甲＋乙＋丙＋丁之四行）必俱在。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r273faceneg.py
"""
import io
import os
import subprocess
import sys
import tempfile

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
SRC = os.path.join(ROOT, u'_print', max([q for q in os.listdir(os.path.join(ROOT, u'_print'))
                                         if q.startswith(u'ver39') and q.endswith(u'.pdf')
                                         and u'\u5217\u5370' in q], key=len))
assert len(os.path.basename(SRC)) > 30, u'SRC 非交付檔（中介檔名短）：' + SRC
TMP = tempfile.mkdtemp(prefix=u'r273faceneg_')
NEG = os.path.join(WORK, u'r273face.py')
rows = []
made = []
try:
    # ── 道一・移靶
    d = pymupdf.open(SRC)
    toc = d.get_toc()
    texts = [u''.join(d[i].get_text().split()) for i in range(d.page_count)]
    idx = next(i for i in range(len(toc) - 1, 0, -1)
               if toc[i][1].replace(u' ', u'')[:12] not in texts[0])
    new = [[lv, ti, (1 if i == idx else pg)] for i, (lv, ti, pg) in enumerate(toc)]
    d.set_toc(new)
    p1 = os.path.join(TMP, u'wrong_target.pdf')
    d.save(p1, garbage=3, deflate=True)
    d.close()
    made.append(p1)
    # ── 道二・冊首插空白頁（頁腳盡偏移）
    d = pymupdf.open(SRC)
    d.new_page(pno=0, width=595, height=842)
    p2 = os.path.join(TMP, u'shifted_footer.pdf')
    d.save(p2, garbage=3, deflate=True)
    d.close()
    made.append(p2)

    for tag, pdf, want, key in [(u'\u79fb\u9776', p1, u'未中', u'甲'),
                                (u'\u504f\u9801', p2, u'不合', u'乙')]:
        q = subprocess.run([sys.executable, u'-X', u'utf8', NEG, u'\u5217\u5370', pdf],
                           capture_output=True, text=True, encoding=u'utf-8', env=env, cwd=ROOT)
        out = (q.stdout or u'').rstrip()
        line = [l for l in out.split(u'\n') if l[:1] == key and l[1:2] in (" ", u'\u30fb')]
        named = [l for l in out.split(u'\n') if u'\u2717' in l and tag == u'\u79fb\u9776']
        ok = (q.returncode == 1 and not (q.stderr or u'').strip() and len(out.split(u'\n')) >= 6
              and bool(line) and want in line[0])
        rows.append((tag, want, q.returncode, ok, (line[0][:78] if line else u'\uff08\u7121\u6b64\u884c\uff09'),
                     (named[0][:70] if named else u'\uff08\u672a\u9ede\u540d\uff09'),
                     (q.stderr or u'').strip()[:90]))
finally:
    for f in made:
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(TMP)
    except OSError:
        pass

for tag, want, rc, ok, line, named, err in rows:
    print(u'%-4s \u671f\u300e%s\u300f\u6709\u6578\uff5c\u5be6\u9000 %d・%s' % (tag, want, rc, u'\u2713' if ok else u'\u2717'))
    print(u'      %s' % line)
    print(u'      %s' % named)
    if err:
        print(u'      stderr\uff5c%s' % err)
all_ok = all(r[3] for r in rows)
print(u'———— \u8ca0\u6e2c\u5169\u9053\uff5c%s' % (u'\u4ff1\u5982\u6240\u671f' if all_ok else u'\u6709\u4e0d\u5982\u671f'))
sys.exit(0 if all_ok else 1)
