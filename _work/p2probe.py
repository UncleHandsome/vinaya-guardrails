# -*- coding: utf-8 -*-
"""p2probe"""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
LINES = open(MD, encoding="utf-8").read().split("\n")
h1 = [(i + 1, ln[2:].strip()) for i, ln in enumerate(LINES) if ln.startswith("# ")]
NOPRINT_KEY = ("十維驗收", "全書校勘記", "全書竣工呈辭")

def region(n):
    cur = "卷首"
    for ln, t in h1:
        if ln <= n:
            cur = t
        else:
            break
    return cur

def noprint(t):
    return any(k in t for k in NOPRINT_KEY)

TARGETS = {
    "A 編纂腳手架": [r"腳本", r"\bFAIL\b", r"死鏈", r"第[一二三四五六七八九十百]+\輪", r"程式", r"自驗", r"不變量", r"跑版"],
    "B 幽靈附錄指針": [r"[見詳]附錄\s*[CDEFGHIJ]", r"附錄\s*[CDEFGHIJ]"],
    "C 算術自證": [r"\d+\s*[＋+]\s*\d+\s*[＝=]", r"[＝=]\s*\d+\s*[處則條列支]", r"合計", r"適符", r"恰成", r"之數"],
    "D 字頻統計": [r"字頻", r"凡\s*\d+\s*見", r"\d+\s*見", r"頻度"],
    "E 三重編碼": [r"出站口", r"閥門", r"道岔"],
    "F 科技隱喻": [r"木馬", r"\bAI\b", r"人工智慧", r"煤氣燈", r"演算法", r"駭客", r"資料庫", r"操作系統", r"代碼"],
    "G 卸甲呼吸窗": [r"卸甲呼吸窗"],
    "H 禪案律判": [r"南泉斬貓", r"丹霞燒佛", r"百丈野狐"],
    "I 公訴通報": [r"公訴通報", r"通報義務"],
    "J 離場機制": [r"離場"],
    "K 索引維度": [r"索引"],
    "L 變根科判": [r"變根", r"科判"],
    "M 五階漏斗": [r"漏斗"],
    "N 名詞考據": [r"舊譯", r"巴利"],
    "O 四大禁語": [r"四大禁語", r"四禁語"],
    "P 三級標籤": [r"三級心智標籤", r"三級梯隊"],
}

out = []
for tag, pats in TARGETS.items():
    out.append("\n" + "=" * 66)
    out.append("[" + tag + "]")
    for p in pats:
        rx = re.compile(p)
        hits = [(i + 1, ln) for i, ln in enumerate(LINES) if rx.search(ln)]
        pr = [(n, l) for n, l in hits if not noprint(region(n))]
        out.append("  -- %-14s print %3d / noprint %3d" % (p, len(pr), len(hits) - len(pr)))
        for n, ln in pr[:8]:
            out.append("     L%-6d [%s]  %s" % (n, region(n)[:14], ln.strip()[:88]))
        if len(pr) > 8:
            out.append("     ... more %d" % (len(pr) - 8))

with open(os.path.join(HERE, "p2out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("h1", len(h1))
