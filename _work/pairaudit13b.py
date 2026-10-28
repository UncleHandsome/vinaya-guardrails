# -*- coding: utf-8 -*-
"""第十三波・取證乙：覆鉢羯磨・覆藏他粗罪・打戒開緣・菩薩地・書內既存之數。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "_work"))
import _tk  # noqa: E402

TAB = _tk.FOLD
V = _tk.norm(_tk.VINAYA)
Vf = "".join(TAB.get(c, c) for c in V)
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8-sig")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8-sig")
B1 = "".join(TAB.get(c, c) for c in F1)
B2 = "".join(TAB.get(c, c) for c in F2)

print("=" * 76)
print("甲・書內既存（覆鉢／學家／覆他罪／聲聞如地）")
for w in ("覆鉢", "學家", "使無利", "不復翻案", "一事不再理", "知他", "粗罪", "覆藏他", "聲聞戒",
          "如地", "樹", "地種", "菩薩戒", "小乘", "增上慢", "護身", "賊", "惡獸"):
    print("   %-8s F1 %3d｜F2 %3d｜律 %3d" % (w, B1.count(w), B2.count(w), Vf.count(w)))

print("=" * 76)
print("乙・覆鉢羯磨之制戒因緣（語料原文，取可引之句）")
i = [m.start() for m in re.finditer("覆鉢羯磨", Vf)]
print("   『覆鉢羯磨』 %d 見，位：%s" % (len(i), i[:6]))
for p in i[:2]:
    print("   …%s…" % Vf[max(0, p - 700):p + 260].replace("\n", "｜"))

print("=" * 76)
print("丙・覆藏他粗罪戒・戒文與戒次（依本地尾標『N竟』自算）")
p = Vf.find("知他比丘犯粗罪覆藏者波逸提")
print("   戒文位 %d｜前文 …%s…" % (p, Vf[max(0, p - 240):p + 120].replace("\n", "｜")))
for pat in ("四波羅夷僧伽婆尸沙", "不知無犯", "露地"):
    print("   附語『%s』見否：%s" % (pat, Vf.find(pat, p - 400) if pat == "露地" else Vf.count(pat)))
j = re.search(r"[〇一二三四五六七八九十百]{1,4}竟", Vf[p:])
print("   其後首個尾標：%s（距戒文 %d 字）" % (j.group(0) if j else "無", j.start() if j else -1))
seg = Vf[max(0, p - 3000):p]
tk = re.findall(r"([〇一二三四五六七八九十百]{1,4})竟", seg)
print("   前文歷見尾標：%s" % (tk[-3:] if tk else "無"))
print("   檔段定位：波逸提諸條之『竟』計數至本條＝%d" % len(re.findall(r"[〇一二三四五六七八九十百]{1,4}竟", Vf[:p])))

print("=" * 76)
print("丁・打戒（瞋恚打比丘）與其開緣——查『脫身』句式之真形")
for pat in (r"瞋恚不打?比?丘?僧??.{0,40}波逸提", r"以瞋恚打", r"打比丘.{0,20}波逸提"):
    for m in list(re.finditer(pat, Vf))[:2]:
        print("   ● %s｜…%s…" % (pat[:12], Vf[m.start():m.start() + 200].replace("\n", "｜")))
p = Vf.find("若比丘以瞋恚故打比丘")
if p < 0:
    p = Vf.find("瞋恚打")
print("   取戒文位 %d，其『不犯者』段：" % p)
q = Vf.find("不犯者", p)
print("   …%s…" % Vf[q:q + 320].replace("\n", "｜") if q > 0 else "   未見不犯者段")
for w in ("欲死", "斷命", "救身", "逃", "走", "避"):
    print("   关键字『%s』：%d 見" % (w, Vf.count(w)))

print("=" * 76)
print("戊・他典・菩薩地與『捨聲聞戒』之教證")
for k, v in _tk.OTHER.items():
    s = v if isinstance(v, str) else v.decode("utf-8", "ignore")
    s = "".join(TAB.get(c, c) for c in _tk.norm(s))
    for w in ("捨聲聞", "棄聲聞", "聲聞戒", "律儀戒", "如地", "增上慢"):
        p = s.find(w)
        if p >= 0:
            print("   %-28s『%s』…%s…" % (k.split("/")[-1][:26], w, s[max(0, p - 60):p + 90].replace("\n", "｜")))
