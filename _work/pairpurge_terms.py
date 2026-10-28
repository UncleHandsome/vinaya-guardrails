# -*- coding: utf-8 -*-
"""替代語之覆核：凡欲貼上之詞，須先查①本地《四分律》語料、②兩冊今文已用之形。二者俱無者，不自造。"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
sys.path.insert(0, str(ROOT))
tk = importlib.import_module("_tk")
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
CORP = tk.VINAYA_SEP
WORDS = ["持律", "勘問", "訊問", "王法", "有司", "息爭", "平息", "滅諍", "掩窟", "窟", "朋黨",
         "黨援", "由博返約", "去枝取幹", "一問而止", "影音", "現行", "痕跡", "屏處", "伴", "獨處",
         "邪命", "誑惑", "驚怖", "怖畏", "正念", "作意", "貪愛", "結使", "愛樂", "染污惡作",
         "動發勝思", "色身", "肌肉", "骨骼", "末座", "折慢", "郁結", "心疾", "圖利養", "利養",
         "自讚毀他", "未證", "鑽", "文義", "縫", "尋隙", "結黨", "別眾", "窟宅", "城郭", "賊"]
for w in WORDS:
    c = CORP.count(tk.norm_sep(w))
    b = sum(l.count(w) for l in F2) + sum(l.count(w) for l in F1)
    flag = "" if (c or b) else "　◆ 語料與兩冊俱無此形——不自造"
    print("%-6s 語料 %4d・兩冊 %4d%s" % (w, c, b, flag))
