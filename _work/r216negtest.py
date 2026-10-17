# -*- coding: utf-8 -*-
r"""r216negtest.py —— 第 216 輪・第 44 軸 `r216loc` 之植病負測（留檔，自建基準）。

立軸之定例：**新軸初立即失牙，向由植病負測現形，非由零報現形**（歷輪已十一度）。
五路俱在副本上動刀（主檔唯讀，末以哈希自證一字未損），且**每路須中其目**——不只看退出碼，
還要看所報之病目（甲／乙／丙）與其同，否則一路之退 1 可能是別目代勞，其牙在何處無由知
（初版即如此：『乙 虛行』之路由『丙 行號漂』代退，乙之有牙無牙未證——206『先以理想病形測尺』之例。
故本器之的須另擇一『其檔有連續空白段』者：窗擴一行，單枚空行必被兩鄰擠掉，非整段虛行不能發乙目）：
 ⓪ 淨本 → 退 0 且無甲乙丙之報（陰性對照）
 ① 甲 越界：真指針之號改 `L99999` → 退 1 且有『甲』
 ② 乙 虛行：號改至同檔『連續空行段』之中間行 → 退 1 且有『乙』
 ③ 丙 行號漂：號改至同檔他處（其引文確在他行而不在新窗）→ 退 1 且有『丙』
 ④ 從寬：其「」段改為律中所無之語（存在性屬 `r185orphan` 之域）→ 退 0（本軸不判）
退出碼：五路之期望俱符則 0，否則 1。
"""
import hashlib, io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk as t

MASTER = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_work', u'_r216work.md')
AXIS = os.path.join(ROOT, u'_work', u'r216loc.py')
H0 = hashlib.sha256(io.open(MASTER, 'rb').read()).hexdigest()

RAW, NRM = {}, {}
for fn in sorted(os.listdir(os.path.join(ROOT, u'原文'))):
    m = re.match(u'(\\d{1,2}-\\d{1,2})', fn)
    if fn.endswith(u'.txt') and m:
        seg = m.group(1)
        RAW[seg] = io.open(os.path.join(ROOT, u'原文', fn), encoding='utf-8-sig').read().split(u'\n')
        NRM[seg] = [t.norm(x) for x in RAW[seg]]
VOID = {}                                            # 各檔第一段『連續空白 ≥3 行』之中間行號（1-based）
for seg, rows in RAW.items():
    k, hit = 0, None
    while k < len(rows):
        if not rows[k].strip():
            j = k
            while j < len(rows) and not rows[j].strip():
                j += 1
            if j - k >= 3:
                hit = k + 1 + (j - k) // 2           # 1-based 之中間行（窗擴一行，非整段虛行不能發乙目）
                break
            k = j
        else:
            k += 1
    if hit:
        VOID[seg] = hit
print(u'語料檔：%d 檔｜其中有連續空行段者：%s' % (len(RAW), sorted(VOID)))

SRC = io.open(MASTER, encoding='utf-8').read()
lines = SRC.split(u'\n')
VS = re.compile(u'(\\d{1,2}-\\d{1,2})\\s*卷段')
PP = re.compile(u'L(\\d{1,5})(?:\\s*[\\u2013\\u2014~\\u81f3]\\s*(?:L)?(\\d{1,5}))?')
QT = re.compile(u'「([^」]{6,})」')


def pick(need_void=False):
    """取一『同線有卷段標、有「」引文、其號在檔內且窗中見其文』之指針行，作植字之的。"""
    for i, l in enumerate(lines):
        if u'卷段' not in l or u'L' not in l or l.lstrip().startswith(u'#'):
            continue
        mms = list(PP.finditer(l))
        segs = [m.group(1) for m in VS.finditer(l)]
        qs = [t.norm(x) for x in QT.findall(l)]
        if not mms or not segs or not qs:
            continue
        seg = segs[0]
        NL = NRM.get(seg, [])
        if not NL or (need_void and seg not in VOID):
            continue
        a = int(mms[0].group(1))
        b = int(mms[0].group(2)) if mms[0].group(2) else a
        if not (1 <= a and b <= len(NL)):
            continue
        win = u''.join(NL[k - 1] for k in range(max(1, a - 1), min(len(NL), b + 1) + 1))
        if any(len(q) >= 8 and q[:8] in win for q in qs):
            far = [k for k, x in enumerate(NL, 1) if x.strip() and abs(k - a) > 30]
            if not far:
                continue
            return dict(row=i, seg=seg, a=a, void=VOID.get(seg), far=far[len(far) // 2])
    return None


TA = pick()
TB = pick(need_void=True)
assert TA and TB, u'未找到可植字之的'
print(u'的 A：書L%d｜%s 檔｜原號 L%d｜遠行 L%d' % (TA['row'] + 1, TA['seg'], TA['a'], TA['far']))
print(u'的 B：書L%d｜%s 檔｜原號 L%d｜虛行 L%d' % (TB['row'] + 1, TB['seg'], TB['a'], TB['void']))


def swap(d, newnum):
    """同位植字：只換該號，不增不刪字。"""
    ln = re.sub(u'L%d(?![\\d])' % d['a'], u'L%d' % newnum, lines[d['row']], count=1)
    assert ln != lines[d['row']], u'植字未中（原號形不存）'
    return u'\n'.join(lines[:d['row']] + [ln] + lines[d['row'] + 1:])


def run(txt, tag, want, pre=None):
    io.open(WORK, 'w', encoding='utf-8', newline='').write(txt)
    p = subprocess.run([sys.executable, '-X', 'utf8', AXIS, WORK],
                       capture_output=True, text=True, encoding='utf-8')
    got = [x for x in (p.stdout or u'').split(u'\n') if x[:1] in (u'甲', u'乙', u'丙')]
    if (p.stderr or u'').strip():                     # 器崩非器病：退 1 之由若來自 Traceback 須現形
        print(u'   ! 器報stderr：%s' % p.stderr.strip().split(u'\n')[-1][:110])
    ok = p.returncode == want
    if ok:
        ok = any(x.startswith(pre) for x in got) if pre else not got
    print(u'%s %s｜退 %d（須 %d）｜病目 %d 條%s' % (u'✓' if ok else u'✗', tag, p.returncode, want,
                                                   len(got), u'｜例：%s' % got[0][:58] if got else u''))
    return ok


res = []
res.append(run(u'\n'.join(lines), u'⓪ 淨本', 0, pre=None))
res.append(run(swap(TA, 99999), u'① 甲 越界 L99999', 1, pre=u'甲'))
res.append(run(swap(TB, TB['void']), u'② 乙 虛行 L%d（同檔連續空行段之中間行）' % TB['void'], 1, pre=u'乙'))
res.append(run(swap(TA, TA['far']), u'③ 丙 行號漂 L%d' % TA['far'], 1, pre=u'丙'))
ln2 = QT.sub(u'「外道虛構不涉律文之假引號標的」', lines[TA['row']], count=1)
res.append(run(u'\n'.join(lines[:TA['row']] + [ln2] + lines[TA['row'] + 1:]),
               u'④ 從寬 其「」文改為律中所無（存在性屬 185 軸）', 0, pre=None))

H1 = hashlib.sha256(io.open(MASTER, 'rb').read()).hexdigest()
print(u'主檔哈希自證：%s（%s）' % (H1[:16], u'與植病前同，一字未損' if H1 == H0 else u'**已變，須查!**'))
if os.path.exists(WORK):
    os.remove(WORK)
print(u'試檔自除：%s' % (not os.path.exists(WORK)))
sys.exit(0 if all(res) and H1 == H0 else 1)
