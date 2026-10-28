# -*- coding: utf-8 -*-
"""外路報告所提『律據』之語料實證（防偽託律據）＋F2 兩處上下文補量。

用法：python -X utf8 _work/pairclaim2.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import _tk                                            # noqa: E402

print("本地語料檔：原文 %d 支・佛經 %d 支" % (len(list((ROOT / "原文").glob("*.txt"))),
                                              len(list((ROOT / "佛經").glob("**/*.txt")))))
print("佛經目錄：", sorted({k.split("/")[1] for k in _tk.OTHER})[:20])

print("\n■ 報告擬補之『律據』是否見於本律（term_count＝逐字出現數）")
for w in ["隨處解界", "隨處更結", "解界", "現前和合", "和合僧", "白二羯磨", "現前毘尼",
          "僧事以現前和合為宗", "界清淨", "結大界", "小界", "忘解", "不解界", "羯磨不成"]:
    print(f"   {w:14} 本律 {_tk.term_count(w):>4} 見")

print("\n■ 《行事鈔》《四分律行事鈔》之本地可得性")
for w in ["行事鈔", "資持記", "隨機羯磨"]:
    where = [k for k, v in _tk.OTHER.items() if w in v[:200000]]
    print(f"   {w}：佛經檔命中 {where[:3] or '無（本地未收其文）'}")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
print("\n■ F2 四署節之上下文（L4571-4612）")
for i in range(4570, 4612):
    if F2[i].strip():
        print(f"   L{i+1}: {F2[i].strip()[:88]}")

print("\n■ F2 有無法域自限之語（報告稱宣稱了中立）")
import re
for rx in ["世俗實定法", "不依任何", "僅供", "以本域", "各地", "法域", "只作引橋", "引橋"]:
    hits = [(i + 1, l.strip()[:70]) for i, l in enumerate(F2) if re.search(rx, l)]
    print(f"   /{rx}/ → {len(hits)} 行", "｜例：" + hits[0][1] if hits else "")
