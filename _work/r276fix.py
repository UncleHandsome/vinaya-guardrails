# -*- coding: utf-8 -*-
"""276 輪・第六章新稿之清理與歸自制（一檔一次，冪等：一律自 `_work/r276c.md` 重敷 ➔ `_work/r276d.md`）。

四事：
  甲・**段級交付殘跡**：以『發送／圓滿／審閱／本次推進內容』為鑰，逐行切除並全數印出（標題級殘跡已由 v39draft 切）；
  乙・**名相歸制**：解耦➔分立・『某某令』➔禁約・未證自創語「」➔『』；
  丙・**逐字回查之真文重建**：三处掛《四分律》卷次而文非語料者，**自語料原位切片**回填（復核 `_tk.classify`＝hit 方寫）；
  丁・**分隔線之重複**：切除後相連之『---』斂為一枚。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276fix.py [--go]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                                        # noqa: E402

SRC = os.path.join(ROOT, u'_work', u'r276c.md')
DST = os.path.join(ROOT, u'_work', u'r276d.md')
GO = u'--go' in sys.argv
L = io.open(SRC, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').rstrip(u'\n').split(u'\n')
log = []

# ── 甲・段級殘跡（逐行判，全數印出）
META = re.compile(u'^\\*\\((.*(發送|結卷|審閱|推進).*)\\)\\*$')
SEND = re.compile(u'^這是\\*\\*全新重構版.*發送')
PLAN = re.compile(u'^本次推進內容：\\s*$')
keep, i = [], 0
while i < len(L):
    l = L[i]
    if META.match(l.strip()) or SEND.match(l.strip()):
        log.append(u'甲｜切 L%d｜%s' % (i + 1, l.strip()[:56]))
        i += 1
        continue
    if PLAN.match(l.strip()):
        j = i + 1
        while j < len(L) and (L[j].strip() == u'' or L[j].strip().startswith(u'*')):
            if L[j].strip().startswith(u'*'):
                log.append(u'甲｜切 L%d｜%s' % (j + 1, L[j].strip()[:56]))
            j += 1
        log.append(u'甲｜切 L%d｜本次推進內容：（連其下 %d 行要目）' % (i + 1, j - i - 1))
        i = j
        continue
    keep.append(l)
    i += 1
L = keep

# ── 乙・名相歸制（每項斷言錨數）
def rep(old, new, tag, want=1):
    global L
    n = sum(x.count(old) for x in L)
    assert n == want, u'%s｜錨非 %d（得 %d）：%s' % (tag, want, n, old[:26])
    L = [x.replace(old, new) for x in L]
    log.append(u'乙｜%s（%d 處）' % (tag, n))


rep(u'意志迎合的本質解耦', u'意志迎合的本質分立', u'解耦➔分立')
rep(u'補入第三值預防禁令', u'補入第三值預防禁約', u'預防禁令➔禁約')
rep(u'【常態公堂絕對排除令】', u'【常態公堂絕對排除禁約】', u'排除令➔禁約')
rep(u'依《波逸提法》「作疑惱戒」從嚴反坐審查者',
    u'依『作疑惱』之制從嚴反坐審查者', u'作疑惱戒：撤逐字之掛而歸名相')
# 三枚虛指之節級指針（276 量：『三認知層次』『罪刑法定檢核』俱在第三章閘門二，新稿誤掛第一章）
rep(u'第一章「三認知層次」', u'第三章閘門二之『認知三層次』', u'三認知層次歸閘門二')
rep(u'依第一章第四節確立之「罪刑法定原則」', u'依第三章閘門二確立之『罪刑法定檢核』', u'罪刑法定歸閘門二')
rep(u'第一章第三節「三認知層次」', u'第三章閘門二之『三認知層次』', u'檀尼迦案之認知指針')

# ── 丙・逐字回查重建（語料切片，先核 hit 方用）
V = _tk.VINAYA


def frag(start_key, end_key, tag):
    i = V.find(start_key)
    assert i >= 0, u'語料無起錨：%s｜%s' % (tag, start_key[:14])
    j = V.find(end_key, i)
    assert j >= 0, u'語料無訖錨：%s｜%s' % (tag, end_key[:14])
    s = V[i:j + len(end_key)]
    kind, det = _tk.classify(s)
    assert kind == 'hit', u'語料切片不自證：%s（%s）' % (tag, kind)
    log.append(u'丙｜%s：%d 字（語料原段 L%d，classify=%s）' % (tag, len(s), V[:i].count(u'\n') + 1, kind))
    return s


牛 = frag(u'時得剎尸羅國復有長者', u'婆羅門牛得勝長者牛不如', u'黑牛本事（實為力牛之報恩因緣）')
善 = frag(u'爾時佛語諸比丘凡人欲有所說', u'能不有慚愧耶', u'善語惡語之敕')
衣 = frag(u'爾時佛在舍衛國祇樹給孤獨園世尊聽諸比丘持三衣不得長', u'藏舉', u'六群畜長衣之事相')
衣2 = frag(u'諸比丘見已語六群比丘言佛聽持三衣不得長', u'是我等長衣', u'六群長衣之問答')
衣戒 = frag(u'自今已去聽畜長衣齊十日', u'尼薩耆波逸提', u'長衣十日之戒文')
餘 = frag(u'時世尊以無數方便呵責闡陀比丘已告諸比丘自今已去聽白已', u'聽白已當名作餘語', u'作餘語之白')
舉 = frag(u'云何僧與作不同住僧與作不見犯羯磨', u'是為僧與作不同住', u'三種擯舉之不同住')

BQ = u'> '
new_毀 = [BQ + u'**《四分律》卷十一（波逸提法第二條·毀呰語戒）·大正藏 No. 1428**  ',
           BQ + u'「時六群比丘斷諍事種類罵比丘，比丘慚愧忘失前後不得語。」……  ',
           BQ + u'「爾時佛語諸比丘：『凡人欲有所說，當說善語、不應說惡語。』……『' + 牛 + u'』……」  ',
           BQ + u'「『' + 善 + u'』……『欲說戒者當如是說：若比丘種類毀呰語者，波逸提。』」']
new_衣 = [BQ + u'**《四分律》卷四（初分·三十捨墮法之一·長衣戒）·大正藏 No. 1428**  ',
          BQ + u'「' + 衣 + u'……『' + 衣2 + u'……』」  ',
          BQ + u'「『' + 衣戒 + u'。』」']
new_舉 = [BQ + u'**《四分律》卷四十五（呵責犍度第十一之餘·作餘語與三舉）·大正藏 No. 1428**  ',
          BQ + u'「『我不見罪，云何言我有罪？』……『' + 餘 + u'。』……  ',
          BQ + u'『' + 舉 + u'。』」']


def replace_block(head_key, n_lines, newlines, tag):
    """以『某行起・連 n 行』之式換块；錨須唯一，換後即核。"""
    global L
    idx = [i for i, x in enumerate(L) if head_key in x]
    assert len(idx) == 1, u'%s｜出處錨非一（得 %d）' % (tag, len(idx))
    a = idx[0]
    assert a + n_lines <= len(L), u'%s｜块越界' % tag
    log.append(u'丙｜重建 %s：L%d..L%d ➔ %d 行' % (tag, a + 1, a + n_lines, len(newlines)))
    L = L[:a] + newlines + L[a + n_lines:]


replace_block(u'（波逸提法第二條·毀呰語戒）·大正藏', 5, new_毀, u'毀呰語回查块')
replace_block(u'（初分·三十捨墮法之一·第一條長衣戒）·大正藏', 3, new_衣, u'長衣回查块')
replace_block(u'（呵責犍度第十一之餘·作不見罪舉）·大正藏', 2, new_舉, u'不見罪回查块')

# ── 丁・分隔線與空行：相連者斂一；隔隔線前后各留一空行；連綴空行收一
out = []
for l in L:
    if l.strip() in (u'---', u'--'):
        while out and out[-1].strip() == u'':
            out.pop()
        if out and out[-1].strip() == u'---':
            continue
        out.append(u'---')
    else:
        out.append(l)
L2 = []
for l in out:
    if l.strip() == u'---':
        if L2 and L2[-1] != u'':
            L2.append(u'')
        L2.append(l)
        continue
    if l.strip() == u'' and (not L2 or L2[-1] == u''):
        continue
    L2.append(l)
while L2 and L2[-1] == u'':
    L2.pop()
L2.append(u'')
log.append(u'丁｜分隔線：%d ➔ %d｜行數 %d ➔ %d' % (
    sum(1 for x in L if x.strip() in (u'---', u'--')),
    sum(1 for x in L2 if x.strip() == u'---'), len(L), len(L2)))
L = L2

print(u'\n'.join(log))
print(u'輸出 %d 行（原 %d）' % (len(L), len(io.open(SRC, encoding=u'utf-8').read().split(u'\n'))))
if not GO:
    print(u'（dry-run｜加 --go 方落盤）')
    sys.exit(0)
io.open(DST, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(L) + u'\n')
print(u'落盤 %s' % DST)
