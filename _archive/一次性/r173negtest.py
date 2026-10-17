# -*- coding: utf-8 -*-
"""r173neg.py —— 不變量 76／77 之負測：回植原病必 FAIL，復原後雜湊與植前全同。"""
import hashlib, io, os, re, subprocess, sys

SRC = [f for f in os.listdir('.') if f.startswith('ver38') and f.endswith('.md')][0]
orig = io.open(SRC, 'rb').read()
h0 = hashlib.sha256(orig).hexdigest()


def run_check():
    r = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    rep = io.open(os.path.join('_work', 'check.txt'), encoding='utf-8').read()
    fails = [l.strip()[:56] for l in rep.split(u'\n') if l.strip().startswith(u'FAIL')]
    tot = [l for l in rep.split(u'\n') if u'不變量' in l]
    return r.returncode, fails, (tot[-1] if tot else u''), rep


def write(text):
    io.open(SRC, 'w', encoding='utf-8', newline=chr(10)).write(text)


txt = orig.decode('utf-8')

# 植甲：『---』緊接散文（回退 172 輪前『留白』原形）
key = u'> *留白：鉢已洗淨，倒扣晾乾。有漏斷處，便是歸家。*' + chr(10) + chr(10) + u'---'
assert txt.count(key) == 1, txt.count(key)
write(txt.replace(key, u'> *留白：鉢已洗淨，倒扣晾乾。有漏斷處，便是歸家。*' + chr(10) + u'---'))
rc, f, tot, rep = run_check()
print(u'植甲（setext 劫持）：rc=%d｜%s' % (rc, tot))
for x in f:
    print(u'   FAIL：%s' % x)
assert any(u'setext' in x for x in f), u'植甲未逮，閘無牙'
write(txt)

# 植乙：引言塊吞段（抽去『逆向制衡』前之空行）
key2 = (u'法統與法人才兩得其全。' + chr(10) + chr(10) + u'**逆向制衡——打破單向監護之歷史陳規**')
assert txt.count(key2) == 1, txt.count(key2)
write(txt.replace(key2, u'法統與法人才兩得其全。' + chr(10) + u'**逆向制衡——打破單向監護之歷史陳規**'))
rc, f, tot, rep = run_check()
print(u'植乙（引言吞段）：rc=%d｜%s' % (rc, tot))
for x in f:
    print(u'   FAIL：%s' % x)
assert any(u'引言塊' in x for x in f), u'植乙未逮，閘無牙'
write(txt)

after = io.open(SRC, 'rb').read()
h1 = hashlib.sha256(after).hexdigest()
print(u'復原：雜湊%s（植前 %s…／復原 %s…）' % (u'相同' if h1 == h0 else u'不同', h0[:12], h1[:12]))
assert h1 == h0, u'復原後雜湊不同——主檔未還原！'
rc, f, tot, rep = run_check()
print(u'復原後複測：%s｜FAIL %d' % (tot, len(f)))
assert rc == 0 and not f
print(u'兩閘俱有牙，主檔毫髮無損。')
