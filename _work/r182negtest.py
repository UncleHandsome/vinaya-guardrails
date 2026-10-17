# -*- coding: utf-8 -*-
# 第 182 輪·批二之負測：把一处拆拍**同位還原為分號**（不增不刪行、不動一字），
# `_work/r180voice.py` 之乙目須報起（今制 3 → 植病 4），證『9 減為 3』乃實治而非尺寬。
# 另證本輪自犯之『粗體開符被吞』一病確由閘逮：植同款之落單粗體，不變量 80 須 FAIL 退 1，還原後雜湊同。
# 第 228 輪隨動：REVERTS 第二拍之字面舊作『構成世俗刑法之湮滅刑事證據罪』，該句今依第九章自制之式
# 歸一為『在世俗法上涉嫌構成湮滅證據罪』（漢字十四對十四、三拍之制不動），故其鍵隨文換形——負測之錨須從今文。
import hashlib
import io
import os
import re
import subprocess
import sys

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/_r182neg.md'
env = dict(os.environ)
env[u'PYTHONIOENCODING'] = u'utf-8'

t = io.open(MASTER, encoding=u'utf-8').read()
# 回植須**一次還原該句三拍**：本目之判為『括外分號 ≥3』，治後僅存二，单植一拍不會報起——
# 此非器之盲，而是『病已過閾』之實；負測若只植一拍而見零，即誤判器無牙（記之以戒）。
REVERTS = [(u'視同重罪之隱匿共犯。若有銷毀帳冊', u'視同重罪之隱匿共犯；若有銷毀帳冊'),
           (u'在世俗法上涉嫌構成湮滅證據罪。若以威脅、脅迫手段', u'在世俗法上涉嫌構成湮滅證據罪；若以威脅、脅迫手段'),
           (u'則另涉刑法強制罪或恐嚇罪。於出世律相上', u'則另涉刑法強制罪或恐嚇罪；於出世律相上')]
tc0 = t
for a, b in REVERTS:
    assert t.count(a) == 1 and t.count(b) == 0, u'回植錨不合：%s' % a[:24]
    t = t.replace(a, b, 1)
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(t)
p = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py', COP],
                   capture_output=True, text=True, encoding=u'utf-8', env=env)
m = re.search(u'乙·長句（≥100 字）標點嵌套：(\\d+)', p.stdout)
yi_plant = int(m.group(1)) if m else -1
os.remove(COP)
# 單拍之測：只還原一拍時應仍不報（证『過閾』之說，非器能報之證）
t1 = tc0.replace(REVERTS[0][0], REVERTS[0][1], 1)
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(t1)
p1 = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py', COP],
                    capture_output=True, text=True, encoding=u'utf-8', env=env)
m1 = re.search(u'乙·長句（≥100 字）標點嵌套：(\\d+)', p1.stdout)
yi_one = int(m1.group(1)) if m1 else -1
os.remove(COP)
# 復掃主檔以還原清冊（r180voice 之落點共用）
subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py'],
               capture_output=True, text=True, encoding=u'utf-8', env=env)
tc = tc0


raw = io.open(MASTER, 'rb').read()
h0 = hashlib.sha256(raw).hexdigest()
tc = raw.decode(u'utf-8')
GOOD = u'其前置條件唯為**客觀上確不可追**——經專業律師或會計師查核'
BAD = u'其前置條件唯為**客觀上確不可追——經專業律師或會計師查核'      # 吞一枚閉符＝本輪自犯之復刻
assert tc.count(GOOD) == 1
lines = tc.split(u'\n')
i = [k for k, l in enumerate(lines) if GOOD in l][0]
lines[i] = lines[i].replace(GOOD, BAD, 1)
assert lines[i].count(u'**') % 2 == 1, u'植形未成落單——器將無從可報'
io.open(MASTER, 'wb').write(u'\n'.join(lines).encode(u'utf-8'))
rc_plant = 1
hit = []
try:
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    rc_plant = q.returncode
    rep = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    hit = [x for x in rep.split(u'\n') if x.startswith(u'FAIL') and u'粗體記號' in x]
finally:
    io.open(MASTER, 'wb').write(raw)
h1 = hashlib.sha256(io.open(MASTER, 'rb').read()).hexdigest()

print(u'乙目：三拍俱回植 → %d（須 4）｜只回植一拍 → %d（須 3，證治後已過閾而非器無牙）' % (yi_plant, yi_one))
print(u'粗體落單：check rc=%d｜FAIL 報 %d（須 ≥1）｜%s' % (rc_plant, len(hit), hit[:1]))
print(u'還原：雜湊%s（須同）' % (u'相同' if h0 == h1 else u'不同！'))
ok = (yi_plant == 4 and yi_one == 3 and rc_plant == 1 and hit and h0 == h1)
print(u'結果斷：%s' % (u'三測俱中：回植能報、過閾不報（口徑如實）、落單閘能逮（本輪自犯即證）、主檔無損'
                       if ok else u'負測不合'))
sys.exit(0 if ok else 1)
