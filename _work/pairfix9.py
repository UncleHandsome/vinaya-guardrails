# -*- coding: utf-8 -*-
"""第七波・收外路第九報告（八項俱先量今檔與今印面，量得始動）。

甲・F2 第四章第五節『原則三』截斷（一目一条而句尾留『；』）→ 補回二条（律制之語，不取世俗法名）。
乙・F2『律典《四分律》卷一中，此戒之恩給僅見於難提比丘一人』→ 本地語料實證：難提與波羅夷戒之文
    見於『31-37 原文』『50-60 原文』兩檔（卷三十一〜三十七段・卷五十〜六十段），卷一唯勿力伽難提
    殺雇之因緣，無與學之事。改如實之稱。
丙・F1 內跨冊之引〔調部專題 NN〕未冠冊名 → 冠《如法推尋》。
丁・圍欄（<pre>）內之粗體標記 pandoc 不解析，印面直出字面星號 → 交 `pairfencestar.py` 以等寬空格淨之（不動框線）。
戊・巴利標音之性別誤（Sikkhamānā 乃陰性，指式叉摩那）→ 去其標音，唯留漢語『與學羯磨（與波羅夷戒）』。
己・字數宣稱膨脹（三十萬字／三十二萬言／三十餘萬言）→ 依實測改『近二十萬言』（兩冊都計 197,812 漢字）。
庚・F1 自序『天下林下，風清月朗』語意重疊 → 『歸向林下，風清月朗』。
辛・F2 二部僧換算矩陣之表頭被欄寬擠斷（法/定人數）→ 表頭改為刻意之兩行（<br>），使『法定人數』整詞不破。
用法：python -X utf8 _work/pairfix9.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv

REP = {
    F2: [
        ("律典《四分律》卷一中，此戒之恩給僅見於難提比丘一人",
         "律典《四分律》記此事於說戒與調部諸卷（本地語料見於卷三十一至三十七段・卷五十至六十段兩檔；"
         "卷一別有勿力伽難提殺雇之因緣，非此恩給），此戒之恩給僅見於難提比丘一人"),
        ("**「與學羯磨（與波羅夷戒·Sikkhamānā / 與學比丘）」**",
         "**『與學羯磨（與波羅夷戒）』**"),
        ("| 羯磨事項 | 比丘尼僧初審院法定人數 | 比丘僧覆審院法定人數 | 合計參與僧數與程序形態 |",
         "| 羯磨事項 | 比丘尼僧初審院<br>法定人數 | 比丘僧覆審院<br>法定人數 | 合計參與僧數與程序形態 |"),
    ],
    F1: [
        ("走過三十萬字的微觀推演", "走過近二十萬言的微觀推演"),
        ("翻過三十二萬言的推演", "翻過近二十萬言的推演"),
        ("若問全書三十餘萬言", "若問兩冊都計近二十萬言"),
        ("走出急診室的大門，天下林下，風清月朗。", "走出急診室的大門，歸向林下，風清月朗。"),
    ],
}
# 丙・跨冊之引：F1 內〔調部專題 NN〕須冠冊名
CROSS = (F1, re.compile(r"(?<!《如法推尋》)〔調部專題"), "《如法推尋》〔調部專題")
# 甲・補回二条（律制之語）
TAIL = ["", "* **追還之責不隨身分而息**：其人縱已捨戒、已去僧籍，所侵僧物仍當如數追還；"
        "常住得依白二羯磨議定數目與主事之人，隨時追索，不令因身分變更而墮其債；",
        "* **管轄之歸處**：物在何界，即由何界之僧團如法議追；涉及他界者，依『移轉管轄』之例通報彼界協查，"
        "不得互相推擲，亦不得以『人已去』為由閉檔不問。"]


def main():
    books = {f: (ROOT / f).read_bytes().decode("utf-8").split("\r\n") for f in (F1, F2)}
    n = {}
    for f, rules in REP.items():
        for old, new in rules:
            L = books[f]
            idx = [i for i, l in enumerate(L) if old in l]
            if len(idx) != 1:
                print(f"  ✗ {f[:6]}・錨命中 {len(idx)}：{old[:30]}")
                continue
            L[idx[0]] = L[idx[0]].replace(old, new)
            n[f] = n.get(f, 0) + 1
            print(f"  ・{f[:6]} L{idx[0] + 1}・治（{old[:16]}…）")
    # 丙
    L1 = books[F1]
    cc = 0
    for i, l in enumerate(L1):
        if CROSS[1].search(l):
            L1[i] = CROSS[1].sub(CROSS[2], l)
            cc += 1
            print(f"  ・心法卷 L{i + 1}・〔調部專題〕冠冊名")
    n[F1] = n.get(F1, 0) + cc
    # 甲・補回
    L2 = books[F2]
    if any(l.startswith("* **追還之責不隨身分而息**") for l in L2):
        print("  · 補回已在檔（重入之護），跳過")
        ks = []
    else:
        ks = [i for i, l in enumerate(L2) if l.startswith("* **物權不因身分而消滅**")]
    if len(ks) != 1:
        if ks:
            raise SystemExit("補回之錨不唯一：%s" % ks)
        ks = [-1]
    k = ks[0]
    if k >= 0:
        if L2[k].rstrip().endswith("；"):
            L2[k] = L2[k].rstrip()[:-1] + "。"
        L2[k + 1:k + 1] = TAIL
        n[F2] = n.get(F2, 0) + 1
        print(f"  ・法制卷 L{k + 2}・補回二条（原以『；』收尾之截斷）")
    bad = sorted({c for f in (F1, F2) for l in books[f] for c in PS.hits(l)})
    print(f"治：心法卷 {n.get(F1, 0)}・法制卷 {n.get(F2, 0)}・全冊簡形 {bad}")
    if bad:
        raise SystemExit("帶簡形，不落盤")
    if not W:
        print("（試跑：未落盤）")
        return
    for f in (F1, F2):
        p, raw = ROOT / f, (ROOT / f).read_bytes()
        (BAK / (f + ".pre_fix9")).write_bytes(raw)
        data = "\r\n".join(books[f]).encode("utf-8")
        p.write_bytes(data)
        print(f"  ● {f[:6]}・{data.decode('utf-8').count(chr(13)) + 1} 行・SHA "
              f"{hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")


main()
