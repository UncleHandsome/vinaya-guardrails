# -*- coding: utf-8 -*-
"""通器・新稿六面差分與清理（274 輪之 r274probe/clean2 汎用版，275 輪起覆用於任何章段之換入）。

用法：
  PYTHONIOENCODING=utf-8 python -X utf8 _work/v39draft.py probe <新稿> <起章> <迄章>[-1]   # 只量
  PYTHONIOENCODING=utf-8 python -X utf8 _work/v39draft.py clean <新稿> <輸出> <起章> <迄章> # 清並產檔
六面：甲 交付殘跡（含重複章題・批次 H2・小結預告）／乙 黑話・『某某令』・無號指針／丙 簡形／
      丁 案例指針之**歸屬面**（名須見於本號卡身，第 27 目之盲處）／戊 掛出處之逐字宣稱／
      己 章節之形（與今冊對應區一比：節題・H2/H3/H4・圍欄・指針之數）。
名單不兩抄：禁詞・黑話・代號一律自 `_work/v39chk.py` 之源以 ast 取字面。
"""
import ast
import glob
import io
import os
import re
import sys
import contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, '_work'))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
BOOK = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
CHK = io.open(os.path.join(ROOT, u'_work', u'v39chk.py'), encoding=u'utf-8').read()


def lit(name):
    m = re.search(u'%s = \\[((?:.|\\n)*?)\\n?\\]' % name, CHK)
    return ast.literal_eval(u'[' + m.group(1) + u']') if m else []


PROMPT, JARGON, CODES = lit('PROMPT'), lit('JARGON'), lit('CODES')
assert PROMPT and JARGON and CODES, u'名單不可空'
# 殘跡之標題鑰：批次・回数・交付語（只flag標題，不动正文）
NARR = re.compile(u'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+\u56de|\u5171[\u4e00\u4e8c\u4e09\u56db\u4e94]+\u56de'
                  u'|交付|小結|預告|圓滿|呈辭|驗收|定本|發送')
# 「接力」不入鑰——今稿之正經小節有「管轄接力」之語，舊版以flag誤切 14 行（275 輪量得）
# 「總結」「公約」不入鑰——276 輪量得：第六章新稿之正文有「雙螺旋專題法理合龍總結」六枚與
# 「本章的三大重構公約」一枚，皆作者自設之正經小節；歷輪之交付殘跡另有「交付/回/圓滿/預告」可捕，
# 故刪此二詞以保正文。**切刀之闊，一律以誤傷之字證之。**
HEAD = re.compile(u'^(#{1,6}) +(.*)$')


def load(path):
    return io.open(path, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').rstrip(u'\n').split(u'\n')


def headings(L):
    return [(i, len(m.group(1)), m.group(2).strip()) for i, l in enumerate(L) if (m := HEAD.match(l))]


def flagged(L):
    """回傳 (被flag之標題行索引集合, 説明)。重複之 H1 亦flag（分批交付必重覆章題）。"""
    seen, out = {}, {}
    hs = headings(L)
    for i, lv, ti in hs:
        if lv == 1 and ti in seen:
            out[i] = u'\u91cd\u8907 H1\uff08\u9996\u898b L%d\uff09' % (seen[ti] + 1)
        elif NARR.search(ti[:40]):
            out[i] = u'\u6279\u6b21/\u4ea4\u4ed8\u984c\uff1a' + ti[:32]
        if lv == 1 and ti not in seen:
            seen[ti] = i
    return out, hs, seen

def spans(L):
    """切除範圈：每個被flag之標題，切至下一個**未flag**之 ≤3 級標題前。另加首行前之頁眉。"""
    fl, hs, seen = flagged(L)
    cut, why = set(), []
    order = [i for i, lv, ti in hs]
    for k, i in enumerate(order):
        if i not in fl:
            continue
        j = len(L)
        for m in range(k + 1, len(order)):
            q = order[m]
            lv = HEAD.match(L[q]).group(1).__len__()
            if lv <= 3 and q not in fl:
                j = q
                break
        cut.update(range(i, j))
        why.append((i + 1, fl[i], j - i))
    first = next((i for i in order if i not in fl and HEAD.match(L[i]).group(1).__len__() == 1), None)
    if first:
        cut.update(range(0, first))
        why.insert(0, (1, u'\u9996\u9801\u984c\u524d\u4e4b\u4ea4\u4ed8\u9801\u7709', first))
    return cut, why, fl, hs


def bookspan(a, b):
    ia = next(i for i, l in enumerate(BOOK) if l.startswith(u'# ' + a))
    ib = next(i for i, l in enumerate(BOOK) if l.startswith(u'# ' + b))
    return BOOK[ia:ib]


def report(path, a, b):
    L = load(path)
    T = u'\n'.join(L)
    print(u'\u65b0\u7a3f %d \u884c\uff08\u53bb\u7a7a\u767d %d \u5b57\uff09' % (len(L), len(re.sub(u'\\s', u'', T))))
    cut, why, fl, hs = spans(L)
    print(u'\n\u7532\u30fb\u6b98\u8de1\u5207\u9664 %d \u8655\u3001\u5171 %d \u884c' % (len(why), len(cut)))
    for i, s, n in why:
        print(u'   L%-5d \u5207 %3d \u884c\uff5c%s' % (i, n, s))
    print(u'\n\u4e59\u30fb\u9ed1\u8a71/\u4ee4/\u7121\u865f\u6307\u91dd')
    for w in JARGON + CODES:
        ln = [i + 1 for i, l in enumerate(L) if w in l]
        if ln:
            print(u'   %-8s %d \u898b L%s' % (w, len(ln), ln[:6]))
    LING = re.compile(u'(?:\\*\\*|\u3010)[^*\u3010\u3011\\n]{2,18}\u4ee4(?:\\*\\*|\u3011|\uff1a)')
    print(u'   \u300e\u67d0\u67d0\u4ee4\u300f\u6a19\u984c\u5f62\uff1a%d \u898b %s' % (
        sum(1 for l in L if LING.search(l)), [i + 1 for i, l in enumerate(L) if LING.search(l)][:8]))
    NOREF = re.compile(u'\u3014(?:\u6848\u4f8b|\u88dc\u907a)\u00b7|\u3014(?:\u6848\u4f8b|\u88dc\u907a)\u3015')
    print(u'   \u7121\u865f\u5f62\u5236\uff1a%d \u898b' % len(NOREF.findall(T)))
    with contextlib.redirect_stdout(io.StringIO()):
        import recordsimp
    from _simpdict import MAP as SD
    CORP = set()
    for f in glob.glob(os.path.join(ROOT, u'\u539f\u6587', u'*.txt')):
        CORP |= set(io.open(f, encoding=u'utf-8', errors=u'ignore').read())
    SIMP = (set(recordsimp.S) | set(u'\u4e24\u5f53\u5f3a\u968f\u65e7\u603b')
            | (set(SD) - {c for c in SD if c in CORP}))
    hits = sorted({c for c in T if c in SIMP})
    print(u'\n\u4e19\u30fb\u7c21\u5f62 %d \u679a\uff1a%s' % (len(hits), ' '.join('U+%04X' % ord(c) for c in hits)))
    # 丁・歸屬面
    from difflib import SequenceMatcher
    heads = [(i, l) for i, l in enumerate(BOOK) if re.match(u'^### \u3014\u6848\u4f8b [0-9]+\u3015', l)]
    BODY = {}
    for k, (i, l) in enumerate(heads):
        num = re.match(u'^### \u3014\u6848\u4f8b ([0-9]+)\u3015(.*)$', l)
        end = heads[k + 1][0] if k + 1 < len(heads) else len(BOOK)
        end = next((j for j in range(i + 1, end) if BOOK[j].startswith(u'#')), end)
        BODY[num.group(1)] = (re.sub(u'\\s+', u'', num.group(2)),
                              re.sub(u'\\s+', u'', u''.join(BOOK[i:end])))
    nm_ok = nm_no = 0
    for i, l in enumerate(L):
        for m in re.finditer(u'\u3014\u6848\u4f8b ?([0-9]{1,3})\u3015\\s*(?:\\*\\*)?([\u4e00-\u9fff]{2,12})', l):
            n = m.group(1).zfill(2)
            if n not in BODY:
                print(u'   \u26a0 L%-5d \u67e5\u7121\u6b64\u5361\uff1a%s' % (i + 1, n)); nm_no += 1; continue
            nm = re.sub(u'\\s+', u'', m.group(2))
            if nm in BODY[n][1] or BODY[n][0].startswith(nm[:2]):
                nm_ok += 1
            else:
                el = [k for k, (t, bd) in BODY.items() if k != n and len(nm) >= 3 and nm in bd]
                print(u'   \u26a0 L%-5d \u6848\u4f8b %s\u300e%s\u300f\u4e0d\u898b\u65bc\u672c\u865f\u5361\u8eab\uff08\u984c\u300e%s\u300f\uff09%s' % (
                    i + 1, n, m.group(2)[:10], BODY[n][0][:10],
                    u'\uff5c\u898b\u65bc ' + u'\u3001'.join(el[:4]) if el else u'\uff5c\u5168\u66f8\u5361\u8eab\u7686\u7121'))
                nm_no += 1
    print(u'\n\u4e01\u30fb\u5e36\u540d\u6307\u91dd\uff1a\u5f52\u5c6c\u5408 %d・\u5f85\u6c7a %d' % (nm_ok, nm_no))
    # 戊・引文
    with contextlib.redirect_stdout(io.StringIO()):
        import _tk
    tally, bad = {}, []
    for i, l in enumerate(L):
        gates = [g.start() for g in _tk.SRC_STRICT.finditer(l)]
        if not gates:
            continue
        for m in _tk.Q_RE.finditer(l):
            if not any(g < m.start(1) for g in gates):
                continue
            v, _b = _tk.classify(m.group(1))
            k = v if not v.startswith(u'other') else u'other'
            tally[k] = tally.get(k, 0) + 1
            if v == u'miss':
                bad.append((i + 1, m.group(1)))
    print(u'\u620a\u30fb\u639b\u51fa\u8655\u9010\u5b57\u5ba3\u7a3d %d \u6bb5\uff5c%s' % (sum(tally.values()), tally))
    for i, q in bad:
        ln = L[i - 1]
        gate = u'\u3001'.join(sorted({g.group(0)[:14] for g in _tk.SRC_STRICT.finditer(ln)}))[:40]
        punct = bool(re.search(u'[\uff0c\u3001\uff1b\uff1a\u3002]', q))
        way = (u'\u5be9\u300e\u662f\u5426\u70ba\u66f8\u540d\u865f\u5167\u4e4b\u672c\u5f8b\u7bc7\u540d\u300f' if False else
               (u'\u9577\u53e5\u2192\u9010\u5b57\u5ba3\u7a3d\uff1a\u56de\u586b\u6216\u6539\u300e\u5f8b\u610f\uff1a\u300f\u63aa\u8ff0'
                if (punct or len(q) >= 10) else u'\u77ed\u8a9e\u2192\u6539\u300e\u300e \u300f\u8853\u8a9e\u5f0f\uff08\u51e1\u4f8b\u7b2c\u4e8c\u5f8b\uff09'))
        print(u'   \u26a0 L%-5d \u672a\u4e2d\u3001%d \u5b57\uff5c\u9293\uff1a%s\uff5c%s' % (i, len(q), gate, way))
        print(u'        \u5167\u5bb9\uff5c%s' % q[:64])
    # 己・形
    print(u'\u5df1\u3002\u7bc0\u984c\u4e4b\u5c0d\u6bd4\uff08\u65b0\u7a3d vs \u4eca\u518a %s〜%s\uff09' % (a, b))
    oldseg = bookspan(a, b)
    for lab, seg in ((u'\u65b0', L), (u'\u65e7', oldseg)):
        secs = re.findall(u'(?m)^### \\u7b2c([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+\u7bc0)\u3000(.{0,18})', u'\n'.join(seg))
        print(u'   %s\uff5c\u7bc0 %d\uff1a%s' % (lab, len(secs), u'・'.join(s[0] for s in secs)))
    for lab, seg in ((u'\u65b0', L), (u'\u65e7', oldseg)):
        print(u'   %s\uff5cH2 %d・H3 %d・H4 %d・H5 %d・\u570d\u6b04 %d・\u300c\u300d %d・\u6848\u4f8b\u6307\u91dd %d' % (
            lab, sum(1 for l in seg if l.startswith('## ')), sum(1 for l in seg if l.startswith('### ')),
            sum(1 for l in seg if l.startswith('#### ')), sum(1 for l in seg if l.startswith('##### ')),
            sum(1 for l in seg if l.strip().startswith(u'```')) // 2,
            len(re.findall(u'\u300c[^\u300d]{1,}\u300d', u'\n'.join(seg))),
            len(re.findall(u'\u3014\u6848\u4f8b', u'\n'.join(seg)))))
    # 節題逐一對照（目次同步與第八尺之據）
    def secs(seg):
        ch = u''
        out = []
        for l in seg:
            if l.startswith(u'# '):
                ch = l[2:8].strip()
            m = re.match(u'^### (\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+\u7bc0)\u3000(.+)$', l)
            if m:
                out.append((ch, m.group(1), m.group(2).strip()))
        return out
    so, sn = secs(oldseg), secs([l for i, l in enumerate(L) if i not in cut])
    print(u'   \u7bc0\u984c\u5c0d\u7167\uff08\u65e7 \u2194 \u65b0\uff09\uff1a')
    for k in range(max(len(so), len(sn))):
        a1 = u'%s %s\u3000%s' % (so[k][0], so[k][1], so[k][2]) if k < len(so) else u'\uff08\u7121\uff09'
        b1 = u'%s %s\u3000%s' % (sn[k][0], sn[k][1], sn[k][2]) if k < len(sn) else u'\uff08\u7121\uff09'
        same = (k < len(so) and k < len(sn) and so[k][0] == sn[k][0] and so[k][1] == sn[k][1] and so[k][2] == sn[k][2])
        print(u'   %s %-46s %s %-46s' % (u'  ' if same else u'\u2260\u2260', a1[:44], u'' if same else u'\u2794', b1[:44]))
    # 新稿獨有之 H3 名（供目次與指針之裁）
    onames = {re.sub(u'\\s+', u'', s) for s in re.findall(u'(?m)^### (.+)$', u'\n'.join(oldseg))}
    extra = [l for i, l in enumerate(L) if l.startswith('### ') and re.sub(u'\\s+', u'', l[4:]) not in onames]
    print(u'   \u65b0\u7a3f\u4e4b \u22653 \u7d1a\u65b0\u984c %d \u679e\uff1a%s' % (len(extra), [e[:34] for e in extra[:10]]))


def clean(path, out, a, b):
    L = load(path)
    cut, why, fl, hs = spans(L)
    K = [l for i, l in enumerate(L) if i not in cut]
    # 去重後之重複章題（同 H1 只留首枚）
    T = u'\n'.join(K)
    # 名相歸位：黑話詞→（須人工指名，此處只報不誤改）
    LING = re.compile(u'(\u7981\u4ee4)(?=\u3011|\\*\\*)')
    n2 = len(LING.findall(T))
    T = LING.sub(u'\u7981\u7d04', T)
    # 版式之淨
    LL, out2 = T.split(u'\n'), []
    for l in LL:
        if (len(l) - len(l.rstrip(u' '))) == 1:
            l = l.rstrip(u' ')
        if l.strip() in (u'---', u'***') and out2 and out2[-1].strip():
            out2.append(u'')
        if l.strip() == u'' and len(out2) >= 2 and out2[-1].strip() == u'' and out2[-2].strip() == u'':
            continue
        out2.append(l)
    io.open(out, 'w', encoding=u'utf-8').write(u'\n'.join(out2) + u'\n')
    print(u'\u5207\u9664 %d \u8655\u3001%d \u884c\uff5c\u7981\u4ee4\u2794\u7981\u7d04 %d \u8655\uff5c\u8f38\u51fa %s (%d \u884c)' % (
        len(why), len(cut), n2, os.path.basename(out), len(out2)))
    for w in JARGON:
        if w in u'\n'.join(out2):
            print(u'   \u26a0 \u9ed1\u8a71\u300e%s\u300f\u733a\u5728\u6e05\u7a3f\uff0c\u9808\u4eba\u5de5\u5b9a\u5176\u6539' % w)
    for l in out2:
        if re.search(u'(?:\\*\\*|\u3010)[^*\u3010\u3011\\n]{2,18}\u4ee4(?:\\*\\*|\u3011|\uff1a)', l):
            print(u'   \u26a0 \u300e\u4ee4\u300f\u6a19\u984c\u5f62\u733a\u5728\uff1a%s' % l[:44])


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == u'probe':
        report(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        clean(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
