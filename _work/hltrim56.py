# -*- coding: utf-8 -*-
"""第 56 輪・我自削（外路第六・七報連番點名之三段，俱是我在第 55 輪起草、作者放行者）。

去取：標記（本書之解／推／行法）一律保留——那是凡例款①②之界，削之即把今解掛成佛說；
     所削者唯『替古人編動機』與『現代行政細目』與『文藝抒情』三樣，論點本身不動。
  L1636 微型道場 221→150字：削『兩段行法／常住出具行治紀錄／移轉管轄於大叢林或聯合僧團』
        之章程細目，留『法權隨人而存，不隨地理而絕』之原則與『非律明文』之自標。
  L2993 向下轉移的怒氣 151→~86字：律只記『不喜見烏』；削『一個在體制內受了處分…於是削竹
        為弓，殺一庭啼鴉』之敘事推演，只留替代性攻擊之通說一句與慈悲之判語。
  L3689 退堂之後 151→~76字：削『掃地、洗碗、搬柴，親手把自己從審判者的位子上請下來』之抒情，
        留『案結則審者之職畢・語業歸零・護欄是擋自己的』。
護三道：備份＋SHA；三錨各斷命中＝1；斷行數與 CRLF 不動；回讀斷舊形＝0。
用法：python -X utf8 _work/hltrim56.py [--go]
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402

CUTS = [
    (u"**按：微型道場之困與出罪法權之移（本書之解）。**依律，出罪須二十人僧；而今之小道場多一師二三眾，"
     u"犯者縱已誠心服法，常苦於僧數不足。律於人數本有四級之判（四人、五人、十人、二十人，邊地別開減省），"
     u"其意一貫：法權隨人而存，不隨地理而絕。故本書以為，僧數不具之道場宜作兩段行法——服滿六夜摩那埵後，"
     u"由常住如實出具行治紀錄（所犯、所治、日數、有無更犯），移轉管轄於鄰近大叢林或區域聯合僧團，"
     u"由其足數出罪。此乃本書據律意所作的現代設計，非律之明文。",
     u"**按：微型道場之困（本書之解）。**依律，出罪須二十人僧；而今之小道場多一師二三眾，"
     u"犯者縱已誠心服法，常苦於僧數不足。律於人數本有四級之判（四人、五人、十人、二十人，邊地別開減省），"
     u"其意一貫：法權隨人而存，不隨地理而絕。故僧數不具之處，行治當往足數之僧團完成——"
     u"此係本書據律意之推衍，非律之明文。"),
    (u"* **向下轉移的怒氣（本書之推）：**律在此只記不喜見烏，不記他此前受過何呵責；"
     u"本書敢補的只有一層現代心理學——一個在體制內受了處分又不肯正視自己過失的人，"
     u"常把胸中積壓的羞辱轉嫁給絕無反抗之力的弱小者，於是削竹為弓，殺一庭啼鴉。"
     u"慈悲不是抽象的口號：慈悲是絕不把自身的受挫，轉嫁到比你更弱小的存在身上。",
     u"* **向下轉移的怒氣（本書之推）：**律只記「不喜見烏」，不記他此前受過何呵責。"
     u"此處只取一層通說：受挫而不肯正視己過的人，常把羞辱轉嫁給絕無反抗之力的弱小者。"
     u"慈悲不是口號——慈悲是不把自身的受挫，轉嫁到比你更弱小的存在身上。"),
    (u"* **退堂之後（本書之行法）：**案已結、羯磨已成，審者之職即畢。散會之後，走廊與茶席上"
     u"不復咀嚼案情、不復品評他人過失——語業歸零；然後去做一件粗重的活，掃地、洗碗、搬柴，"
     u"親手把自己從審判者的位子上請下來，回到我亦隨時可能失足的人。"
     u"護欄是擋自己的，不是拿量別人的；把法讀成一張驗傷單，便是學錯了方向。",
     u"* **退堂之後（本書之行法）：**案已結、羯磨已成，審者之職即畢。散會之後不復咀嚼案情、"
     u"不復品評他人過失——語業歸零，回到我亦隨時可能失足的人。"
     u"護欄是擋自己的，不是拿量別人的；把法讀成一張驗傷單，便是學錯了方向。"),
]
GO = "--go" in sys.argv[1:]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
lines = raw.split("\r\n")
print(u"正本 SHA %s｜%d 行｜CRLF %d" % (sha0[:16], len(lines), raw.count("\r\n")))
for i, (old, new) in enumerate(CUTS, 1):
    idx = [n for n, l in enumerate(lines) if l == old]
    if len(idx) != 1:
        idx = [n for n, l in enumerate(lines) if old[:40] in l]
        if len(idx) != 1:
            raise SystemExit(u"第 %d 錨命中 %d 行（須 1），未動一字。" % (i, len(idx)))
        raise SystemExit(u"第 %d 錨僅前 40 字相符（全文不合，或有異形空白），中止待查：L%d" % (i, idx[0] + 1))
    n = idx[0]
    print(u"刀%d：L%-5d %4d字 → %4d字（%+d）" % (i, n + 1, len(old), len(new), len(new) - len(old)))
    lines[n] = new
out = "\r\n".join(lines)
if out.count("\r\n") != raw.count("\r\n") or len(out.split("\r\n")) != len(lines):
    raise SystemExit(u"行數或換行不合，未寫檔。")
for old, _n in CUTS:
    if old in out:
        raise SystemExit(u"舊形殘留，未寫檔。")
print(u"總計：%d 字 → %d 字（%+d）" % (len(raw), len(out), len(out) - len(raw)))
if not GO:
    print(u"（覆核模式，未寫檔；加 --go 即入刀）")
    raise SystemExit(0)
bak = HP.SRC + u".bak56b"
if not os.path.exists(bak):
    io.open(bak, "w", encoding="utf-8", newline="").write(raw)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(out)
chk = io.open(HP.SRC, encoding="utf-8", newline="").read()
print(u"已入刀：SHA %s｜備份 %s" % (hashlib.sha256(chk.encode("utf-8")).hexdigest()[:16],
                                    os.path.basename(bak)))
print(u"回讀：本書之解 %d・本書之推 %d・本書之行法 %d（三標俱須仍在）"
      % (chk.count(u"本書之解"), chk.count(u"本書之推"), chk.count(u"本書之行法")))
