# -*- coding: utf-8 -*-
"""第 74 輪・欠帳之收束（自裁定奪，候裁諸案一次清）。
甲・辛丁 18 段降式樣（判別取共器 `lane.pin_kind`，與尺同法源）；
乙・破窗表增第六行（說過人法 ➔ 第四重大妄語，條號據附錄：比單提第8條・落點第八章案例一）；
丙・第十八章補『淨人（執事人）』之指針（第七章案例十二已解剖其法，此只引路，不新立律據）；
丁・第十七章補宋世『會正／資持』之諍一句（明標『據通說，本地無從覆核』）；
戊・第十八章立『兩部戒本篇聚對照表』（ arithmetic 自證：六篇全同，差額二十三盡在外圍）；
己・第十八章補三對映（事前承諾／雙系統／驗證成本，俱標『本書之對映，非引今人原話』）。
已裁而不动筆者（記於記憶）：兩章之題仍從作者親筆『（上）／（下）』；案外十二條保留登記；
隨方毘尼・元照逐字・弘一『自居沙彌』・五義分通之完整五目＝不採（本地無從覆核，掛逐字即違凡例）。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402
import hlpara  # noqa: E402
import lane  # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []
apx0 = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
CF = lane.corpus_flat()

# ── 甲・降式樣（一匹配一動刀，不由整行 sub，免誤傷同行之真逐字）───────────
EDITS = []
for i in range(apx0):
    for m in lane.PIN.finditer(L[i]):
        q0 = (m.group(1) or m.group(2) or u"").strip()
        lit, ping = lane.pin_kind(q0, CF)
        if lit or not ping:
            continue                      # 含律句者留硬檢・全中語料者本不必動
        EDITS.append((i, m.start(), m.end(), q0, ping[0]))
for i, a, b, q, frag in sorted(EDITS, key=lambda x: (x[0], -x[1])):
    inner = L[i][a:b]
    # 匹配串本身已含「」，只剝粗體星號；若再包一層「」即成「「…」」（74c 收之，punctchk 今有目）
    L[i] = L[i][:a] + inner.replace(u"**", u"") + L[i][b:]
print(u"甲・降式樣：%d 處（原 18 段之評語，一處或含多段）" % len(EDITS))
for i, a, b, q, frag in EDITS:
    print(u"    △ L%-5d|%s" % (i + 1, frag[:44]))

# ── 乙～己・內容諸刀 ───────────────────────────────────────────────
INS = []

ROW6 = (u"| **說過人法戒**<br>（比丘九十單提第8條；向未受大戒人自稱證得上人法） "
        u"| **在社群媒體包裝『開悟善知識』之人設、虛構證量以收割供養**<br>（以神聖外殼經營流量與信徒） "
        u"| 自我神化之後，良知對謊言脫敏；說一次大話，便須編十次小話來圓。 "
        u"| 巨額精神詐騙、破人慧命（滑向第四重大妄語戒與根本盜戒）；信眾退轉，法脈受損。 |")
ANCH6 = u"| **不看棄便戒**<br>（比丘尼單提第78條；倒穢物時必須先探頭查看） |"
INS.append((u"乙・破窗表第六行", ANCH6, 1, [ROW6]))

JINGREN = (u"或人問：現代之世寸步須錢，『手不捉金銀』如何行得通？答曰：律中本有代理人之制——淨人（執事人）。"
           u"本書第七章案例十二已解剖其法：犯者其物當眾捨與僧，僧不之留，推與淨人執掌，須衣・鉢・藥・針筒則向彼取足。"
           u"森林派所以能在貨幣社會中不摸錢而跨國運轉，靠的正是這套兩千年前的信託機制接上今世的帳務與居士大會。"
           u"**不捉錢的是人，管錢的是制**——此即『拿掉作案條件』之防錯工程從個人放大到組織的一步。")
ANCH_J = u"森林派的現代傳奇向全人類證實"
INS.append((u"丙・淨人之指針", ANCH_J, 2, [u"", JINGREN]))

HUIZHENG = (u"（且不止外侮：依律史通說，元照之《資持記》另有的一家敵手——霅溪允堪律師之《會正記》。"
            u"一家主依字面判《四分》終屬小乘、戒體當從非色非心之說；一家主道宣分通大乘・圓教心法之判。"
            u"宋世律門『會正／資持』之諍即此（此據通說，本地無從覆核）。"
            u"本書不取其是非，但記其實在——護欄之學，連自家也會為『牆該畫在哪裡』爭上一百年。）")
ANCH_H = u"元照律師著作了洋洋灑灑數十萬言的《四分律行事鈔資持記》"
INS.append((u"丁・會正資持之諍", ANCH_H, 2, [u"", HUIZHENG]))

TABLE = [u"兩部戒本之對照，列為一目（南傳之數出彼方通行本，本書未校原本）：",
         u"",
         u"| 篇聚 | 南傳巴利律（比丘） | 漢傳《四分律》（比丘） |",
         u"| :--- | :--- | :--- |",
         u"| 四波羅夷 | 4 | 4 |",
         u"| 十三僧殘 | 13 | 13 |",
         u"| 二不定法 | 2 | 2 |",
         u"| 三十捨墮 | 30 | 30 |",
         u"| 九十單提（波逸提） | 92 | 90 |",
         u"| 四提舍尼（悔過） | 4 | 4 |",
         u"| 眾學法 | 75 | 100 |",
         u"| 七滅諍法 | 7 | 7 |",
         u"| **合計** | **227** | **250** |",
         u"",
         u"看得仔細：**四重、僧殘、二不定、三十捨墮、四提舍尼、七滅諍六篇，兩部全同**；"
         u"二百五十與二百二十七之間二十三條的差額，全在最外圍的兩層——"
         u"眾學法多二十五條（敬塔・飲食・威儀之細行），單提少二條。"
         u"**要塞的王城與宮牆萬古不改，動的只是護城河的寬窄。**"]
ANCH_T = u"差異集中在最外圍的兩層：單提一篇"
INS.append((u"戊・篇聚對照表", ANCH_T, 2, TABLE))

SAN = (u"另有三義，與本書之旨最親，隨文標出，以免讀者誤會戒律只是一套『習慣養成術』："
       u"其一，**事前承諾（precommitment）**——人於未來遠大利與當下口腹之欲之間，向來是後者說服力更強"
       u"（今人謂之雙曲貼現），故唯一解法是在清醒之時簽下一份不可撤銷之約；"
       u"比丘受大戒之當眾發誓、納受戒體、歸入僧團法庭，正是人類史上最嚴肅的一份終身事前承諾。"
       u"其二，**雙系統之辨**——自動化者省力而易墮，深思者省力不得且易疲；"
       u"百眾學法之於行、住、坐、臥、食，是一項把覺知從『要想』改寫為『不必想』的工程："
       u"持戒純熟的人不是忍得住，是不必忍。"
       u"其三，**驗證成本**——律藏何以死磕『幾寸、幾夜、幾語、有光無光、手碰沒碰』這些物理尺度？"
       u"因為心念不可查而門閾可查；邊界劃在物理層，僧團的司法才付得起查證的代價。"
       u"（此三義皆本書之對映，非引今人原話，亦不假其名以自重。）")
ANCH_S = u"把三層混為一談，正是現代讀者最容易犯的誤解"
INS.append((u"己・三對映", ANCH_S, 2, [u"", SAN]))

touched = []
for tag, anchor, after, block in INS:
    hit = [i for i, s in enumerate(L[:apx0]) if anchor in s]
    if len(hit) != 1:
        errs.append(u"%s｜锚命中 %d 次" % (tag, len(hit)))
        continue
    i = hit[0]
    L[i + 1 + (after - 1):i + 1 + (after - 1)] = block
    touched.append(i)
    n_漢 = max(hlpara.cn(x) for x in block if x)
    print(u"  ✓ %-16s 插於 L%-5d 後（+%d 行｜新段最長 %d 漢字%s）"
          % (tag, i + 1, len(block), n_漢, u"｜⚠逾 320" if n_漢 > 320 else u""))

# ── 自證：降式樣之後，評語之軟報須歸零；逐字之硬閘須仍綠 ───────────────
left = 0
for i in range(apx0):
    for m in lane.PIN.finditer(L[i]):
        lit, ping = lane.pin_kind((m.group(1) or m.group(2) or u"").strip(), CF)
        left += len(ping)
print(u"\n自證：辛丁軟報今餘 %d（須 0）｜律句硬檢餘 %d（須 0）"
      % (left, sum(len(lane.pin_kind((m.group(1) or m.group(2) or u"").strip(), CF)[0])
                    for i in range(apx0) for m in lane.PIN.finditer(L[i]))))
import _simpmap  # noqa: E402
WATCH = [u"\u540e", u"\u516e", u"\u91cc", u"\u636e", u"\u6258", u"\u6c89", u"\u53f0", u"\u9762"]
for c in WATCH:
    rows = [k + 1 for k, s in enumerate(L[:apx0]) if c in s]
    if rows:
        print(u"  盯形 U+%04X 見於 %s（須目驗：后・托・面・里 等乃同形正字，非盡簡）" % (ord(c), rows[:6]))
print(u"本輪新增・觸及各行之 MAP 命中：%s"
      % sorted(set(c for blk in INS for x in blk[3] for c in x if c in _simpmap.MAP)))

print(u"\n行數 %d → %d" % (len(raw.split(u"\r\n")), len(L)))
if errs:
    print(u"✗ 擲不寫：")
    for e in errs:
        print(u"   " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
out = u"\r\n".join(L)
BK = HP.bakpath("74a")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s"
      % (sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
         u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
