# -*- coding: utf-8 -*-
"""第 43 輪补丁（第十批）：①私呵將軍之國別與族人（從律文）②蒜案之現世因緣（自語料逐字）
   ③「五種不如法」改「七種」（標題・目錄・地圖・靶點四處）④犍度／揵度字形歸一（書中自敘九處）
   ⑤微細字兩處（里→裡、兩引文間補頓號）。逐字先過語料閘，替換必斷命中數。
用法：python -X utf8 _work/r10patch.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
V, NV = _tk.VINAYA, _tk.norm(_tk.VINAYA)
nsub = nins = 0


def verbatim(t):
    s = _tk.norm(t)
    assert s and s in NV, u"語料無此連写：%s" % t[:44]
    return t


def sub(old, new, want=1):
    global nsub
    hits = [i for i, s in enumerate(L) if old in s]
    tot = sum(L[i].count(old) for i in hits)
    assert tot == want, u"命中 %d（應 %d）：%s" % (tot, want, old[:52])
    for i in hits:
        L[i] = L[i].replace(old, new)
    print(u"  ✓ ×%-2d｜%s" % (want, old[:40]))
    nsub += tot


def ins_after(anchor, lines, want=1):
    global nins
    hits = [i for i, s in enumerate(L) if anchor in s]
    assert len(hits) == want, u"插入錨命中 %d（應 %d）：%s" % (len(hits), want, anchor[:44])
    i = hits[0]
    L[i + 1:i + 1] = lines
    nins += len(lines)
    print(u"  ＋ 插 %d 行 @L%d 後" % (len(lines), i + 1))


# ===== 〇・語料與現況自證 =====
print(u"【〇】自證")
assert V.count(u"持幡唱令") == 1 and V.count(u"先尼楗") == 1
assert V.count(u"私呵將") == 7, u"私呵將軍之見數走樣"
assert V.count(u"即時現園蒜取盡") == 1 and V.count(u"云何不見主拔取他蒜盡") == 1
nj = sum(s.count(u"揵度") for s in L)
print(u"  書中『揵度』今 %d 處（皆在引號之外）；『五種不如法』%d 處；『七種名字』%d 處" % (
    nj, sum(s.count(u"五種不如法") for s in L), sum(s.count(u"七種名字") for s in L)))
assert u"波斯匿國" in u"".join(L) and u"同一族里" in u"".join(L)

QS = [verbatim(u"汝為國之大臣"), verbatim(u"汝說有作法，瞿曇說無作法以化弟子，止，不須往。"),
      verbatim(u"我今寧可不辭尼揵師往見瞿曇，師能使我作何等？"),
      verbatim(u"阿姨欲須蒜耶"), verbatim(u"得蒜已後數數復往"),
      verbatim(u"從今日給比丘尼人各五枚蒜"),
      verbatim(u"汝等知不？某處某甲檀越日給比丘尼人各五枚蒜，可往迎取。"),
      verbatim(u"我不得自在，我正可守視而已耳"), verbatim(u"大家見施，奴不肯與"),
      verbatim(u"即勅沙彌尼拔取蒜，數知多少"),
      verbatim(u"此與上座、次座、和上、阿闍梨，此與同和上、同阿闍梨、親厚知識，此今日食、此明日食、此後日食"),
      verbatim(u"即時現園蒜取盡"), verbatim(u"正使檀越施與，猶應知足，況不見主而取盡"),
      verbatim(u"云何不見主拔取他蒜盡"), verbatim(u"今復愛故令蒜盡，更得貧窮。")]
print(u"  新增逐字 %d 段俱過語料閘 ✓" % len(QS))

# ===== 一、私呵將軍（律但記毘舍離・斷事堂・五百諸梨奢，不記其國；『波斯匿國』乃王名誤作國名）=====
print(u"\n【一】私呵將軍")
sub(u"私呵將軍是波斯匿國的大臣，梨奢族人再三勸他往見佛陀。他第一次說：",
    u"私呵將軍是毘舍離的一位大人物——律記他與五百諸梨奢共坐斷事堂，本是尼揵弟子；佛後來稱他「**汝為國之大臣**」，卻不記他是哪一國的大臣。那天斷事堂上諸梨奢以無數方便讚歎佛法僧，他在座中聽見，心生信樂，想去見佛，先回去稟報舊師，被攔下：「**汝說有作法，瞿曇說無作法以化弟子，止，不須往。**」他退了一次。諸梨奢第二、第三如是讚歎，他才想到：「**我今寧可不辭尼揵師往見瞿曇，師能使我作何等？**」於是逕往佛所，一開口便說：")

# ===== 二、蒜案之現世因緣 =====
print(u"\n【二】蒜案現世因緣")
sub(u"  蒜一案有本生：昔婆羅門死為雁，園主之端政婦多生男女，以貪愛故令金羽盡而更白羽——「**今復愛故令蒜盡，更得貧窮。**」佛以此呵責偷羅難陀比丘尼。",
    u"  毘舍離城外有一處蒜園。偷羅難陀比丘尼走過園邊，園主主動問：「**阿姨欲須蒜耶？**」她說要，園主便給；她「**得蒜已後數數復往**」，園主又給，並自此吩咐守園人：「**從今日給比丘尼人各五枚蒜。**」她回僧團把這樁好事告知同修：「**汝等知不？某處某甲檀越日給比丘尼人各五枚蒜，可往迎取。**」然後帶著沙彌尼、式叉摩那去取。守園人不肯給，說要等園主回來——「**我不得自在，我正可守視而已耳。**」她留下一句全案最關鍵的話：「**大家見施，奴不肯與。**」隨即「**即勅沙彌尼拔取蒜，數知多少**」，當場派定：「**此與上座、次座、和上、阿闍梨，此與同和上、同阿闍梨、親厚知識，此今日食、此明日食、此後日食。**」——「**即時現園蒜取盡。**」園主賣蒜回來，問蒜何故盡，守園人如實交底，居士當街譏嫌：「**比丘尼受取無厭足……正使檀越施與，猶應知足，況不見主而取盡！**」佛集僧呵責的正是這一句：「**云何不見主拔取他蒜盡？**」")
ins_after(u"云何不見主拔取他蒜盡？**」", [u"",
    u"  此案的定性，律交給了一則本生：昔有婆羅門，年百二十、形體羸瘦，其婦端政、多生男女，他繫心不捨，愛著情篤，命終便生雁中，毛羽盡為金色；他自念以何方便養活妻兒，遂日日來至其家，落一枚金羽而去。家人起謀，捉住他盡拔金羽——羽盡更生素羽，飛去不復再來。「**今復愛故令蒜盡，更得貧窮。**」律並逐一點名：彼婆羅門即園主，端政婦多生男女者即偷羅難陀，男女者即式叉摩那、沙彌尼。"])
sub(u"3. **律不跟你爭「動機好不好」，它問：別人現在看見的是什麼？** 當眾剝蒜、食蒜，所失者非味，是僧相；故戒從身口下手，不從心意下手。",
    u"3. **律不跟你爭「動機好不好」，它問：別人現在看見的是什麼？** 居士看見的不是她在吃蒜，而是她把整座園子拔空，還當場派定誰今天吃、誰明天吃——所失者非味，是僧相；故戒從身口下手，不從心意下手。")

# ===== 三、七種不如法（律列七名，書中標題誤承「五座道場」之五）=====
print(u"\n【三】七種不如法")
sub(u"五種不如法的表決", u"七種不如法的表決", 5)

# ===== 四、犍度字形歸一（書中自敘從今制；引律之逐字段本不作揵度，故無傷）=====
print(u"\n【四】犍度字形")
sub(u"揵度", u"犍度", nj)

# ===== 五、微細字 =====
print(u"\n【五】微細字")
sub(u"同一族里的第75條", u"同一族裡的第75條")
sub(u"佛答「**且止！佛自知時**」「**比丘中未有犯有漏法**」那一段",
    u"佛答「**且止！佛自知時**」、「**比丘中未有犯有漏法**」那一段")

txt = u"\r\n".join(L)
assert txt.count(u"揵度") == 0, u"揵度仍有殘留"
assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
print(u"\n替换 %d 處｜插入 %d 行｜行數 %d→%d｜%s" % (
    nsub, nins, len(raw.split(u"\r\n")), len(L), u"寫檔" if GO else u"覆核模式（未寫檔）"))
if GO:
    io.open(BOOK, u"w", encoding="utf-8", newline=u"").write(txt)
