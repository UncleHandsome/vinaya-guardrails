# -*- coding: utf-8 -*-
import io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import hulan_path as HP

t = io.open(HP.SRC, encoding="utf-8", newline="").read()
lines = t.split("\r\n") if "\r\n" in t else t.split("\n")
print(u"正本：%s｜行 %d" % (os.path.basename(HP.SRC), len(lines)))


def c(pat):
    return len(re.findall(pat, t))


ITEMS = [
    (u"三批共列・按語「按：」獨立段", u"按："),
    (u"卷首白衣閱律自陳", u"白衣"),
    (u"如實標記：義引／義譯／括其旨／大意", u"義引|義譯|括其旨|括其大意|之大意"),
    (u"版權式自白：本書撮舉／本書之解／本書語／本書之讀法", u"本書撮舉|本書之解|本書語|本書的讀法|本書之讀法|撮舉之喻|撮舉之語"),
    (u"考據夾註：本律無文／此詞本律無文／非律文", u"本律無文|本律不記|非此段之文|律無"),
    (u"詞頻自證：N 見／N 次", u"\\d+ ?見|\\d+ ?次"),
    (u"跨章指針：說見／具見／詳見／見第", u"說見|具見|詳見|說詳"),
    (u"體例凡例（章首『從題不從號』）", u"從題不從號|體例凡例|體例須先明|體例同上章"),
    (u"同篇並制／同一組者／律中並制", u"同篇並制|同一組者|律中並制"),
    (u"【律制】續行括號（另起 `> （…）`）", u"^> （"),
    (u"名相隨文註（括號內『謂／即／乃／猶言』）", u"（[^）]{0,3}(謂|即|乃|猶言)[^）]{2,40}）"),
    (u"版本差異標籤（唯全本有之）", u"唯全本有之"),
    (u"算式（連加等式）", u"＝\\d+ ?[＋+]|\\d+ ?＋ ?\\d+ ?＝"),
    (u"精簡版之削錄交代", u"精簡"),
    (u"却（疑簡形）", u"却"),
]
for name, pat in ITEMS:
    print(u"  %-42s %4d 處" % (name, c(pat)))

print(u"\n【兩處疑為剪貼事故・逐句取證】")
for key in (u"保留了修行的次序之爭", u"却極少被明答"):
    hit = [(i + 1, l) for i, l in enumerate(lines) if key in l]
    print(u"『%s』見 %d 行：%s" % (key, len(hit), [h[0] for h in hit]))
    for n, l in hit:
        print(u"   L%-5d %s" % (n, l.strip()[:150]))
    if hit:
        n, l = hit[0]
        rep = l.count(key)
        print(u"   同行內重複 %d 次" % rep)

print(u"\n【『却』之上下文（分引號內外）】")
qin = qout = 0
for i, l in enumerate(lines, 1):
    for m in re.finditer(u"却", l):
        s = max(0, m.start() - 14)
        seg = l[s:m.start() + 14]
        inn = (seg.count(u"「") > seg.count(u"」")) or (seg.count(u"『") > seg.count(u"』"))
        if inn:
            qin += 1
        else:
            qout += 1
            if qout <= 4:
                print(u"   欄外 L%-5d …%s…" % (i, seg))
print(u"  『却』引號內 %d 枚｜引號外 %d 枚" % (qin, qout))
