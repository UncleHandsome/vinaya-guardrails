# -*- coding: utf-8 -*-
"""新冊清創規則：把兩本舊冊的「後台語法」逐條還原為出版文字。

每一規則自計其數，由 `_book/check.py` 另以產物本身復量——規則自報之數只供調試，
不作為『已清除』之憑據（量產物方為憑）。
"""
import re

# ── 道岔代號 → 規範之法律與法相用語（指南模組二・四）────────────────────────
DAOCHA = [
    (u"道岔一-B", u"中止未遂減免"), (u"道岔三A", u"開許回撤即淨"), (u"道岔三B", u"開許逾期轉犯"),
    (u"道岔五B", u"私省止步"),
    (u"道岔一", u"無心差誤免責"), (u"道岔二", u"止犯補行還淨"), (u"道岔三", u"急難開許終止"),
    (u"道岔四", u"公訴法權讓位"), (u"道岔五", u"教誡防護示令"), (u"道岔六", u"移轉管轄救濟"),
]

# ── 舊冊術語 → 出版用語 ─────────────────────────────────────────────────────
WORDS = [
    (u"六道岔口：全書離場通道唯此一名", u"離場通道六事"),
    (u"〔道岔編號之用〕", u"〔通道次序之說明〕"),
    (u"道岔編號", u"通道之名"),
    (u"道岔分流", u"免責與轉軌之分流"),
    (u"道岔出口", u"免責與轉軌之出口"),
    (u"分流處置與道岔", u"分流處置與通道"),
    (u"核發分流碼", u"核定分流"), (u"分流碼", u"分流之裁"),
    (u"扣合四階漏斗", u"合於四階之序"),
    (u"決策圖", u"審理流程圖"),
    (u"負測", u"逆向查核"),
    (u"三階縮放協議", u"三階取用之序"),
    (u"自然人心證自律卡", u"自然人作證之自律規範"),
    (u"慎獨隱私自律卡", u"慎獨與隱私之自律規範"),
    (u"禁語防護自律卡", u"禁語防護之自律規範"),
    (u"群組正命自律卡", u"群組正命之自律規範"),
    (u"四大隨身行動卡", u"數位通訊與隱私自律規範"),
    (u"行動卡一", u"其一"), (u"行動卡二", u"其二"), (u"行動卡三", u"其三"), (u"行動卡四", u"其四"),
    (u"終局裁決存檔卡", u"終局裁決之存檔法式"),
    (u"移轉管轄求生落地卡", u"移轉管轄求生之法式"),
    (u"求生卡", u"求生之單一指針"),
    (u"隨身三印卡", u"隨身三印"),
    (u"竹筏自捨協議", u"竹筏自捨之行持準則"),
    (u"語業零", u"語業歸零"),
    (u"判例單元", u"案例"),
    (u"附錄J-", u"附錄四・J-"), (u"附錄J", u"附錄四"),
    (u"附錄A-", u"附錄一・A-"), (u"附錄A", u"附錄一"),
    (u"附錄B", u"附錄二"), (u"附錄D-", u"附錄五・D-"), (u"附錄E-", u"附錄五・E-"),
    (u"附錄F-", u"附錄五・F-"), (u"附錄D", u"附錄五"), (u"附錄E", u"附錄五"), (u"附錄F", u"附錄五"),
    (u"附錄I-2", u"第五章"), (u"附錄I-1", u"第二十七章"), (u"附錄H-0", u"第十二章"), (u"附錄H", u"第十二章"),
    (u"附錄I", u"第二十七章"),
    (u"九章百則", u"全書諸案"), (u"百則判例", u"諸案判例"), (u"百則案例庫", u"判例之庫"),
    (u"百則底冊", u"判例之檔"), (u"百則編號", u"案例之名"), (u"百則", u"諸案"),
    (u"澈底", u"徹底"),
    (u"物體脱離本處", u"物體脫離本處"),
]

# ── 自報帳目・校勘痕跡之整行剷除 ───────────────────────────────────────────
GUIDE_BLOCK = re.compile(u"^\\s*>?\\s*〔?◈?跨章精準導流〕?.*$|^\\s*\\*\\*〔◈跨章精準導流〕\\*\\*")
JIAER = re.compile(u"、?\\s*【[^】]*慢心療法[^】]*】")


LEDG_QUOTE = [u"章末檢索附註", u"之查檢指針", u"之收束指針", u"《總表與終極壓縮》", u"由定位行自算"]


def drop_ledger_quotes(text, stats):
    """整塊『章末檢索／收束指針』之圍注全落：彼乃舊冊之後台導航，非義理。"""
    lines = text.split(u"\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if any(x in l for x in LEDG_QUOTE) and (l.lstrip().startswith(u">") or l.lstrip().startswith(u"**")):
            stats["台帳圍注"] += 1
            i += 1
            while i < len(lines) and (lines[i].lstrip().startswith(u">") or not lines[i].strip()):
                i += 1
            continue
        out.append(l)
        i += 1
    return u"\n".join(out)


def strip_guide_blocks(text, stats):
    out = []
    for l in text.split(u"\n"):
        if GUIDE_BLOCK.match(l.strip()):
            stats["導流脚手架"] += 1
            continue
        nl = JIAER.sub(u"", l)
        if nl != l:
            stats["舊說指針"] += 1
        out.append(nl)
    return u"\n".join(out)


LEDGER_LINE = re.compile(
    u"133 處|133 綁|共 133|綁定點|綁定台帳|落點次數|107 處|與落點對齊|三向加總|"
    u"百則基準|唯一法定底冊|100 判例單元|100 案|判例單元之數|計入百則|不計入百則|"
    u"權威基準承諾|本地語料未收之?數|全書核得|由定位行自算|自算器|"
    u"全書附錄共十二篇|經評議取消|舊撮合之語|不另列儲備")

# 詞頻・檢索式之數據（指南模組二・六：考據結果採用，細節退入腳註，正文不數詞頻）
COUNT_PAREN = re.compile(
    u"（[^（）]{0,60}?(?:檢索|凡|出現|得)[^（）]{0,60}?[見次發][^（）]{0,20}?）")
COUNT_INLINE = re.compile(u"〔檢索式〕[^。]*。|檢索式[：:][^。\n]*。")
# 以句為單位改寫之詞頻句（舊冊自報語料之數，今存其理而削其數）
SENT_REWRITE = [
    (re.compile(u"在三百四十八則排查邊緣疑難案件的判例段落中，檢索得[^。]*。"),
     u"於邊緣疑難之判例段落中，『波羅夷』與『無犯』往復交見，"
     u"而世尊開庭審查動機之垂問「汝以何心」尤數數見之。"),
]
COUNT_TOKEN = re.compile(r"『[^』]{1,12}』\s*[0-9]+\s*(?:見|次)|[0-9]+\s*見")

# ── 標題塊之整塊剷除（指南模組二・三・八，模組四・二）───────────────────────
DROP_HEAD = [
    u"三十格", u"林下留白", u"空白格", u"留白觀",
    u"章末收卷", u"全章收卷", u"公堂燈熄", u"吃茶去", u"松風吹拂", u"樹下吹風",
    u"章末引橋", u"把法袍留在門外", u"走出解剖室", u"核心引橋", u"引橋：手握總帳",
    u"五維立體檢索", u"檢索總表", u"檢索樞紐", u"檢索指南", u"速查軸",
    u"綁定台帳", u"複統攝深水稱重", u"終極壓縮四階",
    u"附錄收編之界", u"開卷標準目錄", u"全書詳細目錄", u"卷首導讀",
    u"心智生態系統全貌圖", u"人機協同", u"自然人心證自律宣告書",
]
DROP_HEAD_EXACT = [u"八、附錄收編之界", u"三、非染污端多軌整合法則與三十格檢索總表",
                   u"四、隨犯隨制偏態原理與矩陣空白格之意趣（林下留白觀）",
                   u"五、空白格之如實與三項治理通則"]

# 表格之整張剷除（台帳型）
DROP_TABLE = re.compile(u"綁定數|完整案例清單|篇別綁定點|落點|詞頻|見數|檢索|速查|座標與空格")

QUOTE = u"「」『』“”‘’"


def fence_split(text):
    """切為 (圍欄外行, 圍欄內行) 之標記序列：返 [(is_fence, line)]。"""
    out, ins = [], False
    for l in text.split("\n"):
        if l.startswith("```"):
            ins = not ins
            out.append((True, l))
            continue
        out.append((ins, l))
    return out


def strip_tags(text, stats):
    """剷〔◈…〕符號帽子；帽子獨占之行連同其導流整塊一併落下。"""
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        m = re.search(u"〔◈[^〕]*〕", l)
        if m:
            bare = re.sub(u"〔◈[^〕]*〕", u"", l).strip()
            stats["符號帽子"] += len(re.findall(u"〔◈[^〕]*〕", l))
            if u"跨章精準導流" in l:
                i += 1
                while i < len(lines) and lines[i].startswith(">"):
                    i += 1
                continue
            if bare in (u"", u">", u"**", u"> **", u"** **", u"#"):
                i += 1
                continue
            out.append(re.sub(u"^(#{1,6} )", lambda z: z.group(1), bare))
            i += 1
            continue
        out.append(l)
        i += 1
    return "\n".join(out)


def drop_blocks(text, stats):
    """命中 DROP_HEAD 之標題連其身一併剷除（含其下較深層之全部標題）。"""
    lines = text.split("\n")
    out = []
    skip_lvl = 0
    fence = False
    for l in lines:
        if l.startswith("```"):
            fence = not fence
            if not skip_lvl:
                out.append(l)
            continue
        m = re.match(r"^(#{1,6}) (.*)$", l)
        if fence:
            out.append(l)
            continue
        if m:
            lvl = len(m.group(1))
            if skip_lvl and lvl <= skip_lvl:
                skip_lvl = 0
            title = m.group(2)
            hit = any(k and k in title for k in DROP_HEAD) or title in DROP_HEAD_EXACT
            if hit:
                skip_lvl = lvl
                stats["剷除標題塊"] += 1
                continue
        if skip_lvl:
            if l.strip() in (u"---", u"***"):
                continue
            stats["剷除塊內行"] += 1
            continue
        out.append(l)
    return "\n".join(out)


def drop_ledger_lines(text, stats):
    out = []
    for l in text.split("\n"):
        if l.startswith("```"):
            out.append(l)
            continue
        if l.strip().startswith("|") and DROP_TABLE.search(l):
            stats["剷除台帳表"] += 1
            continue
        if not l.startswith(">") and LEDGER_LINE.search(l):
            stats["剷除台帳行"] += 1
            continue
        out.append(l)
    return "\n".join(out)


def tables_purge(text, stats):
    """台帳型表格整張剷除：以表頭行為判。"""
    lines = text.split("\n")
    out, i, fence = [], 0, False
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            fence = not fence
            out.append(l); i += 1; continue
        if (not fence and l.strip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1])
                and DROP_TABLE.search(l)):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            stats["台帳表整張"] += 1
            i = j
            continue
        out.append(l); i += 1
    return "\n".join(out)


def decount(text, stats):
    """剷正文詞頻數據。"""
    def c1(m):
        stats["詞頻括號"] += 1
        return u""
    t = COUNT_PAREN.sub(c1, text)
    for rx, rep in REGEX_REWRITE:
        k = len(rx.findall(t))
        if k:
            stats["正则改寫"] = stats.get(u"正则改寫", 0) + k
            t = rx.sub(rep, t)
    t = COUNT_INLINE.sub(lambda m: u"", t)
    t = re.sub(u"[（(][^（()）]{0,40}?檢索得[^（()）]{0,80}?[）)]", u"", t)
    for rx, rep in SENT_REWRITE:
        k = len(rx.findall(t))
        if k:
            stats["詞頻改句"] = stats.get("詞頻改句", 0) + k
            t = rx.sub(rep, t)
    return t


def names_fix(text, stats, pairs):
    """正名令：引號內不動，敘述文字改從律典正名。"""
    out = []
    for l in text.split("\n"):
        if l.startswith(">"):
            out.append(l)
            continue
        parts = re.split(u"(「[^」]*」|『[^』]*』)", l)
        n = 0
        for k, p in enumerate(parts):
            if k % 2 == 0:
                for bad, good in pairs:
                    if bad in p:
                        n += p.count(bad)
                        p = p.replace(bad, good)
                parts[k] = p
        if n:
            stats["正名改寫"] += n
        out.append("".join(parts))
    return "\n".join(out)


def soften(text, stats):
    """感嘆號降溫・演講腔轉為法理斷語（引文區不動）。"""
    out = []
    for l in text.split("\n"):
        if l.startswith(">"):
            out.append(l)
            continue
        nl = re.sub(u"!{2,}|！{2,}", u"！", l)
        if nl != l:
            stats["連嘆號降溫"] += 1
        out.append(nl)
    return "\n".join(out)


DING = re.compile(u"^\*\*定位｜.*\*\*$")


NUM_ITEM = re.compile(u"^\\s+(\\d+\\.\\s)")


def detent_items(text, stats):
    """舊冊以兩空格接排之『2. 3. 4.』條目，於本冊須各自成項（否則全併入第一項）。"""
    lines = text.split(u"\n")
    out, fence = [], False
    n = 0
    for l in lines:
        if l.startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        m = NUM_ITEM.match(l)
        if m and out and out[-1].strip():
            out.append(u"")
            out.append(NUM_ITEM.sub(u"\\1", l))
            n += 1
        else:
            out.append(l)
    stats["序號歸位"] = stats.get(u"序號歸位", 0) + n
    return u"\n".join(out)


# 舊冊之括弧標籤 → 出版之自然小標
LABELS = [(u"**【案發現場（制戒因緣）】：**", u"**制戒因緣**："),
          (u"**【案發現場（犍度因緣）】：**", u"**犍度因緣**："),
          (u"**【案發現場】：**", u"**案發現場**："),
          (u"**【制戒因緣】：**", u"**制戒因緣**："),
          (u"**【行為心理剖析】：**", u"**行為心理剖析**："),
          (u"**【防禦靶點】：**", u"**此戒所護**："),
          (u"**【律制】：**", u"**律制**："),
          (u"**【心理剖析】：**", u"**心理剖析**："),
          (u"【條文】：", u"戒文："), (u"【律文】：", u"律文："),
          (u"【初制戒文】：", u"初制戒文："), (u"【二制戒文】：", u"二制戒文："),
          (u"【三制戒文】：", u"三制戒文："),
          (u"**現代對應：**", u"**現代對讀**："),
          (u"本冊", u"本書")]
LABEL_NUM = re.compile(u"【第([0-9]+)條 條文】：")


TOOLBOX = [(u"卷末・工具箱第三節", u"第二十六章"), (u"卷末・工具箱第二節", u"第二十七章"),
           (u"卷末・工具箱第四節", u"第二十六章"), (u"卷末・工具箱第五節", u"第二十八章"),
           (u"卷末・工具箱", u"第二十六至二十八章")]


def repoint_toolbox(text, stats):
    """舊冊『卷末・工具箱』之指針改指新章，唯行於內文——結構標題自有其名，不受此改。"""
    out = []
    for l in text.split(u"\n"):
        if l.startswith(u"#"):
            out.append(l)
            continue
        for bad, good in TOOLBOX:
            if bad in l:
                stats["工具箱改指"] += l.count(bad)
                l = l.replace(bad, good)
        out.append(l)
    return u"\n".join(out)


def naturalize_labels(text, stats):
    t = text
    for bad, good in LABELS:
        if bad in t:
            stats["標籤歸形"] = stats.get(u"標籤歸形", 0) + t.count(bad)
            t = t.replace(bad, good)
    k = len(LABEL_NUM.findall(t))
    if k:
        stats["標籤歸形"] = stats.get(u"標籤歸形", 0) + k
        t = LABEL_NUM.sub(lambda m: u"第%s條戒文：" % m.group(1), t)
    return t


def apply_rules(text, stats, ref_fn=None, name_pairs=(), overrides=None):
    """規則之總序：先塊後行、先形後數。"""
    t = text
    t = text
    for bad, good in (overrides or []):        # 指定改寫先行
        if bad and bad in t:
            stats["指定改寫"] = stats.get("指定改寫", 0) + 1
            t = t.replace(bad, good)
    t = naturalize_labels(t, stats)
    t = repoint_toolbox(t, stats)
    keep = []
    for l in t.split(u"\n"):
        if DING.match(l.strip()):
            stats["案頭定位行"] += 1
            continue
        keep.append(l)
    t = u"\n".join(keep).replace(u"\n\n\n", u"\n\n")
    t = strip_tags(t, stats)
    t = strip_guide_blocks(t, stats)
    t = drop_ledger_quotes(t, stats)
    t = drop_blocks(t, stats)
    t = tables_purge(t, stats)
    t = drop_ledger_lines(t, stats)
    t = decount(t, stats)
    for bad, good in DAOCHA:
        for form in (u"【%s】" % bad, bad):
            if form in t:
                stats["道岔改語"] += t.count(form)
                t = t.replace(form, u"【%s】" % good if form.startswith(u"【") else good)
    n = len(re.findall(u"問\\[\\d+\\]|第\\[\\d+\\]問", t))
    t = re.sub(u"第\\[(\\d+)\\]問", lambda m: u"第%s問" % m.group(1), t)
    t = re.sub(u"問\\[(\\d+)\\]", lambda m: u"第%s問" % m.group(1), t)
    t = re.sub(u"\\[(\\d+)\\]", lambda m: u"〔%s〕" % m.group(1) if False else m.group(0), t)
    stats["問卷代碼歸形"] += n
    t = t.replace(u"**[", u"**第").replace(u"] ", u"問 ")
    t = re.sub(u"^\\s*\\| \\*\\*第(\\d+)問 (.*?)\\*\\* \\|", lambda m: u"| **%s、%s** |" % (m.group(1), m.group(2)), t, flags=re.M)
    t = t.replace(u"[ ]", u"□").replace(u"[　]", u"□")
    for bad, good in WORDS:
        if bad in t:
            stats["術語改語"] += t.count(bad)
            t = t.replace(bad, good)
    t = detent_items(t, stats)
    t = names_fix(t, stats, name_pairs)
    t = soften(t, stats)
    if ref_fn:
        t = ref_fn(t, stats)
    t = re.sub(u"\n{4,}", u"\n\n\n", t)
    return t


# 以正则行指定改寫（錨點不dependency章號之變者）
REGEX_REWRITE = [
    (re.compile(u"各案暫不佔[^。]*台帳之點；綁定以[^。]*台帳為準。"),
     u"正理參照僅為研讀之指引，不別立全書之綁定清冊。"),
    (re.compile(u"正式入編[^。]*後之綜合三環與正理對位，一律以[^。]*為準。"),
     u"正式入編之後之綜合三環與正理對位，一律以各案『心相照鏡』與『佛陀處斷』兩欄為準。"),
    (re.compile(u"完整正理組合見[^；]*；"), u"完整正理組合見各案『佛陀處斷』之欄；"),
    (re.compile(u"複統攝案"), u"一案而貫數理者"),
    (re.compile(u"附錄三第三節出罪復權"), u"附錄五經論互證之出罪復權"),
    # 指南模組二・八：『三印卡』之實還原為正式章節名（原題保留為副）
    (re.compile(u"^(## 第[一二三四五六七八九十]+節　)法庭淨空、消磁與歸家$", re.M),
     u"\\1結案與法庭消磁程序（法庭淨空與歸家之儀）"),
    (re.compile(u"並經校驗程序逐字比對；第三十八版統一口徑覆核後，[^；]*不再有部分案例為縮寫撮要之情形"),
     u"並經逐字比對；凡引號內之片段皆可回查得之，未復有縮寫撮要之情形"),
    (re.compile(u"今天，在第三十八版全書深度校勘與引文純淨化工程告一段落之際"), u"今天，全書校稿既畢"),
    (re.compile(u"《四分律》起心動念心智分析框架（第三十八版·全書深度校勘清創版，Ver 38\\.0）"),
     u"《佛陀的護欄：四分律行為心理學與現代僧伽治理》"),
    (re.compile(u"秋月·沙門釋子於阿蘭若空閑處·合掌熔封"), u"秋月·沙門釋子於阿蘭若空閑處·合掌"),
    (re.compile(u"附錄三（總表與終極壓縮）"), u"第二十一章（解縛還淨）"),
    (re.compile(u"以附錄三第一節『七層生克機制深描』為準"), u"以第五章『七層生克機制深描』為準"),
    (re.compile(u"附錄三第二節第四軸之七階"), u"處分階梯之七階"),
    (re.compile(u"附錄三總表既畢"), u"諸案判例既畢"),
    (re.compile(u"承接附錄三終極壓縮之引橋"), u"承接前文由繁入簡之序"),

]
