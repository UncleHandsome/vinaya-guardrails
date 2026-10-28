# -*- coding: utf-8 -*-
"""第四波・遺失資產之精準回流（物歸原主，非倒退 ver39）。

法源＝本檔 ASSETS 之 ver39 行域；目錄與附錄之目由 ASSETS 自算，不兩抄。
三閘俱在本檔內：
  甲・形制閘：層級按冊移位（附錄題作 H2，得另起一頁；節款目隨之）。
  乙・逐字閘：迎回區內凡「…」式樣，先在本地語料見形（_tk.VINAYA＋他部，只留漢字並折異文）；
             無形者自動降為『…』（本書之撮述式樣），不虛掛逐字。含嵌套者列紅候理，不擅改。
  丙・指針閘：ver39 之章次指針一律按兩冊之實歸位；錨非唯一即報不改（不造數）。

用法：python -X utf8 _work/pairreflow.py            （試跑：印落點・降格・指針，不移檔）
      python -X utf8 _work/pairreflow.py --write    （落盤：先備份 .pre_reflow＋SHA-12）
"""
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _tk  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "ver39四分律_起心動念心智分析框架_修正版.md"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
BAK = ROOT / "_archive/備份/AI清理前"
APX_LV = {1: 2, 2: 3, 3: 3, 4: 4, 5: 5, 6: 6}

ASSETS = [
    (F1, "卷首・出版凡例", 241, 312, "## 【出版凡例與引文承諾】", "## 【全書標準總目錄】"),
    (F2, "卷首・出版凡例", 241, 312, "## 【出版凡例與引文承諾】", "## 第一篇：憲政基石"),
    (F1, "附錄一", 7352, 7452, "## 附錄一　宗門心法——禪案與自性觀照輯要", None),
    (F1, "附錄二", 7453, 7512, "## 附錄二　心相與病相照對清冊", None),
    (F1, "附錄三", 7513, 7529, "## 附錄三　境想與心識名相釋義", None),
    (F1, "附錄四", 1531, 2073, "## 附錄四　照鏡察心：六重心智閘門", None),
    (F2, "附錄一", 6281, 6420, "## 附錄一　判例四維極速檢索矩陣", None),
    (F2, "附錄二", 7625, 7804, "## 附錄二　判例原典逐條回查索引", None),
    (F2, "附錄三", 7529, 7624, "## 附錄三　律制名相與梵巴對照釋義", None),
    (F2, "附錄四", 7805, 7839, "## 附錄四　大乘經論逐字互證表", None),
]
# 凡例七節之去留：六＝跨域轉譯隔離（一、二、三令既剷除跨域名相，留之即虛約）；
# 二節之通道標籤段唯 F2 有其事，F1 除該段。
APX_SECTIONS = {F1: ["一", "二", "三", "四", "五", "六", "七"], F2: ["一", "二", "三", "四", "五", "七"]}

CUT_LINE = {F1: [("又 `〔…〕` 之形在本冊唯供二用：", "通道標籤")]}

# 甲・自稱歸位（唯施於該件之內：形如 (冊, 件) → [(舊, 新)]）
SELF = {
    (F1, "附錄二"): [(k, v) for k, v in [
        ("本節借用當代認知心理學、臨床精神醫學與社會心理學語彙", "本附錄借今時治病用人之常言作對位")]],
    (F1, "附錄四"): [(k, v) for k, v in [
        ("本章將佛陀那一聲千古垂問", "本附錄將佛陀那一聲千古垂問"),
        ("貫穿本章的導航工具", "貫穿本附錄的導航工具"),
        ("本章專司其動機與構成要件之定性，後續處分階梯各依本篇軌道分流",
         "本附錄專司其動機與構成要件之定性，後續處分階梯各依《如法推尋》之軌分流")]],
}

# 整行改寫（唯一前錨，非新撰逐字，俱是本書自陳之語）
REWRITE = {
    F1: [("2. **原典層**",
          "2. **原典層**：大正藏 No. 1428 六十卷正文及 No. 1429 之逐字經文，他部律別例加註說明。"
          "**今冊之落點如實記**：本冊第七章至第十章之【案卷】卡，其律據俱以引框出之——"
          "框內為逐字之文（掛「」），框下一行署出處卷次與篇聚；逐字者俱就地覆核，"
          "撮述與本書之解不掛「」。本冊不立台帳之欄，一百零二案之原典逐字底冊"
          "在其姊妹篇《如法推尋》附錄二，兩冊互參。"),
         ("### 六、現代跨域轉譯隔離", "### 六、跨域對位之限"),
         ("凡引入現代法學、管理學及認知科學名相",
          "本冊正文一依律典原生法相與唯識心所之語彙，不引外來學科之名。唯附錄二為便行者以今時病相驗其所得，"
          "存『功能對位』一類：其性質純屬溝通之引橋，非概念等同，更非新立之戒相；律典所診者乃活生生之行為表業"
          "與心識染淨，非今時醫學之病名。逐組俱以法相為本體，讀者取其所指，勿拘其名。"),
         ("1. **章直轄節**：全書章直轄節",
          "1. **章直轄節**：本冊章直轄節，節下為款，款下為目；卷首諸件（自序、開卷心印、生命之樹、凡例、總目錄）"
          "於印面與章同級，各另起一頁。")],
    F2: [("2. **原典層**",
          "2. **原典層**：大正藏 No. 1428 六十卷正文及 No. 1429 之逐字經文，他部律別例加註說明。"
          "**今冊之落點如實記**：第五篇一百零二案以集群矩陣・經典地標之案號列・節題三形載其定義，"
          "其原典逐字之文彙於**附錄二《判例原典逐條回查索引》**（今 102 案一案一行，引段俱就地覆核）；"
          "調部疑難判例法理十五則在第十九章。凡此俱外之逐字，一依第一節之出處閘門判之，"
          "不得以撮述之文掛逐字之名。"),
         ("#### 二、罪性與刑名之階（犯相之輕重）", "#### 一、罪性與刑名之階（犯相之輕重）"),
         ("#### 三、羯磨・法權與滅諍（程序之成就）", "#### 二、羯磨・法權與滅諍（程序之成就）"),
         ("#### 四、行治階序與律事名物（出罪之路・制中之人相時相）",
          "#### 三、行治階序與律事名物（出罪之路・制中之人相時相）"),
         ("1. **章直轄節**：全書章直轄節",
          "1. **章直轄節**：本冊篇下設章，章直轄節，節下為款，款下為目；卷首諸件（自序、開卷總綱、結構全貌圖、凡例）"
          "於印面與章同級，各另起一頁。")],
}
INSERT = {F2: [("## 附錄三　律制名相與梵巴對照釋義", ["", "### 一、律典原生核心名相法意釋義（律制之部）", ""])]}


# 丙・指針歸位（舊 ver39 章次 → 今冊之實；俱經對冊查證，見本輪帳）
POINTER = {
    F1: [
        ("第六章之判例集群矩陣、生活場域分類、心理病相歸位與程序處斷摘要",
         "第五章之生活場域分類、附錄二之心相病相照對與本冊處斷摘要"),
        ("第六章一百零二案以集群矩陣", "本冊第七章至第十章之案卷以案例卡"),
        ("六重閘門、三環自省", "六重心智閘門、夜半四照"),
        ("仍須嚴格依照第四章求聽、現前開庭、自言治定罪之羯磨程序處理",
         "仍須嚴格依照《如法推尋》現前開庭、自言治定罪之羯磨程序處理"),
        ("對治之道**：第四章白四羯磨如法三諫", "對治之道**：本冊第五章白四羯磨如法三諫"),
        ("第六章〔案例 47〕波逸提法譏嫌戒", "本冊第三章正理二（世間信心）譏嫌之防"),
        ("第一章正理五不可逆底線", "第三章正理五不可逆底線"),
        ("第三章閘門二『怠學加重律』", "附錄四閘門二『怠學加重律』"),
        ("第三章閘門五嚴格審查破僧程序", "附錄四閘門五嚴格審查破僧程序"),
        ("第六章〔案例 49〕波逸提法勸足食戒", "本冊第八章【案卷 49】波逸提法勸足食戒"),
        ("第六章〔案例 44〕確立", "本律『二人不前不後俱不收，二俱波逸提』確立"),
        ("第六章〔案例 16〕第四僧殘自讚身索淫供戒", "本冊第七章【案卷 16】第四僧殘自讚身索淫供戒"),
        ("第八章第二節確立【反靈性煤氣燈操縱防護禁約】", "《如法推尋》第十四章【調查倫理與舉罪五德】"),
        ("**【第三章提撕：窗櫺非牢籠】**", "**【附錄四提撕：窗櫺非牢籠】**"),
        ("承第二章第五節引橋", "承第二章藉事顯心之公約"),
        ("第七章【夜半四照】", "第十一章【夜半四照】"),
        ("見第四章第一節", "見《如法推尋》羯磨瑕疵之判"),
        ("如法懺悔（第五章）", "如法懺悔（《如法推尋》第九章）"),
        ("直接對接第五章之戒體損益模型", "直接對接《如法推尋》第九章之戒體損益模型"),
    ],
    F2: [
        ("第六章之判例集群矩陣、生活場域分類、心理病相歸位與程序處斷摘要",
         "第五篇之判例集群矩陣、經典地標之案號列與程序處斷摘要"),
        ("第六章一百零二案以集群矩陣", "第五篇一百零二案以集群矩陣"),
        ("六重閘門、三環自省", "六重檢索維度、四階審查"),
        ("本節將第六章 102 則判例", "本表將第五篇 102 則判例"),
        ("第三章閘門二之『生疑妄動』", "《起心動念》附錄四閘門二之『生疑妄動』"),
        ("第三章見軸阿利吒宣稱淫欲非障道法", "《起心動念》附錄四見軸阿利吒宣稱淫欲非障道法"),
        ("繇第六章案號之定義載體", "繇第五篇案號之定義載體"),
        ("**第二章·止犯煩惱引擎**", "**《起心動念》第四章·止犯煩惱引擎**"),
        ("**第二章·掉舉散亂之辨**", "**《起心動念》第六章·掉舉散亂之辨**"),
        ("**第二章·戒禁取見唯識定義**", "**《起心動念》第四章·戒禁取見唯識定義**"),
        ("**第一章·撥無二諦惡取空**", "**《起心動念》第三章·撥無二諦惡取空**"),
    ],
}

# ── 語料口岸（乙閘）──
def _plain(s):
    return "".join(_tk.FOLD.get(c, c) for c in re.sub(r"[^\u4e00-\u9fff]", "", s))


CORPUS = _plain(_tk.VINAYA)
for _v in _tk.OTHER.values():
    CORPUS += _plain(_v)


def verbatim_ok(q):
    for part in re.split(r"…+|⋯+", q):
        p = _plain(part)
        if len(p) >= 2 and p not in CORPUS:
            return False
    return True


def cn(n):
    return "一二三四五六七八九十"[n - 1] if 1 <= n <= 10 else str(n)


def apx_line(dst):
    """凡例第七節之附錄目錄由 ASSETS 自算（不兩抄）。"""
    ts = [h.lstrip("#").strip() for d, t, _, _, h, _ in ASSETS if d == dst and t.startswith("附錄")]
    body = "；".join(re.sub(r"^附錄([一二三四])　", r"\1：", x) for x in ts)
    return ("%d. **附錄收編**：今冊附錄收編%s篇（%s）。其餘歷代修訂日誌、款級索引與自動化測試報告，"
            "轉存內部開發檔案，不佔讀者頁面。" % (2, cn(len(ts)), body))


def cut(a, b):
    return SRC.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")[a - 1:b]


def shift(line):
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not m:
        return line
    return "#" * APX_LV.get(len(m.group(1)), 6) + " " + m.group(2)


def keep_sections(seg, keep, dst, tag):
    """凡例按節取捨：自『### N、』起，至下個『### 』止；首節之前（題與引子）一律留。"""
    out, on = [], True
    for l in seg:
        m = re.match(r"^###\s*([一二三四五六七])、", l)
        if m:
            on = m.group(1) in keep
        if on:
            out.append(l)
    drop = [x for x in ("一", "二", "三", "四", "五", "六", "七") if x not in keep]
    if drop:
        print(f"    {tag}・除節 {drop}")
    return out


def demote(seg, dst, tag):
    """乙閘：語料無形之『「…」』降為『『…』』；含嵌套者列紅不動。"""
    n = red = 0
    for k, l in enumerate(seg):
        if l.strip().startswith("```"):
            continue
        for q in re.findall(r"「([^」]{4,})」", l):
            if verbatim_ok(q):
                continue
            n += 1
            if "『" in q or "』" in q:
                red += 1
                print(f"    ！嵌套未降 L{k + 1}「{q[:30]}」")
                continue
            seg[k] = seg[k].replace("「" + q + "」", "『" + q + "』", 1)
    if n:
        print(f"    {tag}・逐字降格 {n} 枚（嵌套未降 {red}）")
    return seg


HIT = {F1: set(), F2: set()}


def apply_pointers(seg, dst, tag):
    for old, new in POINTER[dst]:
        hits = [(k, seg[k]) for k in range(len(seg)) if old in seg[k]]
        if not hits:
            continue
        if len(hits) > 1:
            print(f"    ！{tag}・錨非唯一 {len(hits)}：{old[:26]}")
            continue
        seg[hits[0][0]] = seg[hits[0][0]].replace(old, new)
        HIT[dst].add(old)
    return seg


def rewrite(seg, dst, tag):
    """整行改寫與插入（前錨唯一者方動，命中非一即報）。"""
    for pre, newline in REWRITE.get(dst, []):
        hits = [k for k, l in enumerate(seg) if l.startswith(pre)]
        if not hits:
            continue
        if len(hits) > 1:
            print(f"    ！{tag}・改寫前錨歧義 {len(hits)}：{pre[:22]}")
            continue
        seg[hits[0]] = newline
    for head, lines in INSERT.get(dst, []):
        hits = [k for k, l in enumerate(seg) if l.strip() == head]
        if len(hits) > 1:
            print(f"    ！{tag}・插入錨歧義 {len(hits)}：{head[:22]}")
            continue
        if not hits:
            continue                              # 此段無其題，插入之事歸他段，非病
        seg[hits[0] + 1:hits[0] + 1] = lines
        print(f"    {tag}・插節 1 行（{head[:16]}）")
    return seg


def selfwords(seg, dst, tag):
    for o, nw in SELF.get((dst, tag), []):
        seg = [l.replace(o, nw) for l in seg]
    return seg


def build(dst, tag, a, b, new_head):
    seg = cut(a, b)
    if seg and re.match(r"^#{1,6}\s", seg[-1]):
        raise SystemExit(f"收邊之破：{tag}・迄行 L{b} 尚為標題（{seg[-1].strip()[:28]}）——行域多吃一行")
    rest = [shift(x) for x in seg[1:]]
    # 新題之下須有空行：本管線啟 blank_before_header，題前無空行即不成其為題（字面出之）
    if rest and rest[0].strip() and not rest[0].startswith("#"):
        rest = [""] + rest
    seg = [new_head] + ([""] if rest and rest[0].startswith("#") else []) + rest
    seg = [l for l in seg if "《四分律：起心動念心智分析框架》" not in l]
    if tag.startswith("卷首"):
        seg = keep_sections(seg, APX_SECTIONS[dst], dst, tag)
        for pat, why in CUT_LINE.get(dst, []):
            seg = [l for l in seg if not l.startswith(pat)]
            print(f"    {tag}・除段（{why}）")
        seg = [apx_line(dst) if l.startswith("2. **附錄精簡收編**") else l for l in seg]
    seg = rewrite(seg, dst, tag)
    seg = selfwords(seg, dst, tag)
    seg = apply_pointers(seg, dst, tag)
    seg = demote(seg, dst, tag)
    return seg


def toc_block(dst, mine):
    ts = [x[3] for x in mine]
    if dst == F1:
        head = ["* **【附錄】**"]
        for h in ts:
            head.append("  * **" + re.sub(r"^附錄([一二三四])　", r"附錄\1・", h.lstrip("#").strip()) + "**")
        return head
    head = ["***", "", "**【今冊附錄之目】**", ""]
    for h in ts:
        head.append("* **" + re.sub(r"^附錄([一二三四])　", r"附錄\1・", h.lstrip("#").strip()) + "**")
    return head


def main():
    write = "--write" in sys.argv
    print("語料口岸：漢字 %d" % len(CORPUS))
    plan = {F1: [], F2: []}
    for dst, tag, a, b, new_head, anchor in ASSETS:
        seg = build(dst, tag, a, b, new_head)
        plan[dst].append((tag, a, b, new_head, seg, anchor))
        print(f"■ {dst[:4]}・{tag:<12} ver39 L{a}-{b} → {len(seg)} 行・{new_head[:34]}")
    for dst in (F1, F2):
        n = sum(len(x[4]) for x in plan[dst])
        print(f"— {dst[:4]}・迎回 {len(plan[dst])} 件／{n} 行")
        dead = [o for o, _ in POINTER[dst] if o not in HIT[dst]]
        print(f"  指針歸位 {len(HIT[dst])}/{len(POINTER[dst])}・未命中（死錨，須查表）：{len(dead)}")
        for d in dead:
            print(f"      · {d[:44]}")
    if not write:
        print("\n（試跑：未落盤）")
        return
    for dst in (F1, F2):
        p = ROOT / dst
        raw = p.read_bytes()
        BAK.mkdir(parents=True, exist_ok=True)
        (BAK / (dst + ".pre_reflow")).write_bytes(raw)
        L = p.read_bytes().decode("utf-8").split("\r\n")
        mine = [x for x in plan[dst] if x[0].startswith("附錄")]
        head = [x for x in plan[dst] if x[0].startswith("卷首")]
        for tag, _, _, _, seg, anchor in head:
            k = next((i for i, l in enumerate(L) if l.strip().startswith(anchor)), None)
            if k is None:
                raise SystemExit(f"插錨求不得：{dst}・{anchor}")
            L = L[:k] + seg + ["", "***", ""] + L[k:]
        toc = toc_block(dst, mine)
        if dst == F1:
            k = next(i for i, l in enumerate(L) if l.startswith("# 第一篇：天平"))
            L = L[:k] + toc + ["", "---", ""] + L[k:]
            for i, l in enumerate(L):
                if l.startswith("## 【全書標準總目錄】"):
                    L[i] = "## 【全書標準總目錄】（四篇十二章・附錄四篇）"
                if l.strip() == "* 生命之樹生態全景與心智顯微鏡導航":
                    L.insert(i + 1, "* 出版凡例與引文承諾")
        else:
            k = next(i for i, l in enumerate(L) if l.strip() == "```" and i > 70)
            L = L[:k + 1] + [""] + toc + L[k + 1:]
            for i, l in enumerate(L[:200]):
                if l.startswith("## 【全書五篇二十章結構全貌圖】"):
                    L[i] = "## 【全書五篇二十章結構全貌圖與附錄】"
        add = []
        for tag, _, _, _, seg, _ in mine:
            add += ["", "***", ""] + seg
        L = L + add
        data = "\r\n".join(L).encode("utf-8")
        p.write_bytes(data)
        print(f"  ● {dst[:4]}・{len(raw.splitlines())} → {len(L)} 行・SHA "
              f"{hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")


main()
