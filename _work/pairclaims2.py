# -*- coding: utf-8 -*-
"""外路『五大深水區』報告之逐條實測（量今檔＋查本律語料，防偽託律據）。

用法：PYTHONPATH=. python -X utf8 _work/pairclaims2.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import _tk                                                # noqa: E402

F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")


def scan(nm, lines, rx, cap=4, show=78):
    hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(rx, l)]
    print(f"  [{nm}] /{rx}/ → {len(hits)} 行")
    for i, l in hits[:cap]:
        print(f"        L{i}: {l[:show]}")
    return hits


def heads(lines, rx, cap=8):
    return scan("標題", lines, r"^#{1,6}\s*.*" + rx, cap, 66)


print("■ 一・六根本煩惱之『疑』與『惡見』是否真被架空（F1）")
for rx in ["戒禁取", "邪見", "見取", "身見", "邊見", "惡見", "五利使", "見惑"]:
    scan("F1", F1, rx, 3, 70)
scan("F1", F1, r"疑心所|生疑|自疑|疑罪|審慎自疑|猶豫", 6, 70)
scan("F1", F1, r"提婆達多|阿利吒|馬鳴比丘", 5, 70)
heads(F1, r"第十章|第十節|第三節")
print("  F1 第五・九章之煩惱目：")
scan("F1", F1, r"四根本煩惱|貪瞋癡慢|貪、瞋、癡、慢", 5, 70)

print("\n■ 二・發露與世俗侵權（F2・F1）")
for nm, L in (("F2", F2), ("F1", F1)):
    scan(nm, L, r"名譽權|隱私權|個資|個人資料|去識別|保密義務|在場旁聽|閉門|不說他人|不舉他名", 5, 74)
scan("F2", F2, r"晨旦白眾|白眾|對首發露|發露", 6, 70)
scan("F2", F2, r"麁惡語|身相觸", 4, 70)

print("\n■ 三・女眾法益與『尼不得舉比丘』之律據")
for nm, L in (("F2", F2), ("F1", F1)):
    scan(nm, L, r"八敬法|二部僧|尼僧|比丘尼.{0,12}舉|舉比丘|女眾|被害.{0,6}主體|強制受理", 6, 74)
print("  本律語料逐字出現數（term_count）：")
for w in ["八敬法", "敬法", "不得舉比丘", "舉比丘罪", "比丘尼舉", "二部僧", "學法", "意喜"]:
    print(f"     {w:12} {_tk.term_count(w):>5} 見")

print("\n■ 四・『滿五錢』之量化")
for nm, L in (("F1", F1), ("F2", F2)):
    scan(nm, L, r"五錢", 4, 72)
    scan(nm, L, r"隨王法|隨國法|王法|折算|換算|今值|銅錢|黃金|克|人民幣|台幣|新臺幣|金額標準|立案", 6, 72)
print("  本律語料：")
for w in ["五錢", "隨王法", "王法", "五錢故", "滿五錢"]:
    print(f"     {w:8} {_tk.term_count(w):>5} 見")

print("\n■ 五・夜半四照之臨床安全閥（F1 第十一章）")
scan("F1", F1, r"三分鐘|限時|五分鐘|失眠|精神科|醫療|諮商|強迫|反芻|血清素|熔斷|疑罪從無|良知過載|暫止|掩卷", 10, 74)
heads(F1, r"夜半四照|觀心協議|自省手冊")

print("\n■ 六・報告表列之 1・7（上輪已判，此处只核行號未動）")
scan("F2", F2, r"不得自創免供詞|宣告性羯磨|Declaratory", 5, 74)
scan("F2", F2, r"四署|缺署者|缺一無效", 5, 74)
