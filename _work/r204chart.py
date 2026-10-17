# -*- coding: utf-8 -*-
"""r204chart.py —— p281『十六觀心問動態決策圖』之**接線與寬度自證**（第 204 輪立・升閘：己病非零即退 1）。

緣起：作者令⑤『不拆圖，唯水平緊縮 116→98–100 半形，使 `fit_pre_blocks` 之字級由 8.24pt 升至約 9.5pt』。
圖乃 67 行 ASCII 樹，緊縮只准動空格與橫線之長；而**任何一次移欄皆可使某個 ▼ 指到鄰欄之空處**——
紙上最毒之錯（箭頭無所指、分支懸空）歷輪皆賴親目見之（131／134／165 三輪），今歸器。

口径（全以『半形格』為軸：全形符占兩格，第二格記 '\\x00' 續符，故欄位之切移必不切字）：
 甲·孤箭：'▼' 之上一格非導線（│┌┐┴┬┘└─◄►）。
 乙·空落：'▼' 之下既非導線、亦無文字段盖其欄（箭無所往）。
 丙·斷柱：'│' 之上一格非導線且非出自文字段（立柱憑空而起）。
 丁·歪角：'┌┐└┘' 之橫臂或豎臂缺一。
 戊·歪扅：'┴' 上無来線，或 '┬' 下無去線。
 己·逾寬：全圖最寬 > 寬限（預設 100 半形 ⇒ 字級 9.52pt）。
 庚·文字簽名（給基準副本時才校）：逐行『去空格與橫線『─』後之字符序列』須與基準一字不差。
 辛·導線骨架（給基準副本時才校）：逐行『│▼┌┐┴┬┘└◄► 之枚數（唯『─』不計，其長乃緊縮之所動）』須與基準同
    ——**一行有幾枚立柱與箭頭，即該行開了幾個分支**；緊縮前後同數，則分支無增無減無斷。

用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r204chart.py [基準副本] [寬限]`
退出碼：諸目有病退 1。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
HEAD = u'#### 一、十六觀心問動態決策圖（扣合四階漏斗）'
WIRE = set(u'│┌┐┴┬┘└─▼◄►')
COR = {u'┌': (1, 1), u'┐': (-1, 1), u'└': (1, -1), u'┘': (-1, -1)}
NUMS = [a for a in sys.argv[1:] if a.isdigit()]
LIMIT = int(NUMS[0]) if NUMS else 100
REF = next((a for a in sys.argv[1:] if not a.isdigit() and not a.startswith(u'--')), None)
MD = next((a.split(u'=', 1)[1] for a in sys.argv[1:] if a.startswith(u'--file=')), MD)
REF = next((a.split(u'=', 1)[1] for a in sys.argv[1:] if a.startswith(u'--ref=')), REF)


def block(lines):
    h = next(i for i, l in enumerate(lines) if l.strip() == HEAD)
    st = next(i for i in range(h, len(lines)) if lines[i].strip().startswith(u'```'))
    en = next(i for i in range(st + 1, len(lines)) if lines[i].strip().startswith(u'```'))
    return lines[st + 1:en], st + 2


def cells(s):
    out = []
    for c in s:
        out += [c, u'\x00'] if ord(c) > 0x2E80 else [c]
    return out


def grid_of(body):
    g = [cells(x) for x in body]
    w = max(len(x) for x in g)
    return [x + [u' '] * (w - len(x)) for x in g], w


def tokmap(g, w):
    toks = []
    for r, row in enumerate(g):
        c = 0
        while c < w:
            if row[c] not in WIRE and row[c] not in (u' ', u'\x00'):
                s = c
                while c < w and g[r][c] not in WIRE and g[r][c] != u' ':
                    c += 1
                    if c < w and g[r][c] == u'\x00':
                        c += 1
                toks.append((r, s, c - 1, u''.join(x for x in row[s:c] if x != u'\x00')))
            else:
                c += 1
    return toks


def sig(body):
    return [u''.join(c for c in x if c not in u' ─') for x in body]


def parents(toks, gg):
    """僅供診斷：段之『父段』＝段之欄域內最近之上方『▼』所屬之更上段。換裝式重排必改其落點，
    故只列印不判（判則以辛·導線計數為準——每行 │▼┌┐┴┘◄ 之數乃圖之骨架，緊縮前後須同）。"""
    at = {}
    for (r, a, b, t) in toks:
        for c in range(a, b + 1):
            at[(r, c)] = t
    out = []
    for (r, a, b, t) in toks:
        pv = None
        for rr in range(r - 1, -1, -1):
            hits = [(rr, c) for c in range(a, b + 1) if gg[rr][c] == u'▼']
            if hits:
                pv = hits[0]
                break
        if not pv:
            out.append((t, None))
            continue
        vr, vc = pv
        pp = None
        for rr in range(vr - 1, -1, -1):
            if (rr, vc) in at:
                pp = at[(rr, vc)]
                break
        out.append((t, pp))
    return out


def skeleton(body):
    """逐行之導線骨架計數（『─』除外——橫線之長乃緊縮之所動）。"""
    KEYS = u'│▼┌┐┴┬┘└◄►'
    return [dict((k, sum(1 for c in x if c == k)) for k in KEYS) for x in body]


L = io.open(MD, encoding=u'utf-8').read().split(u'\n')
body, r0 = block(L)
g, w = grid_of(body)
toks = tokmap(g, w)
print(u'決策圖 L%d–%d｜%d 行｜圖寬 %d 半形｜文字段 %d｜字級推算 %.2fpt'
      % (r0, r0 + len(body) - 1, len(body), w, len(toks), 538.58 / (0.55 * w + 1.6)))

bad = []
cover = {}
for (r, a, b, _t) in toks:
    for c in range(a, b + 1):
        cover[(r, c)] = True
raw = lambda r, c: g[r][c] if 0 <= r < len(g) and 0 <= c < w else u' '


def cell(r, c):
    """格 → 其主字符：全形符之第二格（'\\x00' 續符）歸其左鄰，故 ▼ 落於框線字之半亦算對齊。"""
    ch = raw(r, c)
    return raw(r, c - 1) if ch == u'\x00' else ch


for r in range(len(g)):
    for c in range(w):
        ch = raw(r, c)
        if ch == u'▼':
            if cell(r - 1, c) not in WIRE:
                bad.append((u'甲', r0 + r, c, u'▼ 上無導線（孤箭）'))
            nxt = cell(r + 1, c)
            if nxt not in WIRE and (r + 1, c) not in cover:
                bad.append((u'乙', r0 + r, c, u'▼ 下無所指（空落）'))
        elif ch == u'│':
            up = cell(r - 1, c)
            if up not in WIRE and (r - 1, c) not in cover:
                bad.append((u'丙', r0 + r, c, u'│ 上無來處（斷柱）'))
        elif ch in COR:
            dh, dv = COR[ch]
            ah = raw(r, c + 2 if dh > 0 else c - 1) == u'─'
            av = any(cell(r + dv, cc) in (u'│', u'▼') for cc in (c, c + 1))
            if not (ah and av):
                bad.append((u'丁', r0 + r, c, u'%s 臂缺（橫%s 豎%s）' % (ch, ah, av)))
        elif ch == u'┴' and cell(r - 1, c) not in WIRE:
            bad.append((u'戊', r0 + r, c, u'┴ 上無來線'))
        elif ch == u'┬' and cell(r + 1, c) not in WIRE:
            bad.append((u'戊', r0 + r, c, u'┬ 下無去線'))
if w > LIMIT:
    bad.append((u'己', r0, w, u'最寬 %d > 寬限 %d 半形' % (w, LIMIT)))

if REF:
    R = io.open(REF, encoding=u'utf-8').read().split(u'\n')
    rb, rr0 = block(R)
    d_sig = [(i, a, b) for i, (a, b) in enumerate(zip(sig(rb), sig(body))) if a != b]
    sk_ref, sk_new = skeleton(rb), skeleton(body)
    d_skel = [(i, a, b) for i, (a, b) in enumerate(zip(sk_ref, sk_new))
              if dict((k, v) for k, v in a.items() if v) != dict((k, v) for k, v in b.items() if v)]
    rg, rw = grid_of(rb)
    print(u'基準對照：%d 行 vs %d 行｜文字段 %d vs %d' % (len(rb), len(body), len(tokmap(rg, rw)), len(toks)))
    for i, a, b in d_sig[:6]:
        print(u'  庚 L%-6d 基準『%s』今『%s』' % (rr0 + i, a, b))
    for i, a, b in d_skel[:8]:
        print(u'  辛 L%-6d 骨架基準%s 今%s' % (rr0 + i,
              u'，'.join(u'%s%d' % (k, v) for k, v in a.items() if v),
              u'，'.join(u'%s%d' % (k, v) for k, v in b.items() if v)))
    if len(rb) != len(body) or len(tokmap(rg, rw)) != len(toks):
        bad.append((u'庚', r0, 0, u'行數或段數已變'))
    if d_sig:
        bad.append((u'庚', r0, 0, u'文字簽名異 %d 行' % len(d_sig)))
    if d_skel:
        bad.append((u'辛', r0, 0, u'導線骨架（分支數）異 %d 行' % len(d_skel)))

for k, r, c, why in bad[:24]:
    print(u'  %s L%-6d 欄%-4d %s' % (k, r, c, why))
print(u'病：%d 處（甲乙丙丁戊己庚辛）→ %s' % (len(bad), u'待診' if bad else u'接線完好、寬合於制'))
sys.exit(1 if bad else 0)
