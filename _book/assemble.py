# -*- coding: utf-8 -*-
"""《佛陀的護欄：四分律行為心理學與現代僧伽治理》新冊產器。

讀 `_archive/舊本/` 兩冊（只讀一字不動）→ 依指南之「七部二十八章」合編，並就地施行
去人工化清創（道岔・問卷・母案碼・台帳・符號帽子・儀式收尾）。**冊內不立任何帳目標記**：
缺欄不編造、亦不掛〔待寫〕——有文則出，無文則闕其目。
用法：python -X utf8 _book/build.py [--out=路徑]
"""
import os, re, sys, io, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parse as P
import clean as CL
import refmap as CM
import mirrors as MR
import jieben_ni as JN

OUT = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
for a in sys.argv[1:]:
    if a.startswith("--out="):
        OUT = a.split("=", 1)[1]

TITLE = u"佛陀的護欄"
SUBTITLE = u"四分律行為心理學與現代僧伽治理"

fw_lines, hl_lines = None, None
fw, hl = None, None


def boot():
    global fw, hl
    fw, hl = P.load(ROOT)


boot()
CARDS = P.fw_cards(fw)
STATS = {}

# 補遺十五則之欄目以行內粗體標籤行之（非 H5），此處歸入同一六段之形
BUYI = [(u"事相因緣", u"事相經過"), (u"事相經過", u"事相經過"), (u"佛陀判語", u"佛陀處斷"),
        (u"法理核心與心理動力學", u"法相剖析"), (u"法理要旨與心智指針", u"治理與修持對治"),
        (u"調部文獻定位", u"律藏原文"), (u"正理參照", u"正理參照")]
BL_RE = re.compile(r"^\*+\s*\*\*([^*｜：]{2,16})\*\*[:：](.*)$")


def buyi_split(body):
    parts, cur = {}, None
    for l in body.split(u"\n"):
        m = BL_RE.match(l)
        if m:
            cur = m.group(1).strip()
            parts.setdefault(cur, []).append(m.group(2).strip())
        elif cur:
            parts[cur].append(l)
    return {k: u"\n".join(v).strip() for k, v in parts.items()}


for _code, _c in CARDS.items():
    if _c["fields"]:
        continue
    raw = buyi_split(_c["body"])
    got = {}
    for src, dst in BUYI:
        if raw.get(src):
            got[dst] = raw[src]
    _c["fields"] = got
    _c["正理"] = raw.get(u"正理參照", u"")


def st(k):
    STATS[k] = STATS.get(k, 0)
    return STATS[k]


# ── 章界 ────────────────────────────────────────────────────────────────────
def _k(num):
    """章鍵可容『一』・『第一章』・『7』三形。"""
    s = re.sub(u"^第|章$", u"", num)
    return s


def chap_span(book, num):
    for i, lvl, t in book.h:
        if lvl == 1:
            m = re.match(u"第([一二三四五六七八九十]+)章", t)
            if m and m.group(1) == num:
                nxt = [j for j, l2, _ in book.h if l2 == 1 and j > i]
                return (i, nxt[0] - 1 if nxt else len(book.lines), t)
    raise KeyError(num)


FW_SP = {n: chap_span(fw, n) for n in
         [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]}
HL_SP = {n: chap_span(hl, n) for n in
         [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十",
          u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九", u"二十"]}


def shift(text, delta=-1, floor=2):
    """搬入之塊降其標題層（章題已由本冊自立）；圍欄內不動。"""
    out, fence = [], False
    for l in text.split(u"\n"):
        if l.startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        m = re.match(r"^(#{1,6}) (.*)$", l)
        if m:
            n = max(floor, min(6, len(m.group(1)) + delta))
            out.append(u"#" * n + u" " + m.group(2))
        else:
            out.append(l)
    return u"\n".join(out).strip()


def drop_chap_head(text):
    """去掉原冊之章題行（唯 H1 與其 `## ——` 副題），H2 以上之節題保留。"""
    lines = text.split(u"\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(u"^# ", lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith(u"## ——"):
        lines.pop(0)
    return u"\n".join(lines).strip()


def vch(num, sec=None):
    a, b, _ = FW_SP[_k(num)]
    if sec:
        s = fw.sec(a, b, sec, 3)
        return relink(shift(drop_chap_head(s)), u"v") if s else u""
    body = fw.slice(a + 1, b)
    return relink(shift(drop_chap_head(body)), u"v")


def vminus(num, sec):
    """取整章而挖去其一節（供第十九章＝框架第四章除第五節；第五節另立為第廿章，不使兩出）。"""
    a, b = FW_SP[_k(num)][0], FW_SP[_k(num)][1]
    full = shift(drop_chap_head(fw.slice(a + 1, b)))
    s = fw.sec(a, b, sec, 3)
    if not s:
        return relink(full, u"v")
    seg = shift(s.strip())
    out = full.replace(seg, u"") if seg in full else full
    return relink(out, u"v")


def hch(num, before=None, after=None):
    a, b, _ = HL_SP[_k(num)]
    body = hl.slice(a + 1, b)
    if before:
        body = body.split(before)[0]
    elif after:
        body = body[body.find(after):] if after in body else body
    return relink(shift(drop_chap_head(body)), u"h")


def hsec(num, sub):
    """護欄某章之某一 H3 節。"""
    a, b, _ = HL_SP[_k(num)]
    for title, i, e in hl.secs(a, b, 3):
        if sub in title:
            return relink(shift(hl.slice(i, e)), u"h")
    return u""


# ── 落點表・對位表 ───────────────────────────────────────────────────────────
PLACE_FW, PLACE_HL = {}, {}
for l in io.open(os.path.join(HERE, u"落點表.tsv"), encoding=u"utf-8").read().split(u"\n"):
    if not l.strip() or l.startswith(u"#"):
        continue
    side, key, chap = l.split(u"\t")
    if side == u"FW":
        PLACE_FW[key] = chap
    else:
        PLACE_HL[tuple(key.split(u"|"))] = chap

PAIR = {}
for l in io.open(os.path.join(HERE, u"對位表.tsv"), encoding=u"utf-8").read().split(u"\n"):
    cs = [c.strip() for c in l.split(u"\t")]
    if len(cs) >= 3 and cs[0].startswith(u"第") and cs[2].startswith(u"〔"):
        key = cs[1] if cs[1].startswith(u"案例") else u"案例" + cs[1]
        PAIR.setdefault((cs[0], key), []).append(cs[2])

CARD_NAME = {}
for code, c in CARDS.items():
    ttl = c["title"]
    cut = lambda z: re.sub(u"[「」『』〔〕【】（）：；]", u"", z or u"")
    head = cut(re.split(u"——|：|（", ttl)[0].strip())
    tail = cut(re.split(u"——", ttl)[-1].strip()) if u"——" in ttl else u""
    nm = head if len(head) >= 3 and head not in (u"婬戒", u"盜戒", u"殺戒", u"大妄語戒") else (tail or head)
    CARD_NAME[code] = u"『%s』" % (nm[:12] or head[:8])

HOME_BY_NEW = {}
for code, chap in PLACE_FW.items():
    HOME_BY_NEW.setdefault(chap, []).append(code)
HL_HOME = {}
for (hc, cs), chap in PLACE_HL.items():
    HL_HOME.setdefault(hc, []).append(cs)

FAMILY_ORD = {u"遮": 0, u"開": 1, u"僧": 2, u"補遺": 3}


def fw_order(chap):
    def fam(z):
        return 3 if z.startswith(u"〔補遺") else FAMILY_ORD[z[1]]
    return sorted(HOME_BY_NEW.get(chap, []),
                  key=lambda z: (fam(z), int(re.search(r"\d+", z).group())))


# ── 指針重算 ────────────────────────────────────────────────────────────────
RELINK = {u"n": 0, u"case": 0}
CASE_MAP = {}          # (護欄原章, 案例X) → (新章, 新案例序)


def _map(num, sec, src):
    m = CM.V_MAP if src == u"v" else CM.H_MAP
    key = num if num.startswith(u"第") else u"第%s章" % num
    sp = CM.SPLIT.get(key)
    if sp:
        if not sec:
            return CM.pair(sp[0], sp[1])
        if u"節" in sec or (sp[2] and sp[2] in sec):
            # 散置之章：其節分隸主副兩章，此處只立混合名，落點由 `sequence.resolve_span` 據實文算
            return CM.pair(sp[0], sp[1])
        return sp[0]
    return m.get(key)


def relink(text, src):
    """案例指針先以護符收起，改完章次再放出——防『已落地之新章』再被二次換算。"""
    toks = []

    def stash(m):
        key = (u"第%s章" % m.group(1), m.group(2))
        if src == u"h" and key in CASE_MAP:
            nc, n = CASE_MAP[key]
            RELINK[u"case"] += 1
            toks.append(u"%s案例%s" % (nc, P.cn_num(n)))
            return u"%d" % (len(toks) - 1)
        return m.group(0)
    text = re.sub(u"第([一二三四五六七八九十]+)章(案例[一二三四五六七八九十]+)", stash, text)
    # 圍欄內之路標圖一樣是源冊章次，同須改指——昔以『圖形勿動』skip 之，遂留舊章號於新冊
    out = []
    for l in text.split(u"\n"):
        if l.startswith(u">"):
            # 引文行亦得改指針，唯引號之內不動（律文自稱卷段，不含章號；章號唯作者之語）
            segs = re.split(u"(「[^」]*」|『[^』]*』)", l[2:] if l.startswith(u"> ") else l[1:])
            hit = [0]

            def fx2(mo):
                tg = _map(mo.group(1), mo.group(2) or u"", src)
                if not tg:
                    return mo.group(0)
                hit[0] += 1
                return tg + (mo.group(2) or u"")
            rebuilt = []
            for k2, s in enumerate(segs):
                rebuilt.append(s if k2 % 2 else re.sub(
                    u"第([一二三四五六七八九十]+)章(第[一二三四五六七八九十]+節)?", fx2, s))
            RELINK[u"n"] += hit[0]
            out.append(u"> " + u"".join(rebuilt) if l.startswith(u"> ") else u">" + u"".join(rebuilt))
            continue

        def fx(mo):
            tg = _map(mo.group(1), mo.group(2) or u"", src)
            if not tg:
                return mo.group(0)
            RELINK[u"n"] += 1
            return tg + (mo.group(2) or u"")
        out.append(re.sub(u"第([一二三四五六七八九十]+)章(第[一二三四五六七八九十]+節)?", fx, l))
    t2 = u"\n".join(out)
    return re.sub(u"\x01(\d+)\x01", lambda m: toks[int(m.group(1))], t2)


def ref_fn(text, stats):
    """母案碼 → 以案例名為鑰之自然指針。先化「〔遮44〕解牛牽牛」為「解牛牽牛案」，
    再化裸碼為「第N章『某』案」；無名可歸者原樣保留，由尺高報。"""
    CODE = u"〔(?:遮|開|僧|補遺)\\d+〕"

    def loc(code):
        stats[u"母案碼歸名"] = stats.get(u"母案碼歸名", 0) + 1
        got = CODE_LOC.get(code)
        if not got:
            return code
        ch, n, ttl = got
        return u"%s案例%s" % (ch, P.cn_num(n))

    def named(m):
        stats[u"母案碼歸名"] = stats.get(u"母案碼歸名", 0) + 1
        return m.group(2)          # 名在则留名，碼去即得自然之稱（如「解牛牽牛案」）

    t = re.sub(u"(" + CODE + u")([\\u3400-\\u9fffA-Za-z0-9]{2,12}?)(?=[，。、；：）」\\s|])", named, text)
    return re.sub(CODE, lambda m: loc(m.group(0)), t)


# ── 案例之缝合（指南第三部：文獻一詳本為血肉・文獻二三環裁斷為骨架）─────────
SEC_LABEL = [u"事相經過", u"心相照鏡", u"法相剖析", u"佛陀處斷", u"微觀動力學深描",
             u"人間智慧與行持", u"現代對讀", u"治理與修持對治", u"律藏原文", u"戒文（戒本次第）"]
MOD_ITEM = re.compile(u"^\\s*[0-9]+[.、]\\s*\\*\\*現代(?:對應|對讀)[^*\\n]{0,2}\\*\\*\\s*[：:]?\\s*(.+?)"
                      u"(?=\\n\\s*[0-9]+[.、]\\s*|\\Z)", re.M | re.S)
NARR_VERB = re.compile(u"^(把|自|將|以|看|聽|貪|瞋|癡|慢|疑|惧|恐|逐|求|爭|執|守|掩|藏|隱|規|避|"
                       u"託|藉|憑|恃|挾|營|圖|算|計|怨|恨|責|諂|誑|覆|掉|散|怠|放|認|見|聞|知|受|想|行|做|作|說|言|動|起|犯|修|持|犯)")
# ── 奉令①・真合併：同一因緣之兩卡合為一案（敘事不兩出，治理正理兩存）──
FW_MERGE = {u"〔開24〕": u"〔僧15〕"}
MERGE_TITLE = {u"〔開24〕": u"涅槃日之二態——眼淚藏不住修為，狂言逼出結集"}
MERGE_CAPS = {u"〔開24〕": (u"未離欲者哀慟之判", u"跋難陀狂言之判")}
MERGE_CUT = {u"〔開24〕": u"爾時有跋難陀"}   # 併案引文取其所獨出之部分（其前與主案同段，省以『……』）


def tidy(x):
    return re.sub(u"\\s*\\n?---\\s*$", u"", (x or u"").strip()).strip()


def novel_sents(main_text, para):
    """段內逐句核：主案已有之句不復重出——『刪敘事』至此方落得實處。"""
    have = tri(main_text)
    out, kept = [], 0
    for s in re.split(u"(?<=[。！？])", para):
        if not s.strip():
            continue
        t = tri(s)
        if t and len(t - have) * 2 <= len(t):
            continue
        out.append(s)
        have |= t
        kept += 1
    return u"".join(out).strip(), kept


def tri(s):
    s = re.sub(u"[^\\u3400-\\u9fff]", u"", s or u"")
    return set(s[i:i + 3] for i in range(max(0, len(s) - 2)))


def novel(paras, new):
    """併案之段與主案已有之段較其三元重疊：過半則同其敘事，棄之。"""
    have = set()
    for p in paras:
        have |= tri(p)
    t = tri(new)
    return bool(t) and len(t - have) * 2 > len(t)


def dup_body(code):
    """併案之欄：依新冊式樣取出（只取框架卡所有之欄，不增一法）。"""
    f = CARDS[code][u"fields"]
    out = {}
    v = relink(f.get(u"事相經過", u""), u"v").strip()
    if v:
        out[u"事相經過"] = v
    mir, _ok = to_second(relink(f.get(u"心相照鏡", u""), u"v"))
    if mir.strip():
        out[u"心相照鏡"] = mir.strip()
    for k, fk in ((u"佛陀處斷", u"佛陀處斷"), (u"人間智慧與行持", u"人間智慧"), (u"律藏原文", u"律藏原文")):
        w = relink(f.get(fk, u""), u"v").strip()
        if w:
            out[k] = w
    return out


def fold_merge(body, fw_code):
    """主案既成，併案之欄歸一處：敘事去重、判語分其二題、餘欄並列。"""
    dp = dup_body(FW_MERGE[fw_code])
    cap1, cap2 = MERGE_CAPS.get(fw_code, (u"主判", u"併判"))
    n = 0
    if u"事相經過" in dp:
        ps = [p for p in body.get(u"事相經過", u"").split(u"\n\n") if p.strip()]
        add, drop = [], []
        for p in dp[u"事相經過"].split(u"\n\n"):
            if not p.strip():
                continue
            if not novel(ps, p):
                drop.append(p)
                continue
            head = p[:p.index(u"\n")] if u"\n" in p else u""
            rest, kept = novel_sents(body.get(u"事相經過", u""), p[len(head):] if head else p)
            tot = len([1 for s in re.split(u"(?<=[。！？])", (p[len(head):] if head else p)) if s.strip()])
            SENT[u"merge_drop"] += max(0, tot - kept) + (1 if not kept else 0)
            if not kept:
                drop.append(p)
                continue
            add.append((head + u"\n" + rest if head else rest).strip())
        SENT[u"merge_drop"] += len(drop)
        if add:
            body[u"事相經過"] = u"\n\n".join(ps + add).strip()
            n += len(add)
    if dp.get(u"佛陀處斷") and body.get(u"佛陀處斷"):
        body[u"佛陀處斷"] = u"**%s**\n\n%s\n\n**%s**\n\n%s" % (
            cap1, tidy(body[u"佛陀處斷"]), cap2, tidy(dp[u"佛陀處斷"]))
        n += 1
    for k in (u"心相照鏡", u"人間智慧與行持"):
        if dp.get(k):
            body[k] = (tidy(body.get(k, u"")) + u"\n\n" + tidy(dp[k])).strip()
            n += 1
    if dp.get(u"律藏原文"):
        q = tidy(dp[u"律藏原文"])
        cut = MERGE_CUT.get(fw_code)
        if cut:
            j = q.find(cut)
            if j > 0:
                s = max(q.rfind(u"。", 0, j), q.rfind(u"』", 0, j)) + 1
                k2 = q.rfind(u"\n> ", 0, j)
                if k2 > 0 and s > k2:
                    q = q[:k2] + u"\n> 「……" + q[s:]
        tgt = u"律藏原文" if body.get(u"律藏原文") else (
            u"戒文（戒本次第）" if body.get(u"戒文（戒本次第）") else u"律藏原文")
        body[tgt] = (tidy(body.get(tgt, u"")) + u"\n\n" + q).strip()
        n += 1
    SENT[u"merge_fold"] += n
    return n
MIRROR_LEAD = [u"你且自照：", u"你照此心：", u"你當自問：", u"你——"]
ML = [0]
NO_PREFIX = re.compile(u"^(這|那|此|其|所|是|一|凡|若|但|而|且|又|或|故|蓋|夫|唯|莫|無|不|每|真正|一切)")


def to_second(text):
    """心相照鏡統一為第二人稱。"""
    text = text.strip()
    if not text:
        return text, False
    if u"你" in text[:120]:
        return text, True
    paras = text.split(u"\n\n")
    first = paras[0].strip()
    if first and not NO_PREFIX.match(first) and NARR_VERB.match(first):
        paras[0] = u"你" + first
        return u"\n\n".join(paras), True
    if first and not NO_PREFIX.match(first) and len(first) > 6:
        paras[0] = MIRROR_LEAD[ML[0] % 3] + first
        ML[0] += 1
        return u"\n\n".join(paras), True
    return text, False


def dedupe(a, b):
    """兩源同述一事：以四串重疊度判複，留甲去乙之複段。"""
    if not b:
        return u""
    ga = set(a[i:i + 4] for i in range(max(0, len(a) - 4))) if a else set()
    keep = []
    for para in re.split(u"\n\n+", b):
        seg = [para[i:i + 4] for i in range(0, max(0, len(para) - 4))]
        if not seg or (len([s for s in seg if s in ga]) / float(len(seg))) < 0.45:
            keep.append(para)
    return u"\n\n".join(keep)


def render_case(idx, title, fw_code, hl_case):
    """一案之全文（H3 標題＋H4 欄目）。"""
    f = CARDS[fw_code][u"fields"] if fw_code else {}
    hp, hq = ({}, u"")
    if hl_case:
        ordn, htitle, hp, hq, _ = hl_case
    body = {}
    narr = []
    h_narr = relink(u"\n\n".join(v for k, v in hp.items() if u"案發現場" in k or k in (u"制戒因緣",)), u"h")
    f_narr = relink(f.get(u"事相經過", u""), u"v")
    if h_narr:
        narr.append(h_narr)
    if not h_narr:
        narr.append(f_narr)          # 同案不兩抄：有今語詳本者，框架之約述不復重出
    body[u"事相經過"] = u"\n\n".join(narr).strip()
    f_mir, ok = to_second(relink(f.get(u"心相照鏡", u""), u"v"))
    body[u"心相照鏡"] = f_mir
    h_mir = relink(u"\n\n".join(v for k, v in hp.items() if u"行為心理" in k or k == u"心理剖析"), u"h")
    body[u"法相剖析"] = (dedupe(f_mir, h_mir) if f_mir else h_mir).strip()
    mo = MOD_ITEM.search(body[u"法相剖析"])
    if mo:
        # 一說一處：舊源將『現代對應』作剖析清單之末項，合編時又據之以立小節，遂同段兩出。
        # 今定其歸——其文唯入『現代對讀』小節，剖析之中刪末項而不多其文。
        body[u"_末項"] = mo.group(1).strip()
        body[u"法相剖析"] = body[u"法相剖析"][:mo.start()].rstrip()
    if fw_code and not f_mir and fw_code in MR.MIRROR_FILL:
        # 舊源此等卡唯作通相剖析，未立自照之欄；今就本卡之剖析與處斷轉一機位，不增一法
        f_mir = MR.MIRROR_FILL[fw_code]
        body[u"心相照鏡"] = f_mir
        SENT[u"mirror_fill"] += 1
        MR.MIRROR_WHY[title] = u"補遺親筆"
        ok = True
    if not body.get(u"心相照鏡") and body.get(u"法相剖析"):
        # 奉令②・統一六段：無鏡之案，即本案剖析之骨幹轉一機位（不增一義，只換一位）
        why, g = MR.make_mirror(body[u"法相剖析"], idx)
        if g:
            body[u"心相照鏡"] = g
            SENT[u"mirror_gen"] += 1
            MR.MIRROR_WHY[title] = why
        else:
            SENT[u"mirror_nog"] += 1
            MR.MIRROR_WHY[title] = u"無骨可轉"
    elif f_mir and title not in MR.MIRROR_WHY:
        MR.MIRROR_WHY[title] = u"源冊自照"
    if fw_code:
        SENT["second_ok" if ok else "second_missing"] += 1
    jud = [relink(f.get(u"佛陀處斷", u""), u"v")]
    if not jud[0]:
        jud = [relink(hp.get(u"律制", u""), u"h"), relink(hp.get(u"佛陀判語", u""), u"h"),
               relink(hp.get(u"結罪", u""), u"h")]
    body[u"佛陀處斷"] = u"\n\n".join(x for x in jud if x).strip()
    fw_wis = relink(f.get(u"人間智慧", u""), u"v").strip()
    if fw_wis:
        if u"我們" not in fw_wis[:160]:
            fw_wis = WIS_LEAD[idx % 4] + fw_wis
        body[u"人間智慧與行持"] = fw_wis
    if body.get(u"_末項"):
        body[u"現代對讀"] = body.pop(u"_末項")
    src = []
    if f.get(u"律藏原文"):
        src.append(relink(f[u"律藏原文"].strip(), u"v"))
    if hq:
        src.append(relink(hq.strip(), u"h"))
    raw_src = u"\n\n".join(x for x in src if x).strip()
    # 出處閘門：唯冠卷段／大正／戒本者得自稱『律藏原文』，餘者降其名為『戒文』
    keyed = bool(re.search(u"卷[一二三四五六七八九十0-9]|卷 [0-9]+|大正|No\\.142|《戒本》", raw_src))
    body[u"律藏原文" if keyed else u"戒文（戒本次第）"] = raw_src
    body[u"_原文key"] = u"律藏原文" if keyed else u"戒文（戒本次第）"
    body[u"微觀動力學深描"] = relink(f.get(u"微觀心理動力學深描", u""), u"v").strip()
    body[u"治理與修持對治"] = relink(f.get(u"治理與修持對治", u""), u"v").strip()
    shield = relink(u"\n\n".join(v for k, v in hp.items() if u"防禦靶點" in k), u"h")
    if fw_code and CARDS[fw_code].get(u"正理"):
        shield = (shield + u"\n\n" if shield else u"") + u"**正理參照**：" + CARDS[fw_code][u"正理"]
    if fw_code in FW_MERGE:
        fold_merge(body, fw_code)
    if fw_code in MERGE_TITLE:
        title = MERGE_TITLE[fw_code]
    t = [u"### 案例%s：%s" % (P.cn_num(idx), title)]
    for key in SEC_LABEL:
        txt = body.get(key, u"").strip()
        if key in (u"律藏原文", u"戒文（戒本次第）") and not txt:
            continue
        if not txt:
            continue
        t.append(u"")
        t.append(u"#### %s" % key)
        t.append(u"")
        t.append(txt if txt else u"（此案律庭無別斷之文，制戒之斷即上件事相。）")
    if shield.strip():
        t.append(u"")
        t.append(u"#### 此戒所護")
        t.append(u"")
        t.append(shield.strip())
    return u"\n".join(t), body


WIS_LEAD = [u"我們共勉：", u"我們同道共勉：", u"我們同勘此心：", u"我們且共勉："]
SENT = {u"second_ok": 0, u"second_missing": 0, u"case": 0, u"fw_only": 0, u"hl_only": 0,
        u"mirror_fill": 0, u"merge_fold": 0, u"merge_drop": 0,
        u"mirror_gen": 0, u"mirror_nog": 0}
USED_FW = set()


PLAN = {}          # 新章 → [(標題, 框架碼 or None, 護欄案 or None)]，預先算齊，指針方得一次落地


def _plan(new_chap, hl_src_chap):
    items = []
    for _m, _d in FW_MERGE.items():
        USED_FW.add(_d)              # 併案不自立一_slot，其欄歸於主案
    cset = P.hl_cases(hl, *HL_SP[_k(hl_src_chap)][:2]) if hl_src_chap else []
    # 一案源可分授數章（如護欄第十章：眾學法諸案留第十二章，七滅諍三案歸第二十章），
    # 故本章之案須逐案照落點表取，不得把該源全部案例倒進每一章。
    seq = [cid for (hc, cid), ch in PLACE_HL.items() if hc == hl_src_chap and ch == new_chap]
    for ordn, htitle, hp, hq, raw in cset:
        if u"案例%s" % P.cn_num(ordn) not in seq:
            continue
        codes = PAIR.get((hl_src_chap, u"案例%s" % P.cn_num(ordn)), [])
        code = next((c for c in codes if c not in USED_FW), None)
        if code:
            USED_FW.add(code)
        items.append((htitle, code, (ordn, htitle, hp, hq, raw)))
    for code in fw_order(new_chap):
        if code in USED_FW:
            continue
        USED_FW.add(code)
        items.append((CARDS[code][u"title"], code, None))
        SENT[u"fw_only"] += 1
    for n, (htitle, code, hcase) in enumerate(items, 1):
        if hcase:
            CASE_MAP[(hl_src_chap, u"案例%s" % P.cn_num(hcase[0]))] = (new_chap, n)
    return items


CASE_CHAPS = [(u"第七章", u"第五章"), (u"第八章", u"第六章"), (u"第九章", u"第七章"),
              (u"第十章", u"第八章"), (u"第十一章", u"第九章"), (u"第十二章", u"第十章"),
              (u"第十三章", u"第十一章"), (u"第十四章", None), (u"第十五章", u"第十二章"),
              (u"第十六章", u"第十三章"), (u"第十七章", u"第十四章"), (u"第十八章", u"第十五章"),
              (u"第二十章", u"第十章")]   # 七滅諍三案隨其篇聚歸此（其文已在第二十章第二節）
for _c, _h in CASE_CHAPS:
    PLAN[_c] = _plan(_c, _h)


def cases_of(new_chap, _unused=None):
    """本冊某章之全部案例・依預設計劃渲染（劃在先，故指針得以前瞻落地）。"""
    out = []
    for n, (title, code, hcase) in enumerate(PLAN.get(new_chap, []), 1):
        txt, body = render_case(n, title, code, hcase)
        out.append(txt)
    SENT[u"case"] += len(out)
    return u"\n\n---\n\n".join(out), len(out)


# ── 護欄章之「非卡散文」（卡身連其標題一併挖去，不使兩出）───────────────────
def hprose(num, before=None, after=None, cut=None, drop_sec=None):
    a, b = HL_SP[_k(num)][0], HL_SP[_k(num)][1]
    seg = hl.slice(a + 1, b)
    if before and before in seg:
        seg = seg.split(before)[0]
    elif after and after in seg:
        seg = seg[seg.find(after):]
    if cut:
        seg = seg.split(cut)[0]
    if drop_sec:
        for title, i, e in hl.secs(a, b, 3):
            if drop_sec in title:
                seg = seg.replace(hl.slice(i, e), u"")
    for ordn, htitle, hp, hq, raw in P.hl_cases(hl, a, b):
        seg = seg.replace(raw, u"")
        seg = seg.replace(u"#### 案例%s：%s" % (P.cn_num(ordn), htitle), u"")
    seg = re.sub(u"\n{3,}", u"\n\n", seg).strip()
    return relink(shift(drop_chap_head(seg)), u"h") if len(seg) > 60 else u""


def hfront(pat, lvl=3):
    """護欄卷首某 H3 塊（題詞・自序・導讀）。"""
    for i, l2, t in hl.h:
        if l2 == lvl and re.search(pat, t):
            nxt = [j for j, x, _ in hl.h if x <= lvl and j > i]
            return relink(shift(hl.slice(i, nxt[0] - 1 if nxt else i + 40), -1, 2), u"h")
    return u""


def vfront(pat):
    """框架卷首某 H2 塊。"""
    for i, l2, t in fw.h:
        if l2 == 2 and re.search(pat, t):
            nxt = [j for j, x, _ in fw.h if x <= 2 and j > i]
            return relink(shift(fw.slice(i, nxt[0] - 1 if nxt else i + 40), -1, 2), u"v")
    return u""


def vappx(letter):
    for i, l2, t in fw.h:
        if l2 == 1 and t.startswith(u"附錄%s" % letter):
            nxt = [j for j, x, _ in fw.h if x == 1 and j > i]
            return relink(shift(fw.slice(i + 1, nxt[0] - 1 if nxt else len(fw.lines)), -1, 3), u"v")
    return u""


def vappx_sec(letter, sub):
    """附錄內某一同層小塊（取 I-1・I-2 等）。"""
    a = next((i for i, l2, t in fw.h if l2 == 1 and t.startswith(u"附錄%s" % letter)), None)
    if not a:
        return u""
    nxt = [j for j, l2, _ in fw.h if l2 == 1 and j > a]
    b = nxt[0] - 1 if nxt else len(fw.lines)
    for title, i, e in fw.secs(a, b, 3):
        if sub in title:
            return relink(shift(fw.slice(i, e), -1, 3), u"v")
    return u""


def vappx_minus(letter, drop_marks=()):
    """整篇附錄而挖去若干的卡（附錄 H 之補遺已分隸第十二章）。"""
    a = next((i for i, l2, t in fw.h if l2 == 1 and t.startswith(u"附錄%s" % letter)), None)
    if not a:
        return u""
    nxt = [j for j, l2, _ in fw.h if l2 == 1 and j > a]
    b = nxt[0] - 1 if nxt else len(fw.lines)
    raw = fw.slice(a + 1, b)
    for code, c in CARDS.items():
        if not any(m in code for m in drop_marks):
            continue
        block = u"#### " + code + c["title"]
        i0 = raw.find(block)
        if i0 < 0:
            continue
        m = re.search(r"^#{1,4} ", raw[i0 + len(block):], re.M)
        i1 = i0 + len(block) + (m.start() if m else len(raw) - i0 - len(block))
        raw = raw[:i0] + raw[i1:]
    raw = re.sub(r"\n{3,}", "\n\n", raw).strip()
    return relink(shift(raw), u"v")


def vbody(pat):
    """框架之 H1 非章塊（結語・終卷）。"""
    for i, l2, t in fw.h:
        if l2 == 1 and re.search(pat, t):
            nxt = [j for j, x, _ in fw.h if x == 1 and j > i]
            return relink(shift(fw.slice(i + 1, nxt[0] - 1 if nxt else len(fw.lines))), u"v")
    return u""


# ── 附錄三・戒本表之指針落地 ────────────────────────────────────────────────
def jieben():
    a = next(i for i, l2, t in hl.h if l2 == 1 and t.startswith(u"附錄"))
    raw = hl.slice(a + 1, len(hl.lines))
    raw = JN.insert(JN.fix_claim(raw), ROOT)      # 補乙部三組・改通數之宣稱
    txt = relink(raw, u"h")
    jn_stats(txt)
    return shift(txt, -1, 3)


def jn_stats(txt):
    """表題之數必由表身自算，不許手打（帳掛 STATS，供 build 印與 check 核）。"""
    c = JN.counts(txt)
    STATS["戒本號數"] = c
    return c


def case_refs(text):
    """（保留同名外廓・實已由 relink 一手落地）"""
    return text


def fw6_intro():
    """框架第六章之『非卡散文』（三篇之立言總意）——卡身分隸第七～十三章，唯此導言舊册未帶則亡。"""
    a, b = FW_SP[_k(u"六")][0], FW_SP[_k(u"六")][1]
    seg = fw.slice(a + 1, b)
    for code, c in CARDS.items():
        block = u"#### " + code + c[u"title"]
        i0 = seg.find(block)
        if i0 < 0:
            continue
        m = re.search(r"^#{1,4} ", seg[i0 + len(block):], re.M)
        i1 = i0 + len(block) + (m.start() if m else len(seg) - i0 - len(block))
        seg = seg[:i0] + seg[i1:]
    seg = re.sub(r"\n{3,}", u"\n\n", seg).strip()
    return relink(shift(drop_chap_head(seg)), u"v") if len(seg) > 40 else u""


def vfanli_part(sub):
    """框架【全書凡例】內某一 H3/H4 小塊（引文承諾六律・三層標記系統）。"""
    a = next((i for i, l2, t in fw.h if l2 == 2 and u"全書凡例" in t), None)
    if not a:
        return u""
    nxt = [j for j, l2, _ in fw.h if l2 <= 2 and j > a]
    b = nxt[0] - 1 if nxt else len(fw.lines)
    for title, i, e in fw.secs(a, b, 3):
        if sub in title:
            return relink(shift(fw.slice(i, e)), u"v")
    for title, i, e in fw.secs(a, b, 4):
        if sub in title:
            return relink(shift(fw.slice(i, e)), u"v")
    return u""


def vdaodu_part(sub):
    """框架【卷首導讀】內某一小塊（四種讀者極速導航動線）。"""
    a = next((i for i, l2, t in fw.h if l2 == 2 and u"卷首導讀" in t), None)
    if not a:
        return u""
    nxt = [j for j, l2, _ in fw.h if l2 <= 2 and j > a]
    b = nxt[0] - 1 if nxt else len(fw.lines)
    for title, i, e in fw.secs(a, b, 3):
        if sub in title:
            return relink(shift(fw.slice(i, e)), u"v")
    return u""


CODE_LOC = {}      # 〔XN〕→ (新章, 案序, 標題)——PLAN 定後方能成形
for _ch, _items in PLAN.items():
    for _n, (_t, _code, _hc) in enumerate(_items, 1):
        if _code:
            CODE_LOC[_code] = (_ch, _n, MERGE_TITLE.get(_code, _t))
for _m, _d in FW_MERGE.items():
    if _m in CODE_LOC:
        CODE_LOC[_d] = CODE_LOC[_m]      # 併案之碼，指針歸於主案之位（不使成孤碼）

