# -*- coding: utf-8 -*-
"""第十一波・外路『五調整四盲點』報告之取證（只量不寫）。

用法：python -X utf8 _work/pairaudit11.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
sys.path.insert(0, str(ROOT))
import _tk  # noqa: E402
import paircase_lib as PC  # noqa: E402

F1 = ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"
BOOKS = {"F1": F1, "F2": F2}
TXT = {k: v.read_bytes().decode("utf-8-sig").replace("\r\n", "\n") for k, v in BOOKS.items()}
LN = {k: t.split("\n") for k, t in TXT.items()}

TERMS = ["IIA", "三道防線", "三重護念", "Trauma", "創傷知情", "體恤受暴", "LINE", "Slack", "微信",
         "通訊群組", "實質受益人", "UBO", "多巴胺", "獎賞迴路", "目標致盲", "作意偏執", "煤氣燈",
         "Gaslighting", "法審字", "四署", "簽名欄", "簽押", "□", "- [ ]", "未細核", "外來說",
         "未及就地覆核", "分段檔", "特留分", "勞基法", "信託", "洗錢", "AML", "移轉管轄", "奔赴他寺",
         "陳情", "證據問", "言詞問", "256", "二百五十六", "九十二", "歇", "和", "先例", "提要"]
print("■ 一・詞之所在（報告所點之『現代殘留』今檔有無）")
print("%-14s %-6s %s" % ("詞", "F1", "F2"))
for t in TERMS:
    a = sum(1 for l in LN["F1"] if t in l)
    b = sum(1 for l in LN["F2"] if t in l)
    if a or b:
        print("  %-14s %-6d %-6d" % (t, a, b))

print("\n■ 二・報告與『宣稱載體』之對合")
for k in ("F1", "F2"):
    m = re.search(r"案卷\s*(\d+)\s*則|案卷 ([〇一二三四五六七八九十]+) 卡", TXT[k])
    print("  %s 封面宣稱之自算：由 build_pair 取（見 --dry）" % k)
print("  兩冊案卷之數：F1 卡 %d（子案 %d）・F2 卡 %d（子案 %d）"
      % (len(PC.findable(LN["F1"])), len(PC.subs(LN["F1"])),
         len(PC.findable(LN["F2"])), len(PC.subs(LN["F2"]))))
cards = {k: [l.strip() for l in LN[k] if re.match(r"^#{1,6}\s*[【\[](?:制度)?案卷\s*[0-9]{2}", l.strip())]
         for k in ("F1", "F2")}
for k in ("F1", "F2"):
    nums = sorted({int(re.search(r"案卷\s*([0-9]{2,3})", c).group(1)) for c in cards[k]})
    gaps = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []
    print("  %s 案卷之號：%s" % (k, nums))
    print("     缺號：%s（共 %d）" % (gaps[:24], len(gaps)))

print("\n■ 三・調整一之靶：F1 內之『公堂／程序』語彙與第十一章第三節")
p11 = None
for i, l in enumerate(LN["F1"], 1):
    if re.match(r"^#\s*第十一章", l.strip()):
        p11 = i
    if p11 and re.match(r"^#{1,6}\s*第[一二三四五]節", l.strip()) and i > p11:
        print("   第十一章之節 L%d %s" % (i, l.strip()[:60]))
for i, l in enumerate(LN["F1"], 1):
    if re.search(r"移轉管轄|奔赴他寺|陳情|出界前單向口宣", l):
        print("   F1 L%-5d %s" % (i, l.strip()[:96]))
for i, l in enumerate(LN["F2"], 1):
    if re.search(r"移轉管轄|跨界陳情|奔赴他寺", l):
        print("   F2 L%-5d %s" % (i, l.strip()[:78]))

print("\n■ 四・調整一之二：F1『言詞問／證據問』之所在（報告命移交 F2 第五章）")
for i, l in enumerate(LN["F1"], 1):
    if "言詞問" in l or "證據問" in l:
        print("   F1 L%-5d %s" % (i, l.strip()[:92]))
for i, l in enumerate(LN["F2"], 1):
    if "言詞問" in l or "證據問" in l:
        print("   F2 L%-5d %s" % (i, l.strip()[:64]))

print("\n■ 五・問題三之靶：F2 第四篇今制之章與節")
in4 = False
for i, l in enumerate(LN["F2"], 1):
    s = l.strip()
    if re.match(r"^#{1,6}\s*第[四]篇", s):
        in4 = True
    elif re.match(r"^#{1,6}\s*第[五]篇", s):
        in4 = False
    if in4 and re.match(r"^#{1,6}\s*(第[一二三四五六七八九十]+章|第[一二三四五六七八九十]+節|【)", s):
        print("   L%-5d %s" % (i, s[:76]))

print("\n■ 六・問題一之靶：F2 引『彼冊案名』而不具事相之處（前 12 條）")
NAMES = ["須提那", "檀尼迦", "解牛", "迦留陀夷", "慈地", "沓婆", "闡陀", "六群", "守籠那", "難陀比丘尼",
         "蓮華色", "般陀", "琉璃", "提婆達", "耶舍", "拘睒彌", "富羅那", "大迦葉", "阿難", "畢陵伽"]
cnt = {}
for i, l in enumerate(LN["F2"], 1):
    if PC and l.strip().startswith("```"):
        continue
    for nm in NAMES:
        if nm in l and ("案" in l or "〔" in l or "【" in l):
            cnt.setdefault(nm, []).append(i)
tot = sum(len(v) for v in cnt.values())
print("   合 %d 處・涉及案名 %d 個" % (tot, len(cnt)))
for nm, ii in sorted(cnt.items(), key=lambda x: -len(x[1]))[:12]:
    print("     %-8s %2d 處  L%s" % (nm, len(ii), ", ".join(str(x) for x in ii[:6])))

print("\n■ 七・調整四／問題四之靶：F2 開卷總綱與『正理』之用量")
for i, l in enumerate(LN["F2"], 1):
    if re.match(r"^#{1,6}\s*【?開卷", l.strip()):
        print("   總綱 L%d %s" % (i, l.strip()[:60]))
n5 = sum(1 for l in LN["F2"] if re.search(r"五大基石|憲政基石|五大宣言之", l))
nr = sum(1 for l in LN["F2"] if re.search(r"正理[一二三四五六七八]", l))
print("   F2：五大基石之稱 %d 行・『正理N』之引 %d 行" % (n5, nr))
for i, l in enumerate(LN["F2"], 1):
    if re.search(r"宣言[一二三四五]（|宣言[一二三四五][：:]", l):
        print("     L%-5d %s" % (i, l.strip()[:70]))

print("\n■ 八・調整五之靶：F2 第二十章今制")
c20 = None
for i, l in enumerate(LN["F2"], 1):
    if re.match(r"^#{1,6}\s*第二十章", l.strip()):
        c20 = i
    if c20 and i > c20 and re.match(r"^#{1,6}\s*第[一二三四]節", l.strip()):
        print("   L%-5d %s" % (i, l.strip()[:70]))
    if c20 and i > c20 and re.match(r"^#{1,6}\s*第[一二三]十?[一二三四五六七八九十]?章", l.strip()) and i > c20 + 3:
        break
for i, l in enumerate(LN["F2"], 1):
    if "法審字" in l or "判定" in l and "□" in l:
        print("   公文之跡 L%-5d %s" % (i, l.strip()[:70]))
