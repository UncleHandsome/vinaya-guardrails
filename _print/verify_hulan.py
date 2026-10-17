# -*- coding: utf-8 -*-
"""《佛陀的護欄》產物層驗收——承 verify38 之口徑，唯取其能用於此冊者。

硬檢（任一不合格即退 1）：
  甲 書訊與大綱：title 含版次、大綱非空、抽驗首／中／末三條書籤所指頁確有其題
  乙 篇題居頁首：源檔每個 H1 於冊內所在頁，其首個文字塊即該題（第 109 輪之誡）
  丙 表格未散架：表頭欄數與列數實測（第 110 輪之病：標籤名被改寫則整表化為連寫文字）
  丁 圍欄圖未腰斬：每段 pre 之首行與末行須同頁（鎖頁生效與否以印面驗，不信 CSS）
  戊 文字層逐條回驗：錨自動取自本式送排之中介 md 的所有自報逐字引文（千餘條），
    應見者俱見於印面；應無之形俱零（markdown 殘相、未閉星號、舊誤句、$ math 殘形）。
    跨頁之句須先擲去每頁首尾之純頁碼行，否則正常跨頁即被報成漏印。
軟報（只列不判）：細字級分布、孤懸標題、近空頁。

用法：python _print/verify_hulan.py [PDF 路徑]
"""
import io
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import build_hulan as BH                                  # noqa: E402  同源之標題口徑

PDF = sys.argv[1] if len(sys.argv) > 1 else BH.PDF_OUT
SRC = BH.SRC
FENCE = "```"

# 應見——不自抄名單，逕取『本式實際送排之中介 md』中所有自報逐字之引文
# （「引號＋星號」式樣，與 _work/hlchk.py 之戊同一口徑；白話「…」不較）。
# 手抄樣本必落後於正文：第 244 輪新增之十二案全不在舊單中，尺照過——此即虛尺。
STRUCT = [u"以遮衛性", u"全書詳細目錄", u"小戒不是鎖鏈", u"城郭宮殿之喻",
          u"律藏中的古老防禦護欄", u"制戒因緣", u"結戒", u"開緣"]
# 自報逐字之式樣（與 _work/hlchk.py 之戊同）：「**…**」 與 **「…**」 兩形
QUOTE = re.compile(u"「\\*\\*([^」\\n]+?)\\*\\*」|\\*\\*「([^」\\n]+?)」\\*\\*")
QN = 8                                   # 短於此字之引文（如「無所犯」）易為印面他處偶合，不入錨
# 應無：源層形漏入印面、已改正之舊文、以及一字兩型之兆
# （u"*"：清單前未留空行時，pandoc 壓段並印出字面星號——第 8 輪『源碼外洩』之族）
NOT = [u"$", u"*", u"**", u"```", u"| :---", u"<!--", u"這反正是荒野無主之物",
       u"阿蘭若森林中修行", u"\\times", u"\x01", u"・"]

fail = []


def norm(s):
    return re.sub(r"\s+", u"", s)


# 篇題之期望取於本式實際送排之中介 md（精簡版削附錄，若仍按源檔索之即虛報「篇題查無」）
MD_SRC = BH.MD if os.path.isfile(BH.MD) else SRC
src_lines = io.open(MD_SRC, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
heads = BH.headings(src_lines)
h1 = [t for lv, t in heads if lv == 1]
seen_q, AUTO = set(), []
for mq in QUOTE.finditer(u"\n".join(src_lines)):
    k = norm(mq.group(1) or mq.group(2)).replace(u"*", u"")
    if len(k) >= QN and k not in seen_q:
        seen_q.add(k)
        AUTO.append(k)
if not AUTO:
    raise SystemExit("中介 md『%s』無自報逐字之引文，錨為零——尺已失能，須查式樣" % os.path.basename(MD_SRC))
pre_first, pre_last = [], []
inf = False
for l in src_lines:
    if l.startswith(FENCE):
        inf = not inf
        if inf:
            cur = []
        else:
            if cur:
                pre_first.append(cur[0])
                pre_last.append(cur[-1])
        continue
    if inf and l.strip():
        cur.append(l)

def page_body(doc, i):
    """取一頁之正文串接：擲去頁眉／頁腳之純頁碼行。
    不擲則引文一跨頁，串接中便夾入下頁頁碼（實測 p34『從今日沙門、』下接 p35『35婆羅門』），
    尺將把正常跨頁之句報成漏印。"""
    L = [x.strip() for x in doc[i].get_text().split(u"\n") if x.strip()]
    if L and re.fullmatch(u"\\d{1,3}", L[0]):
        L = L[1:]
    if L and re.fullmatch(u"\\d{1,3}", L[-1]):
        L = L[:-1]
    return norm(u"".join(L))


doc = pymupdf.open(PDF)
np_ = doc.page_count
pages = [page_body(doc, i) for i in range(np_)]
print(u"冊：%s｜%d 頁｜%d KB｜大綱 %d 條"
      % (os.path.basename(PDF), np_, os.path.getsize(PDF) // 1024, len(doc.get_toc())))

# 甲——書訊與大綱
meta = doc.metadata or {}
title = meta.get("title") or u""
if u"版" not in title:
    fail.append(u"【甲1】書訊 title 未含版次：%r" % title[:40])
toc = doc.get_toc()
if not toc:
    fail.append(u"【甲2】PDF 大綱為空")
if toc:
    for tag, idx in ((u"首", 0), (u"中", len(toc) // 2), (u"末", len(toc) - 1)):
        lv, ti, pg = toc[idx]
        key = norm(ti)[:10]
        if 0 < pg <= np_ and key and key not in pages[pg - 1]:
            fail.append(u"【甲3】%s條書籤 p%d 查無其題：%s" % (tag, pg, ti[:26]))
        else:
            print(u"  書籤抽驗 %s：p%-4d %s" % (tag, pg, ti[:34]))

# 乙——篇題居頁首。取「首塊即其題」為判準，故目錄頁之同名條目天然不中（目錄首塊是目錄題）；
#     逐篇以游標向前搜，免把後章誤定位到卷首目錄那一頁。
def blocks_sorted(i):
    bs = [b for b in doc[i].get_text("blocks") if norm(b[4])]
    return sorted(bs, key=lambda b: (round(b[1], 1), b[0]))


firsts = [norm(blocks_sorted(i)[0][4]) if blocks_sorted(i) else u"" for i in range(np_)]
PART = re.compile(u"^【(?:第[一二三四五]部：|卷首·扉頁)")   # 部Banner 得居頁首，其下即該部之首篇


def page_tops(key):
    out = []
    for i in range(np_):
        if key in firsts[i]:
            out.append(i)
            continue
        if PART.search(firsts[i]):
            bs = blocks_sorted(i)
            if len(bs) > 1 and key in norm(bs[1][4]):
                out.append(i)
    return out


mis, notfound = [], []
for t in h1:
    key = norm(t)[:8]
    tops = page_tops(key)        # 首塊即其題（或部Banner 之下第一題）之頁
    if not tops:
        (notfound if not any(key in p for p in pages) else mis).append((t[:22], key))
        continue
    tops = [i + 1 for i in tops]
    if len(tops) > 1:
        print(u"  同題居兩頁之首：%s → p%s" % (t[:20], tops[:4]))
for t, _ in mis[:6]:
    print(u"  篇題未居頁首（他頁見其文）：%s" % t)
if notfound:
    fail.append(u"【乙】篇題查無 %d 篇：%s" % (len(notfound), u"、".join(t for t, _ in notfound[:4])))
if mis:
    fail.append(u"【乙】%d／%d 篇題未居頁首" % (len(mis), len(h1)))
if not mis and not notfound:
    print(u"  篇題居頁首：%d／%d 俱中" % (len(h1), len(h1)))

# 丙——表格實形（欄數與列數以印面向量線重構為第一證據）
tbl_key = norm(u"律藏中的古老防禦護欄")
at = next((i for i in range(np_) if tbl_key in pages[i]), None)
if at is None:
    fail.append(u"【丙】表頭查無（第十七章對照表未印？）")
else:
    tf = doc[at].find_tables()
    ok = any(t.col_count == 4 and t.row_count >= 5 for t in tf.tables)
    print(u"  表格 p%d：find_tables 得 %d 張，4 欄×≥5 列之表=%s"
          % (at + 1, len(tf.tables), u"有" if ok else u"無"))
    if not ok:
        fail.append(u"【丙】p%d 表已散架（未測得 4 欄×≥5 列）" % (at + 1))

# 丁——圍欄圖不跨頁
bad_pre = 0
for a, b in zip(pre_first, pre_last):
    ka, kb = norm(a)[:10], norm(b)[:10]
    ia = next((i for i in range(np_) if ka in pages[i]), None)
    ib = next((i for i in range(np_ - 1, -1, -1) if kb in pages[i]), None)
    if ia is None or ib is None:
        bad_pre += 1
        print(u"  圍欄行佚：首=%s｜末=%s" % (ka[:8], kb[:8]))
    elif ia != ib:
        bad_pre += 1
        print(u"  圍欄腰斬：首 p%d／末 p%d ｜%s" % (ia + 1, ib + 1, ka[:16]))
print(u"  圍欄圖 %d 段：俱在同頁者 %d，異頁或佚者 %d"
      % (len(pre_first), len(pre_first) - bad_pre, bad_pre))
if bad_pre:
    fail.append(u"【丁】圍欄圖腰斬／佚行 %d 處" % bad_pre)

# 戊——文字層逐條回驗：錨自動取自送排之 md，正文增一行即多驗一條（不待人記）
whole = u"".join(pages)
miss = [w for w in STRUCT + AUTO if w not in whole]
ghost = [w for w in NOT if norm(w) in whole]
if miss:
    fail.append(u"【戊1】應見未見 %d 條：%s" % (len(miss), u"、".join(m[:24] for m in miss[:8])))
if ghost:
    fail.append(u"【戊2】應無而有 %d 形：%s" % (len(ghost), u"、".join(repr(g) for g in ghost)))
apx_i = next((i for i, l in enumerate(src_lines) if l.startswith(u"# 附錄")), None)
apx_norm = norm(u"\n".join(src_lines[apx_i:])) if apx_i is not None else u""
n_apx = sum(1 for a in AUTO if a in apx_norm)
# 附錄之有無須雙向驗：全本丟附錄即不成其為全本，精簡版若帶著附錄即失去立身之本。
# （附錄之戒文與正文重覆、且不用自報逐字之記號，故看不出在錨數之差裡——只能這樣直接驗。）
has_apx = norm(u"全戒本歷條總表") in whole
if apx_i is None and has_apx:
    fail.append(u"【戊3】精簡版印面竟含『全戒本歷條總表』（削附錄未生效）")
if apx_i is not None and not has_apx:
    fail.append(u"【戊3】隨冊印附錄之式，印面卻查無『全戒本歷條總表』")
print(u"  抽驗：應見 %d 條（結構 %d＋逐字錨 %d，亦見附錄者 %d）、缺 %d｜應無 %d 形（中 %d）｜附錄=%s"
      % (len(STRUCT) + len(AUTO), len(STRUCT), len(AUTO), n_apx, len(miss), len(NOT), len(ghost),
         u"隨冊" if has_apx else u"不印"))

# 軟報——字級分布、孤懸標題、近空頁
sizes = {}
for i in range(np_):
    for b in doc[i].get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln.get("spans", []):
                if sp["text"].strip():
                    sizes.setdefault(round(sp["size"], 2), 0)
                    sizes[round(sp["size"], 2)] += len(sp["text"])
top = sorted(sizes.items())
print(u"  字級分布（最細五級）：%s" % u"、".join(u"%spt×%d字" % (s, n) for s, n in top[:5]))
tiny = sum(n for s, n in top if s < 9.0)
print(u"  細於 9.0pt 之字數：%d%s" % (tiny, u"（圍欄圖層，屬第 3 期候裁）" if tiny else u""))
widow = 0
for i in range(np_):
    bs = blocks_sorted(i)
    if bs and re.match(u"^(第[一二三四五六七八九十]+章|【|一、|二、|三、)", norm(bs[-1][4])) \
       and len(bs[-1][4].strip()) < 40:
        widow += 1
        print(u"  疑孤懸標題 p%d：%s" % (i + 1, bs[-1][4].strip()[:34]))
# 近空頁改以「尾白量」為準：先擲去頁碼頁腳，再取本頁最低文字塊底緣與可印下界之差。
# （舊口徑以每頁字數多寡判，會被頁腳掩護而看不見近全空之頁——第 244 輪之 5 張部題頁即如此漏網。）
PH = doc[0].rect.height
FLOOR = PH - 56.0
gaps = []
for i in range(np_):
    bs = [b for b in doc[i].get_text("blocks") if norm(b[4])]
    body = [b for b in bs if not (re.fullmatch(r"\d{1,3}", b[4].strip()) and b[1] > PH - 70)]
    if not body:
        gaps.append((i + 1, FLOOR, u"全頁無文"))
        continue
    g = FLOOR - max(b[3] for b in body)
    if g > 250:
        nb = blocks_sorted(i + 1) if i + 1 < np_ else []
        nxt = norm(nb[0][4]) if nb else u""
        # 「另起一頁」之正當者不止各章：部題【、尾聲、附錄、十線地圖同掛 break-before:page，
        # 其前一頁尾白屬版式必然，非病（今 p201 之尾聲末頁即如此，舊口徑誤報待查）。
        kind = u"章末另起頁（常）" if re.match(u"^(第[一二三四五六七八九十]+章|【|尾聲|附錄|十線地圖)", nxt) \
            else (u"末頁" if i + 1 >= np_ else u"待查：非章末")
        gaps.append((i + 1, g, kind))
print(u"  孤懸標題之疑=%d（只報不判）" % widow)
print(u"  尾白>250pt 之頁：%d 處" % len(gaps))
for i, g, kind in sorted(gaps, key=lambda r: -r[1]):
    print(u"    p%-4d 空%-6.0f｜%s" % (i, g, kind))

doc.close()
print(u"=" * 62)
if fail:
    print(u"不合格 %d 項：" % len(fail))
    for f in fail:
        print(u"  ✗ " + f)
    sys.exit(1)
print(u"合格：甲乙丙丁戊五檢俱中（軟報不計）")
