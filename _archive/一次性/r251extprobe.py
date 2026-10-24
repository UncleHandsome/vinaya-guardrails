# -*- coding: utf-8 -*-
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

# 逐條量外部「除重去執」提案所點之名，分印面（主檔）／底冊（備檔）兩區，並列印面落點。
main = T.DOC_MAIN.split("\n")
bot = (T.DOC_BOTTOM or "").split("\n")

PATS = [
    (u"百則・一百則", r"百則|一百則"),
    (u"九章百則", r"九章百則|全書九章"),
    (u"45／25／30 配額", r"45[／/、]|遮止 ?45|開許 ?25|僧伽 ?30"),
    (u"壹·貳·參三輯", r"壹·|貳·|參·"),
    (u"133", r"133"),
    (u"71單／25雙／4三", r"71 單|71單|25 雙|25雙|4 三|4三"),
    (u"107", r"107"),
    (u"合規率", r"合規率"),
    (u"100.0%", r"100\.0 ?%"),
    (u"120/120", r"120/120|120／120|120 片段|片段計"),
    (u"二十三行／23 行", r"二十三行|23 行|23行|唯二十四|唯四典範"),
    (u"348 減 326", r"348 ?[-−減] ?326|326"),
    (u"複統攝 29", r"複統攝"),
    (u"台帳", r"台帳"),
    (u"定位行", r"定位行"),
    (u"落點", r"落點"),
    (u"綁定", r"綁定"),
    (u"平帳", r"平帳"),
    (u"字頻・詞頻", r"字頻|詞頻"),
    (u"前十二年", r"前十二年"),
    (u"五階心印漏斗", r"五階|心印漏斗|十六字"),
]


def scan(lines, pat):
    rx = re.compile(pat)
    return [(i + 1, l.strip()) for i, l in enumerate(lines) if rx.search(l)]


print("區｜名｜印面處數｜底冊處數")
for name, pat in PATS:
    hm, hb = scan(main, pat), scan(bot, pat)
    print("%-18s 印面 %3d｜底冊 %3d" % (name, len(hm), len(hb)))

print("\n== 印面落點（每目最多列 6 行，截 96 字）==")
for name, pat in PATS:
    hm = scan(main, pat)
    if not hm:
        continue
    print("\n--- %s（印面 %d 處）---" % (name, len(hm)))
    for ln, txt in hm[:6]:
        print("  L%-6d %s" % (ln, txt[:96]))
