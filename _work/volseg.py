# -*- coding: utf-8 -*-
"""第 134 輪軸（乙）：卷段之歸屬——引文須見於**該行所稱之任一卷段**

校正紀錄：初版以『行內逐個卷段標記』各自配對其後之引文，遂生 17 筆偽訊——書中體例本作
    「01-10卷段·某品兼11-21卷段某法」，複合引文之各段可分屬其中**任何**一標記。
    今以『行內全部標記之集合』為可接受域；引文再按『……』切段，逐段（≥12 字）求之。

量訖而不立之維（第 216 輪・卷段標與卷次之三維）：
 乙 **卷段標之形**——印面『NN-MM卷段』去重唯 (1,10)(11,21)(22,30)(31,37)(38,49)(50,60) 六形，
    與本地六檔全同，非六檔之形 **0 處**；既有不變量已鎖其制（『卷段標記』之形），再立一軸即重架。
 丙 **卷次之界**——印面『卷X』（漢字序與阿拉伯俱辨，53 形、總見 297）其值全在 1..59，越界 **0 處**。
    （尺之自犯一課：初版之漢字序解析把「七」讀成 70——單字無『十』時須取個位，
     遂生出 13 處假越界，且「六八」之並列式亦誤；正解須先分『十』之前後，非枚數相加。）
 丁 **卷次是否落在其卷段之內**——『NN-MM卷段·卷X』並列式可校 18 筆，X∉[NN,MM] 者 **0 筆**。
    （又一尺課：初版之窗跨「、《楞嚴經》」而把 L11707 之他典卷次算入本律卷段，成 1 筆假陽性——
     引證並列之界須止於『、』『《』，與 214 輪『跨引號誤捕』同族。）
三維俱無病，故不入軸名冊；而行號級之語料指針另立第 44 軸 `r216loc`（本軸校『引文在其卷段檔之列』，
彼軸校『號在該檔之內、不落虛行、且副其所引』——兩軸一縱一橫，互不可替代）。
"""
import glob
import io
import os
import re
import sys

MD = sys.argv[1] if len(sys.argv) > 1 else u'ver38四分律_起心動念心智分析框架_修正版.md'
PUNCT = re.compile(u'[\\s「」『』【】（）()、，。；：！？…‥·．\\-—_/《》*]')


def norm(s):
    return PUNCT.sub(u'', s)


CORPUS = {}
for f in glob.glob(u'原文/*.txt'):
    CORPUS[os.path.basename(f)[:5]] = norm(io.open(f, encoding='utf-8', errors='replace').read())

T = io.open(MD, encoding='utf-8').read()
L = T.split('\n')
# 第 250 輪：底冊四篇已另檔，主檔之印面尾今為「# 終卷」（不隨冊），故界標隨之
MSTART = next((i for i, l in enumerate(L) if l.startswith(u'# 終卷')), len(L))

volpat = re.compile(u'(\\d{2}-\\d{2})\\s*卷段')     # 「11-21 卷段」之夾空白同收
qpat = re.compile(u'「(.{12,600}?)」')
nseg = 0
bad = []
for i, l in enumerate(L[:MSTART]):
    if u'卷段' not in l or u'「' not in l:
        continue
    claimed = set(volpat.findall(l))
    if not claimed:
        continue
    for qm in qpat.finditer(l):
        for seg in re.split(u'……|…', qm.group(1)):
            q = norm(seg)
            if len(q) < 12:
                continue
            nseg += 1
            where = {k for k, v in CORPUS.items() if q[:16] in v}
            if not where:
                continue                     # 全語料查無：屬 f 口徑之標界職守
            if not (where & claimed):
                bad.append((i + 1, sorted(claimed), sorted(where), q[:18]))
for x in bad[:20]:
    print(u'  行 %5d｜稱 %s｜實見 %s｜%s…' % (x[0], u'/'.join(x[1]), u'/'.join(x[2]), x[3]))
print(u'==== 卷段歸屬：查 %d 段，錯置 %d 段（去重 %d 類）====' % (
    nseg, len(bad), len({(tuple(b[1]), tuple(b[2]), b[3]) for b in bad})))
sys.exit(1 if bad else 0)
