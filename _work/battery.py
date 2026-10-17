# -*- coding: utf-8 -*-
"""battery.py —— 諸軸跑批器（第 198 輪立）。單一法源＝`_work/_axes.txt`。

緣起：歷輪『全閘綠』之遍掃，其實是把數十個軸名**手打在指令裡**——名單不在檔，則新立之軸一旦忘了
補進我的指令，便永遠不會被跑到，而報告照樣寫『諸軸零病』。此即本專案屢記之『名單之外』敗因
（第 61／124／174／180 輪）在**工序層**的變種：**跑批的清單本身也是待驗之器**。

做兩件事：
 ① 逐軸跑 `_work/<軸>.py`（PYTHONPATH=. 供 `import _tk`），逐支**獨立取 rc**（178／179 之誡：
    勿以管線尾端之 rc 冒充，亦勿把 stdout 覆寫到該軸之 emit 檔）；有敗則列名並退 1。
 ② **防漏列**：凡 `_work/rNNN名.py` 而**檔首三行**自稱『待診』『長駐』『第 NNN 輪立』者，須在冊上；未列即點名退 1
    （新軸命名慣例如此，舊軸名不可枚舉，故只防『新加的軸沒進名單』這一向漂移。第 199 輪補『輪立』之記：
    升閘之軸不自稱待診，舊記號恰好漏網。**記號須取軸之自稱格式，不得取泛指之詞**——嘗兼認
    『升閘／專軸』，而記錄腳本之碼內註引及此二字便被誤點名，本輪自蹈一次，遂收為『輪立』。）

用法：
    PYTHONIOENCODING=utf-8 python -X utf8 _work/battery.py            # 全跑
    PYTHONIOENCODING=utf-8 python -X utf8 _work/battery.py --list     # 只列冊與漂移檢查
退出碼：任一軸退非 0，或有未列之軸 → 1；否則 0。
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REG = os.path.join(u'_work', u'_axes.txt')
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

raw = [l.split(u'#')[0].strip() for l in io.open(REG, encoding='utf-8').read().split(u'\n')]
raw = [r for r in raw if r]
axes = [r.split()[0] for r in raw]          # 軸名（供漂移檢查比對）
ARGV = {r.split()[0]: r.split()[1:] for r in raw}   # 軸名 -> 附加參數（如中介檔路徑）

# ──  漂移檢查：自稱待診／長駐／某輪所立之軸（含升閘者），未入冊者點名 ──────────
CAND = re.compile(r'^r\d{3}[a-z]+\.py$')
MARK = re.compile(u'待診|長駐|輪立')      # 第 199 輪擴『輪立』：升閘之軸不自稱待診，漏列即漏網。
# 記號**只認檔首三行**（即 docstring 之標題行——軸之自稱格式在此，如「（第 199 輪立・升閘）」）。
# 第 199 輪兩度自蹈：先以『升閘／專軸』泛指之詞為記，記錄腳本之碼內註引及此二字便被誤點名；
# 收為『輪立』後，同一支記錄腳本因**轉述**漂移記號（『待診／長駐』）而在第 13 行觸發——
# **記號須取格式與其位置，凡轉述記號者不得算自稱記號**。
drift = []
for f in sorted(os.listdir(u'_work')):
    if not CAND.match(f) or 'negtest' in f or 'neg.md' in f:
        continue
    name = f[:-3]
    if name in axes:
        continue
    head = u'\n'.join(io.open(os.path.join(u'_work', f), encoding='utf-8').read().split(u'\n')[:3])
    if MARK.search(head):
        drift.append(name)

if drift:
    print(u'未列之軸（須補進 _work/_axes.txt）：%s' % u'、'.join(drift))

# ── ① 逐軸跑 ───────────────────────────────────────────────
if u'--list' in sys.argv:
    print(u'冊上 %d 軸；漂移 %d。' % (len(axes), len(drift)))
    sys.exit(1 if drift else 0)

miss = [a for a in axes if not os.path.exists(os.path.join(u'_work', a + u'.py'))]
if miss:
    print(u'冊上有軸而檔不在：%s（名冊與實檔已分岔）' % u'、'.join(miss))

bad = []
for a in axes:
    p = os.path.join(u'_work', a + u'.py')
    if not os.path.exists(p):
        bad.append((a, u'無檔'))
        continue
    q = subprocess.run([sys.executable, u'-X', u'utf8', p] + ARGV[a], capture_output=True,
                       text=True, encoding='utf-8', errors='replace', env=env)
    rc = q.returncode
    tail = u''
    out = (q.stdout or u'').rstrip(u'\n').split(u'\n')
    if rc and out:
        tail = out[-1][:90]
    if rc:
        bad.append((a, u'rc=%d %s' % (rc, tail)))
    sys.stdout.write(u'·' if not rc else u'✘')
    sys.stdout.flush()
print(u'\n跑畢：%d 軸，病 %d。' % (len(axes), len(bad)))
for a, why in bad:
    print(u'  BAD %-12s %s' % (a, why))
sys.exit(1 if (bad or drift or miss) else 0)
