# -*- coding: utf-8 -*-
"""第 225 輪新軸 r225toc 之負測（留檔）：五路分擊其口徑，各中其目。
   主檔唯讀——TKSRC 指副本、用完即除，並斷主檔哈希前後相同（第 223 輪之誡：植病之測不得染主檔）。
   另測其尺之寬嚴兩向：款級 H4 不校（勿報）、目錄加括註而異形（勿報）——免於『一致性』一刀切。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r225neg.md'
raw = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
BASE = raw.split(NL)

PTR = u'  * 【章末指針：從公堂急診，走向自心免疫】'
SEC1_1 = u'  * 第一節　歷史現場與立法本懷（迦蘭陀村跌倒、十句義五維結構、樹幹判準「汝以何心」）'
H4 = u'#### 附設・憑空之款（負測③所用）'


def run(lines, want_rc, wants, tag):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = NEW
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_work/r225toc.py'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    ok = rc == want_rc and all(w in out for w in wants)
    if want_rc == 0:
        ok = ok and (u'目不屬' not in out and u'未列' not in out)
    print(u'%-38s rc=%d（期 %d）%s｜%s' % (tag, rc, want_rc, u'中' if ok else u'不中',
                                          out.strip().split(NL)[-1][:76]))
    return ok


cases = []
cases.append(run(list(BASE), 0, [u'病 0 處'], u'⓪ 自建淨本（陰性基準）'))

a = list(BASE)
ia = a.index(PTR)
ib = a.index(u'* **第一章　立法本懷與八大正理**')
del a[ia]
a.insert(ib + 1, PTR)                      # 移掛第一章末：該條既不在第五章亦非第一章之節
cases.append(run(a, 1, [u'目不屬其所掛之單元', u'單元內有題而目錄未列'],
                 u'① 移條至他章（當報雙面・中其目）'))

b = list(BASE)
b.remove(SEC1_1)                           # 刪一條目：印面有其節而目錄不列
cases.append(run(b, 1, [u'單元內有題而目錄未列', u'歷史現場與立法本懷'],
                 u'② 削一目（當報『有題未列』）'))

c = list(BASE)
ic = c.index(u'# 第二章　樹根與枝幹：根本心與六大領域')
c.insert(ic + 2, H4)                       # 款級 H4 不入目錄，乃其體
cases.append(run(c, 0, [u'病 0 處'], u'③ 新增款級 H4（口徑不校・勿報）'))

d = list(BASE)
id_ = d.index(SEC1_1)
d[id_] = SEC1_1 + u'（另加括註之異形）'      # 目錄加尾註，前綴配對應仍相容
cases.append(run(d, 0, [u'病 0 處'], u'④ 目錄添括註異形（前綴相容・勿報）'))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                               u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（五路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
