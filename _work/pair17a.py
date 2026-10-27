# -*- coding: utf-8 -*-
"""第十七波・第一本（《起心動念》）之校訂：外路兩報之真病九刀。
每刀唯一錨・乾跑印前後・落畢自證（舊字盡去・新文無簡形・CRLF 不動・BOM 不動）。

用法：python -X utf8 _work/pair17a.py [--write]
"""
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp as PS                                         # noqa: E402

F1 = os.path.join(ROOT, "起心動念：四分律的心智顯微鏡與唯識解剖.txt")
BAK = os.path.join(ROOT, "_archive", "備份", "AI清理前")
WRITE = "--write" in sys.argv

JOBS = [
    (u"生命之樹・常住公產➔僧團事務（與第五章同名）",
     u"        〔個人修煉〕  〔人際互動〕  〔常住公產〕                         │",
     u"        〔個人修煉〕  〔人際互動〕  〔僧團事務〕                         │"),
    (u"四照卡・名實相符（收攝之實）",
     u"【用·四照察心印】（臨事急診·夜半四照）",
     u"【用·四照察心印】（臨事急診·夜半四照之收攝）"),
    (u"案卷16・三度➔四度",
     u"**主觀惡意定性**：三度換裝皆由根本貪與增上慢驅使",
     u"**主觀惡意定性**：四度換裝皆由根本貪與增上慢驅使"),
    (u"案卷16・補第四階之定性",
     u"第四僧殘（自讚身索淫供戒）；",
     u"第四僧殘（自讚身索淫供戒）；第四階之屏處坐與露地對坐，不入僧殘，"
     u"別依波逸提法之空間遮戒科罪；"),
    (u"附錄四・跨冊斷鏈（現前清淨擬制）",
     u"依『現前清淨擬制與善意信賴保護』條（第四章第一節）護之",
     u"依『現前清淨擬制與善意信賴保護』條"
     u"（見姊妹篇《如法推尋》第一篇第二章第二節『善意信賴保護與現前清淨擬制』）護之"),
    (u"凡例・102 案之帳（本冊附錄四非總帳）",
     u"全書總帳一以附錄四 102 案為準",
     u"全書總帳（一百零二案）以姊妹篇《如法推尋》附錄一之集群矩陣與附錄二之回查索引為準"),
    (u"排版・雙空格一",
     u"律典所判之受樂，  唯指第六意識與根本貪愛相應、主動迎合之耽著  。",
     u"律典所判之受樂，唯指第六意識與根本貪愛相應、主動迎合之耽著。"),
    (u"凡例・四十字之但書（本地檔無標點者）",
     u"不得以『引文從省』諉之。",
     u"不得以『引文從省』諉之；唯本地檔原無標點者不在此數——照錄其形並自標『原檔無標點』，"
     u"不以今人句讀改易原卷。"),
    (u"中阿含・補文獻之界（本地未收）",
     u"> 「如異學沙門文祁子所說，若當爾者，嬰孩童子支節柔軟，仰向臥眠，亦當成就善、第一善、"
     u"無上士，得第一義、質直沙門。」",
     u"> 「如異學沙門文祁子所說，若當爾者，嬰孩童子支節柔軟，仰向臥眠，亦當成就善、第一善、"
     u"無上士，得第一義、質直沙門。」  \n"
     u"> 〔文獻之界〕本段所引《中阿含經》屬他部之典，本地分段檔未收，"
     u"依凡例屬『照錄未覆核』之界，不充就地覆核之數。"),
    (u"阿梨吒／阿利吒・敘事歸一（引文仍存原形）",
     u"佛陀遣比丘傳喚，阿梨吒來至佛所",
     u"佛陀遣比丘傳喚，阿利吒來至佛所"),
    (u"附錄三・去懸空之序（無二則不稱一）",
     u"### 一、律典原生核心名相法意釋義",
     u"### 律典原生核心名相法意釋義"),
    (u"附錄三・去懸空之序（次級）",
     u"#### 一、境想與心識之判（故意之有無）",
     u"#### 境想與心識之判（故意之有無）"),
    (u"四奪・層名之混稱",
     u"（無規範拘束力，不入前三層判準）",
     u"（無規範拘束力，不入三層標記之判準層）"),
]
BAN = (u"不入前三層判準", u"〔常住公產〕", u"三度換裝", u"（第四章第一節）護之",
       u"全書總帳一以附錄四 102 案為準", u"### 一、律典原生核心名相", u"阿梨吒來至佛所")


def run(path):
    raw = io.open(path, "rb").read()
    txt = raw.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in txt else "\n"
    for why, old, new in JOBS:
        n = txt.count(old)
        print(u"  · %-34s 命中 %d" % (why, n))
        if n != 1:
            raise SystemExit(u"錨不唯一／不見：%s" % why)
        i = txt.find(old)
        print(u"      ⟪%s⟫" % txt[max(0, i - 20):i + len(old) + 16].replace(nl, u"¶"))
        txt = txt.replace(old, new.replace("\n", nl))   # 刀內之換行以 nl 落地（CRLF 檔不得混入裸 LF）
    for b in BAN:
        if b in txt:
            raise SystemExit(u"落刀後仍見禁字『%s』" % b)
    bad = [(k, PS.hits(l)) for k, l in enumerate(txt.split(nl), 1) if PS.hits(l)]
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
        dst = os.path.join(BAK, os.path.basename(path) + ".pre_a17")
        if not os.path.isfile(dst):
            shutil.copy2(path, dst)
        with open(path, "wb") as f:
            f.write(out)
        print(u"  ✎ 已寫入（備份 %s）" % os.path.basename(dst))


print("=" * 74)
run(F1)
print("=" * 74)
print(u"%s" % (u"落盤完畢" if WRITE else u"乾跑（未寫）：python -X utf8 _work/pair17a.py --write"))
