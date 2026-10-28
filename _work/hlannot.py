# -*- coding: utf-8 -*-
"""尺（hlannot）——『界說與按語』一族之戶口與句式密度（外路歷輪以此為『系統性痼疾』，今立尺答之）。

所以立之：同族外路報告四度而至（拆鷹架・按語砍八成・紅隊等五處・微型道場等六處），
    歷次皆臨時寫探針量一遍——臨時探針必落後於下一次指控。今定為常尺，一跑即得三數：
      ① 戶口：按語獨立段・（本書之X）標籤段・界說標記行（義引／大意／本書之解／本律無文…）；
      ② 分量：各段字數與占全書之比（『大段大段』之說須以字判，不以印象判）；
      ③ 句式密度：破折號與全形括號之每千字計數，對全書正文之比（外路『黏滯』一項為可量者）。
判：標記行與按語段數須不低於 FLOOR（削之即破凡例款①②——如實標記乃第 41 輪親裁全數保留、
    且為 `hlchk` 庚轴之不变量；要降須作者明令，並同步改本檔之 FLOOR，不得靜默下滑）。
用法：python -X utf8 _work/hlannot.py [--detail]
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402

MARKS = [u"義引", u"義譯", u"大意", u"括其旨", u"本律無文", u"非逐字", u"不稱其逐字",
         u"取其意", u"本書之解", u"本書之推", u"本書之行法", u"本書之程序倫理",
         u"本書撮", u"本書語", u"須老實標明", u"另辨", u"如實記", u"須辨",
         u"本書括旨", u"未及逐覆", u"非其書之句", u"非其經之句", u"大正藏",
         u"自為之文", u"自為之語", u"效古德語氣", u"非《行事鈔》之文", u"非《資持記》之文"]
FLOOR_MARK = 31      # 今量（第 56 輪再制後）：帶標記之【去重行數】。
                     # 前值 43 係『〔本書括旨〕＋未及逐覆＋編號』三件套在印面的計數；奉問
                     # 『是不是乾脆不要署名』後，未經覆核者一律去名去號去標籤（只作本書題記），
                     # 標記行遂降至 31——此為**設計之降**，非病。今護印面之尺改由 `sigchk` 丙軸擔當
                     # （款①形制掛他師／未覆核而附號／標籤入印面，三者皆紅）。
FLOOR_ANNOT = 10     # 今量：以『按：』起頭之獨立段數（全書另有 4 枚行內『按：』，不在此口徑）
DASH = chr(0x2014) * 2
OP, CP = chr(0xff08), chr(0xff09)
CRLF = chr(13) + chr(10)

detail = "--detail" in sys.argv[1:]
ls = io.open(HP.SRC, encoding="utf-8", newline="").read().split(CRLF)
body = [l for l in ls if l.strip() and not l.strip().startswith("#")]
bchars = sum(len(l.strip()) for l in body)

mark_rows = sorted({n for n, l in enumerate(ls, 1) for m in MARKS if m in l})
annot = [(n, l.strip()) for n, l in enumerate(ls, 1)
         if l.strip().startswith(u"按：") or l.strip().startswith(u"**按：")]
tags = [(n, l.strip()) for n, l in enumerate(ls, 1)
        if re.match(u"^[*>\\s]*\\*\\*[^*]{0,28}（本書之[^）]*）", l.strip()) and not l.strip().startswith(u"**按：")]

a_chars = sum(len(s) for _n, s in annot)
t_chars = sum(len(s) for _n, s in tags)
sel = [s for _n, s in annot + tags]
s_chars = sum(len(x) for x in sel) or 1


def dens(rows):
    t = "".join(rows)
    n = len(t) or 1
    return 1000.0 * t.count(DASH) / n, 1000.0 * t.count(OP) / n


bd, bp = dens([l.strip() for l in body])
sd, sp = dens(sel)
print(u"正本：%s｜%d 行" % (os.path.basename(HP.SRC), len(ls)))
print(u"① 戶口：按語獨立段 %d 段・%d 字｜『（本書之X）』標籤段 %d 段・%d 字｜界說標記行 %d 行"
      % (len(annot), a_chars, len(tags), t_chars, len(mark_rows)))
print(u"   兩族合計 %d 字＝全書正文 %d 字之 %.2f%%" % (a_chars + t_chars, bchars,
                                                    100.0 * (a_chars + t_chars) / bchars))
print(u"② 分量：按語每段均 %.0f 字（最長 %d）｜標籤段每段均 %.0f 字（最長 %d）"
      % (a_chars / max(1, len(annot)), max([len(s) for _n, s in annot] or [0]),
         t_chars / max(1, len(tags)), max([len(s) for _n, s in tags] or [0])))
print(u"③ 句式密度（每千字）：破折號 界說 %.1f／全書 %.1f（%+.0f%%）・全形括號 界說 %.1f／全書 %.1f（%+.0f%%）"
      % (sd, bd, 100.0 * (sd / bd - 1), sp, bp, 100.0 * (sp / bp - 1)))
if detail:
    for n, s in annot:
        print(u"   按 L%-5d %4d字 %s" % (n, len(s), re.sub(u"[*\\s]", u"", s)[:26]))
    for n, s in tags:
        print(u"   標 L%-5d %4d字 %s" % (n, len(s), re.sub(u"[*\\s]", u"", s)[:26]))
# ④ 段長之上限（第 57 輪立，同輪改單位）：以『印面段落』計，非以源檔單行計——
#    案例卡欄內一行一拍而相鄰無空行者，pandoc 併為一段（曾單行 559 而印面 841，尺之單位錯則綠亦非綠）。
#    模型取共器 _work/hlpara.py（與補空行之刀同源）。實害兩案已治：307／559 字之黑塊分段、
#    欄內併段者補空行 301 處。豁免採如實列名：連綴式列舉（一、二、…在一行之內）之節奏在序號本身，
#    分段反成斷鏈（h4seq 現形），故不拆——但其字數仍在此印出，不靜默放過。
CEIL = 320
LONG_EXEMPT = [u"十一條如次"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hlpara  # noqa: E402
apx0 = hlpara.apx_of(ls)
cen = hlpara.census(ls, apx0)
ex = [(c, n) for c, n in cen if any(x in ls[n - 1] for x in LONG_EXEMPT)]
overs = [(c, n) for c, n in cen if c > CEIL and (c, n) not in ex]
print(u"④ 段長（印面段落）：正文 %d 段｜最長 %d 字｜>320 字者 %d 段｜豁免（連綴列舉）%d 段%s" % (
    len(cen), cen[0][0], len(overs), len(ex),
    u"・最長 %d 字如實印" % max(c for c, _n in ex) if ex else u""))
for c, n in overs[:6]:
    print(u"   長 L%-5d %4d字 %s" % (n, c, re.sub(u"[*\\s]", u"", ls[n - 1])[:26]))
bad = []
if len(mark_rows) < FLOOR_MARK:
    bad.append(u"標記行 %d＜下限 %d" % (len(mark_rows), FLOOR_MARK))
if len(annot) < FLOOR_ANNOT:
    bad.append(u"按語段 %d＜下限 %d" % (len(annot), FLOOR_ANNOT))
if overs:
    bad.append(u"印面單段逾 %d 字者 %d 段（黑塊，須於語意轉折處補空行或分段）" % (CEIL, len(overs)))
print(u"判：標記行須≥%d・按語段須≥%d・單段須≤%d 字｜今 %s"
      % (FLOOR_MARK, FLOOR_ANNOT, CEIL, u"合格" if not bad else u"不：" + u"；".join(bad)))
sys.exit(1 if bad else 0)
