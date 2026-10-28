# -*- coding: utf-8 -*-
"""292・乙組刀（斜線次碼自正文退出，彙為附錄四末之對照一節）。

口徑：只退『遮NN／僧NN／開NN』之舊次；同列之他案純數字（〔案例 10 / 11〕）與支名
      （異分支・伴黨支・安居段・僧殘算定通則）俱保留。對照節之行形不用〔案例 NN〕字面，
      免攪動附錄四之百二行計數。乾跑先印映射全表與計數，核對無誤方 --apply。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv

RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')
LOG = []

CODE = re.compile(u'(遮|僧|開)(\\d+)(.*)$')
TOK = re.compile(u'〔案例 ([^〕]+)〕')

MAP = {}          # 主號(int) ➔ {'碼': [遮NN…], '支': […], '合': [他案號…]}
NSTRIP = 0


def fix(m):
    global NSTRIP
    inner = m.group(1).strip()
    if u'/' not in inner:
        return m.group(0)
    parts = [p.strip() for p in inner.split(u'/')]
    head = parts[0]
    if not re.match(u'^\\d+$', head):
        return m.group(0)                       # 現-1 之屬，非純數字主號，不動
    n = int(head)
    codes, tails, co = [], [], []
    rest = []
    for p in parts[1:]:
        mm = CODE.match(p)
        if mm:
            codes.append(mm.group(1) + mm.group(2))
            if mm.group(3).strip():
                tails.append(mm.group(3).strip())
        elif re.match(u'^\\d+$', p):
            co.append(int(p))
            rest.append(p)
        else:
            tails.append(p)
    rec = MAP.setdefault(n, {'碼': [], '支': [], '合': []})
    rec[u'碼'] += codes
    rec[u'支'] += tails
    rec[u'合'] += co
    if not codes:
        return m.group(0)                        # 唯有他案同列：原形保留
    NSTRIP += 1
    keep = [head] + rest
    out = u' / '.join(x for x in keep if x)
    if tails:
        return u'〔案例 %s〕（%s）' % (out, u'・'.join(tails))
    return u'〔案例 %s〕' % out


for i, x in enumerate(L):
    y = TOK.sub(fix, x)
    if y != x:
        L[i] = y
        LOG.append(u'L%-5d %s' % (i + 1, (u'次碼退 ➔ ' + y[:60])))

print(u'次碼退位之枚數：%d｜涉主號：%d' % (NSTRIP, len(MAP)))
for n in sorted(MAP):
    r = MAP[n]
    if r[u'碼'] or r[u'支'] or r[u'合']:
        print(u'  %02d 碼%s 支%s 合%s' % (n, r[u'碼'], r[u'支'], r[u'合']))
print(u'刀數：%d｜行數 %d ➔ %d' % (len(LOG), len(T.split(u'\n')), len(L)))

# ── 對照節之成文（自 MAP 算數，不自證不報）────────────────────────
GRP = {u'遮': [], u'僧': [], u'開': []}
NODUP = {}
for n in sorted(MAP):
    r = MAP[n]
    if not r[u'碼']:
        continue
    s = u'%02d↔%s' % (n, u'・'.join(r[u'碼']))
    if r[u'合']:
        s += u'（與 %s 合案）' % u'・'.join(u'%02d' % c for c in r[u'合'])
    if r[u'支']:
        s += u'（%s）' % u'・'.join(r[u'支'])
    GRP[r[u'碼'][0][0]].append(s)
    NODUP[n] = s
NTOT = sum(len(v) for v in GRP.values())
BLK = [
    u'### 〔新舊次碼對照〕（三十五〜三十八版舊次・唯備對讀）',
    u'',
    u'> **【此節之義】**：本書三十五至三十八版曾依『遮罪・僧殘・開許』之舊編次，於主號之右掛斜線次碼'
    u'（`〔案例 05 / 遮44〕` 之屬）。自三十九版起，**正文案號一律純號**——舊碼退出正文，彙錄於此，'
    u'唯備新舊對讀；**主號唯 01〜102，舊次不另計案**，亦不帶語源分級之義。今收 %d 案之舊次如次，'
    u'括註者乃該案之支名或同列之他案，非舊次。' % NTOT,
    u'',
]
LBL = {u'遮': u'遮罪舊次', u'僧': u'僧殘舊次', u'開': u'開許舊次'}
for k in (u'遮', u'僧', u'開'):
    BLK.append(u'* **%s（%d 案）**：%s' % (LBL[k], len(GRP[k]), u'・'.join(GRP[k])))
BLK.append(u'')
i = [k for k, x in enumerate(L) if x.startswith(u'# 附錄五')][0]
ins = max(k for k in range(i) if L[k].strip() == u'---')
L[ins:ins] = BLK
LOG.append(u'L%-5d 插 對照節 %d 行' % (ins + 1, len(BLK)))

OLD_FL = (u'又一：`〔案例 NN / 遮MM〕`・`〔案例 NN / 僧MM〕`・`〔案例 NN / 開MM〕` 之斜線次碼，'
          u'乃本書歷版（三十五至三十八版）依『遮罪・僧殘・開許』立號之**舊次**（舊稿唯以此碼為主號），'
          u'今存之以便新舊對讀；**主號唯 01〜102，次碼不另計案**，亦不帶語源分級之義。')
NEW_FL = (u'又一：正文之案例主號今**一律純號**（〔案例 05〕之屬）。本書三十五至三十八版曾依'
          u'『遮罪・僧殘・開許』立舊次、於主號之右掛斜線次碼（`〔案例 05 / 遮44〕` 之屬），'
          u'今其碼**自正文退出**，彙為附錄四末〔新舊次碼對照〕一節，唯備新舊對讀；'
          u'**主號唯 01〜102，舊次不另計案**，亦不帶語源分級之義。')
n = sum(x.count(OLD_FL) for x in L)
assert n == 1, u'凡例次碼條：命中 %d 枚（須 1）' % n
for i, x in enumerate(L):
    if OLD_FL in x:
        L[i] = x.replace(OLD_FL, NEW_FL)
        LOG.append(u'L%-5d 凡例次碼條歸今制' % (i + 1))
        break

OUT = u'\n'.join(L)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
newbad = sorted(({c for c in OUT if c in SIMPS} - {c for c in T if c in SIMPS}))
print(u'簡形新增：%s' % (u''.join(newbad) or u'無'))
for c in newbad:
    j = OUT.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), OUT[max(0, j - 22):j + 12].replace(u'\n', u' ')))
print(u'對照節計數：遮 %d・僧 %d・開 %d・合 %d' % (
    len(GRP[u'遮']), len(GRP[u'僧']), len(GRP[u'開']), NTOT))
print(u'終行數：%d' % len(L))
for x in LOG[-8:]:
    print(u'  ' + x)
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
io.open(os.path.join(ROOT, u'_work', u'r292cutlogB.txt'), 'w', encoding='utf-8',
        newline='\n').write(u'\n'.join(LOG) + u'\n')
