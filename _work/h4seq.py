# -*- coding: utf-8 -*-
"""第七十二輪軸一：各節 H4 款序之連續性與重複（含漢字序與阿拉伯序，及『十至十三』式合款）。

產出：① 每一 H3 節內 H4 之序數列；② 缺號、重號、倒序、跳號者列出待人工斷。
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
if len(sys.argv) > 1:                      # 負測用：植病之副本可另路注入，主檔路徑為預設
    DOC = open(sys.argv[1], encoding='utf-8').read()
LINES = DOC.split('\n')

CN = u'一二三四五六七八九十'
val = {}
for i, c in enumerate(CN[:10]):
    val[c] = i + 1


def cn2num(s):
    if s == u'十':
        return 10
    if s.startswith(u'十'):
        return 10 + val.get(s[1], 0)
    if u'十' in s:
        a, b = s.split(u'十')
        return val.get(a, 1) * 10 + (val.get(b, 0) if b else 0)
    return val.get(s, 0)


def num(s):
    s = s.strip()
    if re.match(r'^\d+$', s):
        return int(s)
    return cn2num(s)


pat = re.compile(u'^(####)\\s+(\\d{1,2}|[一二三四五六七八九十]{1,3})\\s*(?:至\\s*(\\d{1,2}|[一二三四五六七八九十]{1,3}))?\\s*、')
cur_h1 = cur_h2 = cur_h3 = None
seq = []
out = []
for i, l in enumerate(LINES):
    if l.startswith('# '):
        cur_h1 = l[2:].strip()
        cur_h2 = cur_h3 = None
    elif l.startswith('## '):
        cur_h2 = l[3:].strip()
        cur_h3 = None
    elif l.startswith('### '):
        cur_h3 = l[4:].strip()
        seq = []
    elif l.startswith('#### '):
        m = pat.match(l)
        if m:
            a = num(m.group(2))
            b = num(m.group(3)) if m.group(3) else a
            seq.append((a, b, i + 1, l[5:33]))

# 以節為單位報告
prev_key = None
bucket = []
for a, b, ln, t in seq:
    pass

# 重建：走一次，遇 ### 重置
res = []
cur = None
for i, l in enumerate(LINES):
    if l.startswith('### ') and not l.startswith('####'):
        cur = (l[4:].strip(), i + 1, [])
        res.append(cur)
    elif l.startswith('#### '):
        m = pat.match(l)
        if m and cur is not None:
            cur[2].append((num(m.group(2)), num(m.group(3)) if m.group(3) else num(m.group(2)), i + 1))

bad = []
for title, h3ln, items in res:
    if not items:
        continue
    exp = 1
    for a, b, ln in items:
        if a != exp:
            bad.append(u'  %s（H3 L%d）款序 L%d：得 %d，期望 %d｜%s' % (title[:24], h3ln, ln, a, exp, u'' ))
        exp = b + 1
out.append(u'=== 一、各節 H4 款序：應由一起而連續 ===')
out.append(u'節數 %d，款數 %d，序數不連續 %d 處' % (len([r for r in res if r[2]]), sum(len(r[2]) for r in res), len(bad)))
out += bad[:40]

out.append(u'')
out.append(u'=== 二、〔◈本書法式·現代治理指針〕計數與書中宣稱 ===')
n = DOC.count(u'\u25c8')
out.append(u'  ◆ 全書 ◈ 字出現 %d 次' % n)
for m in re.finditer(u'[^\n]{0,40}\u25c8[^\n]{0,10}(?:\u51e1|\u5171)\\s*(\\d+|[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+)\\s*[\u8655\u9805\u689d]', DOC):
    out.append(u'  宣稱：' + m.group(0)[:90])
for m in re.finditer(u'[^\n]{0,50}(\u51e1|\u5171)\\s*(\\d{2,3})\\s*[\u8655\u9805](?=.{0,24}\u25c8)', DOC):
    out.append(u'  宣稱(倒裝)：' + m.group(0)[:90])
# 三、散文行首之手寫序號（一、二、…）之連貫——第 125 輪立
#     病緣：新條插入時只改自身之號，未隨動其下舊條，遂成『一→三→二』或『三、三』；
#     上軸但取標題（####）之款序，此類號生在散文行首，故另走一串一查。
HEADP = re.compile(u'^(?:\\*\\*)?(十[一二三四五六七八九]?|[一二三四五六七八九])[、．]\\s*(?:\\*\\*)?')
chains, cur2 = [], []
for i, l in enumerate(LINES):
    m = HEADP.match(l)
    if m and num(m.group(1)):
        if cur2 and i - cur2[-1][0] > 2:
            chains.append(cur2)
            cur2 = []
        cur2.append((i, num(m.group(1))))
    elif l.strip():
        if cur2:
            chains.append(cur2)
            cur2 = []
if cur2:
    chains.append(cur2)
pro_bad, nchain = [], 0
for c in chains:
    if len(c) < 2:
        continue
    nchain += 1
    nums = [v for _, v in c]
    if nums != list(range(1, len(nums) + 1)):
        pro_bad.append(u'  L%d–%d：%s｜%s' % (c[0][0] + 1, c[-1][0] + 1,
                                             u'→'.join(str(v) for v in nums),
                                             LINES[c[0][0]][:30]))

out.append(u'')
out.append(u'=== 三、散文行首手寫序號之連貫（卷首警示、編年條下分項皆入掃） ===')
out.append(u'串數 %d（長≥2），不連貫 %d 處' % (nchain, len(pro_bad)))
out += pro_bad[:40]
open(os.path.join(HERE, 'h4seq.txt'), 'w', encoding='utf-8').write(u'\n'.join(out))
print(u'H4 款序不連續 %d 處｜散文手寫序號：串 %d 組、不連貫 %d 處' % (len(bad), nchain, len(pro_bad)))
for s in pro_bad[:40]:
    print(s)
sys.exit(1 if (bad or pro_bad) else 0)
