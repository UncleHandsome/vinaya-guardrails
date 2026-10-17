# -*- coding: utf-8 -*-
r"""r216loc.py —— 語料行號指針之可達、不虛、副其所引（第 216 輪立，**升閘：三判任一即退 1**）。

緣起：附錄H〔補遺〕諸則與部分正條之『文獻定位』以『NN-MM卷段 L754–758』式指針標明律文在本地
語料檔之何行——此是本書**唯一可由讀者自行覆驗**之憑據（按卷段開檔、依號求行、逐字對引）。
歷輪諸軸校章級指針（`r195ref`）、版面承接（`anchorref`）、詞條級指針（`termref`）、案號連貫
（`r213case`），**行號級之語料指針向無守者**。語料檔今為靜態（六檔不改），而書稿屢增屢刪，
新寫之指針最易犯三病：號超出檔行數、號落在檔之空行、號在而其所引之文其實在他行。

口徑：
 ① 印面為界（擯 `_tk.bottom_lines()` 與圍欄）；副本注入時以 `argv[1]` 並自算其底冊界（各檔自算其界）。
 ② 指針形：`L123`；連號式 `L754–758`（`–—~至` 俱識）取其全段。
 ③ 卷段標 `(\d{1,2})-(\d{1,2})卷段` 統領其後之指針（同列枚舉『L318、L320』承前標而不復舉）；
    行內無標則承上三行內最近之標；仍不得者入『無從解』目，**不判**（器之限，如實報數）。
 ③b 行內之標以『指針之前最近者』歸群——一行引兩處（『01-10卷段 L236；50-60卷段 L656』）必錯配，
    此 v2 之失（40 筆假未中）。
 ④ 三判（病）：
    甲 **越界**：段之兩端不在 1..該檔行數；
    乙 **虛行**：該指針之窗（段之各行並擴一行）全為空白行——號存而無文；
    丙 **行號漂**：該行之「」逐字引文確在**其群檔**之他行查得，而不在本群窗內——引真而指錯。
 ⑤ 從寬（不判）：引文在他檔查得者（本書有『引而無指』之常式，其存在性由 `r185orphan` 守）；
    六檔俱查無者（同上）；該行無「」段者（純卷次／篇題之定位指針）；『』之概括語（凡例第一律許其非逐字）。
 ⑥ 引文比對：唯取「」段（≥6 字），依刪節號分段（凡例第二律之節引），兩側俱 `_tk.norm()` 折一
    （刪標點與 markdown 記號），段長 ≥4 方校；群窗以檔之連續行併成一律（引文得越語料兩段）。
退出碼：病 > 0 即退 1；`argv[1]` 注副本以供負測。
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
LINES = (io.open(COP, encoding='utf-8-sig').read() if COP else t.DOC).split(u'\n')

RAW, NRM = {}, {}
for fn in sorted(os.listdir(os.path.join(ROOT, u'原文'))):
    m = re.match(u'(\\d{1,2}-\\d{1,2})', fn)
    if fn.endswith(u'.txt') and m:
        seg = m.group(1)
        RAW[seg] = io.open(os.path.join(ROOT, u'原文', fn), encoding='utf-8-sig').read().split(u'\n')
        NRM[seg] = [t.norm(x) for x in RAW[seg]]
if not NRM:
    print(u'本地無語料檔（原文／*.txt）——本軸無從校，如實報而不充綠燈。')
    sys.exit(0)

FENCE, _in = set(), False
for i, l in enumerate(LINES):
    if l.lstrip().startswith(u'```'):
        _in = not _in
        FENCE.add(i)
    elif _in:
        FENCE.add(i)
if COP is not None:                                   # 副本自算底冊界：逐篇取『其題至下一 H1』
    H1 = [i for i, l in enumerate(LINES) if re.match(u'#(?!#)\\s', l)]
    BOT = set()
    for nm in t.BOTTOM_NAMES:
        for s in [i for i in H1 if nm in LINES[i]]:
            nxt = [h for h in H1 if h > s]
            BOT.update(range(s, nxt[0] if nxt else len(LINES)))
else:
    BOT = t.bottom_lines()

VS = re.compile(u'(\\d{1,2}-\\d{1,2})\\s*卷段')
PP = re.compile(u'L(\\d{1,5})(?:\\s*[\\u2013\\u2014~\\u81f3]\\s*(?:L)?(\\d{1,5}))?')
QT = re.compile(u'「([^」]{6,})」')

nptr = nunseg = jia = yi = 0
groups = {}                                           # (行, seg) -> set(行號)
lineq = {}                                            # 行 -> [segments]
for i, l in enumerate(LINES):
    if i in BOT or i in FENCE or u'L' not in l:
        continue
    vsp = [(m.start(), m.group(1)) for m in VS.finditer(l)]
    carry = None
    j = i - 1
    while carry is None and j >= max(0, i - 3):
        c2 = VS.findall(LINES[j])
        if c2:
            carry = c2[-1]
        j -= 1
    if carry is None:
        for j2 in range(i + 1, min(len(LINES), i + 4)):
            c3 = VS.findall(LINES[j2])
            if c3:
                carry = c3[0]
                break
    got = False
    for m in PP.finditer(l):
        seg = carry
        for st, sg in vsp:
            if st < m.start():
                seg = sg
        if seg is None:
            nunseg += 1
            continue
        got = True
        nptr += 1
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        if b < a:
            a, b = b, a
        NL = NRM.get(seg, [])
        w = set(range(max(1, a - 1), min(len(NL), b + 1) + 1)) if NL else set()
        groups.setdefault((i, seg), set()).update(w)
        if seg not in NRM:
            jia += 1
            print(u'甲 越界｜書L%d｜無『%s』卷段檔' % (i + 1, seg))
            continue
        if not (1 <= a and b <= len(NL)):
            jia += 1
            print(u'甲 越界｜書L%d｜指 %s 檔 L%d–%d（該檔 %d 行）' % (i + 1, seg, a, b, len(NL)))
        if w and all(not RAW[seg][k - 1].strip() for k in w if k <= len(RAW[seg])):
            yi += 1
            print(u'乙 虛行｜書L%d｜指 %s 檔 L%d–%d 而窗內全空行' % (i + 1, seg, a, b))
    qs = []
    for q in QT.findall(l):
        parts = [t.norm(x) for x in re.split(u'\\u2026+', q)]
        parts = [p for p in parts if len(p) >= 4]
        if parts:
            qs.append(parts)
    if got and qs:
        lineq[i] = qs

bad = 0
for i, qs in lineq.items():
    segs = [s for (j, s) in groups if j == i]
    for parts in qs:
        ok = False
        for s in segs:
            NL = NRM[s]
            win = u''.join(NL[k - 1] for k in sorted(groups[(i, s)]) if 1 <= k <= len(NL))
            pos = -1
            for p in parts:
                k2 = win.find(p, pos + 1)
                if k2 < 0:
                    break
                pos = k2
            else:
                ok = True
                break
        if ok:
            continue
        for s in segs:                                  # 其文確在此群檔（依序得見），唯不在群窗？
            whole = u''.join(NRM[s])
            pos = -1
            for p in parts:
                k2 = whole.find(p, pos + 1)
                if k2 < 0:
                    break
                pos = k2
            else:
                print(u'丙 行號漂｜書L%d｜引「%s…」在其 %s 檔他行，而群窗 L%s 之內無此文'
                      % (i + 1, parts[0][:20], s, sorted(groups[(i, s)])))
                bad += 1
                break

print(u'=============================')
print(u'今制｜語料行號指針 %d 枚（涉 %d 行）｜無從解（不判）%d 枚｜群窗可校之「」引文 %d 段'
      % (nptr, len(set(g[0] for g in groups)), nunseg, sum(len(v) for v in lineq.values())))
print(u'病｜越界 %d｜虛行 %d｜行號漂 %d' % (jia, yi, bad))
sys.exit(1 if (jia or yi or bad) else 0)
