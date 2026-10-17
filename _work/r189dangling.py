# -*- coding: utf-8 -*-
"""r189dangling.py —— 行末懸領與硬換行落空之自掘軸（第 189 輪立・待診・恆退 0）。

緣起：散文句末以『：』或『——』收而**其後無所領**，與 168 軸所列『項之有領無續』同族，然 168 唯校列項，
散文行之懸領向無器；行尾之硬換行（兩個以上半形空格）若落在段末，紙上 <br> 無所指，亦是同類之『空诺言』。
此兩維純然可量，不需讀文意。

口徑（四修之後之定形，初版之盲俱記於下）：
 ① 印面為界（擯底冊與圍欄）；表列行與標題行不預。
 ② **行末之標點先剝行尾空格**再判『：』『——』收。
 ③ 甲·懸領之判：自本行之後**跳過空行、空引言行（『>』）、分隔線**，若先到者是一行內文（含列項、表、圖、引塊正文）
    ⇒ 領有所屬，非病；若先到者又是**標題**，則查該標題之下直至下一標題之前有無內文——無內文方是真懸領。
    （初版把『其後即表列／圍欄／標題／分隔』一律算病，得 105 筆；親量則盡屬『冒號領表』『冒號領圖』『冒號領下列子標題』
    之本書常式——**器不分层即以常式為病**，159／188 兩輪之教再驗。）
 ④ 乙·硬換行落空：行尾 ≥2 空格而其後直至本段之末再無內文（即 <br> 無所指）。
 ⑤ 丙·空引言行（『> 』尾隨一格）與『』內之尾隨空格俱屬**製式**，只計不判。
    （初版把『> 』算作尾隨單空格行，得 72 筆假訊號——實測 74 枚單空格尾行**全數**是空引言行。）
退出碼：恆 0（待診）。`argv[1]`＋`require-hit` 供負測（唯甲／乙計入 hit）。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

if COP:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    BOT, inb = set(), False
    for i, l in enumerate(L):
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

FENCE = chr(96) * 3
fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(FENCE):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf

COLON = re.compile(u'[：:]\s*$')
DASH = re.compile(u'——\s*$')


def is_skip(j):
    s = L[j].strip()
    return (not s) or s == u'>' or s in (u'---', u'***', u'___') or s.startswith(FENCE[:3])


def is_head(j):
    return L[j].strip().startswith(u'#')


def content_after_head(j):
    """標題 j 之下、下一標題之前，有無實文。"""
    k = j + 1
    while k < len(L) and not is_head(k) and not L[k].strip().startswith(u'|'):
        if L[k].strip() and L[k].strip() != u'>' and not is_skip(k):
            return True
        k += 1
        if k - j > 400:
            break
    return False


def first_solid(i):
    j = i + 1
    while j < len(L) and is_skip(j):
        j += 1
    return j if j < len(L) else None


rows = {u'甲': [], u'乙': [], u'丙': []}
n_quote_blank = 0
for i, l in enumerate(L):
    if i in BOT or fence[i]:
        continue
    s = l.rstrip(u' ')
    if not s or s.startswith(u'|') or is_head(i):
        continue
    if s.strip() == u'>':
        n_quote_blank += 1
        continue
    j = first_solid(i)
    if (COLON.search(s) or DASH.search(s)):
        if j is None:
            rows[u'甲'].append((i + 1, s[-46:], u'文盡'))
        elif is_head(j):
            if not content_after_head(j):
                rows[u'甲'].append((i + 1, s[-46:], u'標題下亦無文'))
    trail = len(l) - len(s)
    if trail >= 2 and (j is None or is_head(j)):
        rows[u'乙'].append((i + 1, s[-46:], u'段末硬換'))

print(u'行末兩維：甲·懸領無所屬 %d｜乙·硬換行落空 %d｜（空引言行製式 %d 枚，只計不判）'
      % (len(rows[u'甲']), len(rows[u'乙']), n_quote_blank))
for kk in (u'甲', u'乙'):
    for ln, tail, why in rows[kk][:10]:
        print(u'  %s L%-6d %s｜…%s' % (kk, ln, why, tail))
with io.open(u'_work/r189list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for kk in (u'甲', u'乙'):
        f.write(u'═══ %s：%d ═══\n' % (kk, len(rows[kk])))
        for ln, tail, why in rows[kk]:
            f.write(u'%s\tL%d\t%s\t…%s\n' % (kk, ln, why, tail))
print(u'清冊：_work/r189list.txt')
if COP and REQ:
    sys.exit(0 if (rows[u'甲'] or rows[u'乙']) else 1)
sys.exit(0)
