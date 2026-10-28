# -*- coding: utf-8 -*-
"""第五輪報告五筆之實測：法域殘留之逐章定位・破冰之現況・四主角詞頻・體感密度。

用法：python -X utf8 _work/pairvoice2.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = [("護欄", "佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt", 1),
     ("起心動念", "起心動念：四分律的心智顯微鏡與唯識解剖.txt", 1),
     ("如法推尋", "如法推尋：僧伽憲政、法權審理與修復正義.txt", 3)]
LAWY = ["裁量階梯", "管轄", "缺席", "突襲", "公訴", "國法", "思想不施", "極刑", "自言治", "司法", "訴訟", "證據"]
BODY = ["心跳", "呼吸", "冷汗", "胃", "下頜", "牙關", "胸口", "肌肉", "神經", "多巴胺", "前額葉",
        "視野", "管道", "緊繃", "鬆開", "防空洞", "喉嚨", "眼神", "一毫秒", "閃電"]
MEN = ["跋難陀", "迦留陀夷", "闡陀", "六群", "須提那", "提婆達多", "耶舍", "阿難", "目連", "優波離"]


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def load(fn):
    return (ROOT / fn).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").split("\n")


for nm, fn, lvl in B:
    L = load(fn)
    n = cjk("\n".join(L)) or 1
    print("=" * 72)
    print(f"■ {nm}｜印面漢字 {n:,}")
    for lbl, ws in (("世俗法域詞", LAWY), ("生理體感詞", BODY), ("人物", MEN)):
        tot = sum(L[i].count(w) for w in ws for i in range(len(L)))
        print(f"   {lbl}：每千字 {tot / n * 1000:.2f}｜" +
              "・".join(f"{w} {sum(l.count(w) for l in L)}" for w in ws[:9]))
    if nm == "起心動念":
        idx = [(i, l.strip().lstrip("# ").strip()) for i, l in enumerate(L)
               if re.match(r"^#\s*第[一二三四五六七八九十]+章[　 ]", l.strip())]
        idx.append((len(L), "END"))
        print("   逐章『世俗法域詞』密度（每千字）：")
        for k in range(len(idx) - 1):
            a, b = idx[k][0], idx[k + 1][0]
            seg = L[a:b]
            m = cjk("\n".join(seg)) or 1
            t = sum(l.count(w) for l in seg for w in LAWY)
            print(f"      {idx[k][1][:26]:28} {t / m * 1000:5.2f}")
        print("\n   第一章第一節之開頭十二行（破冰現況）：")
        s = next(i for i, l in enumerate(L) if l.strip().startswith("### 第一節"))
        for i in range(s, min(s + 16, len(L))):
            if L[i].strip():
                print(f"      L{i+1}: {L[i].strip()[:88]}")
        print("\n   『八大正理之心性轉譯』是否已存在：")
        for i, l in enumerate(L, 1):
            if "心性轉譯" in l or "自省鏡" in l or "修己之鏡" in l:
                print(f"      L{i}: {l.strip()[:86]}")
