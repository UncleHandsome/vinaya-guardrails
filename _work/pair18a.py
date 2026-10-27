# -*- coding: utf-8 -*-
"""第十八波・第二本（《如法推尋》）之校訂：外路兩報之真病十九刀。
每刀唯一錨・乾跑印前後・落畢自證（舊字盡去・新文無簡形・CRLF 不動・BOM 不動）。

用法：python -X utf8 _work/pair18a.py [--write]
"""
import io
import os
import shutil
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp as PS                                          # noqa: E402

F2 = os.path.join(ROOT, "如法推尋：僧伽憲政、法權審理與修復正義.txt")
BAK = os.path.join(ROOT, "_archive", "備份", "AI清理前")
WRITE = "--write" in sys.argv

JOBS = [
    (u"凡例・跳號七➔六（無第六條）",
     u"### 七、標題層級體例與附錄收編之界",
     u"### 六、標題層級體例與附錄收編之界"),
    (u"凡例・總帳之附錄號（四➔二）",
     u"全書總帳一以附錄四 102 案為準",
     u"全書總帳一以附錄二 102 案為準"),
    (u"凡例・新舊次碼對照之附錄號（四➔二）",
     u"彙為附錄四末〔新舊次碼對照〕一節",
     u"彙為附錄二末〔新舊次碼對照〕一節"),
    (u"附錄一・回查索引之附錄號（四➔二）",
     u"此表與【附錄四】回查索引同一案號",
     u"此表與【附錄二】回查索引同一案號"),
    (u"附錄三・象力之巴利名（未收➔Hatthaka）",
     u"| **象力** | 象力釋子 | 未收 |",
     u"| **象力** | 象力釋子 | Hatthaka Sakyaputta |"),
    (u"梵巴分流・四人僧（梵➔巴）", u"Caturvarga", u"Catuvagga"),
    (u"梵巴分流・五人僧（梵➔巴）", u"Pañcavarga", u"Pañcavagga"),
    (u"梵巴分流・十人僧（梵➔巴）", u"Daśavarga", u"Dasavagga"),
    (u"梵巴分流・二十人僧（梵➔巴）", u"Viṃśativarga", u"Vīsativagga"),
    (u"梵巴分流・戒體無作（梵➔巴）", u"Avijñapti-śīla", u"Aviññatti-sīla"),
    (u"檢綱・其一體例（十一）", u"**十一・使作之檢**", u"**其十一・使作之檢**"),
    (u"檢綱・其一體例（十二）", u"**十二・開許之檢**", u"**其十二・開許之檢**"),
    (u"檢綱・其一體例（十三）", u"**十三・第三值之檢**", u"**其十三・第三值之檢**"),
    (u"檢綱・其一體例（十四）", u"**十四・自白之檢**", u"**其十四・自白之檢**"),
    (u"檢綱・其一體例（十五）", u"**十五・四署之檢**", u"**其十五・四署之檢**"),
    (u"檢綱・其一體例（十六）", u"**十六・平息之檢**", u"**其十六・平息之檢**"),
    (u"對位表・世俗欄混入僧語",
     u"**外部客僧覆審之體**", u"**獨立稽核與外部獨立保證**"),
    (u"長照圖・四➔五大支柱",
     u"【長照耗竭防禦作持儀軌四大支柱】", u"【長照耗竭防禦作持儀軌五大支柱】"),
    (u"五盾圖・四五欄黏連",
     u"本訴獨立審結原則機密調查期間正當",
     u"本訴獨立審結原則  機密調查期間正當"),
    (u"十六章一節・題文相符",
     u"### 第一節　穿透名義代持與四種僧物不可分割",
     u"### 第一節　穿透名義代持與實質受用人審查"),
    (u"十五章末款・分號收句",
     u"僧團得無限期維持「不見罪舉（與僧不同住）」；",
     u"僧團得無限期維持「不見罪舉（與僧不同住）」。"),
    (u"僧物分位・第四分➔第三分（圖）",
     u"【第四分：果葉日用（消耗分潤·現前物）】",
     u"【第三分：果葉日用（消耗分潤·現前物）】"),
    (u"僧物分位・第四分➔第三分（題）",
     u"#### 二、第四分：數位果葉（現前現前物·如法分配）",
     u"#### 二、第三分：數位果葉（現前現前物·如法分配）"),
    (u"僧物分位・第四分➔第三分（定性）", u"（第四分僧物）", u"（第三分僧物）"),
    (u"僧物分位・明其唯涉二物",
     u"律典在《房舍犍度》確立的**「四種僧物」**，為數位資產提供了精準的法相錨定：",
     u"律典在《房舍犍度》確立的**「四種僧物」**，為數位資產提供了精準的法相錨定："
     u"四物之中，數位資產所涉者唯第一分（常住常住）與第三分（現前現前）："),
    (u"凡例・四十字之但書（本地檔無標點者）",
     u"不得以『引文從省』諉之。",
     u"不得以『引文從省』諉之；唯本地檔原無標點者不在此數——照錄其形並自標『原檔無標點』，"
     u"不以今人句讀改易原卷。"),
]
BAN = (u"### 七、標題層級", u"附錄四 102 案", u"附錄四末〔新舊次碼", u"【附錄四】回查索引",
       u"Caturvarga", u"Pañcavarga", u"Daśavarga", u"Viṃśativarga", u"Avijñapti",
       u"【第四分：果葉", u"第四分僧物", u"四大支柱】", u"穿透名義代持與四種僧物不可分割")

DIV_OLD = (u"  > **「大德僧聽！此住處若有前人所結大小界、行處無行處界，僧今為和合說戒（受戒）故，"
           u"如法解前界，解已更結！若僧時到僧忍聽，僧今解前界。白如是。」**")
DIV_NEW = (u"  > **「大德僧聽！今此住處比丘同一住處同一說戒，若僧時到僧忍聽，解界。白如是。」**  \n"
           u"  >  \n"
           u"  > **「大德僧聽！此住處比丘同一住處同一說戒，今解界。誰諸長老忍僧今同一住處同一說戒"
           u"解界者默然，誰不忍者說。」**  \n"
           u"  >  \n"
           u"  > **「僧已忍同一住處同一說戒解界竟，僧忍默然故，是事如是持。」**  \n"
           u"  >  \n"
           u"  > ——《四分律》解界白二羯磨（本地語料 31-37 檔段・原檔無標點，今依義斷句）")
LEAD_OLD = u"* 大眾於大界召開常規大會之開端，先召開白二羯磨，由說白僧唱出清障定文："
LEAD_NEW = u"* 大眾於大界召開常規大會之開端，先召開白二羯磨，由說白僧唱出解界定文（白・羯磨・結三節，缺一不成）："


def run(path):
    raw = io.open(path, "rb").read()
    txt = raw.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in txt else "\n"
    for why, old, new in JOBS:
        n = txt.count(old)
        print(u"  · %-30s 命中 %d" % (why, n))
        if n < 1:
            raise SystemExit(u"錨不見：%s" % why)
        i = txt.find(old)
        print(u"      ⟪%s⟫" % txt[max(0, i - 16):i + len(old) + 12].replace(nl, u"¶"))
        txt = txt.replace(old, new.replace("\n", nl))
    for why, old, new in ((u"解界羯磨・白二全文", DIV_OLD, DIV_NEW),
                          (u"解界羯磨・領起語", LEAD_OLD, LEAD_NEW)):
        if txt.count(old) != 1:
            raise SystemExit(u"錨不唯一：%s（%d）" % (why, txt.count(old)))
        txt = txt.replace(old, new.replace("\n", nl))
        print(u"  · %s 已換" % why)
    # 結構全貌圖：第四篇之副題（補副題而保右欄之位）——以顯示寬計，不以字元索引
    def dw(s):
        u = unicodedata.east_asian_width
        return sum(2 if u(c) in "WF" else 1 for c in s)
    lines = txt.split(nl)
    hit = [k for k, l in enumerate(lines) if l.startswith(u"道場秩序與僧俗邊界")]
    if len(hit) != 1:
        raise SystemExit(u"結構圖第四篇之行列不唯一：%s" % hit)
    k = hit[0]
    old_line = lines[k]
    sub_old = u"道場秩序與僧俗邊界"
    sub = u"執事任事與常住物權之防線"
    rest = old_line[len(sub_old):]
    right = rest.lstrip(" ")
    spaces = len(rest) - len(right)
    gap = max(2, spaces - (dw(sub) - dw(sub_old)))
    new_line = sub + " " * gap + right
    lines[k] = new_line
    txt = nl.join(lines)
    print(u"  · 結構圖第四篇·副題  展示寬 %d→%d（右欄補齊）"
          % (dw(old_line.rstrip()), dw(new_line.rstrip())))
    for b in BAN:
        if b in txt:
            raise SystemExit(u"落刀後仍見禁字『%s』" % b)
    bad = [(x, PS.hits(l)) for x, l in enumerate(txt.split(nl), 1) if PS.hits(l)]
    if bad:
        raise SystemExit(u"簡形：%s" % bad[:4])
    if txt.count("\r") != txt.count("\r\n") or txt.count("\n") != txt.count("\r\n"):
        raise SystemExit(u"換行不齊（CR %d・LF %d・CRLF %d）"
                         % (txt.count("\r"), txt.count("\n"), txt.count("\r\n")))
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    out = bom + txt.encode("utf-8")
    print(u"  行數 %d・CRLF %d・BOM %s" % (txt.count(nl) + 1, txt.count(nl), u"有" if bom else u"無"))
    if WRITE:
        os.makedirs(BAK, exist_ok=True)
        dst = os.path.join(BAK, os.path.basename(path) + ".pre_a18")
        if not os.path.isfile(dst):
            shutil.copy2(path, dst)
        with open(path, "wb") as f:
            f.write(out)
        print(u"  ✎ 已寫入（備份 %s）" % os.path.basename(dst))


print("=" * 74)
run(F2)
print("=" * 74)
print(u"%s" % (u"落盤完畢" if WRITE else u"乾跑（未寫）：python -X utf8 _work/pair18a.py --write"))
