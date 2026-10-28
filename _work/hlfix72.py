# -*- coding: utf-8 -*-
"""第 72 輪・收外路報告（第十六・十九・二十章兩輪校閱 16 目）。
判：真病 12・偽病灶 2（十六-1『無文』與十九(二)-1『百萬分之一秒』俱係舊版之說，今檔已治）・候裁 2（引《五分律》隨方毘尼、破窗表增一大妄語行——俱屬新增論述，不作病灶治）。
法源：語料 `_tk.VINAYA`（集法毘尼段・猿猴之形）・附錄 `_work/appendix_jieben.md`（條號→戒文→部別）。
自證：每錨須命中唯一次，否則整擲不寫；圍欄之刀只換等長八字目（欄位起點自算，不靠手打空格），另增一行以容第二部五目。
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
import _tk  # noqa: E402
import hlpara  # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []
nknife = 0

SUBS = [
    (u"十六-3 白四羯磨",
     u"大迦葉隨即升座，進行如法合規的白四羯磨表決，全票通過了這條震古爍今的**「不增不減鐵律」**：",
     u"大迦葉隨即升座，以此宣告與大眾共立制限（律文但云「**時即共立如此制限**」，未記白四羯磨之儀），"
     u"全場默然忍可，遂定這條震古爍今的『不增不減鐵律』："),
    (u"十六(二)-1 溫和派",
     u"應當以波羅夷與僧殘為大戒，從三十捨墮以下，方屬於微細戒，可以捨棄！",
     u"應當以波羅夷、僧殘與二不定法為大戒，從三十捨墮以下，方屬於微細戒，可以捨棄！"),
    (u"十六(二)-1 括注",
     u"（有言除四波羅夷，有言除四波羅夷十三事，乃至除九十事）",
     u"（有言除四波羅夷，有言除四波羅夷十三事，有言並除二不定法，乃至除九十事）"),
    (u"十九-3 百倍電信號", u"以百倍電信號", u"以壓倒性權重"),
    (u"十九(二)-3 如猿捉柳",
     u"佛陀在阿含與律藏中無數次開示：**凡夫的心念，是「念念遷流、如猿捉柳」的。**",
     u"佛陀在阿含中數數警誡：**凡夫的心念，是念念遷流、如獼猴經林、捨一取一的。**（此乃本書據喻意作今語，非逐字）"),
    (u"十九-1 不滑向",
     u"廢棄一切修行與定力（此條不滑向某一根本罪，而是使全線護欄同時失效——小戒既廢，大戒即無外防）",
     u"廢棄一切修行與定力（此條於律中亦掛在根本重戒之外圍——迦留陀夷夜乞、孕婦驚恐墮胎，"
     u"第八章案例九即標其靶於第三重殺戒與第一重婬戒；而小戒既廢，全線護欄同時失效，大戒即無外防）"),
    (u"十九-2 表一", u"| **與女人同室宿戒**<br>（嚴禁男女黑夜共處密室） |",
     u"| **與女人同室宿戒**<br>（比丘九十單提第4條；嚴禁男女黑夜共處密室） |"),
    (u"十九-2 表二", u"| **自手捉持金銀戒**<br>（雙手與貨幣徹底絕緣） |",
     u"| **自手捉持金銀戒**<br>（比丘三十捨墮第18條；雙手與貨幣徹底絕緣） |"),
    (u"十九-2 表三", u"| **與女人說法過五六語戒**<br>（嚴禁藉由崇高理由曖昧長談） |",
     u"| **與女人說法過五六語戒**<br>（比丘九十單提第9條；嚴禁藉由崇高理由曖昧長談） |"),
    (u"十九-2 表四", u"| **非時食戒／不過中食**<br>（過午不食，保持身心輕安） |",
     u"| **非時食戒／不過中食**<br>（比丘九十單提第37條；過午不食，保持身心輕安） |"),
    (u"十九-2 表五", u"| **不看棄便戒**<br>（倒穢物時必須先探頭查看） |",
     u"| **不看棄便戒**<br>（比丘尼單提第78條；倒穢物時必須先探頭查看） |"),
    (u"二十-1 暗室錯配",
     u"【九十單提第4條：與女人同室宿戒】、【第86條：與男子共入暗室戒】。",
     u"【比丘九十單提第4條：與女人同室宿戒】、【比丘尼單提第86條：與男子共入暗室戒】。"),
    (u"二十-2 上限錯配",
     u"【三十捨墮第18條：自手捉持金銀戒】、【第29、30條：服飾價格上限】。",
     u"【比丘三十捨墮第18條：自手捉持金銀戒】、【比丘尼三十捨墮第29、30條：乞重衣與輕衣過限戒（服飾價格上限）】。"),
    (u"二十-3 護欄三", u"【九十單提第9條：說法過五六語戒】", u"【比丘九十單提第9條：說法過五六語戒】"),
    (u"二十-3 護欄四", u"【百眾學法：不大摶食", u"【百眾學法（比丘、比丘尼俱制）：不大摶食"),
    (u"二十(二)-2 捨墮之混",
     u"這就是現代版的「捨墮法」——藉由拉長物理時間差，粉碎消費主義對心智的洗腦。",
     u"此近於律中『十日寬限』之制（長衣過十日不淨施即捨），冷的是衝動，還不是『捨墮法』本身："
     u"捨墮之體在先捨後懺，其物當眾捨與僧，物不捨則罪不除。現代版的捨墮法當別有其一——定期捨出不用的衣物器具。"),
]

for tag, old, new in SUBS:
    idx = [i for i, s in enumerate(L) if old in s]
    if len(idx) != 1:
        errs.append(u"%s｜錨命中 %d 次%s" % (tag, len(idx), u"（%s）" % idx[:3] if idx else u""))
        continue
    i = idx[0]
    L[i] = L[i].replace(old, new, 1)
    nknife += 1
    漢 = hlpara.cn(L[i])
    print(u"  ✓ %-20s L%-5d｜改後此行漢字 %d%s" % (tag, i + 1, 漢,
          u"｜⚠逾 320" if 漢 > 320 else u""))

if u"時即共立如此制限" not in _tk.VINAYA:
    errs.append(u"十六-3 之新逐字『時即共立如此制限』不在語料")

# ── 十六-2：§二 末補【按：律文之序】
NOTE = (u"**按：律文之序，本書不諱。** 卷第五十四之記：阿難自陳佛語在先，大眾各說其次，"
        u"共立制限再次之，大迦葉逐項數阿難之突吉羅（「不問雜碎戒」預焉）又在最後。"
        u"本章先寫審問、後寫眾議，取其理之節次，不記其時之先后。")
ai = [i for i, s in enumerate(L) if s.startswith(u"剛剛失去佛陀的佛教僧伽")]
if len(ai) != 1:
    errs.append(u"十六-2 按語錨命中 %d 次" % len(ai))
else:
    L[ai[0] + 1:ai[0] + 1] = [u"", NOTE]
    nknife += 1
    print(u"  ✓ %-20s 插入 L%-5d（+2 行）｜按語漢字 %d"
          % (u"十六-2 律序之按", ai[0] + 2, hlpara.cn(NOTE)))

# ── 二十(二)-1：全景圖第二部補四波羅夷・十三僧殘（等長換目＋增一行）
IT = [u"三十捨墮斷物欲、", u"九十單提平諍鬥、", u"百眾學法護威儀。"]
NEW = [u"四波羅夷守心臟、", u"十三僧殘築宮牆、", u"三十捨墮斷物欲、"]
pos = []
for t in IT:
    hit = [i for i, s in enumerate(L) if t in s]
    if len(hit) != 1:
        errs.append(u"圖・錨『%s』命中 %d 次%s" % (t, len(hit), u"（%s）" % [x + 1 for x in hit[:4]] if hit else u""))
        pos = None
        break
    pos.append((hit[0], L[hit[0]].index(t)))
if pos:
    c2 = pos[0][1]
    for (i, p), t, nw in zip(pos, IT, NEW):
        assert len(t) == len(nw) == 8, u"圍欄之目須等長（八字）"
        L[i] = L[i][:p] + nw + L[i][p + len(t):]
        print(u"  ✓ 圖・L%-5d col%d『%s』➔『%s』" % (i + 1, c2, t, nw))
        nknife += 1
    li = [i for i, s in enumerate(L) if s.startswith(u" " * (c2 + 20)) and u"二部僧體制立公義。" in s]
    if len(li) != 1:
        errs.append(u"圖・末行之錨命中 %d 次" % len(li))
    else:
        i = li[0]
        p3 = L[i].index(u"二部僧體制立公義。")
        L[i] = u" " * c2 + u"九十單提平諍鬥、" + u" " * (p3 - c2 - 8) + L[i][p3:]
        L[i + 1:i + 1] = [u" " * c2 + u"百眾學法護威儀。"]
        nknife += 2
        print(u"  ✓ 圖・L%-5d 補第二部之單提目，並增一行容眾學目（+1 行）" % (i + 1))

print(u"\n===== 圍欄全段覆印（改後）=====")
k0 = next(i for i, s in enumerate(L) if s.startswith(u"# 第二十章"))
for i in range(k0, len(L)):
    if L[i] == u"```" and i > k0 and u"兩百五十戒" in u"".join(L[i:i + 12]):
        for k in range(i, i + 22):
            print(u"  L%-5d|«%s»" % (k + 1, L[k]))
        break

for kw in (u"如猿捉柳", u"百倍電信號", u"不滑向", u"白四羯磨表決",
           u"【第86條：與男子共入暗室戒】", u"【第29、30條：服飾價格上限】", u"波羅夷與僧殘為大戒"):
    print(u"  殘留『%s』：%d" % (kw, sum(1 for s in L if kw in s)))

print(u"\n共 %d 刀｜行數 %d → %d" % (nknife, len(raw.split(u"\r\n")), len(L)))
if errs:
    print(u"✗ 擲不寫，凡 %d 項：" % len(errs))
    for e in errs:
        print(u"   " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)

out = u"\r\n".join(L)
BK = HP.bakpath("72a")
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
