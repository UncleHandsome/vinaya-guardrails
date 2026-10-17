# -*- coding: utf-8 -*-
"""第 104 輪探針：異體對之並用檢——凡『語料只用甲形，書中卻另用乙形於引號外』者，一律報出。
（『缽／鉢』即此式逮得；今廣其表，含佛典常見之異體與日本新字體。）"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tk

PAIRS = [
    (u"鉢", u"缽"), (u"證", u"証"), (u"遍", u"徧"), (u"慎", u"愼"), (u"峰", u"峯"),
    (u"群", u"羣"), (u"內", u"内"), (u"塵", u"尘"), (u"冊", u"册"), (u"概", u"㮣"),
    (u"往", u"徃"), (u"兔", u"兎"), (u"並", u"併"), (u"尚", u"尙"), (u"線", u"綫"),
    (u"麵", u"麪"), (u"詛", u"呪"), (u"咒", u"呪"), (u"窟", u"𥥏"), (u"賴", u"赖"),
    (u"裏", u"裡"), (u"oto", u"oto")[:2] if 0 else (u"oto", u"oto"),
    (u"峽", u"陝"), (u"稾", u"槀"), (u"據", u"㨿"), (u"哭", u"𥝢"), (u"畧", u"略"),
    (u"惒", u"和"), (u"甞", u"嘗"), (u"𤣥", u"玄"), (u"唘", u"啟"), (u"吂", u"字"),
    (u"迴", u"回"), (u"麁", u"粗"), (u"𤆵", u"破"), (u"拔", u"抜"), (u"直", u"値"),
    (u"會", u"会"), (u"圖", u"図"), (u"畫", u"画"), (u"藏", u"蔵"), (u"禪", u"禅"),
    (u"遞", u"逓"), (u"靜", u"静"), (u"淨", u"浄"), (u"沒", u"沉"), (u"緣", u"縁"),
]
COR = _tk.VINAYA_SEP + "\x00".join(_tk.norm_sep(v) for v in _tk.OTHER.values())
DOC = _tk.DOC
plain = re.sub(u'「[^」]*」|『[^』]*』', '', DOC)
seen = set()
for a, b in PAIRS:
    if not a or a == b or (a, b) in seen:
        continue
    seen.add((a, b))
    ca, cb = COR.count(a), COR.count(b)
    pb = plain.count(b)
    if cb == 0 and ca > 0 and pb > 0:
        i = plain.find(b)
        ctx = plain[max(0, i - 20):i + 12].replace("\n", " ")
        print("  語料唯作『%s』(%d 見)、書中引號外有用『%s』%d 見 ｜…%s…" % (a, ca, b, pb, ctx))
    elif ca and cb and abs(pb) and b != a:
        pass
print("（表內 %d 對，已畢）" % len(seen))
