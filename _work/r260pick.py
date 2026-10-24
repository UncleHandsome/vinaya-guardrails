# -*- coding: utf-8 -*-
"""260 輪・擇段器（書中取句・語料取段，一字不重打）：
靶卡之『律意』按句編號 → 每句與語料求最長共同子串（≥8 字）→ 自該子串**廣展至其本句**（左右至句末符）
→ 驗 `_tk.classify` 自證逐字・印面可用（無合字・『』成對・無 `*`）→ 報候選與句號。
**覆核在報**：人唯選句（改 WANT 之開），不復打一字；apply 自語料複製原文成 「」 行，插入【律典原典】欄。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r260pick.py           # 報候選（標句號）
      PYTHONIOENCODING=utf-8 python -X utf8 _work/r260pick.py apply     # 落 WANT 所選之句
"""
import difflib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

APPLY = u'apply' in sys.argv
CARDS = (u'25', u'31', u'32', u'65')
WANT = {u'25': (), u'31': (), u'32': (7,), u'65': (1, 3)}      # 卡：所選之句號（覆核後定）
MINLCS = 8
BOUND = u'\u3002\uff01\uff1f\uff1b'
LINES = _tk.MAIN_LINES
CARD = re.compile(u'^### 〔案例 (\\d+)〕')
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
SENT = re.compile(u'[^。！？……]+')


def body_of(num):
    i = next(k for k, l in enumerate(LINES) if CARD.match(l) and CARD.match(l).group(1) == num)
    j = next(k for k in range(i, len(LINES)) if HEAD.match(LINES[k]))
    k = j + 1
    while k < len(LINES) and not STOP.match(LINES[k]):
        if u'\u5f8b\u610f\uff1a' in LINES[k]:
            return k, LINES[k].split(u'\u5f8b\u610f\uff1a', 1)[1]
        k += 1
    return None, u''


def expand(seg_fn, raw, nm, a, z):
    lo = max(raw.rfind(b, 0, a) for b in BOUND)
    lo = lo + 1 if lo >= 0 else max(0, a - 30)
    hi = min([raw.find(b, z) for b in BOUND if raw.find(b, z) >= 0] or [z + 1])
    out = raw[lo:hi + 1].strip()
    out = out.replace(u'\u300c', u'\u300e').replace(u'\u300d', u'\u300f')
    if (out.count(u'\u300e') != out.count(u'\u300f') or u'\u300c' in out or u'[' in out
            or u'*' in out or len(out) > 260):
        return None
    return out


plan = []
for num in CARDS:
    lv, body = body_of(num)
    sents = [s.strip() for s in SENT.findall(body) if len(_tk.norm(s.strip())) >= 10]
    picks = range(len(sents)) if not APPLY else [q for q in WANT[num] if q < len(sents)]
    print(u'◐◐ 案例%s（律意之可選句 %d 個・所選 %s）' % (num, len(sents), sorted(WANT[num])))
    for idx in picks:
        s = sents[idx]
        n = _tk.norm(s)
        best = None
        for fn, raw, nt, nm in v39align.CORPUS:
            m = difflib.SequenceMatcher(None, n, nt, autojunk=False).find_longest_match(
                0, len(n), 0, len(nt))
            if m.size < MINLCS:
                continue
            lcs = n[m.a:m.a + m.size]
            cnt = _tk.VINAYA.count(lcs)
            if cnt > 3:                       # 所共唯套語（『欲說戒者當如是說』之類）即擲回——防錯拾他戒
                continue
            if best is None or m.size > best[1]:
                best = (fn, m.size, nm[m.b], nm[m.b + m.size - 1] + 1, raw, lcs, cnt)
        if not best:
            print(u'   [%d] 無合錨之句（或所共唯套語）｜%s' % (idx, s[:34]))
            continue
        fn, size, a, z, raw, lcs, cnt = best
        seg = expand(fn, raw, nm, a, z)
        if not seg:
            print(u'   [%d] 廣展不合閘（共 %d 字・%d 見）｜%s' % (idx, size, cnt, s[:30]))
            continue
        ok = _tk.classify(seg)[0] in (u'hit', u'skip')
        print(u'   [%d] %s・共%d字(%d 見)・證%s｜書句：%s' % (
            idx, fn, size, cnt, u'\u2713' if ok else u'\u2717', s[:30]))
        print(u'        語料段：%s' % seg[:150])
        if ok:
            plan.append((num, lv, idx, seg))

print(u'———— 候選可落 %d 段（涉卡 %d）' % (len(plan), len({p[0] for p in plan})))
if not APPLY:
    sys.exit(0)
# 同一卡之同欄若取多段，綴為一行（以『……』相間，合本書刪節號之制），免兩行爭一落點
by = {}
for num, lv, idx, seg in plan:
    by.setdefault((num, lv), []).append((idx, seg))
n2 = list(LINES)
lines_ins = []
for (num, lv), got in by.items():
    segs = [s for _i, s in sorted(got)]
    line = u'> \u300c%s\u300d' % u'\u2026\u2026'.join(segs)
    assert u'\u5f8b\u610f\uff1a' in n2[lv], u'落點非律意行（案例%s）' % num
    assert u'\u5377' in n2[lv - 1] or u'\u300a' in n2[lv - 1], u'落點上一行無卷引（案例%s）' % num
    lines_ins.append((lv, line))
for lv, line in sorted(lines_ins, key=lambda x: -x[0]):
    n2.insert(lv, line)
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
io.open(os.path.join(ROOT, NAME), 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(LINES) + len(lines_ins), u'行數等式不合（%d＋%d≠%d）' % (
    len(LINES), len(lines_ins), len(back))
bset = set(back)
for _lv, line in lines_ins:
    assert line in bset, u'回讀缺行'
print(u'———— 已落 %d 段（綴為 %d 行）・%d → %d 行・回讀相符' % (
    len(plan), len(lines_ins), len(LINES), len(back)))
