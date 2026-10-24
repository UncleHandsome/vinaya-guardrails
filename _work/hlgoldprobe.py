# -*- coding: utf-8 -*-
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP

t = io.open(HP.SRC, encoding="utf-8", newline="").read()
lines = t.split(u"\r\n") if u"\r\n" in t else t.split(u"\n")
GLOB = [io.open(p, encoding="utf-8", errors="replace").read() for p in sorted(glob.glob(os.path.join(ROOT, u"原文", "*.txt")))]
CORP = u"\n".join(GLOB)
NAMES = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(ROOT, u"原文", "*.txt")))]


def find(pat, cap=3, where=u"書"):
    rx = re.compile(pat)
    hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if rx.search(l)]
    print(u"  [%s] %-34s 書中 %d 行" % (where, pat[:34], len(hits)))
    for n, s in hits[:cap]:
        print(u"        L%-5d %s" % (n, s[:112]))
    return hits


def corp(pat):
    return [(NAMES[k], CORP[k].count(pat)) for k in range(len(GLOB)) if CORP[k].count(pat)]


print(u"== 建議 1・第十五章案例七現文 ==")
find(u"百歲|新受戒比丘|起迎", cap=6)
print(u"  『制度妥協』已在書中否：", find(u"制度妥協", cap=4))
print(u"  『Ego-Crushing／挫折慢心』：", find(u"挫折慢心|Ego", cap=3))
print(u"  律據『除因緣』：", find(u"除因緣|有大因緣|因緣故", cap=2))
print(u"  語料：因緣／除因緣 →", corp(u"除因緣"), corp(u"我有如是因緣"))

print(u"\n== 建議 2・4・法域分立與自言治 ==")
find(u"移送|世俗司法|公訴|包庇|家醜", cap=5)
find(u"不自言不應治|自言治", cap=4)

print(u"\n== 建議 3・邊地五人與出罪人數 ==")
find(u"二十人僧|二十清淨|邊地|五人", cap=5)
print(u"  語料『五人』：%s｜『邊地』：%s" % (corp(u"五人"), corp(u"邊地")))
for q in (u"邊五", u"五人僧", u"二十人僧", u"出罪"):
    print(u"  語料 %-8s → %s" % (q, corp(q)))

print(u"\n== 建議 5・帶贓金句 ==")
find(u"帶贓|物不捨盡|先捨後懺|捨已當懺悔|物權返還", cap=5)

print(u"\n== 建議 6・通行譯名混入（真病候）==")
find(u"頻婆娑羅|目犍連", cap=6)
print(u"  書中：瓶沙 %d 枚｜目連 %d 枚｜頻婆娑羅 %d 枚｜目犍連 %d 枚"
      % (t.count(u"瓶沙"), t.count(u"目連"), t.count(u"頻婆娑羅"), t.count(u"目犍連")))

print(u"\n== 新 5 點 ==")
print(u"  一・踢貓效應／射烏因緣")
find(u"烏|射", cap=4)
for q in (u"烏", u"射", u"迦留陀夷"):
    print(u"     語料 %-8s → %s" % (q, corp(q)))
print(u"  二・舉罪五德（知時・如實・利益・柔軟・慈心）")
find(u"三事|若見|若聞|若疑|知時|柔軟", cap=4)
for q in (u"知時", u"柔軟", u"若見若聞若疑", u"見聞疑"):
    print(u"     語料 %-10s → %s" % (q, corp(q)))
print(u"  三・創傷知情／二次傷害／受樂")
find(u"受樂|不受樂|二次傷害|創傷", cap=4)
for q in (u"受樂", u"不樂", u"強"):
    print(u"     語料 %-6s → %s" % (q, corp(q)))
print(u"  四・特留分／繼承／信託／法人")
find(u"特留分|繼承|信託|法人|過戶", cap=4)
print(u"  五・消磁／出坡／法官袍／淨空")
find(u"消磁|出坡|法袍|法官|淨空|歸家", cap=5)
