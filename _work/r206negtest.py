# -*- coding: utf-8 -*-
# 第 206 輪·負測：閘之第四形（編序跳脫括號）須有牙。
#  ① 印面植『\(1\)』⇒ 該閘須 FAIL 且退 1；
#  ② 同形植於圍欄之內 ⇒ 從寬不報（證其界，非一刀切）；
#  ③ 主檔現形 ⇒ 不報退 0（陰性對照）；末以哈希自證主檔一字未損。
import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
orig = io.open(MD, encoding=u'utf-8').read()
h0 = hashlib.sha256(orig.encode(u'utf-8')).hexdigest()
L = orig.split(u'\n')
BS = chr(92)
NAME = u'印面四制括號各司其形'
K = next(i for i in range(len(L)) if L[i].strip().startswith(u'（1） 被出罪者本人'))
J = next(i for i in range(len(L)) if L[i].strip() == u'```text')


def write(lines):
    io.open(MD, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))


def check():
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                       capture_output=True, text=True, encoding=u'utf-8', errors='replace')
    txt = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    fail = [l for l in txt.split(u'\n') if l.startswith(u'FAIL') and NAME in l]
    return q.returncode, fail


res = []
try:
    # ⓪ 先測樣本（零命中之綠燈最險——先證閘之正則能中理想病形，再談植病）
    import re
    rx = re.compile(r'\\\(\d{1,2}\\\)')
    pre = bool(rx.search(BS + u'(7' + BS + u')')) and not rx.search(u'（7）')
    print(u'  ⓪ 樣本自測：正則中『\(7\)』且不中全形『（7）』：%s' % (u'中' if pre else u'不中'))
    if not pre:
        print(u'     └ 樣本不中：閘之正則本身失牙，須先修尺')
    res.append((u'⓪ 正則樣本自測', pre, []))

    a = list(L)
    a[K] = a[K].replace(u'（1）', BS + u'(1' + BS + u')', 1)
    assert a[K] != L[K] and (BS + u'(1' + BS + u')') in a[K], u'植形未成'
    write(a)
    rc, fail = check()
    res.append((u'① 印面植跳脫編序', bool(fail) and rc == 1, fail[:1]))

    b = list(L)
    b.insert(J + 1, BS + u'(9' + BS + u') 圍欄內之測試行')          # J 乃首個 ```text 起欄行，其下一行必在圍欄之內
    write(b)
    rc, fail = check()
    res.append((u'② 同形落圍欄（須不報此形）', not fail, fail[:1]))

    write(L)
    rc, fail = check()
    res.append((u'③ 現形（須不報退 0）', (not fail) and rc == 0, fail[:1]))
finally:
    write(L)
    back = io.open(MD, encoding=u'utf-8').read()
    h1 = hashlib.sha256(back.encode(u'utf-8')).hexdigest()

for nm, okv, ex in res:
    print(u'  %-26s %s%s' % (nm, u'中' if okv else u'不中', (u'｜' + ex[0][:56]) if ex else u''))
same = (h0 == h1)
print(u'復原自證：主檔哈希 %s（%s）' % (u'如舊' if same else u'已臟！', h0[:12]))
ok = len(res) == 4 and all(x[1] for x in res) and same
print(u'結果斷：%s' % (u'第四形有牙、圍欄從寬、主檔一字未損' if ok else u'負測不合'))
sys.exit(0 if ok else 1)
