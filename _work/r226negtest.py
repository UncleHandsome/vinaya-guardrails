# -*- coding: utf-8 -*-
"""第 226 輪新軸 r226pair／r226tree／r226simp 之負測（留檔）：十二路分擊其口徑，各中其目。
   主檔唯讀——TKSRC 指副本、用完即除，並斷主檔哈希前後相同（第 223 輪之誡：植病之測不得染主檔）。
   另立陰性對照：⑦ 第七章土壤添修辭而兩翼俱存（勿報）；⑨ 同形圍以『』屬照錄（勿報）；ⓠⓡⓢ 淨本自建基準。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r226neg.md'
raw = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
BASE = raw.split(NL)

PAIR = u'_work/r226pair.py'
TREE = u'_work/r226tree.py'

SLOW = u'**第七組「慢 ╳ 增上慢」（慢分）**'
SWING = u'、**第三組之嫉妬分**與**第八組「貪 ╳ 恚」（恚分）**。'
SGNUM = u'**第九組「自譽 ╳ 毀他」**'
SLEAF = u'、有難教、不受訓導、自譽、毀他、增上慢——'
SOIL2 = u'* **土壤（環境母體）**：結界管轄之清淨法權空間與世間信心（正理二）。若無法權之淨與世間之信，整座叢林失去立足之本；'
SLEAF_OLD = SOIL2
SLAYER = u'* **果實（解脫歸宿）**'
SDEEP = u'   由**結界管轄權（清淨法權空間）**與**世間信心防火牆（社會信任土壤）**共同構成。'


def run(lines, axis, want_rc, wants, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = NEW
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', axis],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    ok = rc == want_rc and all(w in out for w in wants)
    if clean:                                   # 陰性路：計數須報零（病 0 處／簡形 0 處）
        ok = ok and (u'0 處' in out)
    print(u'%-40s %-14s rc=%d（期 %d）%s' % (tag, os.path.basename(axis), rc, want_rc,
                                             u'中' if ok else u'不中'))
    if not ok:
        for l in out.strip().split(NL)[-4:]:
            print(u'      · %s' % l[:110])
    return ok


def swap(old, new):
    a = list(BASE)
    hits = [i for i, l in enumerate(a) if old in l]
    assert len(hits) == 1, u'植病之錨非恰一：%s（%d 見）' % (old[:24], len(hits))
    a[hits[0]] = a[hits[0]].replace(old, new, 1)
    return a


cases = []
cases.append(run(list(BASE), PAIR, 0, [u'病 0 處'], u'ⓠ 淨本·對位閉環', clean=True))
cases.append(run(list(BASE), TREE, 0, [u'病 0 處'], u'ⓡ 淨本·七層', clean=True))
cases.append(run(swap(SLOW, u'**第七組「慢 ╳ 增上慢」**'), PAIR, 1,
                 [u'重報'], u'① 去慢分之標（一組兩款全認）'))
cases.append(run(swap(SWING, u'與**第三組之嫉妬分**。'), PAIR, 1,
                 [u'分未齊'], u'② 去恚分之認（一翼無主）'))
cases.append(run(swap(SGNUM, SGNUM.replace(u'九', u'八')), PAIR, 1,
                 [u'組序與組名不符'], u'③ 誤標組序（九作八）'))
cases.append(run(swap(SLEAF, u'、不受訓導——'), PAIR, 1,
                 [u'雙層有遺法'], u'④ 雙層遺五法（底枝不覆）'))
cases.append(run(swap(SOIL2, SLEAF_OLD.replace(u'結界管轄之清淨法權空間與世間信心（正理二）',
                                               u'世間信心與護生不害（正理二、正理三）')), TREE, 1,
                 [u'無『結界』'], u'⑤ 土壤還從舊說（翼異即報）'))
cases.append(run(swap(SLAYER, u'* **菩提（解脫歸宿）**'), TREE, 1,
                 [u'非七層之名', u'層序不合'], u'⑥ 層名改果實為菩提'))
cases.append(run(swap(SDEEP, SDEEP.replace(u'共同構成。', u'共同構成——此即大樹立錐之地、萬目所注。')),
                 TREE, 0, [u'病 0 處'], u'⑦ 深描添修辭而兩翼俱存（勿報）', clean=True))

REC = u'225. **第兩百二十五輪（'
SIMP = u'_work/r226simp.py'
cases.append(run(list(BASE), SIMP, 0, [u'簡形 0 處'], u'ⓢ 淨本·底冊簡形', clean=True))
cases.append(run(swap(REC, REC + u'处'), SIMP, 1, [u'落『处』形'],
                 u'⑧ 底冊植一枚簡形（名單外亦須逮）'))
cases.append(run(swap(REC, REC + u'『处』'), SIMP, 0, [u'簡形 0 處'],
                 u'⑨ 同形圍以『』（照錄之豁免・勿報）', clean=True))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                               u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（十二路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
