# -*- coding: utf-8 -*-
"""一次性・移正本同層之備份檔入 _archive/備份/護欄/（2026-10-27 奉令）。
手法：逐名列檔（不前綴通配）、目標層同名者先報不撞、MoveFile 後回核（源無・得有）。
用法：python -X utf8 _work/mvbak71.py [--go]
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hulan_path as HP

GO = u"--go" in sys.argv
DRY = not GO
root = HP.ROOT
dst = HP.BACKUP
names = sorted(f for f in os.listdir(root)
               if os.path.isfile(os.path.join(root, f)) and u".bak" in f and f.startswith(HP.PREFIX))
other = sorted(f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and u".bak" in f
               and not f.startswith(HP.PREFIX))
print(u"目標層：%s" % dst)
print(u"  碼位：%s" % u" ".join(u"U+%04X" % ord(c) for c in dst.replace(root, u"")))
print(u"正本同層之備份：%d 枚｜異類（不動）：%d 枚 %s" % (len(names), len(other), other))
assert not other, u"根目錄有別冊之備份檔，須另處置之，本器不碰"
if not os.path.isdir(dst):
    print(u"  目標層未存，創之")
    if not DRY:
        os.makedirs(dst)
clash = [f for f in names if os.path.exists(os.path.join(dst, f))]
assert not clash, u"目標層已有同名者 %d 枚：%s" % (len(clash), clash[:4])
for f in names:
    print(u"  ○ %s（%d B）" % (f, os.path.getsize(os.path.join(root, f))))
if DRY:
    print(u"（乾跑：加 --go 始移）")
    sys.exit(0)
for f in names:
    a, b = os.path.join(root, f), os.path.join(dst, f)
    h = io.open(a, encoding="utf-8", newline=u"").read()
    os.rename(a, b)
    assert not os.path.exists(a) and os.path.exists(b), u"移而不成：%s" % f
    assert io.open(b, encoding="utf-8", newline=u"").read() == h, u"移後内容異：%s" % f
print(u"已移 %d 枚｜正本同層現存 .bak：%d 枚" % (
    len(names), len([f for f in os.listdir(root) if u".bak" in f])))
print(u"目標層今存：%d 枚" % len(os.listdir(dst)))
