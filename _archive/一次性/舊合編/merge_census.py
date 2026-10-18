# -*- coding: utf-8 -*-
"""合編盤點尺：《兩書合編企畫審查與實作規劃.md》所引諸數之唯一產出處。

用法：python -X utf8 _merge/merge_census.py
只讀兩本正檔與指南附件，不寫任何檔；逐行印「目＝值」，供規劃檔隨時復算。
"""
import re, os, sys, io, glob
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VN = "ver38" + "".join(map(chr, (0x56DB, 0x5206, 0x5F8B))) + "_"  # ver38四分律_
_LAYERS = [ROOT, os.path.join(ROOT, "_archive", u"舊本")]


def _find(pat):
    for b in _LAYERS:
        g = sorted(glob.glob(os.path.join(b, pat)))
        if g:
            return g[0]
    raise SystemExit("找不到 %s（搜過：%s）" % (pat, _LAYERS))


V = _find("ver38*.md")
H = _find("".join(map(chr, (0x4F5B, 0x9640, 0x7684, 0x8B77, 0x6B04))) + "*.txt")
ATT = glob.glob(os.path.expanduser(r"~\.qoder\tmp\*\attachments\*\*.txt"))

vtxt = open(V, encoding="utf-8").read()
htxt = open(H, encoding="utf-8").read()
v, h = vtxt.split("\n"), htxt.split("\n")


def cjk(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def p(k, x):
    print("%-46s %s" % (k, x))


print("### 0 檔案")
p("ver38 路徑", os.path.basename(V))
p("護欄 路徑", os.path.basename(H))

print("\n### 1 規模")
p("ver38 行／印面漢字", "%d ／ %d" % (len(v), cjk(vtxt)))
p("護欄 行／印面漢字", "%d ／ %d" % (len(h), cjk(htxt)))
p("兩書漢字合計（合編上限）", cjk(vtxt) + cjk(htxt))
p("ver38 第六章百則區（L4708-8264）漢字", cjk("\n".join(v[4707:8264])))

print("\n### 2 ver38 骨架")
p("一級標題數", len(re.findall(r"^# ", vtxt, re.M)))
p("章名", " ".join(m.group(0) for m in re.finditer(r"^# 第[一二三四五六七八九]章", vtxt, re.M)))
p("附錄篇名", " ".join(m.group(1) for m in re.finditer(r"^# 附錄([A-Z])", vtxt, re.M)))
p("主檔內 C/K/L/M/G 附錄標題", len(re.findall(r"^# 附錄[CKLMG]", vtxt, re.M)))
p("編纂底冊", os.path.basename(os.path.join(ROOT, "_archive", "編纂底冊.md")) +
  " 存在=%s" % os.path.isfile(os.path.join(ROOT, "_archive", "編纂底冊.md")))
pat = re.compile(r"^#{2,5}\s*〔([^\d〕]*)(\d+)〕")
codes = {}
for i, l in enumerate(v, 1):
    m = pat.match(l)
    if m:
        codes.setdefault("〔%s%s〕" % (m.group(1), m.group(2)), i)
p("唯一案碼數／遮／開／僧／補遺", "%d／%d／%d／%d／%d" % (
    len(codes), sum(1 for k in codes if k.startswith("〔遮")), sum(1 for k in codes if k.startswith("〔開")),
    sum(1 for k in codes if k.startswith("〔僧")), sum(1 for k in codes if k.startswith("〔補遺"))))
p("定位行 全書／章外四條", "%d／%d" % (len(re.findall(r"^\*\*定位｜根本心", vtxt, re.M)),
                                sum(1 for i, l in enumerate(v, 1) if l.startswith("**定位｜根本心")
                                    and not 4708 <= i <= 8264)))
p("原典 blockquote（> 《）", len(re.findall(r"^> 《", vtxt, re.M)))

print("\n### 3 ver38 自帳諸數")
for kw, lbl in [("133", "133 綁定台帳"), ("定位行", "『定位行』字樣"), ("自算", "『自算』")]:
    p(lbl + " 出現", vtxt.count(kw))
p("第九章 存在", bool(re.search(r"^# 第九章", vtxt, re.M)))
p("凡例第二節定名", re.search(r"### .*承諾六律", vtxt).group(0).strip() if re.search(r"### .*承諾六律", vtxt) else "查無")
p("『逆向審計』全書", vtxt.count("逆向審計"))
p("『獵巫』ver38／護欄", "%d／%d" % (vtxt.count("獵巫"), htxt.count("獵巫")))

print("\n### 4 指南所引母案碼之落地率")
cited = """遮18 遮24 開12 遮27 遮26 補遺40 遮19 遮17 遮21 遮20 遮42 遮40 遮38 遮1 開17 開20
遮29 遮25 遮22 遮4 遮5 遮13 遮35 遮32 遮36 僧20 遮2 遮6 僧22 開7 遮39 遮23 開15 遮44
僧30 開21 開22 開18 僧26 僧27 遮45 遮33 僧3 僧1 開4 僧12 遮28 開11 開5 僧8 僧2 僧7""".split()
miss = [c for c in cited if "〔%s〕" % c not in codes]
p("所引碼數／查無", "%d／%d %s" % (len(cited), len(miss), " ".join(miss) or "（俱存在）"))
p("指南自創尼篇四碼之落地", " ".join("%s=%s" % (k, codes.get(k, "查無")) for k in ["〔尼-波5〕", "〔尼-波6〕", "〔尼-波7〕", "〔尼-波8〕"]))
p("第六章內『比丘尼』見數", "\n".join(v[4707:8264]).count("比丘尼"))
p("第六章尼篇獨立卡", len([k for k in codes if 4708 <= codes[k] <= 8264 and "尼" in k]))

print("\n### 5 指針爆炸半徑")
p("ver38 案內〔X N〕引用", len(re.findall(r"〔(?:遮|開|僧|補遺|遺)\d+〕", vtxt)))
p("ver38 『第N章…節』式引用", len(re.findall(r"第[一二三四五六七八九十]+章[第一二三四五六七八九十]*[節款]*", vtxt)))
p("ver38 『第N節』泛引用", len(re.findall(r"第[一二三四五六七八九十]+節", vtxt)))
p("ver38 『附錄X』引用", len(re.findall(r"附錄[A-Z]", vtxt)))
p("ver38 L#### 大正行錨", len(re.findall(r"L\d{3,4}", vtxt)))
p("ver38 『卷N』出處", len(re.findall(r"卷[一二三四五六七八九十百\d]+", vtxt)))
p("護欄 『第N章』全數", len(re.findall(r"第[一二三四五六七八九十]+章", htxt)))
p("護欄 『書中：第X章案例Y』", len(re.findall(r"書中：第[一二三四五六七八九十]+章案例", htxt)))
p("護欄 『第N條／款』", len(re.findall(r"第\s*\d+\s*[條款]", htxt)))

print("\n### 6 篇聚跨越（依篇聚重排之拆卡數）")
idx = [(i, l) for i, l in enumerate(v, 1) if re.match(r"^#### 〔(?:遮|開|僧)\d+〕", l)]
fam = {"波羅夷": ["波羅夷"], "僧殘": ["僧殘"], "捨墮": ["捨墮", "尼薩耆"],
       "單提": ["波逸提", "單提"], "提舍尼": ["提舍尼"], "眾學": ["眾學"],
       "犍度": ["犍度", "羯磨", "安居", "自恣", "布薩", "分衣"]}
cnt = Counter()
for k, (i, l) in enumerate(idx):
    j = idx[k + 1][0] - 1 if k + 1 < len(idx) else 8264
    t = "\n".join(v[i - 1:j])
    f = [x for x, keys in fam.items() if any(q in t for q in keys)]
    cnt[len(f)] += 1
p("觸及篇聚數分布（0/1/2/3/4）", "／".join(str(cnt[i]) for i in range(5)))
p("跨 >=2 篇聚（須拆或重掛）", sum(cnt[i] for i in (2, 3, 4)))
p("跨 >=3", sum(cnt[i] for i in (3, 4)))
p("章內含『第N條』錨之卡", sum(1 for i, l in idx if re.search(r"第\s*[一二三四五六七八九十\d]+\s*條",
        "\n".join(v[i - 1:(idx[idx.index((i, l)) + 1][0] - 1 if (i, l) != idx[-1] else 8264)]))))

print("\n### 7 卡片欄位與文風")
for lbl, key in [("ver38 事相經過", "##### 事相經過"), ("ver38 心相照鏡", "##### 心相照鏡"),
                 ("ver38 佛陀處斷", "##### 佛陀處斷"), ("ver38 人間智慧", "##### 人間智慧")]:
    p(lbl, vtxt.count(key))
for lbl, key in [("護欄 【案發現場", "【案發現場"), ("護欄 【防禦靶點】", "【防禦靶點】"),
                 ("護欄 【行為心理剖析】", "【行為心理剖析】"), ("護欄 【條文】", "【條文】"),
                 ("護欄 【初制戒文】", "【初制戒文】"), ("護欄 【心相照鏡】", "【心相照鏡】"),
                 ("護欄 【佛陀處斷】", "【佛陀處斷】"), ("護欄 定位行", "定位行")]:
    p(lbl, htxt.count(key))
seg = re.findall(r"##### 心相照鏡\n(.*?)(?=\n#)", vtxt, re.S)
p("ver38 心相照鏡段數／含『你』", "%d／%d" % (len(seg), sum("你" in s for s in seg)))
seg2 = re.findall(r"\*\*【行為心理剖析】：\*\*(.*?)(?=\n---)", htxt, re.S)
p("護欄 行為心理剖析段數／含『你』", "%d／%d" % (len(seg2), sum("你" in s for s in seg2)))
p("護欄 感嘆號 ！／！！／！！！", "%d／%d／%d" % (htxt.count("！"), htxt.count("！！"), htxt.count("！！！")))
p("護欄 指南點名之例句『無恥之尤』『徹底完蛋』", "%d／%d" % (htxt.count("無恥之尤"), htxt.count("徹底完蛋")))

print("\n### 8 義理對照之矛盾點")
i26 = codes.get("〔遮26〕")
p("ver38 〔遮26〕 定名", v[i26 - 1].strip("# "))
p("護欄 第六章案例一 定名", next(l for l in h if l.startswith("#### 案例一") and "改裝" in l).strip("# ")[:44])
p("『挫折慢心療法』在護欄", htxt.count("挫折慢心"))
p("護欄 卷首自限語（凡例 boundaries）", "有" if "本書之譯，不是律文之自稱" in htxt else "查無")

print("\n### 9 工具法源")
p("_tk.py 硬編章數行", [i for i, l in enumerate(open(os.path.join(ROOT, "_tk.py"), encoding="utf-8").read().split("\n"), 1)
                    if "九章齊備" in l])
p("hulan_path.py 偵測式", "根目錄唯一 佛陀的護欄*.txt；根目錄 *.txt 實數=%d" %
  len(glob.glob(os.path.join(ROOT, "*.txt"))))
p("護欄跑批／框架跑批", "hlbattery.py(17尺)／battery.py＋verify_audit.py")

print("\n### 10 指南附件體檢")
if len(sys.argv) > 1:
    ATT = [sys.argv[1]]
else:
    ATT = [f for f in glob.glob(os.path.expanduser(r"~\.qoder\tmp\*\attachments\*\*.txt"))
           if "七部二十八章" in open(f, encoding="utf-8", errors="ignore").read()]
att = ATT[0] if ATT else None
if att:
    a = open(att, encoding="utf-8").read()
    al = a.split("\n")
    p("附件", os.path.basename(att))
    p("附件 行／漢字", "%d／%d" % (len(al), cjk(a)))
    dup = [i for i, l in enumerate(al, 1) if l.startswith("# 第二次對話")]
    p("『第二次對話』標題行", dup)
    if len(dup) == 2:
        d0, d1 = dup
        A = [l.rstrip() for l in al[d0 - 1:d1 - 2] if l.strip()]
        B = [l.rstrip() for l in al[d1 - 1:d1 - 2 + len(A)] if l.strip()]
        p("重複段長（去空白行）", len(A))
        p("第一次出現 ≡ 第二次出現", "逐字同" if A == B else
          ("前 %d 行全同（其後為第二次之續文）" % sum(1 for x, y in zip(A, B) if x == y)
           if all(x == y for x, y in zip(A, B)) else "不同"))
    p("一級／二級／三級目", "%d／%d／%d" % (len(re.findall(r"^# ", a, re.M)), len(re.findall(r"^## ", a, re.M)),
                                       len(re.findall(r"^### ", a, re.M))))
    p("缺『壹、』", not re.search(r"^## 壹", a, re.M))

print("\n### 11 遺漏補量（第二輪自查）")
print("-- 正名變體（指南驗收第 4 條之七名，兩冊各計）")
VAR = [("目連", ["目連", "大目連", "大目犍連", "目犍連"]),
       ("瓶沙王", ["瓶沙王", "頻婆娑羅"]),
       ("闡陀", ["闡陀", "烏陀夷", "優陀夷"]),
       ("守籠那", ["守籠那", "拘留梨"]),
       ("給孤獨", ["給孤獨", "須達"]),
       ("蓮華色", ["蓮華色", "優鉢先那"]),
       ("憂陀延", ["憂陀延", "優陀延"])]
for name, forms in VAR:
    row = []
    for f in forms:
        row.append("%s:%d/%d" % (f, vtxt.count(f), htxt.count(f)))
    p("  " + name, "  ".join(row))

print("-- 兩冊同題之『兩份真相』重疊（字面計數）")
for lbl, kw in [("出堂洗心", "出堂洗心"), ("消磁", "消磁"), ("護欄", "護欄"),
                ("行動卡", "行動卡"), ("四重", "四重"), ("工具箱", "工具箱"),
                ("多巴胺", "多巴胺"), ("前額葉", "前額葉"), ("選擇架構", "選擇架構"),
                ("福格", "福格"), ("破窗", "破窗"), ("無事清涼", "無事清涼")]:
    p("  " + lbl, "框架 %d ／護欄 %d" % (vtxt.count(kw), htxt.count(kw)))

print("-- 道宣與『城郭』『以遮衛性』之歸屬（同列共現）")
for lbl, txt in [("框架", v), ("護欄", h)]:
    hits = [i for i, l in enumerate(txt, 1) if ("道宣" in l or "元照" in l or "弘一" in l)
            and ("城郭" in l or "以遮衛性" in l or "宮殿" in l)]
    p("  %s 共現行" % lbl, hits or "無同列（分置兩處）")
p("  『首創』在護欄", htxt.count("首創"))

print("-- 卷首五件之兩冊對照（行號）")
def find(lst, pats):
    out = []
    for p2 in pats:
        i = next((k for k, l in enumerate(lst, 1) if l.startswith(p2) or l.startswith("## " + p2)), 0)
        out.append("%s=L%d" % (p2, i))
    return " ".join(out)
p("  框架", find(v, ["## 【開卷總提撕】", "## 【卷首導讀", "## 【全書凡例】", "## 【全書開卷標準目錄】", "# 結語"]))
p("  護欄", find(h, ["# 【卷首·扉頁】", "# 自序", "## 導讀指南", "# 【全書詳細目錄】", "# 十線地圖"]))
p("  護欄 目錄內『第N章』條目", len(re.findall(r"第[一二三四五六七八九十]+章", "\n".join(h[76:441]))))
p("  框架 目錄內『第N章』條目", len(re.findall(r"第[一二三四五六七八九]章", "\n".join(v[253:382]))))

print("-- 二十犍度（指南第十三章僅標『上』）")
i11 = next(i for i, l in enumerate(h, 1) if l.startswith("# 第十一章"))
seg = "\n".join(h[i11 - 1:i11 + 40])
p("  護欄 Ch.11 標『廿／二十犍度』名目之行列數", len([l for l in seg.split("\n") if "犍度" in l]))
p("  『犍度』字面 框架／護欄", "%d／%d" % (vtxt.count("犍度"), htxt.count("犍度")))

print("-- 新散文須過之兩冊舊尺（標點與簡形）")
half = lambda t: len(re.findall(r"[\u4e00-\u9fff][,.;:!?][\u4e00-\u9fff]", t))
p("  漢字間半形標點 框架／護欄", "%d／%d" % (half(vtxt), half(htxt)))
p("  全形括號『（』 框架／護欄", "%d／%d" % (vtxt.count("（"), htxt.count("（")))

print("-- 護欄附錄之 250／348 宣稱")
ia = next(i for i, l in enumerate(h, 1) if l.startswith("# 附錄"))
apx = h[ia - 1:]
p("  附錄起訖", "L%d–L%d（檔尾 L%d）" % (ia, len(h), len(h)))
p("  附錄內表格行", len([l for l in apx if l.strip().startswith("|")]))
p("  附錄內三級以上小標", [(k, l[:26]) for k, l in enumerate(apx, ia) if re.match(r"^#{2,3} ", l)][:6])
p("  附錄內『戒』字行數樣本", len([l for l in apx if re.match(r"^\|\s*\d+", l)]))

print("\n### 12 第三輪補量（指南清單之完備性）")
atext = globals().get("a", "")
ap = {}
for i, l in enumerate(v, 1):
    m = re.match(r"^# 附錄([A-Z])", l)
    if m:
        e = next((k for k in range(i + 1, len(v) + 1) if v[k - 1].startswith("# ")), len(v) + 1)
        ap[m.group(1)] = (i, e - 1, e - 1 - i + 1, cjk("\n".join(v[i - 1:e - 1])))
p("  框架八篇附錄（起・迄・行・漢字）", " ".join("%s:%d–%d/%d/%d" % a for a in [(k, *x) for k, x in sorted(ap.items())]))
if atext:
    p("  指南提及『附錄H』／『附錄I』字樣", "%d／%d" % (atext.count("附錄H"), atext.count("附錄I")))
    p("  指南所保留六大附錄之字母", " ".join(k for k in "ABDEFHIJ" if "附錄%s" % k in atext or "（附錄 %s" % k in atext))
    p("  指南所列四名動線", re.findall(r"四種讀者[^（\n]*（([^）]{4,40})）", atext)[:1])
p("  框架 卷首導讀 之四名動線", re.findall(r"（[^（）\n]{2,12}流）", "\n".join(v[85:260]))[:6])
p("  『動線』框架／護欄", "%d／%d" % (vtxt.count("動線"), htxt.count("動線")))
p("  附錄H 內補遺碼（去重）", len(set(re.findall(r"〔補遺\d+〕", "\n".join(v[ap["H"][0] - 1:ap["H"][1]])))))
p("  附錄I 首小標", [l[:30] for l in v[ap["I"][0]:ap["I"][1]] if l.startswith("### ")][:2])

print("-- 戒數之通數（指南「一號不漏」對護欄自制）")
m = re.findall(r"^## ([甲乙])、比丘尼?戒本：(.+?)（戒本\s*(\d+)\s*條，律文別宣\s*(\d+|全)", htxt, re.M)
for g, t, claim, shown in m:
    p("  %s組 %s" % (g, t[:20]), "戒本 %s 條／別宣 %s 條" % (claim, shown))
p("  甲組合計", sum(int(c) for g, t, c, s in m if g == "甲"))
p("  乙組合計", sum(int(c) for g, t, c, s in m if g == "乙"))
i6780 = next((l for l in h if "至通數之別" in l), "")
p("  護欄附錄之自解通數語", i6780.strip()[:120])

print("-- 護欄『一案列多條』之案例（撞指南之條次切分）")
def chap_bounds(lines):
    CNd = {c: i + 1 for i, c in enumerate("一二三四五六七八九十")}
    def n2(s):
        if s == "十": return 10
        if "十" in s:
            a, _, b = s.partition("十"); return CNd.get(a, 1) * 10 + CNd.get(b, 0)
        return CNd.get(s, 0)
    ch = [(n2(mm.group(1)), k) for k, mm in ((k, re.match(r"^# 第([一二三四五六七八九十]+)章", l)) for k, l in enumerate(lines, 1)) if mm]
    return {n: (s, ch[k + 1][1] - 1 if k + 1 < len(ch) else len(lines)) for k, (n, s) in enumerate(ch)}
tb = 0
for n, (s, e) in sorted(chap_bounds(h).items()):
    hd = [l for l in h[s - 1:e - 1] if l.startswith("#### 案例")]
    multi, nums = 0, set()
    for l in hd:
        mm = re.search(r"（第([^）]*)條）", l)
        if mm:
            g = re.findall(r"\d+", mm.group(1)); nums.update(int(x) for x in g)
            if len(g) >= 2: multi += 1
    if multi:
        p("  Ch.%d" % n, "案例 %d・列多條者 %d・條次 %d 個（%d～%d）" % (len(hd), multi, len(nums), min(nums), max(nums)))
        tb += multi
p("  全書『一案列多條』合計", tb)

print("\n### 13 第四輪補量（台帳算式・術語落地・標記公約・底冊・遺碼）")
loc = [(i, l) for i, l in enumerate(v, 1) if l.startswith("**定位｜根本心")]
def binds(l):
    return sorted(set(re.findall(r"正理([一二三四五六七八])", l.split("八大正理：")[-1])))
in6 = [(i, l) for i, l in loc if 4708 <= i <= 8264]
out6 = [(i, l) for i, l in loc if not (4708 <= i <= 8264)]
s6 = sum(len(binds(l)) for i, l in in6)
per = [len(binds(l)) for i, l in in6]
p("  定位行 章內＋章外", "%d＋%d＝%d" % (len(in6), len(out6), len(loc)))
p("  第六章綁定復算（書中宣稱 133）", "%d（%s）" % (s6, "合" if s6 == 133 else "不合"))
p("  每卡綁定分布 0/1/2/3/4", "／".join(str(per.count(x)) for x in range(5)))
p("  章外四卡（附錄J）綁定", sum(len(binds(l)) for i, l in out6))
p("  若 164 案各帶定位行・綁定增數推算", "1.33×164 ≈ %d 處（133→%d）" % (round(s6 / 100 * 164), s6 + round(s6 / 100 * 164)))
TERMS = ["審慮思", "決定思", "動發勝思", "三十格", "留白", "優波離", "三種舉", "使作", "日落",
         "第三值", "四步驗證", "一事不再理", "境想六句", "十三難", "遮法", "精神障礙", "作犯",
         "止犯", "三時心", "破法輪僧", "破羯磨僧", "命難", "貞操", "職守臨界", "財產臨界",
         "五受", "客體非道", "創傷知情", "失念", "憶念現前", "滿五錢", "言聲", "賴寄",
         "數位資產", "拐賣", "阿那般那", "摩那埵", "阿浮呵那", "本日治", "修合別住", "失宿",
         "清淨別住", "善逝推定", "非法足數", "下意羯磨", "帶贓不許懺", "與學比丘", "白四羯磨",
         "白二羯磨", "求聽", "自言治", "與欲", "結小界", "解界重結", "行舍羅", "五德", "罪處所",
         "多人語", "如草覆地", "憶念毘尼", "不癡毘尼", "現前毘尼", "八事成重", "式叉摩那", "二部僧"]
mv = [t for t in TERMS if t not in vtxt]
mh = [t for t in TERMS if t not in htxt]
p("  術語表長度", len(TERMS))
p("  框架查無", "、".join(mv) or "無")
p("  護欄查無（%d 項）" % len(mh), "、".join(mh[:18]) + "…")
p("  『八事』兩義（結集八事開許 vs 尼八事成重）", "框架『八事』%d 見、『八事成重』連寫 %d 見" % (vtxt.count("八事"), vtxt.count("八事成重")))
for m2 in ["◎原典", "◎", "◈", "◆", "▲", "〔◈宗派〕", "──►", "╳", "〔合編說明〕", "〔名相〕"]:
    p("  標記 %s 框架／護欄" % m2, "%d／%d" % (vtxt.count(m2), htxt.count(m2)))
i3 = next((i for i, l in enumerate(v, 1) if l.startswith("### 一、三層標記")), 0)
p("  框架凡例第一節定名", v[i3 - 1].strip() if i3 else "查無")
B = os.path.join(ROOT, "_archive", "編纂底冊.md")
if os.path.isfile(B):
    bt = open(B, encoding="utf-8").read(); bl = bt.split("\n")
    p("  底冊 行／漢字／篇目", "%d／%d／%s" % (len(bl), cjk(bt), " ".join(l[2:8] for l in bl if l.startswith("# 附錄"))))
    kk = next((i for i, l in enumerate(bl, 1) if l.startswith("# 附錄K")), 0)
    kseg = bl[kk - 1:]
    nxt = next((j for j, l in enumerate(kseg[1:], 2) if l.startswith("# ")), len(kseg))
    kseg = kseg[:nxt - 1]
    p("  K 篇 表格數據行／『第N款』行", "%d／%d（指南自稱 55 條）" % (len([l for l in kseg if l.strip().startswith("|")]),
                                                        len([l for l in kseg if re.search(r"第[一二三四五六七八九十]+款", l)])))
p("  〔遺N〕唯一碼／所見", "%d／%d" % (len(set(re.findall(r"〔遺\d+〕", vtxt))), vtxt.count("〔遺")))
p("  〔遺8〕＝千兩金囊案？", "是" if re.search(r"〔遺8〕[^。]{0,12}千兩金", vtxt) else "需目核")
p("  指南盜戒家族三碼之實有", "遮43=%s 開3=%s 遮44=%s（〔開3-附1〕為指南自創子碼）" % tuple(
    "有" if k in codes else "無" for k in ["〔遮43〕", "〔開3〕", "〔遮44〕"]))

print("\n### 14 對照表全量機核（第五輪：指南兩張映射表逐格核）")
al = globals().get("al", [""])
CARD = {}
for i, l in enumerate(v, 1):
    m = re.match(r"^#{2,5}\s*〔([^\d〕]*)(\d+)〕", l)
    if m:
        CARD.setdefault("〔%s%s〕" % (m.group(1), m.group(2)), [i, set()])
    if l.startswith("**定位｜根本心") and CARD:
        ks = [k for k in CARD if CARD[k][0] <= i]
        if ks:
            CARD[max(ks, key=lambda k: CARD[k][0])][1] = set(
                re.findall(r"正理([一二三四五六七八])", l.split("八大正理：")[-1]))
CNd = {c: i + 1 for i, c in enumerate("一二三四五六七八九十")}
def c2n(s):
    if s == "十": return 10
    if "十" in s:
        x, _, y = s.partition("十"); return CNd.get(x, 1) * 10 + CNd.get(y, 0)
    return CNd.get(s, 0)
chp = [(c2n(m.group(1)), i) for i, l in enumerate(h, 1) if (m := re.match(r"^# 第([一二三四五六七八九十]+)章", l))]
CASE, SECT = {}, {}
for kk, (n, s) in enumerate(chp):
    e = chp[kk + 1][1] - 1 if kk + 1 < len(chp) else len(h)
    for i, l in enumerate(h[s - 1:e - 1], s):
        m = re.match(r"^#### 案例([一二三四五六七八九十]+)", l)
        if m: CASE[(n, c2n(m.group(1)))] = 1
        m2 = re.match(r"^### ([一二三四五六七八九十]+)、", l)
        if m2: SECT[(n, c2n(m2.group(1)))] = 1
rows = [l for l in al if l.strip().startswith("|") and ("〔" in l or "文獻一" in l) and "---" not in l and "案例序號" not in l and "本部章次" not in l]
p("  表內資料行（第三部＋第四部兩表）", len(rows))
lostc, lostref, badrat, delta = [], [], [], 0
claim_total = 0
for r in rows:
    cs = [c.strip() for c in r.strip().strip("|").split("|")]
    if len(cs) < 5: continue
    mother, hup, rat = cs[2], cs[3] + " " + cs[1], cs[4]
    cds = re.findall(r"〔[^\n〕]+〕", mother) or re.findall(r"〔[^\n〕]+〕", cs[1])
    for c in cds:
        k = c.split("（")[0]
        if k not in CARD and k not in codes: lostc.append(k)
    cl = set(re.findall(r"正理([一二三四五六七八])", rat))
    claim_total += len(cl)
    if cds:
        act = CARD.get(cds[0].split("（")[0], [0, set()])[1]
        if cl and act and not cl <= act:
            badrat.append((cds[0].split("（")[0], sorted(cl), sorted(act)))
            delta += len(cl) - len(act)
    for cn, num in re.findall(r"Ch\.(\d+)\s*案([一二三四五六七八九十]+)", hup):
        if (int(cn), c2n(num)) not in CASE: lostref.append("Ch.%s 案%s" % (cn, num))
    for cn, num in re.findall(r"Ch\.(\d+)\s*第([一二三四五六七八九十]+)節", hup):
        if (int(cn), c2n(num)) not in SECT: lostref.append("Ch.%s 第%s節" % (cn, num))
p("  『文獻一 Ch.N 案M／第N節』失指", sorted(set(lostref)) or ("零（表內 %d 行指針全數落地）" % len(rows)))
p("  母案碼查無（指南自創）", sorted(set(lostc)))
p("  正理欄宣稱格數／與定位行不合", "%d／%d" % (claim_total, len(badrat)))
for x in badrat:
    p("    不合", "%s 表列%s vs 定位行%s" % x)
p("  若照表覆寫定位行・綁定總數之變", "133 → %d（且正理二・五・六・七之分計全盤重算）" % (133 + delta))

print("-- 合併後同章打架之二例（義理衝突）")
p("  『前十二年』框架／護欄／指南提及", "%d／%d／%s" % (vtxt.count("前十二年"), htxt.count("前十二年"),
                                        "未提" if "前十二年" not in (a or "") else "提"))
p("  框架之用法（卷首敘事前提）", v[15].strip()[:44] + "…")
p("  護欄之自限（第五章）", next(l for l in h if "前十二年" in l).strip()[max(0, next(l for l in h if "前十二年" in l).find("前十二年") - 12):][:78])
p("  『本律無文』式自限 框架／護欄", "%d 行／%d 行" % (sum(1 for l in v if "無文" in l), sum(1 for l in h if "無文" in l)))
p("  道宣之喻：護欄原文小標 L6196", "「以遮衛性」與城郭之喻的**集大成者**（非『首創』）")
p("  指南作『首創』", (a or "").count("首創"))
p("  護欄已立之自限三處", "L6192 非道宣自著・L6197 非《鈔》之文・L6199 括旨非逐字")

print("\n### 15 涵蓋率（第六輪：哪些案在合冊中無著落）")
hundred = {k: t for k, t in codes.items()}
h100 = {k: v[0] for k in codes if not k.startswith("〔補遺")}  # 碼→行
ttl = {}
for l in v:
    m = re.match(r"^#{2,5}\s*〔([^\d〕]*\d+)〕\s*(.*)$", l)
    if m and not m.group(1).startswith("補遺"):
        ttl.setdefault("〔%s〕" % m.group(1), m.group(2).strip())
at = globals().get("a", "")
code_cited = {k for k in ttl if k in at}
def keyforms(t):
    out = []
    for s in re.split(r"[——，、・（]", t):
        s = s.strip()
        if len(s) >= 3:
            out += [s[:8], s[-8:]]
    return [x for x in out if len(x) >= 3]
name_cited = {k for k, t in ttl.items() if k not in code_cited and any(f in at for f in keyforms(t))}
p("  百則・碼形點名／名形補點", "%d／%d" % (len(code_cited), len(name_cited)))
missF = sorted((k for k in ttl if k not in code_cited and k not in name_cited),
               key=lambda z: (z[1], int(re.search(r"\d+", z).group())))
p("  【無著落】百則之中", "%d／100（%s）" % (len(missF), "．".join(
    "%s%d" % (x, sum(1 for k in missF if k.startswith("〔" + x))) for x in "遮開僧")))
i7 = next((i for i, l in enumerate(v, 1) if l.startswith("# 第七章")), 0)
seg7 = "\n".join(v[i7 - 1:i7 + 800])
seen, deep = set(), []
for d in re.findall(r"〔(?:遮|開|僧)\d+〕", seg7):
    if d not in seen:
        seen.add(d); deep.append(d)
deep = [d for d in deep if d in ttl][:29]
p("  第七章板塊 A–I 深水案", "%d 案，其中未被點名 %d 案：%s" % (
    len(deep), len([d for d in deep if d in missF]), "、".join(d for d in deep if d in missF)))
CASES = []
for kk, (n, s) in enumerate([(c2n(m.group(1)), i) for i, l in enumerate(h, 1)
                             if (m := re.match(r"^# 第([一二三四五六七八九十]+)章", l))]):
    e = [(c2n(m2.group(1)), i2) for i2, l2 in enumerate(h, 1) if (m2 := re.match(r"^# 第([一二三四五六七八九十]+)章", l2))]
    e = e[kk + 1][1] - 1 if kk + 1 < len(e) else len(h)
    for i, l in enumerate(h[s - 1:e - 1], s):
        m = re.match(r"^#### 案例([一二三四五六七八九十]+)：(.*)", l)
        if m:
            mm = re.search(r"（第([^）]*)條）", l)
            CASES.append((n, c2n(m.group(1)), i, m.group(2)[:36],
                          {int(x) for x in re.findall(r"\d+", mm.group(1))} if mm else set()))
bycase = {(n, k) for n, k, i, t, ru in CASES if ("Ch.%d 案%s" % (n, "".join(c for c, vv in CNd.items() if vv == k))) in at}
byrule = {(n, k) for n, k, i, t, ru in CASES if ru and any(("第%d條" % x) in at for x in ru)}
bytitle = {(n, k) for n, k, i, t, ru in CASES if (n, k) not in bycase and (n, k) not in byrule
           and any(w in at for w in re.findall(r"[\u4e00-\u9fff]{4,8}", t)[:3])}
missH = [(n, k, i, t) for n, k, i, t, ru in CASES if (n, k) not in bycase and (n, k) not in byrule and (n, k) not in bytitle]
p("  護欄・案次形／條次形／專名形", "%d／%d／%d（全 %d 案）" % (len(bycase), len(byrule), len(bytitle), len(CASES)))
p("  【無著落】三口徑皆未點名", "%d／164" % len(missH))
dist = {}
for n, k, i, t in missH:
    dist[n] = dist.get(n, 0) + 1
p("    分布（章：案數）", "．".join("Ch.%d:%d" % x for x in sorted(dist.items())))
p("  『二部僧』框架／護欄", "%d／%d" % (vtxt.count("二部僧"), htxt.count("二部僧")))
p("  『第N部』部次語 框架／護欄", "%d／%d" % (len(re.findall(r"第[一二三四五六七]部", vtxt)),
                                        len(re.findall(r"第[一二三四五六七]部", htxt))))
p("  章號之形：指南『第 N ～ M 章』", "%d 處；指南『Ch.N』%d 處；指南漢字章號 %d 處" % (
    len(re.findall(r"第\s*\d+\s*～\s*\d+\s*章", at)), len(re.findall(r"Ch\.\s*\d+", at)),
    len(re.findall(r"第[一二三四五六七八九十]+章", at))))
p("  框架『第N條』漢字／阿拉伯", "%d／%d" % (len(re.findall(r"第[一二三四五六七八九十百]+條", vtxt)),
                                      len(re.findall(r"第\s*\d+\s*條", vtxt))))
p("  框架【人間智慧】段含『我們』", "%d／100" % sum(
    "我們" in s for s in re.findall(r"##### 人間智慧\n(.*?)(?=\n#)", vtxt, re.S)))






