# -*- coding: utf-8 -*-
"""外路第八報告（雙子星七事）之逐條實測——量今檔，不據報告之引文為據。

用法：python -X utf8 _work/r286ext.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
V39 = sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\r\n")


def scan(nm, lines, rx, cap=5, show=76):
    hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(rx, l)]
    print(f"  [{nm}] /{rx}/ → {len(hits)} 行")
    for i, l in hits[:cap]:
        print(f"        L{i}: {l[:show]}")
    return hits


def chap_of(lines, ln):
    cur = "?"
    for i, l in enumerate(lines, 1):
        m = re.match(r"^#{1,6}\s*(第[〇一二三四五六七八九十百]+章[　 ]\S.*)$", l.strip())
        if m and i <= ln:
            cur = m.group(1)[:16]
    return cur


print("■ 一・自言治之兩式（報告稱第五章內部撞車）")
a = scan("F2", F2, r"不自創|免口供|免供詞", 6)
b = scan("F2", F2, r"確認既成事實|非憑口供創設|既成事實", 6)
c = scan("F2", F2, r"惡意沉默|惡意保持沉默|死不認罪|排除合理懷疑|三度給予", 6)
for i, l in (a + b + c)[:8]:
    print(f"        ↑ 此行屬：{chap_of(F2, i)}")

print("\n■ 二・102 案與六篇附錄之產權（ver39 有・兩冊有無）")
scan("ver39", V39, r"^#\s*附錄", 10, 60)
scan("ver39", V39, r"102", 4, 70)
for nm, L in (("F1", F1), ("F2", F2)):
    scan(nm, L, r"附錄|集群|全景總表|回查|檢索表", 6, 70)

print("\n■ 三・忘解小界之教理與世俗法學名詞")
for rx in [r"忘解小界", r"既判力", r"禁反言|Estoppel", r"信賴保護", r"隨處解界|隨處更結",
           r"現前和合", r"白二", r"解界"]:
    scan("F2", F2, rx, 3, 74)

print("\n■ 四・四大神聖邊界之兩冊落點")
scan("F1", F1, r"四大神聖邊界|物理邊界|法域邊界|因果邊界|思想邊界", 8, 70)
scan("F2", F2, r"四大神聖邊界|物理邊界|法域邊界|因果邊界|思想邊界", 8, 70)

print("\n■ 五・實定法色彩與法域中立之自我宣告")
for rx in [r"特留分", r"借名登記|借名代持|名義代持", r"假扣押", r"定暫時狀態假處分",
           r"勞動基準法|勞基法", r"除斥期間", r"受託人條例|民法典|宗教事務條例",
           r"普通法|Common Law|歸屬信託|擬制信託", r"法域中立|功能對位|跨法域|各地|當地律師",
           r"台灣|臺灣|中國大陸|香港|星馬|北美"]:
    scan("F2", F2, rx, 3, 72)

print("\n■ 六・四署制度之小道場活口")
scan("F2", F2, r"四署", 6, 76)
scan("F2", F2, r"微型道場|小道場|僧眾人數|不足四人|兼任|拒簽|拒絕簽", 8, 72)

print("\n■ 七・報告所未及而本局歷量在帳者（對照）")
print("   六重心智閘門：F1 %d・F2 %d 行（指南派 F2 全面改裝）"
      % (sum(1 for l in F1 if "閘門" in l), sum(1 for l in F2 if "閘門" in l)))
print("   章末呼吸口：F1 %d 行・F2 %d 行"
      % (sum(1 for l in F1 if re.search(r"林下留白|走出急診|留白：", l)),
         sum(1 for l in F2 if re.search(r"林下留白|消磁|出堂|留白：", l))))
print("   姊妹冊互稱（第一／第二本書）：F1 %d・F2 %d 行"
      % (sum(1 for l in F1 if re.search(r"第一本書|第二本書", l)),
         sum(1 for l in F2 if re.search(r"第一本書|第二本書", l))))
