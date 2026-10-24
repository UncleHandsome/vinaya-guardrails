# -*- coding: utf-8 -*-
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
MAIN = t[:t.index(u'# 【卷末')]

print(u'== 第十二章案例十四 全文 ==')
a = next(i for i, l in enumerate(L, 1) if l.startswith(u'### 案例十四：涅槃日哀慟'))
b = next(i for i in range(a + 1, len(L)) if L[i - 1].startswith((u'### ', u'## ')))
print(u'\n'.join(x[:110] for x in L[a - 1:b]))

print(u'\n== 條號之出处分类（正文區）==')
VINAYA = [u'波逸提', u'僧伽婆尸沙', u'尼薩耆', u'式叉迦羅尼', u'婆尸沙', u'提舍尼', u'波羅夷',
          u'學法', u'戒本', u'犍度', u'四分律', u'律', u'篇', u'章', u'節', u'款', u'經', u'眾法']
rows = []
for m in re.finditer(u'第\\s*[0-9０-９]{1,4}\\s*條', MAIN):
    w = MAIN[max(0, m.start() - 22):m.end()]
    if u'法' in w:
        kinds = [k for k in VINAYA if k in w]
        rows.append((MAIN[:m.start()].count(u'\n') + 1, m.group(0), u''.join(kinds), w.replace(u'\n', u' ')))
sec = [r for r in rows if not r[2]]
print(u'  「第N條」前有『法』者 %d 處；其中不類律文篇名者 %d 處' % (len(rows), len(sec)))
for ln, s, k, w in sec:
    print(u'    L%-6d %-10s ‹%s›' % (ln, s, w[-30:]))

print(u'\n== 世俗法名之現形（正文區，凡以『法』結尾之專名）==')
p = re.compile(u'[一-鿿]{2,14}法(?=[・§》\s『「（(第0-9０-９])')
seen = {}
for m in p.finditer(MAIN):
    s = m.group(0)
    if any(v in s for v in VINAYA[:-4]):
        continue
    seen.setdefault(s, []).append(MAIN[:m.start()].count(u'\n') + 1)
for s, v in sorted(seen.items(), key=lambda x: -len(x[1]))[:26]:
    print(u'    %-22s ×%d  L%s' % (s, len(v), u','.join(str(x) for x in v[:5])))
