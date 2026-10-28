# -*- coding: utf-8 -*-
"""第十三波・取證：外路第十報告『五個法理暗礁與道德漏洞』——逐條向本地語料與今檔要證據。

判準（書之自約）：凡掛『』或「」式樣者須語料見形；語料無文而義理可通者，只作『本書之解』，不掛律據。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "_work"))
import _tk  # noqa: E402

V = _tk.norm(_tk.VINAYA) if callable(getattr(_tk, "norm", None)) else _tk.VINAYA
OT = {}
for k, v in _tk.OTHER.items():
    s = v if isinstance(v, str) else v.decode("utf-8", "ignore")
    OT[k] = _tk.norm(s) if callable(getattr(_tk, "norm", None)) else s
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8-sig")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8-sig")
TAB = _tk.FOLD


def fold(s):
    return "".join(TAB.get(c, c) for c in s)


Vf, F1f, F2f = fold(V), fold(F1), fold(F2)
OTf = {k: fold(v) for k, v in OT.items()}


def ctx(t, w, n=3, back=90, fwd=130, raw=None):
    """回 t 中 w 之上下文（raw＝原形，未折未削標點者）。"""
    out = []
    for m in list(re.finditer(re.escape(w), t))[:n]:
        out.append(t[max(0, m.start() - back):m.start() + fwd].replace("\n", "｜"))
    return out


def show(t, w, label, n=3):
    k = t.count(w)
    print("   %-14s 語料 %2d 見｜%s" % (label, k, ""))
    for c in ctx(t, w, n):
        print("        …%s…" % c[:190])
    return k


print("=" * 76)
print("② 覆鉢羯磨・語料有無（ Pattanikkujjana ）")
for w in ("覆鉢", "鉢覆", "翻鉢", "與鉢", "不得入其家", "斷交"):
    show(Vf, w, "律・" + w, 2)
print("   『雜犍度』之屬：")
for m in list(re.finditer(r"[一-鿿]{0,4}犍度(?:之[一二三])?", Vf))[:2]:
    pass
k = Vf.count("覆鉢")
print("   覆鉢 合計 %d 見" % k)

print("=" * 76)
print("⑤ 脫身防衛・語料有無（『為他所打，欲脫身故打者，無犯』）")
for w in ("脫身", "欲脫", "打者無犯", "他打", "所打", "捉", "解脫"):
    show(Vf, w, "律・" + w, 3)

print("=" * 76)
print("② 覆藏他粗罪・語料有無（防翻案之『舉報人逾期連帶』）")
for w in ("覆藏", "不舉", "見罪不舉", "知他粗罪", "覆他粗罪", "麁罪"):
    show(Vf, w, "律・" + w, 2)

print("=" * 76)
print("③ 暗礁一・書內既存之防狂禪界碑")
for w in ("惡取空", "撥無", "帶贓", "以法為賊", "增上慢", "大妄語", "物權返還先於受懺", "不復翻案", "一事不再理",
          "外緣", "了外緣"):
    print("   『%s』 F1 %d・F2 %d" % (w, F1f.count(w), F2f.count(w)))
print("   F1『歇』之語境（卷首・終卷・附錄各一）：")
for c in ctx(fold(F1), "歇", 40):
    pass
i = [m.start() for m in re.finditer("歇", F1f)]
print("   F1 含『歇』凡 %d 處；其相鄰之『戒／罪／償／還』同線行數：%d" % (
    len(i), sum(1 for x in re.findall(r"[^\n]*歇[^\n]*", F1f) if re.search(r"(還|償|罪|犯|贓|責)", x))))

print("=" * 76)
print("④ 暗礁四・聲聞與菩薩之位階（他典與書內）")
for k, t in OTf.items():
    c = sum(t.count(w) for w in ("聲聞", "菩薩地", "小乘", "心戒"))
    if c:
        print("   %-34s 聲聞 %d・菩薩地 %d・小乘 %d・心戒 %d" % (
            k.split("/")[-1][:22], t.count("聲聞"), t.count("菩薩地"), t.count("小乘"), t.count("心戒")))
for w in ("地種", "如地", "樹", "根本"):
    print("   律『%s』 %d 見" % (w, Vf.count(w)))
print("   書內：F1『菩薩戒』%d・『梵網』%d・『小乘』%d・『聲聞』%d｜F2 同 %d・%d・%d・%d" % (
    F1f.count("菩薩戒"), F1f.count("梵網"), F1f.count("小乘"), F1f.count("聲聞"),
    F2f.count("菩薩戒"), F2f.count("梵網"), F2f.count("小乘"), F2f.count("聲聞")))

print("=" * 76)
print("① 暗礁二・書內『不復翻案／知時』之既有防線")
for w in ("知時", "翻舊帳", "覆藏", "滅諍和解", "發露清淨", "已清淨", "不得重舉"):
    print("   『%s』 F1 %d・F2 %d" % (w, F1f.count(w), F2f.count(w)))
print("   F2『不復翻案』語境：")
for c in ctx(F2f, "不復翻案", 3):
    print("        …%s…" % c[:200])
print("   F2『波逸提第 64／66 條』舊帳：")
for w in ("波逸提法第六十四條", "波逸提法第六十六條", "第六十四條", "第六十六條"):
    print("        %s ➔ F2 %d・語料尾標 %d" % (w, F2f.count(w), Vf.count(w)))
