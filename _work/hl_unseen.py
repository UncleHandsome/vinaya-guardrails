# -*- coding: utf-8 -*-
"""《佛陀的護欄》用字之第二把尺：凡「律藏語料＋本書舊檔」皆未見過之字，一律列出（連同視窗）。
不靠簡形表，故簡體、錯字、外文、罕用形皆無所遁；偽陽性由人工目視判定。
用法：python _work/hl_unseen.py <待檢檔> [基準檔…]（基準預設為工作資料夾根目錄之本書現檔）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = sys.argv[1]
BASES = sys.argv[2:] or [HP.SRC]
CORPUS = [os.path.join(ROOT, "原文", f) for f in sorted(os.listdir(os.path.join(ROOT, "原文")))
          if f.endswith(".txt")]

seen = set()
for f in BASES + CORPUS:
    seen |= set(io.open(f, encoding="utf-8-sig", errors="replace").read())
t = io.open(TARGET, encoding="utf-8").read()
unk = {}
for i, ch in enumerate(t):
    if u"\u4e00" <= ch <= u"\u9fff" and ch not in seen:
        unk.setdefault(ch, []).append(i)
print(u"語料與基準皆未見過之漢字：%d 種" % len(unk))
for ch, idx in sorted(unk.items(), key=lambda kv: -len(kv[1])):
    w = t[max(0, idx[0] - 16):idx[0] + 16].replace("\n", "/")
    print(u"  %s ×%d ｜%s" % (ch, len(idx), w))
odd = {}
for ch in t:
    o = ord(ch)
    if (0xac00 <= o <= 0xd7af) or (0x3040 <= o <= 0x30ff) or (0x3700 <= o <= 0x3fff):
        odd[ch] = odd.get(ch, 0) + 1
print(u"韓日及擴展區字元：%s" % odd)
words = sorted(set(w for w in __import__("re").findall(r"[A-Za-z]{3,}", t)))
print(u"拉丁詞（%d 個）：%s" % (len(words), u"、".join(words[:60])))
