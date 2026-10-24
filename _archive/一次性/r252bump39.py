# -*- coding: utf-8 -*-
"""第 252 輪：管線升版 ver38 → ver39（依 列印SOP 注意事項 9『版次＝工程代號＝檔名』）。

以逐對替換從 build38／verify38 造出 build39／verify39，每對須恰中一次，
不中或重中即擲回——不在舊檔上改，亦不留兩名混用之半升版檔。
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.exists(os.path.join(ROOT, "_tk.py")):
    ROOT = os.path.dirname(ROOT)          # 本檔在 _archive/一次性／內，須上溯至倉根

PAIRS_BUILD = [
    (u'"""ver38 雙版建置（承 build37.py 全套流程，來源改 ver38 修正版／第三十八版）',
     u'"""ver39 雙版建置（承 build38.py 全套流程，來源改 ver39 修正版／第三十九版）\n'
     u'\n'
     u'【ver39 之異於 ver38 者（升版當輪記）】\n'
     u'  一、附錄已改名并收為六篇（附錄一～附錄六，『十五則深描』分上・下兩篇 H1），\n'
     u'      編纂底冊四篇與終卷呈辭之去留一仍舊制（終卷不印）。\n'
     u'  二、正文八章（原第九章升格為第八章），第七章與第八章各分（上）（下）兩 H1。\n'
     u'  三、精簡本之削塊名單係對 ver38 字面而設，ver39 未立新制——run slim 即擲回，\n'
     u'      不產『半削之冊』（第 142 輪『寧可使建置失敗』之制今改為明閘）。'),
    (u'  slim       ：精簡本，僅收附錄 A／B（C～M 歸編纂底冊，不隨冊），卷首加一行存檔聲明',
     u'  slim       ：ver39 未定義精簡規則，跑即擲回（見上『三、』）'),
    (u'STEM = ("ver38四分律_起心動念心智分析框架_第三十八版_列印版" + SUFFIX',
     u'STEM = ("ver39四分律_起心動念心智分析框架_第三十九版_列印版" + SUFFIX'),
    (u'        "ver38四分律_起心動念心智分析框架_第三十八版_螢幕版" + SUFFIX)',
     u'        "ver39四分律_起心動念心智分析框架_第三十九版_螢幕版" + SUFFIX)'),
    (u'SRC = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")',
     u'SRC = os.path.join(ROOT, "ver39四分律_起心動念心智分析框架_修正版.md")'),
    (u'MD = os.path.join(HERE, "ver38_列印版%s%s.md" % (SUFFIX, TAG))',
     u'MD = os.path.join(HERE, "ver39_列印版%s%s.md" % (SUFFIX, TAG))'),
    (u'HTML = os.path.join(HERE, "ver38_列印版%s%s.html" % (SUFFIX, TAG))',
     u'HTML = os.path.join(HERE, "ver39_列印版%s%s.html" % (SUFFIX, TAG))'),
    (u'FINAL = os.path.join(HERE, "final38%s%s.html" % (SUFFIX, TAG))',
     u'FINAL = os.path.join(HERE, "final39%s%s.html" % (SUFFIX, TAG))'),
    (u'PDF = os.path.join(HERE, "ver38_列印版%s%s.pdf" % (SUFFIX, TAG))',
     u'PDF = os.path.join(HERE, "ver39_列印版%s%s.pdf" % (SUFFIX, TAG))'),
    (u'EDITION = ("第三十八版" +', u'EDITION = ("第三十九版" +'),
    (u'APPS = "附錄 A、B　二篇隨冊" if MODE == "slim" else "附錄 A、B、D–F、H–J　八篇隨冊"',
     u'APPS = "附錄一～六　六篇隨冊"'),
    (u'<p class="cov-meta">九章·一百則判例·六重心智閘門·八大正理<br />',
     u'<p class="cov-meta">八章·一百則判例·十五則補遺·六重心智閘門·八大正理<br />'),
    (u'        if ln.startswith("# 《四分律》起心動念心智分析框架"):',
     u'        if ln.startswith("# 《四分律"):'),
    (u'        if ln.strip() == "【第三十八版·全書深度校勘定本】":\n            continue',
     u'        if ln.strip() in ("【第三十八版·全書深度校勘定本】", "**【全新深度校勘定本】**"):\n            continue'),
    (u'            l.startswith("## 【開卷總提撕】") or l.startswith("# 第一章") for l in out',
     u'            l.startswith("## 【開卷總提撕】") or l.startswith("## 【自序")\n            or l.startswith("# 第一章") for l in out'),
    (u'# 中介檔名（實測作「ver38_列印版」）。', u'# 中介檔名（實測作「ver39_列印版」）。'),
    (u'def main():\n    t_all = time.perf_counter()',
     u'def main():\n'
     u'    if MODE == "slim":\n'
     u'        raise SystemExit(u"ver39 未立精簡本規則（削塊名單仍指 ver38 字面），"\n'
     u'                         u"故不產『與完整版同冊身而自稱精簡』之冊。欲出精簡本，先依 ver39 篇目重立 SLIM_KEEP、"\n'
     u'                         u"apply_slim_cuts 與第六章出處段之形（ver39 作『#### 【律典原典】』非『◎原典』）。")\n'
     u'    t_all = time.perf_counter()'),
]

PAIRS_VERIFY = [
    (u'"""ver38 列印版交付驗證：', u'"""ver39 列印版交付驗證：'),
    (u'與 build38 的同一假設互相印證', u'與 build39 的同一假設互相印證'),
    (u'用法：python _print/verify38.py', u'用法：python _print/verify39.py'),
    (u'    m = re.match(u"^附錄([A-Z])", ln)', u'    m = re.match(u"^附錄([一二三四五六七八九十])", ln)'),
    (u'    want = "AB" if "精簡本" in os.path.basename(pdf) else "ABDEFHIJ"',
     u'    want = u"一二三四五六"     # ver39 六篇俱隨冊；精簡本未立規則，故不別其應有'),
    (u'    for a in "ABCDEFHIJK":', u'    for a in u"一二三四五六":'),
    (u'    if u"三十八版" not in title:', u'    if u"三十九版" not in title:'),
    (u'    pairs = [("ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf", "final38.html", "完整版·影印"),\n'
     u'             ("ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf", "final38_精簡本.html", "精簡本·影印"),\n'
     u'             ("ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf", "final38_screen.html", "完整版·螢幕"),\n'
     u'             ("ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf", "final38_精簡本_screen.html", "精簡本·螢幕")]',
     u'    pairs = [("ver39四分律_起心動念心智分析框架_第三十九版_列印版.pdf", "final39.html", "完整版·影印"),\n'
     u'             ("ver39四分律_起心動念心智分析框架_第三十九版_螢幕版.pdf", "final39_screen.html", "完整版·螢幕")]'),
]


def bump(src_name, dst_name, pairs):
    text = io.open(os.path.join(ROOT, "_print", src_name), encoding="utf-8").read()
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            raise SystemExit(u"%s：錨點命中 %d 次（須恰 1）→ %s" % (src_name, n, old[:60]))
        text = text.replace(old, new)
    for key in (u'ver38_列印版', u'final38', u'ver38四分律', u'"第三十八版"'):
        if key in text:
            raise SystemExit(u"%s 內仍留舊冊之鑰『%s』（檔名與版次須全數隨動）" % (dst_name, key))
    out = os.path.join(ROOT, "_print", dst_name)
    io.open(out, "w", encoding="utf-8").write(text)
    print(u"已造 %s（%d 對替換俱中）" % (dst_name, len(pairs)))


bump("build38.py", "build39.py", PAIRS_BUILD)
bump("verify38.py", "verify39.py", PAIRS_VERIFY)
