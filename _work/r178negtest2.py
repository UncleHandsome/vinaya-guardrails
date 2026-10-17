# -*- coding: utf-8 -*-
# 第 178 輪負測乙：新 FAIL 清冊須在『stdout 被截尾』的舊收法下仍然可見（此即本輪所挖之盲）。
import hashlib, io, subprocess, sys

BOOK = u'ver38四分律_起心動念心智分析框架_修正版.md'
CHK = u'_work/check.txt'
A = u'六閘門是給審理者的詳圖'
PLANT = u'（植碼：這是一枚簡形『类』之病，另有間隔號・）'


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


orig = io.open(BOOK, encoding='utf-8').read()
assert orig.count(A) == 1, u'錨點命中數不符，未動檔'
h0 = sha(orig)

# 基態（兩種收法都讀一次）
for tag, red in ((u'全檔收法', u'/dev/null'), (u'截尾收法', CHK)):
    if red == u'/dev/null':
        subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        body = io.open(CHK, encoding='utf-8').read()
    else:
        io.open(CHK, 'w', encoding='utf-8').write(u'')
        subprocess.run(u'%s -X utf8 _tk.py check > %s 2>&1' % (sys.executable, CHK), shell=True)
        body = io.open(CHK, encoding='utf-8').read()
    print(u'基態 %s｜%d 行｜PASS %d｜FAIL %d' % (
        tag, body.count(u'\n') + 1, body.count(u'PASS'), body.count(u'FAIL')))

# 植病：印面插一枚簡形與一枚日式間隔號 → 早期檢必報
io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig.replace(A, A + PLANT))
for tag in (u'全檔收法', u'截尾收法'):
    if tag == u'全檔收法':
        subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        subprocess.run(u'%s -X utf8 _tk.py check > %s 2>&1' % (sys.executable, CHK), shell=True)
    body = io.open(CHK, encoding='utf-8').read()
    lines = [l for l in body.split(u'\n') if l.startswith(u'FAIL') or l.strip().startswith(u'✗')
             or u'失敗清冊' in l]
    print(u'植病 @ %s｜rc 見下｜清冊行 %d 條｜%s' % (tag, len(lines), u' ⏎ '.join(lines[:4])[:170]))
p = subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print(u'植病之 rc＝%d（須非零）' % p.returncode)
io.open(BOOK, 'w', encoding='utf-8', newline='\n').write(orig)
print(u'還原：%s' % (sha(io.open(BOOK, encoding='utf-8').read()) == h0))
subprocess.run([sys.executable, '-X', 'utf8', '_tk.py', 'check'],
               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
