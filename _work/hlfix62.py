# -*- coding: utf-8 -*-
"""第 62 輪・刀：外路第二十五報之真病三事（地理時空・神經科學精度・法理標記）。
  二.3（P0・真病）同一樁娑伽陀公案，第二章作『菴婆羅村』（本地語料 0 見，乃巴利 Ambatiṭṭha），
      第九章作『支陀國』（語料 2 見・「爾時佛在支陀國…時尊者娑伽陀為佛作供養人」）——
      本書自約案例出漢譯六十卷，此處卻混入巴利系地名。治：第二章一從本律（支陀國・編髮梵志處・
      中路醉臥），並依書中既有之『如實標記』成例（L880・L886），補一行說明兩事連敘之從簡。
  六.6（真病）L6707『百萬分之一秒』——突觸傳遞為毫秒級，微秒乃物理學上之誇飾；
      L6708『唯一使命』過稱（多巴胺今說主『想要』而非『喜歡』）；L6710『物理層面上直接下線』
      不實（實為低前額葉活性）。三處俱改，並保留其修辭之力。
  五.5（半真）案例七靶點【第二重戒：盜戒（消耗信施而不行道）】——律之呵責在『居士生慢無有恭敬』
      （譏嫌），『盜』乃本書之延伸論證而非律判。治：不刪其見地，只如實標為『本書之推』。
擯回：一.1『pārājika 漏長音符』自相矛盾（書中 L1481 已作 pārājika，報告亦認此為正確形）；
      『斷頭喻乃部派論師之釋』也錯——喻在律文本身（「譬如人斷頭不可復起…故名波羅夷」），
      本書說『律藏給了一個比喻』正是如實。詞源『被擊敗者』屬通說，非本地語料可證，不擅添。
      一.2 巴利轉寫（Sammukhā／Paṭiññāta-karaṇa）：本地無巴利藏可校，書中所作乃通行參考表之形，
      外路所改亦屬異寫之爭（其『Paṭiññāya kāretabbaṃ』且是動詞形而非名目），無據不 churn。
      四.4 阿姜曼師承補摩訶布瓦：本書此段之職在標出譯者之法脈（Mun→Lee→Fuang→Ṭhānissaro），
      非森林派全史；添名屬作者取捨，且外地事實無從本地核。
"""
import hashlib
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk                                            # noqa: E402

BOOK = os.path.join(HERE, [f for f in os.listdir(HERE)
                           if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0])
BAK = BOOK + u".bak62a"
V = _tk.norm(_tk.VINAYA)
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n")
L = raw.split(u"\r\n")
log = []


def rep(tag, old, new, want=1, corpus_check=False):
    ns = [i for i, x in enumerate(L) if old in x]
    assert len(ns) == want, u"%s：命中 %d（須 %d）：%s" % (tag, len(ns), want, [n + 1 for n in ns][:6])
    if corpus_check:
        t = re.sub(u"[^一-鿿]", u"", _tk.norm(new))
        assert t in re.sub(u"[^一-鿿]", u"", V), u"%s：新掛律文宣稱而語料無據" % tag
    for n in ns:
        L[n] = L[n].replace(old, new)
        log.append(u"%-12s L%-5d｜%s" % (tag, n + 1, L[n][:58]))


# ── 二.3 娑伽陀：一從本律之地理 ──────────────────────────────────────────
rep(u"地理·支陀國", u"大毒龍盤踞在菴婆羅村", u"大毒龍盤踞在支陀國，害人一村")
rep(u"地理·本律事", u"將其降伏皈依三寶，為全城百姓消除了大災難。",
    u"將其降伏——本律所記，尊者是在一編髮梵志的客房里與龍對放火光，"
    u"『我今寧可滅此龍火令不傷龍身耶』，當夜降龍盛著鉢中。百姓由此安寢。")
rep(u"地理·國中居士", u"> 全城居士感念尊者恩德", u"> 國中居士感念尊者恩德")
rep(u"地理·中路醉臥", u"> 走出城門時，酒力發作", u"> 回程路上，酒力發作")
rep(u"如實標記", u"娑伽陀一案另有飲酒十過失之列舉，與以草木頭內著酒之細判，詳第九章案例二十七；此處但取其醉臥一幕，為全書立骨。",
    u"娑伽陀一案另有飲酒十過失之列舉，與以草木頭內著酒之細判，詳第九章案例二十七；此處但取其醉臥一幕，為全書立骨。"
    u"兩事之次弟亦從本律：降龍在支陀國之編髮梵志處，黑酒之供與中路醉臥則在佛至拘睒彌之後，此處連敘而略之。")
assert not [x for x in L if u"菴婆羅村" in x], u"『菴婆羅村』仍有殘留"

# ── 六.6 神經科學三處精度 ───────────────────────────────────────────────
rep(u"科學·毫秒", u"會在百萬分之一秒內釋放出狂暴的多巴胺海嘯",
    u"會在千分之一秒的毫秒尺度內掀起一波狂暴的多巴胺訊號")
rep(u"科學·想要", u"這種神經化學物質的唯一使命，就是向你的大腦發出最高級別的緊急指令",
    u"（按：多巴胺之主職，今說為『想要（wanting）』之驅動，不是『喜歡（liking）』之快感——"
    u"快感另由阿片系統擔當。正因它不必先給你快樂，才更難擋：它只把『去拿』這一步標成最高優先。）"
    u"它向大腦發出的是一條最高級別的緊急指令")
rep(u"科學·下線", u"會被大腦在物理層面上「直接下線」",
    u"會被邊緣系統的訊號壓過——影像所見是前額葉活性顯著下降（所謂低前額葉活性），"
    u"不是神經元真的斷電；但對一個正在被慾望驅動的人而言，這兩者的差別並體感不到")

# ── 五.5 案例七靶點：如實標為本書之推 ───────────────────────────────────
rep(u"靶點·標推", u"【第二重戒：盜戒（消耗信施而不行道）】",
    u"【第二重戒：盜戒之延伸（消耗信施而不行道——本書之推，律之呵責自在『居士生慢無有恭敬』）】")

# ── 簡形掃（改動之行須無簡形：以 U+XXXX 記形，勿只看命中數）──────────────
CHG = set()
for z in log:
    m = re.search(u"L(\\d+)", z)
    if m:
        CHG.add(int(m.group(1)) - 1)
BAD = sorted({c for n in CHG for c in L[n] if 0x4E00 <= ord(c) <= 0x9FFF and c not in V})
print(u"簡形／生僻掃：%d 行改動・語料未見之字 %d 枚：%s" % (
    len(CHG), len(BAD), u" ".join(u"%s U+%04X" % (c, ord(c)) for c in BAD)))

new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔）"
assert chk.count(u"\r") == chk.count(u"\n") == len(L) - 1, u"CRLF 之計異"
print(u"行數：%d（不變）・字數：%d → %d（%+d）" % (len(L), len(raw), len(new_raw), len(new_raw) - len(raw)))
for z in log:
    print(u"  " + z)
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
