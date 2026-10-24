# -*- coding: utf-8 -*-
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GO = "--go" in sys.argv
sys.path.insert(0, ROOT)
import hulan_path as HP

# 一・L3174 剪貼重複（外路所指屬實）：同一半句黏了兩遍，削其第二枚
DUP_OLD = u"開緣（第72條側）保留了修行的次序之爭：開緣保留了修行的次序之爭："
DUP_NEW = u"開緣（第72條側）保留了修行的次序之爭："

# 二・引號外之『却』歸全書通例作『卻』（卻 113 枚 vs 却 20 枚，俱歷輪手洩）
#     留：L4344『却後七年』、L4351『却水』——此二乃本律語（大正一律作『却』），改之即破文獻；
#     引號內 8 枚（如『却後十日當還』）照錄語料，一律不動。
LINES_Q = [1476, 2511, 3035, 3380, 3489, 3784, 4143, 4418, 4461,
           4756, 5302, 5482, 5492, 5500, 5548, 5839, 5876, 6057]

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
NL = u"\r\n" if u"\r\n" in raw else u"\n"
lines = raw.split(NL)
n0, cr0 = len(lines), raw.count(u"\r\n")
print(u"正本行 %d｜CR %d｜通例：卻 %d／却 %d" % (n0, cr0, raw.count(u"卻"), raw.count(u"却")))

bad = []
if raw.count(DUP_OLD) != 1:
    bad.append(u"剪貼錨命中 %d（期 1）" % raw.count(DUP_OLD))
nq = 0
for ln in LINES_Q:
    l = lines[ln - 1]
    if u"却" not in l:
        bad.append(u"L%d 無『却』" % ln)
    elif l.count(u"却") != 1:
        bad.append(u"L%d 有『却』%d 枚，不唯一" % (ln, l.count(u"却")))
    else:
        nq += 1
for keep in (4344, 4351):
    if u"却" not in lines[keep - 1]:
        bad.append(u"L%d 應留而查無『却』" % keep)
print(u"卻字待歸位 %d 行｜律語留 %d 行｜引號內照錄 8 枚" % (nq, 2))
if bad:
    for b in bad:
        print(u"  ✗ " + b)
    sys.exit(1)
if not GO:
    sys.exit(u"試跑畢；加 --go 方寫")

for ln in LINES_Q:
    lines[ln - 1] = lines[ln - 1].replace(u"却", u"卻", 1)
out = NL.join(lines)
assert DUP_OLD in out
out = out.replace(DUP_OLD, DUP_NEW, 1)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(out)

back = io.open(HP.SRC, encoding="utf-8", newline="").read()
errs = []
if len(back.split(NL)) != n0 or back.count(u"\r\n") != cr0:
    errs.append(u"行數或 EOL 走樣：%d/%d" % (len(back.split(NL)), back.count(u"\r\n")))
if DUP_OLD in back or DUP_NEW not in back:
    errs.append(u"剪貼之修未立")
if back.count(u"却") != 10:                      # 8 引號內＋2 律語（却後／却水）
    errs.append(u"『却』殘留 %d 枚（期 10）" % back.count(u"却"))
if back.count(u"卻") != raw.count(u"卻") + nq:
    errs.append(u"『卻』增量不合：%d→%d（期 +%d）" % (raw.count(u"卻"), back.count(u"卻"), nq))
print(u"== 回讀：%s ==" % (u"全中（却 8 照錄＋2 律語｜卻 +%d）" % nq) if not errs else u"有失")
for e in errs:
    print(u"  ✗ " + e)
sys.exit(1 if errs else 0)
