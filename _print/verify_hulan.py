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
  己 附錄歷號之形：源檔三位數以上之號（100.～178.）須在印面文字層如實現形，
    且印面不得有『字母代數字』之號（外路第廿七報稱舊版印作 L00.～L78.；今產物自證 0）。
  庚 頁眉：以冊內大綱推每頁應有之眉（陽頁章題・陰頁書名・開章之頁與卷首則應無），
    再取字層上緣之實字校之；四判（缺・誤・多・合）各植負測點名，管轄與陽頁之數同印。
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
import hulan_head as HH                                   # noqa: E402  同一上緣之門・同一摺空白

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
    """取一頁之正文串接：擲去頁腳／頁眉之純頁碼行，再擲頁眉一句（第 78 輪起，眉由 hulan_head
    蓋於上緣 y<NEED 之帶）。不擲則引文一跨頁，串接中便夾入下頁頁碼（實測 p34『從今日沙門、』
    下接 p35『35婆羅門』）或下頁之眉題，尺將把正常跨頁之句報成漏印。
    眉之形自帶內之字求（幾何），其削則於行列中求同形之第一行——不假設文字之來序
    （實測：蓋入之眉附於內容流之尾，get_text() 仍以頁碼為首行，故『削首行』之法在此全錯）。"""
    L = [x.strip() for x in doc[i].get_text().split(u"\n") if x.strip()]
    if L and re.fullmatch(u"\\d{1,3}", L[0]):
        L = L[1:]
    if L and re.fullmatch(u"\\d{1,3}", L[-1]):
        L = L[:-1]
    _h = norm(u"".join(s["text"] for b in doc[i].get_text("dict")["blocks"]
                       for ln in b.get("lines", []) for s in ln["spans"]
                       if s["bbox"][1] < HH.NEED))
    if _h:
        j = next((k for k, x in enumerate(L) if norm(x) == _h), None)
        if j is None:
            raise SystemExit(u"頁眉無從削（p%d｜眉『%s』・行首『%s』・行尾『%s』）——須查 hulan_head 之形制"
                             % (i + 1, _h[:18], (L[0] if L else u"")[:16], (L[-1] if L else u"")[:16]))
        L = L[:j] + L[j + 1:]
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


# 「居頁首」之判只看有內容之塊：纯饰线之塊（─｜—·框線字符）非文，若以之為首塊，
# 則章前那條 HR 落上頁末或本頁首皆會引虛報（第 74 輪第十章即此：印面首塊為「—」飾線，其下即篇題）。
DECOR = re.compile(u"^[\\s\\u2500-\\u25FF\\u2014\\u2013\\u00B7\\u2022\\u3000\\-—–·．.]+$")


def real_blocks(i):
    return [b for b in blocks_sorted(i) if not DECOR.match(b[4])]


firsts = [norm(real_blocks(i)[0][4]) if real_blocks(i) else u"" for i in range(np_)]
PART = re.compile(u"^【(?:第[一二三四五]部：|卷首·扉頁)")   # 部Banner 得居頁首，其下即該部之首篇


def page_tops(key):
    out = []
    for i in range(np_):
        if key in firsts[i]:
            out.append(i)
            continue
        if PART.search(firsts[i]):
            bs = real_blocks(i)
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
    # 末行須自『首行所見之頁』起往後找——舊法由末頁倒數，遇他處重出之句（如『展轉取最下鉢…』
    # 亦見於本章散文）即錯配他頁，假報腰斬（第 74 輪兩報俱此，正本實未跨頁）。
    ib = None if ia is None else next((i for i in range(ia, np_) if kb in pages[i]), None)
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


def np_lost(src_chars, print_text):
    """源有而印面無之內非 BMP 字（U+10000 以上）——無伴字體時此類字於 Chromium 列印『連字帶形』
    一併消失（第 78 輪 Ext-B 之測），文字層亦抽不回，故歷波全綠而冊上實缺。判式抽出方可植負測。"""
    return [c for c in src_chars if c not in print_text]


_np_src = sorted({c for c in u"\n".join(src_lines) if ord(c) >= 0x10000})
_np_lost = np_lost(_np_src, whole)
_np_plant = np_lost([u"\U00027655"], whole)
print(u"  戊4・非 BMP 之字：源 %d 枚・印面佚 %d 枚｜負測植 U+27655 逮 %d（宜 1）"
      % (len(_np_src), len(_np_lost), len(_np_plant)))
if _np_lost:
    fail.append(u"【戊4】印面佚非 BMP 之字 %d 枚：%s" % (
        len(_np_lost), u"、".join(u"%s(U+%X)" % (c, ord(c)) for c in _np_lost[:8])))
if len(_np_plant) != 1:
    fail.append(u"【戊5】非 BMP 之負測不響：植一枚而逮 %d（宜 1）" % len(_np_plant))

# 軟報——字級分布、孤懸標題、近空頁
# 字級分兩欄記：頁眉帶（y<NEED，第 78 輪起為 hulan_head 所蓋之 8.6pt）與帶外之正文・圍欄。
# 混為一談則『細字』之數陡增而病無一——宣稱之單位須與被量者同域（第 61 輪之誡）。
sizes, hsize = {}, {}
for i in range(np_):
    for b in doc[i].get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln.get("spans", []):
                if sp["text"].strip():
                    d = hsize if sp["bbox"][1] < HH.NEED else sizes
                    d.setdefault(round(sp["size"], 2), 0)
                    d[round(sp["size"], 2)] += len(sp["text"])
top = sorted(sizes.items())
print(u"  字級分布（最細五級）：%s" % u"、".join(u"%spt×%d字" % (s, n) for s, n in top[:5]))
tiny = sum(n for s, n in top if s < 9.0)
n_head = sum(hsize.values())
print(u"  細於 9.0pt 之字數：%d%s｜頁眉帶另 %d 字（%s，裝幀之制，非病）" % (
    tiny, u"（圍欄圖層，屬第 3 期候裁）" if tiny else u"", n_head,
    u"・".join(u"%spt" % s for s in sorted(hsize))))
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

# ── 己・附錄歷號不得為字母（外路第廿七報稱舊版印作『L00.』～『L78.』——今產物以文字層自證，並防此類復發）
rawwhole = u"\n".join(doc[i].get_text() for i in range(np_))
if u"全戒本歷條總表" in whole:                       # 削附錄之式（精簡版）不校此行
    want = sorted({int(m.group(1)) for l in src_lines for m in [re.match(u"^(\\d+)\\.\\s", l)] if m
                   if int(m.group(1)) >= 100})
    lost = [n for n in want if not re.search(u"(?m)^%d\\. " % n, rawwhole)]
    alpha = re.findall(u"(?m)^[A-Z]\\d{1,2}\\. ", rawwhole)
    print(u"  己・附錄三位數以上歷號 %d 枚｜印面缺 %d｜字母誤植行 %d" % (len(want), len(lost), len(alpha)))
    if lost:
        fail.append(u"【己1】印面查無歷號 %d 枚：%s" % (len(lost), u"、".join(str(n) for n in lost[:10])))
    if alpha:
        fail.append(u"【己2】印面歷號以字母代數字 %d 處：%s" % (len(alpha), u"、".join(alpha[:8])))
    # 負測：植兩枚已知之病形，須被同一對樣式逮住（尺不響即啞，啞非綠）
    fix = u"L00. 「若比丘尼往觀王宮」\n101. 「若比丘尼露身形」\n"
    n_alpha = len(re.findall(u"(?m)^[A-Z]\\d{1,2}\\. ", fix))
    n_lost = len([v for v in (100, 101) if not re.search(u"(?m)^%d\\. " % v, fix)])
    print(u"  己之負測｜植 L00. 逮 %d（宜 1）｜植佚 100. 逮 %d（宜 1）" % (n_alpha, n_lost))
    if n_alpha != 1 or n_lost != 1:
        fail.append(u"【己3】自身負測不響：字母 %d・佚號 %d" % (n_alpha, n_lost))

# ── 庚・頁眉（第 78 輪之裝幀案：Chromium 不生效於 running elements，眉由 _print/hulan_head.py
#     蓋於產物層，故此目不問源檔、只問冊——以大綱（冊內另一法源）推每頁『應有之眉』，
#     再取字層上緣（y < 蓋印器之門限）之實有文字校之。開章之頁與卷首・目錄例不蓋，此處校其必無。）
def head_judge(exp, got):
    """頁眉之判式（抽出方可植負測）：應有而無＝缺・應有而是他題＝誤・應無而有＝多・餘者＝合。"""
    e, g = HH.fold(exp), HH.fold(got)
    if not e and not g:
        return u"合"
    if e and not g:
        return u"缺"
    if not e and g:
        return u"多"
    return u"合" if e == g else u"誤"


_pairs = [(ti, pg) for lv, ti, pg in doc.get_toc()
          if lv == 1 and BH.HEAD_H1.match(ti)]
if not _pairs:
    fail.append(u"【庚0】大綱內無章級之題（第[一二三…]章・十線地圖・附錄）——頁眉之尺無靶，不成其為尺")
else:
    _pairs.sort(key=lambda r: r[1])
    _first = _pairs[0][1]
    _opens = {pg for _t, pg in _pairs}
    _k, _n = -1, 0
    _miss, _wrong, _extra, _recto = [], [], [], 0
    for _i in range(_first - 1, np_):
        _p = _i + 1
        while _k + 1 < len(_pairs) and _pairs[_k + 1][1] <= _p:
            _k += 1
        if _p in _opens:
            _exp = u""                                   # 開章之頁不重覆其題（成例）
        elif _p % 2 == 0:
            _exp = BH.BOOK_TITLE
        else:
            _exp = _pairs[_k][0]
            _recto += 1
        _got = HH.fold(u"".join(s["text"]
                                for b in doc[_i].get_text("dict")["blocks"]
                                for ln in b.get("lines", []) for s in ln["spans"]
                                if s["bbox"][1] < HH.NEED))
        _v = head_judge(_exp, _got)
        if _exp or _got:
            _n += 1                           # 管轄：有期望或有實字之頁，俱入尺目（合者亦計）
        if _v == u"合":
            continue
        {"缺": _miss, "誤": _wrong, "多": _extra}[_v].append((_p, _exp[:14], _got[:14]))
    print(u"  庚・頁眉｜大綱章級 %d 條・正文起 p%d・管轄 %d 頁（陽頁 %d）・校 %d 頁・應蓋而無 %d・題不合 %d・應無而蓋 %d"
          % (len(_pairs), _first, np_ - _first + 1, _recto, _n, len(_miss), len(_wrong), len(_extra)))
    for _nm, _lst in ((u"題不合", _wrong), (u"應無而蓋", _extra)):
        if _lst:
            print(u"    %s %d 頁，首三：%s" % (
                _nm, len(_lst), u"、".join(u"p%d宜『%s』實『%s』" % r for r in _lst[:3])))
    if _n < 100 or _recto < 20:
        fail.append(u"【庚1】此尺不響：校 %d 頁（宜 ≥100）、陽頁 %d（宜 ≥20）——綠亦無憑"
                    % (_n, _recto))
    if _miss:
        fail.append(u"【庚2】應有頁眉而無 %d 頁：%s" % (
            len(_miss), u"、".join(str(r[0]) for r in _miss[:10])))
    if _wrong:
        fail.append(u"【庚3】頁眉之題與大綱所指之章不合 %d 頁：%s" % (
            len(_wrong), u"、".join(str(r[0]) for r in _wrong[:10])))
    if _extra:
        fail.append(u"【庚4】開章之頁或卷首不應有眉而現有 %d 頁：%s" % (
            len(_extra), u"、".join(str(r[0]) for r in _extra[:10])))
    # 負測：四判各植一例，判式須點名真答案（器不響即啞，啞非綠）
    _plant = [(u"第二章 正統律學", u"", u"缺"),
              (u"第二章 正統律學", u"第三章 城郭宮殿之喻", u"誤"),
              (u"", BH.BOOK_TITLE, u"多"),
              (BH.BOOK_TITLE, BH.BOOK_TITLE, u"合")]
    _deaf = [u"宜%s實%s" % (w, head_judge(e, g)) for e, g, w in _plant
             if head_judge(e, g) != w]
    print(u"  庚之負測｜四判 %s" % (u"、".join(_deaf) if _deaf else u"俱點名（缺・誤・多・合）"))
    if _deaf:
        fail.append(u"【庚5】判式自身不響：%s" % u"、".join(_deaf))

doc.close()
print(u"=" * 62)
if fail:
    print(u"不合格 %d 項：" % len(fail))
    for f in fail:
        print(u"  ✗ " + f)
    sys.exit(1)
print(u"合格：甲乙丙丁戊己庚七檢俱中（軟報不計）")
