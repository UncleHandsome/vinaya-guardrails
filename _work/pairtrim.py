# -*- coding: utf-8 -*-
"""去匠氣·第二輪（作者親裁 2026-10-26：『去蕪存菁・化繁為簡——褪企管顧問教材與現代法院公文之匠氣』）。

六刀（依作者所列，並附實測之判）：
  刀一・寫作鷹架：F2 卷首【修辭範式與三大法政寫作紀律】（13 行・299 字）整塊削。
        實測：其所禁之『作者無意立某制』『讀者切勿混淆』兩語，全書唯此塊自引一見——削之無殘。
  刀二・商管與科技名相：F2 卷首【四大決策群體實務切入動線】（22 行・582 字）整塊削；
        特定軟體名（Zoom/Teams/Line/LINE/微信/WhatsApp/Slack/臉書/YouTube）與 AI/深偽/演算法 俱抽象化；
        職場語彙（打卡・考勤）歸作務語。
        ⚠ 第四篇之『三道防線・雙院・董事會・稽核・合規』（實測 98 見・64 行）乃骨架而非詞藻，
          連根去則第十三章全空——此屬結構區，另候裁，本刀不動。
  刀三・官僚公文：第二十章 第一節 53 行勾選表・第二節 37 行署押表——圍欄整削，其規程與法意改『綱要』之語（護C）。
  刀四・經院死角：第九章第五節『行治期間突發自然變根』整塊削＋導言殘跡除。
        實測：報告云『第十章第五節・數千字』——章次誤置一（實第九章），字數誇大一層（實 843 字）。
  刀五・重複叮嚀：F1 第四章第一節『心智顯微鏡之法架警示』整塊削（與卷首【入林與觀心警示】四禁全複）。
        實測：兩冊警示語共 48 行，絕大部分嵌在制度內（藉刑洩憤反坐・與狂癡羯磨・黑函開庭之閘・數位獵巫排除標準），
        削之即傷法相；故唯削『獨立成節之複述』一枚，餘留——報曰『半真』。
  刀六・章末留白之節制：只留篇末・大案結案・書末。
        F2 留 6（4・8・12・16・18・20 章）削 13；F1 留 3（3・6・10 章）削 8（連其『第N節 章末指針與林下留白』之節殼）。
        ⚠ 此與外路第五・六報『呼吸口不足』之議正相反：作者以『套路感』為憂，今從其裁。

護六道：唯一錨・不跨界・簡形閘（含全冊順掃）・擇留須自對合（實留之章集合於名單才落盤）・
        兩冊俱校畢全無誤方落盤（一錯俱不動）・削塊必印行數字數並入清冊（備份 .pre_trim）。

用法：python -X utf8 _work/pairtrim.py           # 試跑
      python -X utf8 _work/pairtrim.py --write   # 落盤
"""
import hashlib
import importlib
import pairsimp as PS  # noqa: E402
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
FILES = [F2, F1]
HAN, REV = m._HANMAP, m._HANREV

RE_ANY = m.ANY_HEAD
RE_CHAPTER = re.compile(r"^#{1,6}\s*第([〇一二三四五六七八九十]+)章[　 ]")
RE_PIAN = re.compile(r"^#{1,6}\s*第[一二三四五]篇[:：]")
RE_WRAP = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]章末指針")
RE_BARE = re.compile(r"^#{1,6}\s*【(本章章末|林下留白|章末)")
RE_JIE = re.compile(r"^#{1,6}\s*第([〇一二三四五六七八九十]+)節[　 ]")

BLOCK_CUT = [
    (F2, r"^#{1,6}\s*【四大決策群體實務切入動線】", "刀二・卷首動線"),
    (F2, r"^#{1,6}\s*【修辭範式與三大法政寫作紀律】", "刀一・寫作鷹架"),
    (F2, r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]行治期間突發自然變根", "刀四・變根之節"),
    (F1, r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]心智顯微鏡之法架警示", "刀五・複述之節"),
]
# 第二十章之收束乃其『出堂洗心』與『法架自捨』兩節本身，不另掛章末指針——故名單止於第十八章。
KEEP_BREATH = {F2: {4, 8, 12, 16, 18}, F1: {3, 6, 10}}
# 刀三・表體換骨：公文之圍欄整削，其『四階十六項問句』與『四署心證』改以綱要提撕呈現（護C）。
FENCE_REPL = [
    (F2, r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]僧團執事公堂審計表", [
        "**第一階・前置管轄與界之閥**（前階不通，公堂不開）",
        "* **其一・重罪之檢**：事涉性侵、重傷、巨額侵占之類，不可作內部之私了——當擯者先擯，當白眾者先白，不令戒法替世間遮掩罪惡。",
        "* **其二・結界清淨**：界內合格大僧是否全員通知？有無忘解小界、界標重疊？缺一人通知或界不清淨，羯磨自始無效。",
        "* **其三・足數之檢**：合四人、五人、十人、二十人之階梯否？有無非僧充數？人數不足或非法足數，羯磨自始不成立。",
        "* **其四・與欲如法**：未能親到者有無如法受欲？有無觸犯三大禁區？禁區之內以代票成事者，決議自始無效，壇上須全員親臨。",
        "* **其五・親教迴避**：審理長老無愛、恚、怖、癡；直系師徒有利益衝突者強制迴避。應迴避而未迴避，羯磨無效，移轉客僧專案。",
        "",
        "**第二階・責任能力與事實查驗之閥**（責任阻卻，當下出院）",
        "* **其六・強迫之檢**：行為人是否出於物理強制、身體受暴、天災不可抗力？受暴非自願者，責任前端阻卻，無條件宣告無犯。",
        "* **其七・心疾之檢**：行為人是否神智狂亂？有無良醫診斷？發病期行『與狂癡羯磨』停止追問；病癒以白四作『不癡毘尼』。",
        "* **其八・境想之檢**：如實想、差誤想、生疑？不知有戒之免責唯限遮戒。客體差誤想阻卻故意；自知而故作者量刑跳階。",
        "* **其九・離處之檢**：盜案是否已達實質離處？數額是否滿五錢而涉重大損害？未離處或未滿者阻卻極刑，按未遂方便結偷蘭遮。",
        "",
        "**第三階・動機性質與特殊分流之閥**（定性定量，分流處置）",
        "* **其十・性遮之檢**：所犯屬殺盜淫妄之自性罪，還是教制之遮罪？性戒守死正理五不可逆底線；遮戒審其實質正當之避險。",
        "* **十一・使作之檢**：教唆、代理、轉包之責如何切分？撤回是否實達？教人過五錢而二俱至五錢者俱波羅夷；偏差降階；撤回者降階。",
        "* **十二・開許之檢**：急難病苦之開許，難平事過是否如期回撤？如期回撤者宣告清淨；逾期不撤者轉作犯追責。",
        "* **十三・第三值之檢**：動機純善而手段易啟世間譏嫌者，啟動教誡防護——當庭宣告『無犯，不應作如是事』，不入懲戒之檔，存檔備查。",
        "",
        "**第四階・心證宣告與終局結案之閥**（消磁歸零，關係無痕）",
        "* **十四・自白之檢**：自白出於自由意志否？有無疲勞逼問與脅迫？有無補強之事相？逼供之自白自始無證；有自白而無事相不罰，缺自白而疑罪從無。",
        "* **十五・四署之檢**：卷首心證之宣告，是否四人各具名而親筆？以器物模型代判心證者，程序不備，不得結案。",
        "* **十六・消磁之檢**：裁決當庭宣讀；出堂洗心三事落實；案卷封存。再翻舊帳者結波逸提第六十六條；法庭淨空，全僧回歸無事。",
    ]),
    (F2, r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]卷宗首頁『自然人心證自律宣告", [
        "**其自然人心證自律宣告之文曰**（其辭常附卷宗之首，缺署者程序不備）：",
        "* **一、** 本案卷內所附影音、金流、通訊之紀錄，僅作輔助客觀時地與物理軌跡之參考存證；",
        "* **二、** 關於當事人行為時之境想作意、動機染淨、受樂有無、是否真心慚愧，以及處分量刑之判定，"
        "百分之百由親臨法庭、當面聽訟、面對面質證之執事與長老，本於良知與律相獨立作成；",
        "* **三、** 本僧團自始未曾、亦絕對不允許以自動監控、算計模型或評分數據，替代審理者之主觀心證；",
        "* **四、** 本案恪守自言治與正當程序，無刑訊逼供，無道德勒索，無派系偏私。因果歷歷，誓承其責。",
        "",
        "**四署之名與職**：說白羯磨師（程序宣讀者）・主審執事僧（事實調查者）・評議長老（中立裁判者）・大眾見證僧（和合監察者）。",
    ]),
]

FIX = [
    # 刀二・特定軟體名
    (F2, False, "當代數位科技普及，視訊通訊軟體（Zoom、Teams等）已成為非營利組織與跨國機構開會之常態。",
     "今時遠距傳訊之器既普，異地會議已為非營利組織與跨國機構之常態。"),
    (F2, False, "僧人在通訊軟體（Line、微信、WhatsApp）或社交媒體（臉書、YouTube）上發表言論",
     "僧人在遠距傳訊或公開影音之場域發表言論"),
    (F2, False, "通訊軟體（LINE、微信、WhatsApp）截圖、語音留言、監視影像常被作為舉罪之憑。然而，在數位科技高度發達的今天，偽造一張截圖或合成一段錄音只需數秒。",
     "通訊群組之截圖、語音留言、監視影像常被作為舉罪之憑。然而，偽造一張截圖或合成一段錄音，今只須彈指之間。"),
    (F2, False, "在數位協作時代，寺院的通訊軟體公務群組（LINE、微信、Slack），早已成為",
     "在數位協作時代，寺院的公務通訊群組，早已成為"),
    (F2, True, "· 官方自媒體帳號（YouTube、臉書、公眾號）", "· 官方自媒體帳號（影音・社群・文告）"),
    # 刀二・AI／深偽／演算法
    (F2, False, "#### 三、生成式偽造（Deepfake）與音聲複製之抗辯審查", "#### 三、偽造影音與模仿音聲之抗辯審查"),
    (F2, False, "在 AI 深偽技術普及的環境下，被指控人若對呈堂之錄音或影像提出「生成式偽造抗辯」：",
     "世間既有利器能合成音容，被指控人遂可對呈堂之錄音或影像提出「此乃偽造」之抗辯："),
    (F2, False, "* 被告只要指出具體技術疑點（如音頻頻譜斷裂、嘴型與聲音不同步、邊緣像素失真），即生抗辯釋明效果；",
     "* 被告但能指出具體疑點（如音聲與口型不合、前後斷裂、來歷中絕），即生抗辯釋明之效；"),
    (F2, False, "提出方若無法提供伺服器原始存證日誌與未中斷之數位證據鏈", "提出方若無原始存證與不中斷之證據鏈"),
    (F2, False, "**絕對禁止單憑單一數位影音定案**", "**絕對禁止單憑一影音定案**"),
    (F2, False, "> 科技再發達，機器只能記錄客觀數據，**神聖心證的形成永遠不能外包給演算法**。",
     "> 器巧雖盛，器物只記客觀數據，**神聖心證之形成，永遠不可外包與任何人、任何物**。"),
    # 刀三・表體既削，規程與題面須從『公文表格』改歸『綱要』
    (F2, False, "> **【審計表使用規程】**", "> **【檢綱使用規程】**"),
    (F2, False, "> 本表為僧團召開正式審判羯磨時之**「四階十六項一票否決卡尺」**。由說白羯磨師與監察長老於開庭全程逐項勾稽。",
     "> 此綱為僧團召開正式審判羯磨時之**「四階十六項一票否決卡尺」**。說白羯磨師與監察長老於開庭全程逐項對勘，一階不通則公堂不開。"),
    (F2, False, "### 第一節　僧團執事公堂審計表（開庭軌道甲·標準作業表）",
     "### 第一節　開庭四階十六項檢綱（軌道甲·公堂對勘之目）"),
    (F2, False, "### 第二節　卷宗首頁『自然人心證自律宣告』（四署制度正式格式）",
     "### 第二節　自然人心證自律宣告（四署之制）"),
    (F2, False, "> **【四署制度法意】**", "> **【四署法意】**"),
    (F2, False, "凡涉及心識動機染淨之審查，卷宗首頁必須由四位法定職事親筆簽字宣告，承擔因果與公法責任。",
     "凡涉及心識動機染淨之審查，卷宗首頁須由四位執事親筆宣告，各依其職承擔因果與法責。"),
    # 刀四・殘跡
    (F2, False, "、還俗再受戒之前罪續治算法，以及行治中突發自然變根的管轄接力技術。",
     "，以及還俗再受戒之前罪續治算法。"),
    # 刀二・職場語彙（『考勤表』之句在第十五章章末，已隨留白同削，不另立錨）
    (F2, False, "受打卡考勤之約束", "受時刻約束"),
    # 刀二・企管黑話（最刺眼者）
    (F2, False, "賦能型治理（Enabling Governance）；以制度設計代替道德譴責。", "以制度之設計，代道德之譴責。"),
    (F2, False, "〔專題 08〕賦能設計代懲", "〔專題 08〕設防代懲"),
]


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def han(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def block_end(lines, i, lv):
    j, n = i + 1, len(lines)
    while j < n:
        s = lines[j].strip()
        if RE_ANY.match(s) and m.level(s) <= lv:
            break
        j += 1
    return j


def chapter_of(lines, i):
    for k in range(i, -1, -1):
        mm = RE_CHAPTER.match(lines[k].strip())
        if mm:
            return REV.get(mm.group(1), 0), k
    return 0, None


def trim_tail(lines, j):
    while j > 1 and (not lines[j - 1].strip() or lines[j - 1].strip() in ("---", "***")):
        j -= 1
    return j


def plan(f, lines):
    keep = [True] * len(lines)
    rows, errs, notes = [], [], []
    # 刀一・二・四・五・整塊削
    for fn, pat, tag in BLOCK_CUT:
        if fn != f:
            continue
        idx = [i for i, l in enumerate(lines) if re.compile(pat).match(l.strip())]
        if len(idx) != 1:
            errs.append(f"塊錨不唯一（{len(idx)}）：{pat[:34]}")
            continue
        i = idx[0]
        j = block_end(lines, i, m.level(lines[i].strip()))
        j = trim_tail(lines, j)
        for k in range(i, j):
            keep[k] = False
        rows.append((tag, i + 1, j, lines[i].strip()[:38], j - i, han("\n".join(lines[i:j]))))

    # 刀三・表體換骨：圍欄整削，其問句以綱要代之（護C：問句不可隨表同去）
    for fn, pat, newlines in FENCE_REPL:
        if fn != f:
            continue
        idx = [i for i, l in enumerate(lines) if re.compile(pat).match(l.strip())]
        if len(idx) != 1:
            errs.append(f"表節錨不唯一（{len(idx)}）：{pat[:34]}")
            continue
        i = idx[0]
        j = block_end(lines, i, 3)
        a = None
        for k in range(i, j):
            if lines[k].strip().startswith("```"):
                a = k
                break
        if a is None:
            errs.append(f"表節之內未見圍欄：L{i + 1}")
            continue
        b = a + 1
        while b < j and not lines[b].strip().startswith("```"):
            b += 1
        if not keep[a]:
            errs.append(f"此圍欄已屬他刀之塊：L{a + 1}")
            continue
        n_ = list(newlines)      # 空行須留：markdown 之段落界全在空行，削之則階與階黏成一塊
        old_block = lines[a:b + 1]
        keep[a] = True
        lines[a] = "\n".join(n_)
        for k in range(a + 1, b + 1):
            keep[k] = False
        lines[b] = ""          # 閉柵若留在檔中，fence_mask 會誤判其後一切皆在圍欄內（刀後之錨盡落空）
        rows.append(("刀三・表換為綱", a + 1, b + 1,
                     "圍欄 %d 行 → 綱要 %d 行" % (b + 1 - a, len(n_)),
                     b + 1 - a - len(n_), han("\n".join(old_block)) - han("\n".join(n_))))
        notes.append(f"L{a + 1}　刀三・綱要代表：原表 {b + 1 - a} 行 → 綱要 {len(n_)} 行")

    # 刀六・章末擇留（節殼＋留白併為一軸）
    kept, cut = [], []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not keep[i] or not (RE_WRAP.match(s) or RE_BARE.match(s)):
            i += 1
            continue
        num, _ = chapter_of(lines, i)
        a = i
        j = block_end(lines, a, m.level(s))
        if RE_WRAP.match(s):
            sub = [k for k in range(a + 1, min(j + 1, len(lines))) if RE_BARE.match(lines[k].strip())]
            # 節殼之 block_end 恰止於同級留白，故須再接其塊
            if sub:
                k0 = sub[0]
                j = max(j, block_end(lines, k0, m.level(lines[k0].strip())))
        else:
            for k in range(a - 1, max(a - 6, -1), -1):
                if RE_WRAP.match(lines[k].strip()):
                    a = k
                    j = max(j, block_end(lines, k, m.level(lines[k].strip())))
                    break
        j = trim_tail(lines, j)
        if num in KEEP_BREATH[f]:
            kept.append(num)
            i = j
            continue
        for k in range(a, j):
            keep[k] = False
        cut.append((a + 1, j, lines[a].strip()[:38], j - a, han("\n".join(lines[a:j])), num))
        i = j
    for a1, b1, t1, n1, h1, num in cut:
        rows.append(("刀六・章末留白", a1, b1, t1, n1, h1))
    if sorted(kept) != sorted(KEEP_BREATH[f]):
        errs.append(f"擇留不對合：實留 {sorted(kept)} ≠ 名單 {sorted(KEEP_BREATH[f])}")
    return keep, rows, kept, sorted(KEEP_BREATH[f]), errs, notes


def relabel(f, lines, keep):
    """刀後之『第N節』補號（須刀前本為連續 1..N，方補；父＝所屬之章）。"""
    out = []
    rx = re.compile(r"^(#+)\s*第([〇一二三四五六七八九十]+)(節[　 ].*)$")
    chs = [k for k in range(len(lines)) if RE_CHAPTER.match(lines[k].strip()) and keep[k]]
    for pos, par in enumerate(chs):
        pend = chs[pos + 1] if pos + 1 < len(chs) else len(lines)
        items = [k for k in range(par + 1, pend) if rx.match(lines[k].strip())]
        if not items:
            continue
        nums = [REV.get(rx.match(lines[k].strip()).group(2), 0) for k in items]
        if nums != list(range(1, len(nums) + 1)):
            continue                       # 刀前已亂：非本刀之責
        alive = [k for k in items if keep[k]]
        if len(alive) == len(items):
            continue                       # 未砍及此章之節
        for t, k in enumerate(alive, 1):
            mm = rx.match(lines[k].strip())
            if REV.get(mm.group(2), 0) == t:
                continue
            new = f"{mm.group(1)} 第{HAN[t]}{mm.group(3)}"
            out.append((k + 1, lines[k].strip()[:36], new[:36]))
            lines[k] = new
    return out


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - set("几")
    errs, ledger, plans = [], [], []
    for f in FILES:
        raw = (ROOT / f).read_bytes()
        src = raw.decode("utf-8").split("\r\n")
        lines = list(src)
        keep, rows, kept, exp, e1, notes = plan(f, lines)
        errs += [f"{f[:8]}・{x}" for x in e1]
        ledger += [f"{f}\t{nn}" for nn in notes]
        # 字面之刀（唯一錨・欄內外分治・簡形閘）
        fence = m.fence_mask(lines)
        for fn, inf_, old, new in FIX:
            if fn != f:
                continue
            for c in set(new) & SIMPLE:
                errs.append(f"{f[:8]}・新文簡形：{c}｜{new[:20]}")
            hits = [i for i, l in enumerate(lines) if old in l and keep[i] and fence[i] == inf_]
            if len(hits) != 1:
                errs.append(f"{f[:8]}・錨不唯一（命中 {len(hits)}・欄{'內' if inf_ else '外'}）：{old[:30]}")
                continue
            i = hits[0]
            at = lines[i].index(old)
            head, tail = lines[i][:at], lines[i][at + len(old):]
            if inf_:
                k = len(tail) - len(tail.lstrip(" "))
                tail = " " * max(0, k + dwidth(old) - dwidth(new)) + tail.lstrip(" ")
            o = lines[i]
            lines[i] = head + new + tail
            ledger.append(f"{f}\tL{i + 1}\t字面\t{o.strip()[:42]} → {lines[i].strip()[:42]}")
        # 補號
        for a, o, w in relabel(f, lines, keep):
            ledger.append(f"{f}\tL{a}\t補號\t{o} → {w}")
            print(f"  補號 L{a}: {o} → {w}")
        flat = []
        for k, l in enumerate(lines):
            if keep[k]:
                flat.extend(l.split("\n"))
        simp = [(i + 1, PS.hits(l))
                for i, l in enumerate(flat) if PS.flag(l)]
        if simp:
            errs.append(f"{f[:8]}・刀後簡形 {len(simp)} 行：{simp[:3]}")
        print("=" * 74)
        print("■", f)
        for tag, a, b, t, n, h in sorted(rows):
            print(f"  {tag}｜L{a}〜{b - 1}・{n:3d} 行・{h:5,} 字｜{t}")
        print(f"  小計：削 {sum(r[4] for r in rows)} 行・{sum(r[5] for r in rows):,} 字"
              f"｜章末留白 留 {kept}（名單 {exp}）・削 {len([r for r in rows if r[0].startswith('刀六')])} 枚")
        print(f"  行數 {len(src)} → {len(flat)}・漢字 {han(chr(10).join(src)):,} → {han(chr(10).join(flat)):,}")
        plans.append((f, raw, flat))
    print("=" * 74)
    if errs:
        for e in errs:
            print("  ✗", e)
        print("★有誤 → 兩冊俱不落盤")
        return
    (ROOT / "_work" / "pairtrim_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"刀口清冊 {len(ledger)} 行 → _work/pairtrim_cuts.txt")
    if not write:
        print("（試跑：未落盤）")
        return
    for f, raw, flat in plans:
        bak = ROOT / "_archive" / "備份" / "AI清理前" / (f + ".pre_trim")
        bak.write_bytes(raw)
        data = "\r\n".join(flat).encode("utf-8")
        (ROOT / f).write_bytes(data)
        print(f"  落盤 {f[:12]}…：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}"
              f"・{len(data)} B・備份 {bak.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
