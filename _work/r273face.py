# -*- coding: utf-8 -*-
"""273 輪・重建後之印面覆核（独立器，不抄 builder 之自報）。

四量：甲 大綱逐條驗『其頁確見其題』・乙 頁腳號與物理頁之偏移（含 roman 卷首）・
      丙 圍欄段之起訖是否同頁（跨頁即版式之病）・丁 附錄與產物四件之存在。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r273face.py [列印|螢幕] [--stale]
退碼：甲未中・乙偏移不符・丙跨頁・丁缺件 皆退 1（口徑有未定者如實報『未判』不充綠）；
      冊新於印（陳印）退 2 拒鑑，加 --stale 強量則退 3（其果只作線索，不充綠）。
"""
import io
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHICH = (sys.argv[1] if len(sys.argv) > 1 else u'列印')
TAG = u'' if WHICH == u'列印' else u'_screen'
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
_cands = [q for q in os.listdir(os.path.join(ROOT, u'_print'))
          if q.startswith(u'ver39') and q.endswith(u'.pdf') and WHICH in q]
PDF = os.path.join(ROOT, u'_print', max(_cands, key=len))      # 名最長者＝交付檔（中介檔名短，勿量中介）
assert len(os.path.basename(PDF)) > 30, u'所選非交付檔（中介檔名短）：' + PDF
if len(sys.argv) > 2 and not sys.argv[2].startswith(u'-'):   # 負測之道：`python r273face.py 列印 <假病冊>`
    PDF = sys.argv[2]
BOOK_PATH = os.path.join(ROOT, NAME)
BOOK = io.open(BOOK_PATH, encoding=u'utf-8').read()
LINES = BOOK.split(u'\n')
norm = lambda s: re.sub(u'\\s+', u'', s)
bad = []

# ── 〇・同期之檢：印面所鑑之冊須與 PDF 同龄（275 輪親踩——以 274 之陳印鑑 275 之新冊，
#     遂憑空生出兩枚『起訖不可求』之假待判；凡校驗器拿舊產物量新源，紅綠俱不可信）。
_bm, _pm = os.path.getmtime(BOOK_PATH), os.path.getmtime(PDF)
if _bm > _pm:
    print(u'〇・同期｜⚠ 冊新於印（差 %.0f 分鐘）・所鑑之 PDF 乃陳冊之影——積輪未清' % ((_bm - _pm) / 60.0))
    print(u'   本器不鑑陳印（退 2）；奉令重建後再量。若明知其陳而強量，加 --stale（其果不充綠）。')
    if u'--stale' not in sys.argv:
        sys.exit(2)
else:
    print(u'〇・同期｜冊與印同龄（印晚於冊 %.0f 分鐘）' % ((_pm - _bm) / 60.0))
STALE = u'--stale' in sys.argv

# 口徑不兩抄：鎖頁之閾**逕取產器之源**（build39.fit_pre_blocks 內之常數與 _cw），
# 產器改閾则本器自動跟隨；求不到即如實退（缺尺即無尺，不以記憶補數）。
sys.path.insert(0, os.path.join(ROOT, '_print'))
_ARGV = sys.argv[:]
sys.argv = ['build39.py']                              # 產器於匯入時讀 argv 定模式，須剝去本器之參數
import build39 as _B39                                   # noqa: E402
sys.argv = _ARGV
_cw = _B39._cw
BSRC = io.open(os.path.join(ROOT, '_print', 'build39.py'), encoding=u'utf-8').read()
_m = re.search(r'(MAXF, MINF, LH, PAD, KEEP_H = [0-9., ]+)', BSRC)
assert _m, u'產器之閾不可求（build39 已改形，本器須跟改）'
MAXF, MINF, LH, PAD, KEEP_H = eval(_m.group(1).split('=', 1)[1])
_c = re.search(r'(CONTENT_W = \(210 - \d+\) / 25\.4 \* 72)', BSRC)
assert _c, u'產器之版寬不可求'
CONTENT_W = eval(_c.group(1).split('=', 1)[1])
print(u'口徑取於產器｜版寬 %.1fpt・字級 %.1f–%.1f・行高 %.2f・鎖頁上限 %.0fpt' % (
    CONTENT_W, MINF, MAXF, LH, KEEP_H))


def to_int(tok):
    if tok.isdigit():
        return int(tok)
    R = {u'i': 1, u'v': 5, u'x': 10, u'l': 50, u'c': 100, u'd': 500, u'm': 1000}
    if not tok or any(c not in R for c in tok):
        return None
    vals = [R[c] for c in tok]
    n = 0
    for k, v in enumerate(vals):
        n += -v if (k + 1 < len(vals) and v < vals[k + 1]) else v
    return n


d = pymupdf.open(PDF)
NP = d.page_count
TEXT = [norm(d[i].get_text()) for i in range(NP)]
print(u'%s｜%d 頁・%d KB' % (os.path.basename(PDF)[:40], NP, os.path.getsize(PDF) // 1024))

# ── 甲・大綱逐條：其頁確見其題（取題之頭十二字為窗）
toc = d.get_toc()
hit = miss = 0
for lv, ti, pg in toc:
    w = norm(ti)[:12]
    if w and w in TEXT[pg - 1]:
        hit += 1
    else:
        miss += 1
        bad.append((u'甲', lv, ti[:24], pg))
print(u'甲・大綱 %d 條：頁上確見其題 %d・未中 %d' % (len(toc), hit, miss))

# ── 乙・頁腳：印出之頁碼須等於物理頁（卷首roman・正文阿拉伯；封面與無頁碼者如實分桶）
foot_ok = foot_no = nofoot = wrong = 0
ROM = set(u'ivxlcdm')
for i in range(NP):
    raw = [l.strip() for l in d[i].get_text().split(u'\n')]
    cand = [t for t in raw if t and (t.isdigit() or (len(t) <= 8 and all(c in ROM for c in t)))]
    v = to_int(cand[0]) if cand else None
    if v is None:
        nofoot += 1
        continue
    if v == i + 1:
        foot_ok += 1
    else:
        wrong += 1
        bad.append((u'乙', i + 1, cand[0]))
print(u'乙・頁腳：相符 %d・不合 %d・無頁碼 %d（封面與空白頁如實不入判）' % (foot_ok, wrong, nofoot))

# ── 丙・圍欄段之起訖同頁（43 段；跨頁即版式之病，非字句之病）
FEN, op = [], None
for i, l in enumerate(LINES):
    if l.strip().startswith(u'```'):
        if op is None:
            op = i
        else:
            FEN.append((op, i))
            op = None
same = split = notfound = 0
NARROW = []
PRE = []
for a, b in FEN:
    body = [norm(x) for x in LINES[a + 1:b] if norm(x)]
    src = LINES[a + 1:b]
    nl = sum(1 for x in src if x.strip())
    wmax = max(_cw(x) for x in src) if src else 1
    size = max(MINF, min(MAXF, round(CONTENT_W / max(1.0, 0.55 * wmax + PAD), 2)))
    fits = (nl * size * LH + 6) <= KEEP_H                      # 與產器同算式，不另立口徑
    PRE.append((a + 1, nl, wmax, size, fits))
    if not body:
        continue
    f, g = body[0][:14], body[-1][:14]
    pf = next((k for k in range(NP) if f and f in TEXT[k]), None)
    pg = next((k for k in range(pf if pf is not None else 0, NP) if g and g in TEXT[k]), None) if pf is not None else None
    if pf is None or pg is None:
        notfound += 1
        bad.append((u'丙', a + 1, u'起訖不可求'))
    elif pf == pg:
        same += 1
    elif not fits:
        # 產器之則（build39.fit_pre_blocks）：高過 KEEP_H 之段**如實不鎖**（鎖之即生大塊空白），
        # 故其跨頁乃版式之裁而非病。**例外須立案**：跨頁者須經同一算式判為不可鎖，否則即紅。
        NARROW.append((a + 1, nl, size, pf + 1, pg + 1))
    else:
        split += 1
        bad.append((u'丙', a + 1, u'產器判為可鎖（%d 行×%gpt 高 %d＜閾 %d）而印面猶跨頁 p%d→p%d'
                    % (nl, size, int(nl * size * LH + 6), int(KEEP_H), pf + 1, pg + 1)))
print(u'丙・圍欄 %d 段：同頁 %d・病理性跨頁 %d・起訖不可求 %d・超閾如實不鎖 %s' % (
    len(FEN), same, split, notfound,
    u'（%s）' % u'、'.join(u'L%d %d 行 %gpt p%d→p%d' % x for x in NARROW) if NARROW else u'無'))

# ── 戊・圍欄之字級（細字即印場難讀，須讓日誌看見——165 輪之誡）
small = [x for x in PRE if x[3] < 9.0]
print(u'戊・字級：最細 %gpt・最粗 %gpt｜9pt 以下 %d 段%s' % (
    min(x[3] for x in PRE), max(x[3] for x in PRE), len(small),
    u'（%s）' % u'、'.join(u'L%d %gpt' % (x[0], x[3]) for x in small) if small else u'無'))

# ── 丁・附錄與產物
LU = u'\u9304'                                          # 錄（U+9304；U+530C 乃『厌』，前誤以構錨遂報 0 篇）
apps = [l[2:26] for l in LINES if l.startswith(u'# \u9644') and LU in l[:8]]
inpdf = [t for t in apps if norm(t)[:10] in u''.join(TEXT)]
print(u'丁・附錄 H1 %d 篇，俱見於冊 %d 篇%s' % (len(apps), len(inpdf),
      u'' if len(inpdf) == len(apps) else u'・缺：%s' % [t for t in apps if t not in inpdf]))
for q in [x for x in os.listdir(os.path.join(ROOT, u'_print')) if x.startswith(u'ver39') and x.endswith(('.pdf', '.docx'))
          and u'\u7b2c\u4e09\u5341\u4e5d\u7248' in x]:
    print(u'      %s｜%d KB｜%s' % (q[:52], os.path.getsize(os.path.join(ROOT, u'_print', q)) // 1024,
                                   __import__('time').strftime('%m-%d %H:%M', __import__('time').localtime(
                                       os.path.getmtime(os.path.join(ROOT, u'_print', q))))))
d.close()
print(u'———— 印面覆核（%s）：%s%s' % (
    WHICH, u'全中' if not bad else u'有項待判 %d' % len(bad),
    u'｜陳印強量・此果不充綠（〇・同期未過）' if STALE else u''))
for x in bad[:10]:
    print(u'      ✗ %s' % u'｜'.join(str(y) for y in x))
sys.exit(3 if STALE else (1 if bad else 0))
