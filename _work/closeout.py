# -*- coding: utf-8 -*-
# 結帳之一行器（第 223 輪起）：逐器執行並各取其 rc，任一非零即列名退 1。
#   所以立之：第 223 輪把『三掃俱淨』寫進校勘記時，recglue 其實尚在報病——
#   預寫之宣稱即未測之宣稱。凡跑此器，先測後寫。
#   `_tk.py check` 之細報取其 emit 檔 `_work/check.txt`，勿以 stdout 覆寫之。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/closeout.py [--brief]
import io
import os
import subprocess
import sys

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
# 第 225 輪之序改：先跑『自癒之器』（內含寫檔之軸與 ledger --go），再跑『只讀之器』。
#   所以：第 225 輪改動印面引號後，附錄L 之自算列須由軸重寫；當時 `_tk check` 跑在 battery 之前，
#   先見舊列而報 FAIL 1，battery 一過則自癒，再跑即 92/92——**讀檔之器跑在寫檔之器前，必假報**。
PRE = [
    (u'battery', [u'_work/battery.py']),
    (u'ledger', [u'_work/ledger.py', u'--go']),
]
JOBS = [
    (u'_tk check', [u'_tk.py', u'check']),
    (u'verify_audit', [u'verify_audit.py']),
    (u'syncchk', [u'_work/syncchk.py']),
    (u'recordsimp', [u'_work/recordsimp.py', u'scan']),
    (u'memsimp', [u'_work/memsimp.py']),
    (u'recglue', [u'_work/recglue.py']),
]
WRITE_GO = {u'--go', u'-w', u'--write', u'--apply'}

# 植病之測須走 TKSRC 副本，而結帳諸器含寫檔者（ledger --go 會把副本之文寫回真主檔，第 223 輪之害；
# 諸軸中亦有寫檔之器，未必帶旗標）——故凡 TKSRC 在環境中：自癒之器整批 skip，只讀之器去其寫檔旗標。
_tk = os.environ.get(u'TKSRC')
RUN = list(PRE) + list(JOBS)
if _tk:
    RUN = [(t, [a for a in args if a not in WRITE_GO]) for t, args in JOBS]
    print(u'⚠ TKSRC=%s（副本之測）——自癒之器（battery／ledger）整批略過，寫檔旗標俱去' % _tk)


def key_line(tag, out):
    if tag == u'_tk check':
        chk = io.open(os.path.join(ROOT, u'_work', u'check.txt'), encoding=u'utf-8').read()
        cl = [l for l in chk.split(NL) if l.strip()]
        bad = [l for l in cl if l.startswith(u'FAIL')]
        return u'PASS %d｜FAIL %d' % (len([l for l in cl if l.startswith(u'PASS')]), len(bad)), bad
    ls = [l for l in out.split(NL) if l.strip()]
    for pat in (u'結果', u'跑畢', u'差異', u'合計', u'不變量'):
        for l in reversed(ls):
            if pat in l:
                return l.strip(), []
    return (ls[-1].strip() if ls else u'（無輸出）'), []


os.chdir(ROOT)
fails = []
for tag, args in RUN:
    p = subprocess.Popen([PY, u'-X', u'utf8'] + args,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    line, bads = key_line(tag, out)
    flag = u'ok' if p.returncode == 0 and not bads else u'BAD'
    print(u'%-13s rc=%d %s｜%s' % (tag, p.returncode, flag, line[:88]))
    if flag == u'BAD':
        fails.append(tag)
        if u'--brief' not in sys.argv:
            for b in bads[:8]:
                print(u'   ✗ ' + b[:120])
            for l in [x for x in out.split(NL) if x.strip()][-6:]:
                print(u'   · ' + l[:120])
print(u'結帳：%s' % (u'諸器俱綠' if not fails else u'非零者——' + u'、'.join(fails)))
sys.exit(0 if not fails else 1)
