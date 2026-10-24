# -*- coding: utf-8 -*-
"""語料之『歸一序列＋碼位回圖』與逐字對齊器（第 256 輪立，供 `_work/v39qfix.py` 及他器共用）。

歸一口徑一仍 `_tk.norm`（折異體・展拆字・只存漢字與數字），惟此處另記每一歸一字元之 raw 座標，
故命中之後可自語料還原『帶標點之原文』——無此回圖，逐字回填無從落筆。
"""
import difflib
import glob
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT, os.path.join(_ROOT, '_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402

KEEP = _tk.KEEP
FOLD = _tk.FOLD
MINCOV = float(os.environ.get(u'MINCOV', u'0.80'))
MINRATIO = float(os.environ.get(u'MINRATIO', u'0.72'))


def _decomp_group(g):
    if g in _tk.BRACKET_MAP:
        return _tk.BRACKET_MAP[g]
    for sep in (u'*', u'/'):
        if sep in g:
            return g.split(sep)[-1]
    return g


def norm_index(raw):
    """回 (歸一串, 每一歸一字元之 raw 座標)，與 `_tk.norm` 同口徑。"""
    nt, nm = [], []
    i, n = 0, len(raw)
    while i < n:
        c = raw[i]
        if c == u'[':
            j = raw.find(u']', i + 1)
            if 0 < j - i <= 15:
                for ch in _decomp_group(raw[i + 1:j]):
                    f = FOLD.get(ch, ch)
                    if KEEP.match(f):
                        nt.append(f)
                        nm.append(i)
                i = j + 1
                continue
        f = FOLD.get(c, c)
        if KEEP.match(f):
            nt.append(f)
            nm.append(i)
        i += 1
    return u''.join(nt), nm


FILES = sorted(glob.glob(os.path.join(_ROOT, u'原文', u'*.txt')))
CORPUS = []
for _fp in FILES:
    _raw = _tk.read(_fp)
    _nt, _nm = norm_index(_raw)
    CORPUS.append((os.path.basename(_fp), _raw, _nt, _nm))


def corpus_size():
    return len(CORPUS), sum(len(c[2]) for c in CORPUS)


def _clean(s):
    """語料 raw 切片之印面化：引號折『』並調平；組字碼『[x*y]』唯定字者（BRACKET_MAP）可換正字，
    餘者一律斥候不用——印面不得留校勘符號（歷輪之誡）。"""
    s = _balance(s.replace(u'\u300c', u'\u300e').replace(u'\u300d', u'\u300f'))
    for g, z in _tk.BRACKET_MAP.items():
        s = s.replace(u'[%s]' % g, z)
    if u'[' in s:
        return None
    # 語料之內層引號一併除去：切片常始於引語之中，留之必致 『』 相倒（書中引號只一層）
    return s.replace(u'\u300e', u'').replace(u'\u300f', u'')


def _balance(s):
    """語料引號折成『』後若落單（切片起於引語之中），徑削單邊——形貌不屬內容，留之反破書中括號之平。"""
    while s.count(u'\u300e') > s.count(u'\u300f'):
        i = s.rfind(u'\u300e')
        s = s[:i] + s[i + 1:]
    while s.count(u'\u300f') > s.count(u'\u300e'):
        i = s.find(u'\u300f')
        s = s[:i] + s[i + 1:]
    return s


def realign(seg, mincov=None, minratio=None):
    """待補之歸一段 → (覆盖率, 相似率, 語料原文串（缺处以『……』相綴）)；無合者回 None。

    探點不取一而取四（頭・二・三・尾）：『欲說戒者當如是說』一類套語冠於眾戒之前，
    若只以頭錨求之則遍-hit 而無從選真，故中段與尾段之錨俱试，取其覆蓋最廣者。
    候選須不長於原段 1.6 字倍有奇，防吞他文；語料自身之 「」 改『』，以免書中引號相套。
    """
    mc = mincov if mincov is not None else MINCOV
    mr = minratio if minratio is not None else MINRATIO
    if len(seg) < 6:
        return None
    probes = []
    for a in (0, 4, 8, max(0, len(seg) - 8)):
        pr = seg[a:a + 8]
        if len(pr) >= 6 and pr not in probes:
            probes.append(pr)
    best = None
    # 甲・先窮盡『連續子串』一路（快，且即最可信之候選）
    for probe in probes:
        lead = seg.find(probe)
        for _fn, raw, nt, nm in CORPUS:
            st, tried = 0, 0
            while tried < 60:
                q = nt.find(probe, st)
                if q < 0:
                    break
                st = q + 1
                tried += 1
                p = q - lead
                if p >= 0 and nt.startswith(seg, p):
                    s = _clean(raw[nm[p]: nm[p + len(seg) - 1] + 1].strip())
                    if s is None:
                        continue
                    return (1.0, 1.0, s)
    # 乙・次求『綴合』：段與語料有出入者（書經刪改），以 difflib 取匹配塊
    for probe in probes:
        lead = seg.find(probe)
        for _fn, raw, nt, nm in CORPUS:
            st, tried = 0, 0
            while tried < 12:
                q = nt.find(probe, st)
                if q < 0:
                    break
                st = q + 1
                tried += 1
                p = q - lead
                if p < 0:
                    continue
                win = nt[p: p + len(seg) * 2 + 6]
                sm = difflib.SequenceMatcher(None, seg, win, autojunk=False)
                blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
                cov = sum(b.size for b in blocks)
                if not blocks or cov < len(seg) * mc:
                    continue
                span = blocks[-1].b + blocks[-1].size - blocks[0].b
                # 相似率但免懲『窗大於段』之長：以匹配塊所跨之語料跨度為分母
                ratio = 2.0 * cov / (cov + span)
                if ratio < mr:
                    continue
                pieces = []
                ok = True
                if span <= len(seg) * 1.35 + 6:
                    # 匹配塊所跨不多者，徑取語料之連續原文（不拆『……』，免傷文氣）
                    c = _clean(raw[nm[p + blocks[0].b]: nm[p + blocks[-1].b + blocks[-1].size - 1] + 1].strip())
                    if c is None:
                        ok = False
                    pieces = [c]
                else:
                    for b in blocks:
                        c = _clean(raw[nm[p + b.b]: nm[p + b.b + b.size - 1] + 1].strip())
                        if c is None:
                            ok = False
                            break
                        if c and c not in pieces:
                            pieces.append(c)
                if not ok:
                    continue
                cand = _balance(u'……'.join(pieces))
                if len(_tk.norm(cand)) > len(seg) * 1.6 + 8:
                    continue
                sc = (cov / float(len(seg)), ratio, cand)
                if best is None or sc[:2] > best[:2]:
                    best = sc
                    if cov == len(seg) and ratio > 0.95:
                        return best
    return best
