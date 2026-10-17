# -*- coding: utf-8 -*-
"""第 96 輪探針：印面咬文嚼字之普查（只報數，不改檔）。附錄C／K／L／M 乃編纂底冊，不計。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")

def find(pat):
    for i, l in enumerate(L):
        if l.startswith(pat):
            return i
    raise SystemExit("找不到 " + pat)

aC, aK, aL, aM = find("# 附錄C"), find("# 附錄K"), find("# 附錄L"), find("# 附錄M")
seg = "\n".join(L[:aC] + L[aK:aL] and L[:aC] + L[aK:aL])  # placeholder
body = "\n".join(L[:aC]) + "\n" + "\n".join(L[aK:aL]) + "\n" + "\n".join(L[aM:])
print("印面行数 %d（附錄C 於 %d、K 於 %d、L 於 %d、M 於 %d）" % (body.count("\n"), aC, aK, aL, aM))

pats = collections.OrderedDict([
    ("行内反引號", r"`[^`\n]{1,40}`"),
    ("（此乃", r"（此乃"), ("（即", r"（即"), ("（以下簡", r"（以下簡"),
    ("必須強調", r"必須強調"), ("特別說明", r"特別說明"), ("值得注意", r"值得注意"),
    ("眾所周知", r"眾所周知"), ("不難發現", r"不難發現"), ("綜上所述", r"綜上所述"),
    ("一言以蔽之", r"一言以蔽之"), ("換言之", r"換言之"), ("簡言之", r"簡言之"),
    ("英文縮寫", r"\b[A-Z]{2,6}\b"), ("全形驚嘆", r"！{2,}"), ("問號連用", r"？{2,}"),
    ("之之之", r"[^，。\n]{2,10}之[^，。\n]{2,10}之[^，。\n]{2,10}之"),
    ("（按", r"（按"), ("〔案〕", r"〔案〕"), ("〔註", r"〔註"), ("（原", r"（原"),
    ("笔者/本書自稱", r"本書"), ("同上", r"同上"),
])
for k, p in pats.items():
    ms = re.findall(p, body)
    if ms:
        c = collections.Counter(ms).most_common(5)
        print("  %-12s %4d  %s" % (k, len(ms), " / ".join(("%s×%d" % (a[:28], b)) for a, b in c)))
