# -*- coding: utf-8 -*-
"""第十二波・取證：外路『五個認知過載重災區』報告逐條量今檔（只量不改）。

報告之區次有缺：正文列 區一・區二・區三・區五，**區四之正文缺席**，唯見於總結
『案卷長短節奏交替，大案重裝剖析，小案輕靈點穴』——本器第④目即為補量此項。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8-sig")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8-sig")

def lines(t):
    return t.replace("\r\n", "\n").split("\n")

L1, L2 = lines(F1), lines(F2)

GEN = ["貪", "瞋", "癡", "慢", "疑", "惡見"]
FOL = ["憤", "恨", "惱", "覆", "誑", "諂", "驕", "害", "嫉", "慳", "無慚", "無愧", "惛沉", "睡眠",
       "掉舉", "悔", "忿", "失念", "散亂", "不正知"]
BEN = ["信", "慚", "愧", "無貪", "無瞋", "無癡", "精進", "輕安", "不放逸", "行捨", "不害"]
UNI = ["觸", "作意", "受", "想", "思"]
ALL = {(w, g) for g, s in (("根本", GEN), ("隨", FOL), ("善", BEN), ("遍行", UNI)) for w in s}

CARD = re.compile(r"^#{4}\s*[【\[]案卷\s*([0-9]{2}[A-Z]?)")
NEXT = re.compile(r"^####(?!#)\s")          # 次卡之界：H4 而後接『#』者（#####）是卡內小節，非界


def cards(t):
    """回 F1 各案卷卡：(號, 起行, 迄行, 全文)。卡之界＝下一枚 H4（含章題・终卷），不含 H5 小節。"""
    L = lines(t)
    idx = [(i, CARD.match(l).group(1)) for i, l in enumerate(L) if CARD.match(l)]
    out = []
    for k, (i, n) in enumerate(idx):
        j = next((x for x, l in enumerate(L[i + 1:], i + 1) if NEXT.match(l)), len(L))
        out.append((n, i + 1, j, "\n".join(L[i:j])))
    return out


print("=" * 74)
print("① 區一・心所之密度（F1 案卷卡之解剖層：只數『掛名之處』，即【…】標籤與明書之欄）")
LAB = re.compile(r"【([^】]{1,26})】")
print("   全書marker：根本心 %d・隨煩惱 %d・病根 %d・畫皮 %d・心所 %d" % (
    F1.count("根本心"), F1.count("隨煩惱"), F1.count("病根"), F1.count("畫皮"), F1.count("心所")))
rows = []
for n, a, b, body in cards(F1):
    seg = body.split("#####")
    jie = next((s for s in seg if s.startswith(("二、【解剖", "二、【解剖層")) or "解剖層" in s[:10]), "")
    labs = [m.group(1) for m in LAB.finditer(jie)]
    hit = sorted({w for w, g in ALL for x in labs if w in x})
    gen = [w for w in GEN if any(w in x for x in labs)]
    fol = [w for w in FOL if any(w in x for x in labs)]
    uni = [w for w in UNI if any(w in x for x in labs)]
    rows.append((n, len(labs), len(hit), len(gen), len(fol), "／".join(labs)))
rows.sort(key=lambda x: -x[2])
print("   卡數 %d・解剖層掛名之心所：最多 %d・中位 %d・最少 %d" % (
    len(rows), rows[0][2], sorted(r[2] for r in rows)[len(rows) // 2], rows[-1][2]))
for r in rows[:6]:
    print("   案%s 標籤 %d・心所 %d（根本 %d・隨 %d）｜%s" % (r[0], r[1], r[2], r[3], r[4], r[5][:150]))
print("   俱有『一根本＋一隨』者：%d／%d；根本≥2 或 隨≥3 之卡：%s" % (
    sum(1 for r in rows if r[3] >= 1 and r[4] >= 1), len(rows),
    [r[0] for r in rows if r[3] >= 2 or r[4] >= 3]))

print("=" * 74)
print("② 區五・F1 第十章之案卷清單與字數（並核『連著五六個無犯案』之 Premise）")
L = lines(F1)
i10 = next(i for i, l in enumerate(L) if re.match(r"^#{1,4}\s*第十章", l))
i11 = next(i for i, l in enumerate(L[i10 + 1:], i10 + 1) if re.match(r"^#{1,4}\s*第[一二三四五六七八九十]+章", l))
print("   第十章 L%d-%d（%d 行）" % (i10 + 1, i11, i11 - i10))
for x in range(i10, i11):
    l = L[x]
    if re.match(r"^#{4,5}\s", l):
        print("   %5d|%s" % (x + 1, l[:78]))
sub = "\n".join(L[i10:i11])
print("   章內『無犯／開許／不犯』之宣稱：無犯 %d・開許 %d・不犯 %d・阻卻 %d" % (
    sub.count("無犯"), sub.count("開許"), sub.count("不犯"), sub.count("阻卻")))

print("=" * 74)
print("③ 區四・案卷長短之節奏（全書卡字數分布，報告之正文缺席，補量）")
sizes = sorted(((len(re.findall(r"[一-鿿]", c[3])), c[0]) for c in cards(F1)), reverse=True)
print("   F1 案卷卡 %d 張・漢字數 top5 %s ・bottom5 %s" % (len(sizes), sizes[:5], sizes[-5:]))
q = [s for s, n in sizes]
print("   最長 %d・最短 %d・中位 %d・極差 %d 倍" % (q[0], q[-1], q[len(q) // 2], round(q[0] / q[-1], 2)))

print("=" * 74)
print("④ 區二・F2 第十・十一章之結構與既存之圖")
for zh in ("第十章", "第十一章"):
    i = next(k for k, l in enumerate(L2) if re.match(r"^#{1,3}\s*%s" % zh, l))
    j = next(k for k in range(i + 1, len(L2)) if re.match(r"^#{1,3}\s*第[一二三四五六七八九十]+章", L2[k]))
    seg = L2[i:j]
    print("   %s L%d-%d（%d 行）・H3 %d・H4 %d・H5 %d・圍欄 %d 段・提撕 %s" % (
        zh, i + 1, j, len(seg),
        sum(1 for l in seg if re.match(r"^###\s", l)), sum(1 for l in seg if re.match(r"^####(?!#)\s", l)),
        sum(1 for l in seg if re.match(r"^#####\s", l)),
        sum(1 for l in seg if l.startswith("```")),
        any("章首提撕" in l for l in seg)))
    for l in seg:
        if re.match(r"^#{4,5}\s", l) and any(w in l for w in ("失宿", "時效", "明相", "修合", "本日治", "凍結")):
            print("        款：%s" % l[:70])
print("   全書詞頻：失宿 %d・明相 %d・本日治 %d・修合別住 %d・摩那埵 %d・時效凍結 %d" % (
    F2.count("失宿"), F2.count("明相"), F2.count("本日治"), F2.count("修合"), F2.count("摩那埵"), F2.count("時效凍結")))
i = next((k for k, l in enumerate(L2) if "失宿八事" in l), None)
print("   失宿八事首現 L%s｜上下文：%s" % (i + 1 if i is not None else "-", (L2[i][:180] if i is not None else "-")))

print("=" * 74)
print("⑤ 區三・規矩之『號名』清單與既存之分级語")
NAMES = ["八大正理", "略戒心印", "三十二字", "五大憲政基石", "五大基石", "舉罪五德", "十不如法",
         "非法足數", "十五類", "教授師十德", "十德", "出堂洗心", "三事", "夜半四照", "六重心智閘門",
         "四諍", "七滅諍", "白四羯磨", "白二羯磨"]
for t, nm in ((F1, "F1"), (F2, "F2")):
    print("   %s：%s" % (nm, "・".join("%s%d" % (w, t.count(w)) for w in NAMES if t.count(w))))
print("   既存之『分级・隨身・查考』語：")
for w in ("平日但持", "鏡不照人", "查考", "備查", "字典", "隨身", "臨時翻", "三級", "分級適用", "不需背", "不必背"):
    k1 = [x + 1 for x, l in enumerate(L1) if w in l]
    k2 = [x + 1 for x, l in enumerate(L2) if w in l]
    if k1 or k2:
        print("      『%s』 F1 %s｜F2 %s" % (w, k1[:6], k2[:6]))

print("=" * 74)
print("⑥ 既存之『不必背・備查・字典』宣告（區三之處方是否已有人在守）")
for t, nm, LL in ((F1, "F1", L1), (F2, "F2", L2)):
    for x, l in enumerate(LL):
        if re.search(r"(不(必|需|得)?背|記(不)?住|唯須記|但記|備查|查考|隨文回查|法官字典|檢索之便)", l) and len(l) > 20:
            print("   %s L%-5d|%.130s" % (nm, x + 1, l.strip()))
print("=" * 74)
print("⑦ F1 第十章之全卡（受暴／想差兩包能否容盡）")
for x in range(i10, i11):
    if CARD.match(L[x]):
        print("   %5d|%s" % (x + 1, L[x][:86]))

