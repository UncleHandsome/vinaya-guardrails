# -*- coding: utf-8 -*-
"""第 94 輪探針：印面「咬文嚼字／鑽牛角尖」五族之取證。

只掃印面（編纂底冊 C／K／L／M 不入——其文屬工帳，不勞讀者）；每族列行號與短句，
再由人斷：可刪（純防衛）、可縮（義在而辭費）、當留（法數或誠實標記）。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
DROP = ["修訂誌", "跨章款級索引", "十維驗收", "全書校勘記", "全書竣工呈辭"]
zone, zones, in_drop = "卷首", [], False
for l in LINES:
    if l.startswith("# "):
        in_drop = any(d in l for d in DROP)
        m = re.match(r"# (第[一二三四五六七八九]章|附錄[A-M]|結語|終卷)", l)
        zone = m.group(1) if m else l[2:12]
    zones.append((zone, in_drop))

FAM = {
    "甲·防衛自白": ["免來日", "校計者", "此非漏計", "非漏計", "如實標明", "無從覆核", "已就地",
                "不復追問", "難以推翻", "無可辯駁", "可資覆核", "未虛構", "並非虛", "非本書杜撰",
                "不敢自", "未嘗自", "不敢占", "非形上", "非法理之"],
    "乙·動機假設": ["嚴禁", "不得援", "絕不", "務必", "唯得", "准", "犯者", "违者", "違者", "同科",
                "以杜", "預杜", "杜絕", "防有", "恐人", "免致"],
    "丙·算術自證": ["兩側相符", "三向", "加總", "分毫不差", "無訛", "各安其位", "湊數", "閉環",
                "零漂移", "無一處漂移", "全數閉環", "合計", "覆核相符", "可逐案覆核"],
    "丁·名相所有權": ["餘稱不立", "別稱", "舊稱", "已廢", "不立", "定名", "不與", "同列", "專屬",
                "一名", "命之曰", "稱之", "不得混", "名同實異", "法定正名", "正作", "作正"],
    "戊·微觀强迫": ["情境甲", "情境乙", "態一", "態二", "態三", "A組", "B組", "C組", "第0項",
                "咳嗽", "口誤", "漏念", "一念", "剎那", "咽咽", "逐咽", "四更", "初夜", "中夜",
                "後夜", "明相"],
}
out = []
for fam, keys in FAM.items():
    hits = {}
    for i, l in enumerate(LINES):
        if zones[i][1]:
            continue
        for k in keys:
            if k in l:
                hits.setdefault(k, []).append(i + 1)
    tot = sum(len(v) for v in hits.values())
    out.append("\n##### %s：印面 %d 行 ##### " % (fam, tot))
    for k in sorted(hits, key=lambda x: -len(hits[x])):
        v = hits[k]
        z = {}
        for ln in v:
            z[zones[ln - 1][0]] = z.get(zones[ln - 1][0], 0) + 1
        out.append("  %-8s %3d 行｜%s" % (k, len(v), z))
        for ln in v[:3]:
            j = LINES[ln - 1].find(k)
            out.append("        L%-6d …%s…" % (ln, LINES[ln - 1][max(0, j - 34):j + 44]))
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r94probe.txt"),
        "w", encoding="utf-8").write("\n".join(out) + "\n")
sys.stdout.write("ok\n")
