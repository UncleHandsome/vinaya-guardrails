# -*- coding: utf-8 -*-
"""第十六波・外路報告之真病刀（字句層六事）：版本痕跡二・管線告示一・稿說評語一・
匯出機制一・簡形二。每刀唯一錨、乾跑印前後、落畢自證（舊字盡去・新字無簡形・CRLF 不動）。

用法：python -X utf8 _work/pair16a.py [--write]
"""
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp as PS                                        # noqa: E402

F1 = os.path.join(ROOT, "起心動念：四分律的心智顯微鏡與唯識解剖.txt")
F2 = os.path.join(ROOT, "如法推尋：僧伽憲政、法權審理與修復正義.txt")
BAK = os.path.join(ROOT, "_archive", "備份", "AI清理前")
WRITE = "--write" in sys.argv

# (檔, 說明, 舊, 新, 應見之數)
JOBS = [
    (F1, u"簡形・名目里➔名目裡", u"躲進名目里", u"躲進名目裡", 1),
    (F1, u"簡形・倾➔傾", u"領域倾軋", u"領域傾軋", 1),
    (F1, u"除版本痕跡（133 台帳）",
     u"；三十八版舊有之『133 綁定台帳』（舊編次 100 判例單元所計）自三十九版起**不另立**，"
     u"凡他處引及彼數者皆屬舊版之跡，非今冊之制。", u"", 1),
    (F1, u"除管線告示（自動化測試報告）",
     u"其餘歷代修訂日誌、款級索引與自動化測試報告，轉存內部開發檔案，不佔讀者頁面。", u"", 1),
    (F2, u"除版本痕跡（133 台帳）",
     u"；三十八版舊有之『133 綁定台帳』（舊編次 100 判例單元所計）自三十九版起**不另立**，"
     u"凡他處引及彼數者皆屬舊版之跡，非今冊之制。", u"", 1),
    (F2, u"除管線告示（自動化測試報告）",
     u"其餘歷代修訂日誌、款級索引與自動化測試報告，轉存內部開發檔案，不佔讀者頁面。", u"", 1),
    (F2, u"除稿說評語（唯稿所構）", u"唯稿所構『五級責任順位』", u"舊擬『五級責任順位』", 1),
    (F2, u"除稿說評語（不從稿說）", u"今全依律文作圖，不從稿說。", u"今全依律文作圖。", 1),
    (F2, u"除匯出機制（非手工抄錄）",
     u"一案一行，繇第五篇案號之定義載體（集群矩陣・經典地標之案號列・節題）匯出，非手工抄錄，"
     u"故章內增損一案，此表即隨動一行。",
     u"一案一行，其案號一以第五篇之定義載體（集群矩陣・經典地標之案號列・節題）為準，"
     u"故章內增損一案，此表即隨改一行。", 1),
    (F2, u"除版本痕跡（附錄 J）",
     u"（三十九版以前作附錄 J，自標『研讀備查，不計入百則』；今去其字母之跡，正名曰『現』",
     u"（今正名曰『現』", 1),
    (F2, u"除版本痕數（凡例之舊次）",
     u"本書三十五至三十八版曾依『遮罪・僧殘・開許』立舊次", u"本書舊曾依『遮罪・僧殘・開許』立舊次", 1),
    (F2, u"除版本痕數（附錄四之舊次）",
     u"本書三十五至三十八版曾依『遮罪・僧殘・開許』之舊編次", u"本書舊曾依『遮罪・僧殘・開許』之舊編次", 1),
    (F2, u"除版本痕數（新舊次碼對照之題）",
     u"### 〔新舊次碼對照〕（三十五〜三十八版舊次・唯備對讀）",
     u"### 〔新舊次碼對照〕（舊次・唯備對讀）", 1),
    (F2, u"除版本痕數（自三十九版起）",
     u"自三十九版起，**正文案號一律純號**", u"今**正文案號一律純號**", 1),
]
BAN = (u"三十八版", u"三十九版", u"不從稿說", u"非手工抄錄", u"自動化測試報告",
       u"名目里", u"倾")


def run(path):
    raw = io.open(path, "rb").read()
    crlf = raw.count(b"\r\n")
    txt = raw.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in txt else "\n"
    for fn, why, old, new, want in JOBS:
        if fn != path:
            continue
        n = txt.count(old)
        print(u"  · %-26s 命中 %d（應 %s）" % (why, n, want or u"≥1"))
        if n != 1:
            raise SystemExit(u"錨不唯一／不見：%s" % why)
        i = txt.find(old)
        print(u"      ⟪%s⟫" % txt[max(0, i - 26):i + len(old) + 20].replace(nl, u"¶"))
        txt = txt.replace(old, new)
    for b in BAN:
        if b in txt:
            j = txt.find(b)
            raise SystemExit(u"落刀後仍見禁字『%s』：…%s…" % (b, txt[max(0, j - 30):j + 30]))
    # 新撰之句掃簡形（只管刀痕附近：全文掃由 pairsimp 之尺另跑）
    bad = [(k, PS.hits(l)) for k, l in enumerate(txt.split(nl), 1) if PS.hits(l)]
    if bad:
        raise SystemExit(u"新文有簡形：%s" % bad[:4])
    if txt.count("\r") != txt.count("\r\n") or txt.count("\n") != txt.count("\r\n"):
        raise SystemExit(u"換行不齊（CR %d・LF %d・CRLF %d）——不寫"
                         % (txt.count("\r"), txt.count("\n"), txt.count("\r\n")))
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    out = bom + txt.encode("utf-8")
    print(u"  行數 %d・CRLF %d・BOM %s"
          % (txt.count(nl) + 1, txt.count(nl), u"有" if bom else u"無"))
    if WRITE:
        os.makedirs(BAK, exist_ok=True)
        dst = os.path.join(BAK, os.path.basename(path) + ".pre_a16")
        if not os.path.isfile(dst):
            shutil.copy2(path, dst)
        with open(path, "wb") as f:
            f.write(out)
        print(u"  ✎ 已寫入（備份 %s）" % os.path.basename(dst))
    return txt


print("=" * 74)
for p in (F1, F2):
    print("■", os.path.basename(p)[:16])
    run(p)
print("=" * 74)
print(u"%s：%s" % (u"落盤完畢" if WRITE else u"乾跑（未寫）", u"python -X utf8 _work/pair16a.py --write"))
