# -*- coding: utf-8 -*-
# 第 207 輪·負測：兩條新不變量須有牙（⓪ 陰性對照・①② 分植・③ 圍欄從寬・④ 現形退 0），末以哈希自證。
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
N1 = u'印面標題末不帶句讀'
N2 = u'印面行末空白不是一枚'


def write(lines):
    io.open(MD, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))


def check():
    subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                   capture_output=True, text=True, encoding=u'utf-8', errors='replace')
    txt = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    fails = [l for l in txt.split(u'\n') if l.startswith(u'FAIL')]
    return fails


HI = next(i for i in range(len(L)) if L[i].startswith(u'##### '))
FJ = next(i for i in range(len(L)) if L[i].strip() == u'```text')
res = []
try:
    # ⓪ 陰性對照：兩枚行末空格乃合法硬換行，須不報（證閘只殺一枚，不误放行）
    b = list(L)
    k = next(i for i in range(len(b)) if b[i].startswith(u'> ') and not b[i].strip().endswith(u' '))
    b[k] = b[k] + u'  '
    write(b)
    f0 = check()
    res.append((u'⓪ 兩枚空格乃硬換行（須不報）', not any(N2 in x for x in f0), []))

    # ① 標題尾冒須報
    a = list(L)
    a[HI] = a[HI] + u'：'
    write(a)
    f = check()
    res.append((u'① 標題尾冒', any(N1 in x for x in f), []))

    # ② 行末一枚空格須報
    b = list(L)
    k = next(i for i in range(len(b)) if b[i].startswith(u'> ') and not b[i].strip().endswith(u' '))
    b[k] = b[k] + u' '
    write(b)
    f = check()
    res.append((u'② 行末一枚空格', any(N2 in x for x in f), []))

    # ③ 圍欄內之行末一枚空格須不報（從寬之界）
    c = list(L)
    c[FJ + 1] = c[FJ + 1] + u' '
    write(c)
    f = check()
    res.append((u'③ 同形落圍欄（須不報）', not any(N2 in x for x in f), []))

    # ④ 現形須全綠
    write(L)
    f = check()
    res.append((u'④ 現形退 0（全綠）', not f, f[:2]))
finally:
    write(L)
    h1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()

for nm, okv, ex in res:
    print(u'  %-26s %s%s' % (nm, u'中' if okv else u'不中', (u'｜' + str(ex)[:56]) if ex else u''))
same = h0 == h1
print(u'復原自證：主檔哈希 %s（%s）' % (u'如舊' if same else u'已臟！', h0[:12]))
ok = len(res) == 5 and all(x[1] for x in res) and same
print(u'結果斷：%s' % (u'兩閘俱有牙、圍欄從寬、主檔一字未損' if ok else u'負測不合'))
sys.exit(0 if ok else 1)
