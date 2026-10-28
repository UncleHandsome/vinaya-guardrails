# -*- coding: utf-8 -*-
"""目錄戶口尺（toccensus・第 75 輪立）：全書詳細目錄之涵蓋率，獨立於 `tocsync` 而量。
緣起：`tocsync` 報『覆蓋 0 行』只證其管轄內無漂移，並不自證管轄即全書——本尺不問產生器之記憶，
    直接把正文每一根『應入目錄』之標題到目錄區索其實題，並倒對目錄有無幽靈條。
口徑（豁免亦是宣稱，故記於此）：應入目錄者四形——章（# 第N章）・小節（### N、）・案例（#### 案例N）・
    中間層與附論（###/#### 【…】）；H4 之散文子項（如『1. 什麼是性戒』）由目錄撮述或不列，不作要求，
    但其數須當場印出。『第N部』以 ### **【…】** 之形入目錄，另目校之。
    另二目（第 76 輪添・79 輪改護作者之制）：書中有『# 附錄』H1 則目錄須有其條；
    十線地圖之**條目**須列於目錄之末（尾聲之後）且自注『前置於第一部之前』，
    其**正文區塊**須仍在第一部之前——目錄列末・正文排先乃作者兩地之制，非倒置。
用法：python -X utf8 _work/toccensus.py [-v]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
S = u"零一二三四五六七八九"


def cn2int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    tot, cur = 0, 0
    for ch in s:
        if ch == u"百":
            tot = (tot + (cur or 1)) * 100
            cur = 0
        elif ch == u"十":
            tot = (tot + (cur or 1)) * 10
            cur = 0
        elif ch in S:
            cur = S.index(ch)
    return tot + cur


def norm(s):
    return re.sub(u"[\\s*\u3000\\-＿]", u"", s)


def run():
    L = io.open(BOOK, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    dlo = next(i for i, s in enumerate(L) if s.startswith(u"# 【全書詳細目錄】"))
    dhi = next(i for i in range(dlo + 1, len(L)) if L[i].startswith(u"# 十線地圖"))
    apx = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
    toc = norm(u"".join(L[dlo + 1:dhi]))
    toc_items = [s for s in L[dlo + 1:dhi] if re.match(u"^\\s*[*\\-] ", s)]
    CH = re.compile(u"^# 第([一二三四五六七八九十百]+)章")
    SEC = re.compile(u"^### ([一二三四五六七八九十]+)、 ?(.*)")
    CASE = re.compile(u"^#### (案例[一二三四五六七八九十百]+)[：:](.*)")
    MID = re.compile(u"^### \\u3010.+\\u3011")
    FU = re.compile(u"^#### \\u3010.+\\u3011")
    BU = re.compile(u"^# \\u3010第.+部[^\\u3011]*\\u3011")
    want, sub = [], 0
    for i in range(dhi, apx):
        s = L[i]
        if CH.match(s):
            want.append((i + 1, u"章", s[2:].strip()))
        elif CASE.match(s):
            m = CASE.match(s)
            want.append((i + 1, u"案例", m.group(1) + u"：" + m.group(2)))
        elif FU.match(s) or MID.match(s):
            m = FU.match(s) or MID.match(s)
            want.append((i + 1, u"中間層", m.group(0).lstrip(u"#").strip()))
        elif SEC.match(s):
            m = SEC.match(s)
            want.append((i + 1, u"節", m.group(1) + u"、" + m.group(2)))
        elif s.startswith(u"#### "):
            sub += 1
    bus = [L[i][2:].strip() for i in range(dhi, apx) if BU.match(L[i])]
    bad = []
    for ln, kind, t in want:
        key = norm(t)[:16]
        if key and key not in toc:
            bad.append((ln, u"目錄查無", u"%s｜%s" % (kind, t[:44])))
    for b in bus:
        if norm(b)[:14] not in norm(u"".join(L[dlo + 1:dhi])):
            bad.append((dlo + 1, u"部題查無", b[:40]))
    CI = re.compile(u"^\\s*[*\\-]+ *(案例[一二三四五六七八九十百]+)[：:]")
    body = norm(u"".join(L[dhi:apx]))
    ghost = [s.strip() for s in toc_items if CI.match(s) and norm(CI.match(s).group(1)) not in body]
    for g in ghost:
        bad.append((dlo + 1, u"目錄幽靈條", g[:44]))
    ncase = len([s for s in toc_items if CI.match(s)])
    nsec = len([s for s in toc_items if re.match(u"^\\s*[*\\-]+ *[一二三四五六七八九十]+、", s)])
    # 第 76 輪添二目（外路第廿七報指『目錄漏附錄』與『十線地圖列於末』）：
    # ①書中既有附錄之 H1，目錄须有其實條；②目錄之序不得倒置——前置之物不得列於末章之後。
    if any(s.startswith(u"# 附錄") for s in L) and not any(u"附錄　全戒本歷條總表" in s for s in toc_items):
        bad.append((dlo + 1, u"目錄漏附錄", u"書中有附錄 H1 而目錄無其條"))
    reg = L[dlo + 1:dhi]
    i_x = next((i for i, s in enumerate(reg) if s.startswith(u"* **") and u"十線地圖" in s), None)
    i_1 = next((i for i, s in enumerate(reg) if u"【第一部" in s), None)
    i_z = next((i for i, s in enumerate(reg) if u"尾聲" in s), None)
    # 作者之制（第 79 輪正 76 輪依外路之誤移）：十線地圖之**條目**列於目錄之末（末章尾聲之後），
    # 其**正文區塊**則前置於第一部之前——『列末而排在先』之兩地全仗條目括注交代，
    # 故括注『前置於第一部之前』即此制之法源：缺括注而列末，才是真『倒置』（讀者求不得）。
    if i_x is not None:
        if i_z is not None and i_x < i_z:
            bad.append((dlo + 1 + i_x, u"目錄序位", u"十線地圖條目列於尾聲之前（第 %d 行，尾聲在第 %d 行）"
                                u"——作者之制為列於目錄之末" % (i_x + 1, i_z + 1)))
        if u"前置於第一部之前" not in reg[i_x]:
            bad.append((dlo + 1 + i_x, u"目錄序位無交代",
                        u"條目列末而不注其正文之實位，讀者求不得：%s" % reg[i_x][:40]))
    b_x = next((i for i, s in enumerate(L) if s.startswith(u"# ") and u"十線地圖" in s), None)
    b_1 = next((i for i, s in enumerate(L) if s.startswith(u"# 【第一部")), None)
    if b_x is not None and b_1 is not None and b_x > b_1:
        bad.append((b_x + 1, u"正文序位", u"十線地圖區塊（L%d）在第一部（L%d）之後——作者自標『前置於第一部之前』"
                    % (b_x + 1, b_1 + 1)))
    # 章條之副題（第 82 輪立）：目錄之章條若帶副題，須與正文該章之 H2 副題逐字相合。
    # 病源：第十四・十五章換稿後，正文之副題已改，目錄仍存舊稿之兩句（『身體純化…』『度人考核…』），
    # 而舊尺唯校『章名有無』，副題之漂移遂無人管。此目唯量「兩地之文是否同」，不判文之優劣。
    CH_SUB = re.compile(u"^\\* \\*\\*第([一二三四五六七八九十]+)章(.*?)\\*\\*$")
    sub_bad = []
    for _i, _s in enumerate(reg):
        _m = CH_SUB.match(_s.strip())
        if not _m:
            continue
        _num = _m.group(1)
        _h = next((k for k, x in enumerate(L) if x.startswith(u"# 第" + _num + u"章")), None)
        if _h is None or _h + 1 >= len(L) or not L[_h + 1].startswith(u"## "):
            continue
        _sub = L[_h + 1][3:].strip().lstrip(u"——").strip()
        if _sub and norm(_sub) not in norm(_s):
            sub_bad.append((dlo + 1 + _i, _num, _sub[:26], _s.strip()[:34]))
    print(u"  章條副題：%d 處與正文不合" % len(sub_bad))
    for _n, _num, _sub, _s in sub_bad:
        print(u"✗ L%d｜目錄第%s章之副題非正文之副題（正文今作：%s）" % (_n, _num, _sub))
        bad.append((_n, u"副題漂移", u"第%s章目錄與正文之副題不合：%s" % (_num, _sub)))
    # 負測：植一對已知之不合（目錄存舊副題），判式須逮
    def _sub_ok(toc_line, body_sub):
        return bool(body_sub) and norm(body_sub.lstrip(u"——")) in norm(toc_line)
    _np = [(_sub_ok(u"* **第十四章 X——身體純化、斷除自慰與防暴機制**", u"——身軀、空間與共住心理學"), False),
           (_sub_ok(u"* **第十四章 X——身軀、空間與共住心理學**", u"——身軀、空間與共住心理學"), True)]
    if [v for _l, v in _np] != [False, True]:
        print(u"✗ 副題目之負測不響：%s" % [v for _l, v in _np])
        bad.append((0, u"副題目負測", u"自身負測不響"))
    else:
        print(u"  副題之負測｜舊副題判不合・今副題判合：✓")
    print(u"管轄｜應收 %d 條（章 %d・節 %d・案例 %d・中間層 %d）｜H4 子項 %d 根不作要求｜"
          u"目錄條目 %d（案例項 %d・節項 %d）｜部題 %d" % (
              len(want), sum(1 for _l, k, _t in want if k == u"章"),
              sum(1 for _l, k, _t in want if k == u"節"),
              sum(1 for _l, k, _t in want if k == u"案例"),
              sum(1 for _l, k, _t in want if k == u"中間層"), sub, len(toc_items), ncase, nsec, len(bus)))
    if u"-v" in sys.argv:
        for x in bad[:40]:
            print(u"  L%-5d %s｜%s" % (x[0], x[1], x[2]))
    print(u"判：目錄無漏、無幽靈、部題俱在、附錄有錄、序位不倒" if not bad else u"判：%d 目病" % len(bad))
    return bad


if __name__ == u"__main__":
    b = run()
    sys.exit(1 if b else 0)
