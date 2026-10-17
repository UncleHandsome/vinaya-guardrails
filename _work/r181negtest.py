# -*- coding: utf-8 -*-
# 第 181 輪·批一之負測：把本輪所治之原病**同位植回副本**（不增不刪行），`_work/r180voice.py` 須逐目報起——
# 證『歸零非消音』（173 輪之誡：新閘必以原病回植證其能報）。副本跑畢即刪，主檔不動。
import io
import os
import re
import subprocess
import sys

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/_r181neg.md'

NEW_JIAN = u'其名目以第二章第一節『三級心智標籤深描梯隊』為準。'
OLD_JIAN = u'其名目以第二章第一節『三級心智標籤深描梯隊』為準，此處不重列。'
NEW_BING = (u'（此從寬則依正理七『步步留生路』而立〔◈本書法式·現代治理指針〕：'
            u'若坦白者反負全數重坐，便是制度親手獎勵隱瞞）')
OLD_BING = (u'（此亦本書依正理七『步步留生路』與本款『護念主動發露之良知』所立之從寬則，'
            u'標〔◈本書法式·現代治理指針〕——蓋若坦白者反負全數重坐，便是制度親手獎勵隱瞞）')
NEW_JIA = (u'當庭以六句反問顧左右而言他，答非所問以圖規避；復故作起臥不應機以觸惱大眾——'
           u'喚來不來、應起不起、應語不語，終且拒不懺悔。其如是折騰於程序之間各結何罪，判見下面『佛陀處斷』欄。')
OLD_JIA = (u'當庭以六句反問顧左右而言他，謂僧未作白前盡突吉羅、作白已則盡波逸提；'
           u'復故作起臥不應機以觸惱大眾，謂喚來不來、應起不起、應語不語，未白突吉羅、白竟波逸提；'
           u'此二乃同一戒之初制餘語、二制觸惱，後更拒不懺悔。')
NEW_GENG = u'次乃名目之序，非閘門一至六之行程'
OLD_GENG = u'次乃行程之目，非閘門一至六之名'

t = io.open(MASTER, encoding=u'utf-8').read()
n0 = len(t.split(u'\n'))
swaps = [(NEW_JIAN, OLD_JIAN), (NEW_BING, OLD_BING), (NEW_JIA, OLD_JIA), (NEW_GENG, OLD_GENG)]
for a, b in swaps:
    assert t.count(a) == 1, u'新形錨非恰一：%s' % a[:26]
    t = t.replace(a, b, 1)
# 縮排三處植回（行級操作，行數不動）
lines = t.split(u'\n')
for pref, back in [(u'* **正理綁定之準據**', u'   ' + u'* **正理綁定之準據**'),
                   (u'* **監督揭弊自始不構成破僧', u'   ' + u'* **監督揭弊自始不構成破僧'),
                   (u'     遇上述排除情形，僧團暫緩滅擯宣告', u'  ' + u'遇上述排除情形，僧團暫緩滅擯宣告')]:
    hit = [i for i, l in enumerate(lines) if l.startswith(pref)]
    assert len(hit) == 1, u'植縮排不中：%s → %s' % (pref[:18], hit)
    i = hit[0]
    rest = lines[i][len(pref):]
    lines[i] = back + rest
t = u'\n'.join(lines)
assert t.count(u'   * **正理綁定之準據**') == 1 and t.count(u'   * **監督揭弊自始不構成破僧') == 1 \
    and t.count(u'  遇上述排除情形，僧團暫緩滅擯宣告') == 1, u'植縮排未生效'
assert len(t.split(u'\n')) == n0, u'植病誤增刪行'


io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(t)

env = dict(os.environ)
env[u'PYTHONIOENCODING'] = u'utf-8'
p = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py', COP],
                   capture_output=True, text=True, encoding=u'utf-8', env=env)
out = p.stdout


def grab(key):
    m = re.search(key + u'[：:]? ?(\\d+)', out)
    return int(m.group(1)) if m else -1


res = {u'甲': grab(u'甲·事相欄混量刑科判'), u'丙': grab(u'丙·段末長辯護括註（≥60 字）'),
       u'壬': grab(u'壬·列項有領無續'), u'子': grab(u'子·標記行之野縮排')}
ding = re.search(u'丁·元語言：(\\d+) 見', out)
geng = re.search(u'既有交代句之形：\\[?([^｜\\]]*)\\]?', out)
os.remove(COP)
print(out[:1200])
ok = (res[u'甲'] == 1 and res[u'丙'] == 1 and res[u'壬'] == 1 and res[u'子'] == 2
      and int(ding.group(1)) >= 18 and u'名目之序' not in (geng.group(1) if geng else u''))
print(u'植病所得：甲 %d（須 1）｜丙 %d（須 1）｜壬 %d（須 1）｜子 %d（須 2）｜丁 %s（須 ≥18）｜庚交代句形 %r（須不含名目之序）' % (
    res[u'甲'], res[u'丙'], res[u'壬'], res[u'子'],
    ding.group(1) if ding else u'?', geng.group(1) if geng else u'?'))
# 副本跑畢，清冊須以主檔重掃（OUT 檔乃共用落點，勿留副本之報）
subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py'],
               capture_output=True, text=True, encoding=u'utf-8', env=env)
print(u'今制（主檔）：甲 0／丙 0／壬 0／子 0／丁 17／庚有交代——植病俱起，故歸零乃實測非消音。%s' % (
    u'負測俱中' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)

