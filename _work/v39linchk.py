# -*- coding: utf-8 -*-
"""265 輪・行號尺 `v39linchk.py`：附錄六『調部文獻定位』所列 L行號，須真-hosting 本卡之逐字引文。

緣起：全書 L行號之宣稱共 **36 號／15 行**（盡在附錄六），宣稱『此文在本地檔之第幾行』，向無一尺問及。
      行號是給讀者回查用的——**能找到錯地方的正確行號，比錯行號更壞**（目錄之誡同科）。
口徑：① 許用檔由该行所冠卷次定（『卷三十八（大正藏卷段 38-49，L137…）』・『卷五十六（L909）』皆可解）；
      ② 本卡之**可證引文**＝卡身諸 「」 段中 `_tk.classify` 判 hit／other 者，再按標點切片段（norm ≥4 字）；
      ③ 逐號判：**中**（該號 ±W 行窗內見本卡某片段）／**不合**（卡有可證引文而此號窗內無一片段）／
        **未證**（卡全屬撮述、無可證引文，或行號越出檔之行数）；
      ④ 反面亦量：**卡之片段是否有號可歸**（無歸者報待考，不挡——因一卡可散見數十處，未必要盡列）。
退碼：『不合』≥1 即退 1。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39linchk.py [-v]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

W = 3
KEYS = (u'01-10', u'11-21', u'22-30', u'31-37', u'38-49', u'50-60')
RANGE = {u'01-10': (1, 10), u'11-21': (11, 21), u'22-30': (22, 30),
         u'31-37': (31, 37), u'38-49': (38, 49), u'50-60': (50, 60)}
LINES_TXT = {}
for fn, raw, nt, nm in v39align.CORPUS:
    key = next((k for k in KEYS if k in fn), None)
    if key:
        LINES_TXT[key] = (raw.split(u'\n'), nt)
assert len(LINES_TXT) == 6, u'語料六檔未齊'

L = _tk.MAIN_LINES
CARD = re.compile(u'^### 〔(案例|調部專題) (\\d+)〕')
LIN = re.compile(r'L(\d+)')
VOLS = re.compile(u'卷\\s*([一二三四五六七八九十0-9]{1,4})')
RNG2 = re.compile(u'卷段\\s*(\\d+)\\s*-\\s*(\\d+)')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
verbose = u'-v' in sys.argv


def num(s):
    return int(s) if s.isdigit() else _tk.cn_num(s)


def frags(qs):
    """卡身引文 → 可證之片段：先按刪節號拆『逐字連綴』（凡例第三律：節引必標），
      再按句讀切片段（norm ≥4 字），逐片段自證見於語料者方入——**以整段 classify 會誤擲合法的節引**。"""
    out = []
    for q in qs:
        for run in re.split(_tk.ELL, q):
            # 「、」不作切點：norm 本會抹之，切開反把『應安紐、若玦』碎片化至閾下（尺之單位須與文之單位同寬）
            for part in re.split(u'[，。！？；：「」『』（）\\s]', run):
                n = _tk.norm(part)
                if len(n) >= 4 and (n in _tk.VINAYA or any(n in t for _k, (_l, t) in LINES_TXT.items())):
                    out.append(n)
    return out


rows = []
i = 0
while i < len(L):
    m = CARD.match(L[i])
    if not m:
        i += 1
        continue
    card = u'%s%s' % (m.group(1), m.group(2))
    j = i + 1
    while j < len(L) and not CARD.match(L[j]) and not L[j].startswith(u'# '):
        j += 1
    block = L[i:j]
    qs = []
    for b in block:
        qs += _tk.Q_RE.findall(b)
    ps = frags(qs)
    for k, b in enumerate(block):
        if u'L' not in b or not LIN.search(b):
            continue
        vols = [v for v in (num(x) for x in VOLS.findall(b)) if v]
        keys = []
        for key in KEYS:
            lo2, hi2 = RANGE[key]
            if any(lo2 <= v <= hi2 for v in vols):
                keys.append(key)
        for mm in RNG2.finditer(b):
            key = u'%02d-%s' % (int(mm.group(1)), mm.group(2))
            if key in KEYS and key not in keys:
                keys.append(key)
        for x in [int(t) for t in LIN.findall(b)]:
            host, oob = False, True
            for key in keys:
                lines, _nt = LINES_TXT[key]
                if 1 <= x <= len(lines):
                    oob = False
                    win = _tk.norm(u''.join(lines[max(0, x - 1 - W):x + W]))
                    if any(pf in win for pf in ps):
                        host = True
            if oob:
                v = u'未證'
                d = u'行號越界（許用檔 %s）' % u'・'.join(keys)
            elif not ps:
                v = u'未證'
                d = u'卡無可證引文（全屬撮述）'
            elif host:
                v = u'中'
                d = u'・'.join(keys)
            else:
                v = u'不合'
                d = u'窗內無本卡任何片段（許用 %s；卡片段 %d 個）' % (u'・'.join(keys) or u'?', len(ps))
            rows.append((i + k + 1, card, x, v, d, len(ps)))
    i = j

tal = {}
for _ln, _c, _x, v, _d, _p in rows:
    tal[v] = tal.get(v, 0) + 1
print(u'———— L行號宣稱 %d 號（%d 行）：中 %d・不合 %d・未證 %d' % (
    len(rows), len({r[0] for r in rows}), tal.get(u'中', 0), tal.get(u'不合', 0), tal.get(u'未證', 0)))
if verbose or tal.get(u'不合', 0) or tal.get(u'未證', 0):
    for ln, card, x, v, d, npf in rows:
        if v != u'中' or verbose:
            print(u'  %s L%-6d %-8s L%-5d 引文片段%-3d｜%s' % (
                {u'中': u'·', u'不合': u'✗', u'未證': u'△'}[v], ln, card, x, npf, d[:64]))
sys.exit(1 if tal.get(u'不合', 0) else 0)
