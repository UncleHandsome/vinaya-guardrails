# -*- coding: utf-8 -*-
"""附錄稽核：只量**成文之書**（不複用生成器之記憶），證『每一條都有戶口』。
   一、篇之有無與歷號：兩部戒本之十二篇俱在，篇下歷號 1..N 不缺不重
      （N 以此尺自持之戒本數為準——比 4·13·2·30·90·4·100·7＝250，尼 8·17·30·178＝233）；
   二、每行須有「｜書中：」欄，其值非『－』者須指向書中實存之『第N章案例M』；
   三、篇題自報之「戒本 N 條／律文別宣 M 條」須與實數相符（自報不虛）。
用法：python -X utf8 _work/apxchk.py
四、防『換版而未重算』之漂移（第卅五輪之實害而生）：書中附錄須與產生器所出之草稿逐字同，
   且凡例須含產生器現算之通數句——否則即如本尺第一版之盲：md 是舊的，書卻報為已修。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
U = u"零一二三四五六七八九"

HEAD = re.compile(u"^## (\\S+?)：(\\S+?)（戒本 (\\d+) 條(?:，律文別宣 (\\d+) 條)?[^）]*）")
ROW = re.compile(u"^(\\d+)(?:～(\\d+))?\\. .*｜書中：(\\S.*)$")
CASE = re.compile(u"^#### 案例([一二三四五六七八九十]+)")
SECT = re.compile(u"^### ([一二三四五六七八九十]+)、")
CHAP = re.compile(u"^# 第(\\S+?)章")
NIR = {u"波羅夷": 8, u"僧殘": 17, u"捨墮": 30, u"單提": 178, u"提舍尼": 8}
BHR = {u"波羅夷": 4, u"僧殘": 13, u"不定": 2, u"捨墮": 30, u"單提": 90, u"提舍尼": 4, u"學法": 100, u"滅諍": 7}


def cat_of(stem):
    for k in (u"波羅夷", u"僧殘", u"捨墮", u"單提", u"提舍尼"):
        if k in stem:
            return k
    if u"不定" in stem:
        return u"不定"
    return u"學法" if u"學" in stem else u"滅諍"


def main():
    L = io.open(BOOK, encoding="utf-8", newline=u"").read().split(u"\r\n")
    h = [i for i, l in enumerate(L) if l.startswith(u"# 附錄")]
    if len(h) != 1:
        raise SystemExit(u"附錄標題存 %d 處，無從稽核" % len(h))
    apx = L[h[0]:]

    live, cur = set(), None                       # 書中實存之案例與小節位置
    for l in L[:h[0]]:
        m = CHAP.match(l)
        if m:
            cur = m.group(1)
            continue
        m = CASE.match(l)
        if m and cur:
            live.add(u"第%s章案例%s" % (cur, m.group(1)))
        m = SECT.match(l)
        if m and cur:
            live.add(u"第%s章第%s節" % (cur, m.group(1)))

    tot = hit = 0
    bad, got = [], set()
    i = 0
    while i < len(apx):
        m = HEAD.match(apx[i])
        if not m:
            i += 1
            continue
        bu, stem, n = m.group(1), m.group(2), int(m.group(3))
        nsx = int(m.group(4)) if m.group(4) else None
        fam = u"尼" if u"尼戒本" in bu else u"比"
        cat = cat_of(stem)
        got.add((fam, cat))
        want = (NIR if fam == u"尼" else BHR).get(cat)
        if want is None or want != n:
            bad.append(u"%s：%s 篇題自報 %d 條，戒本之數 %s" % (bu, stem, n, want))
        j, seen, nhit, ntxt = i + 1, [], 0, 0
        while j < len(apx) and not HEAD.match(apx[j]):
            line = apx[j].strip()
            r = ROW.match(line)
            if r:
                a, b = int(r.group(1)), int(r.group(2) or r.group(1))
                tag = u"%d" % a if a == b else u"%d～%d" % (a, b)
                seen.extend(range(a, b + 1))      # 「1～69.」之合列行自展開，歷號之數仍逐號核
                w = r.group(3).strip()
                if w == u"－":
                    pass
                elif w in live:
                    nhit += b - a + 1
                else:
                    bad.append(u"%s：第%s條之指針『%s』書中無此案例" % (stem, tag, w))
                if u"（律文合見前條" not in line and u"（與前部共戒" not in line:
                    ntxt += b - a + 1
                    # 戒文欄既自稱律文原句，須在語料連寫可查——本檢不複用產生器之假設，逕量成文之書。
                    body = line[line.find(u"「") + 1:line.rfind(u"」")] if u"「" in line else u""
                    nb = _tk.norm(re.sub(u"[『「』」]", u"", body))
                    if len(nb) >= 8 and nb not in _tk.VINAYA:
                        bad.append(u"%s：第%s號之戒文於語料不連寫：%s" % (stem, tag, body[:36]))
                # 共戒之號（乙部篇首，律但云「義如上」）依凡例「不可於乙部另指」——
                # 第卅七輪之實害：案例題內「一百零九條的第一條」被指針式樣認成第1條，
                # 遂使共戒之號得了一個指著別宣案例的假戶口（指針存在，故舊檢不報）。
                if u"（與前部共戒" in line and w != u"－":
                    bad.append(u"%s：第%s號為與前部共戒（律不別宣），書中欄卻指『%s』" % (stem, tag, w))
            elif u"書中：" in line and line != u"｜書中：":
                bad.append(u"%s：附錄第 %d 行有『書中：』而不成歷號式：%s" % (stem, j + 1, line[:26]))
            j += 1
        if seen != list(range(1, n + 1)):
            miss = sorted(set(range(1, n + 1)) - set(seen))
            dup = sorted({x for x in seen if seen.count(x) > 1})
            bad.append(u"%s：歷號缺 %s／重 %s｜實列 %d 行" % (stem, miss[:12], dup, len(seen)))
        if nsx is not None and nsx != ntxt:
            bad.append(u"%s：篇題自報別宣 %d，實數 %d" % (stem, nsx, ntxt))
        tot += len(seen)
        hit += nhit
        print(u"  %s戒｜%-16s｜歷號 %3d／%3d｜有戒文 %3d｜書中案例 %3d"
              % (fam, stem, len(seen), n, ntxt, nhit))
        i = j
    exp_p = {(u"比", k) for k in BHR} | {(u"尼", k) for k in (u"波羅夷", u"僧殘", u"捨墮", u"單提")}
    if got != exp_p:
        bad.append(u"篇之有無不合：缺 %s／多 %s" % (sorted(exp_p - got), sorted(got - exp_p)))
    want_tot = sum(BHR.values()) + sum(NIR[k] for k in (u"波羅夷", u"僧殘", u"捨墮", u"單提"))
    if tot != want_tot:
        bad.append(u"歷號總數 %d，兩部戒本應 %d" % (tot, want_tot))
    print(u"== 歷號共 %d 號（合列行已展開）｜書中已標案例 %d 條（書中案例位置共 %d 處可指）" % (tot, hit, len(live)))
    if bad:
        for b in bad[:20]:
            print(u"  ✗ " + b)
        raise SystemExit(u"附錄稽核不合格：%d 項" % len(bad))
    print(u"合格：每一條皆有戶口，指針俱可達，自報俱實")


def drift():
    import os
    """四之檢：書中附錄＝產生器草稿？凡例含產生器現算之通數句？"""
    import contextlib
    import io as _io
    import os
    raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
    a = raw.find(u"# 附錄")
    assert a >= 0, u"書中查無附錄"
    book_apx = raw[a:].replace(u"\r\n", u"\n").rstrip(u"\n")
    ap = os.path.join(os.path.dirname(os.path.abspath(__file__)), u"appendix_jieben.md")
    md = io.open(ap, encoding="utf-8", newline=u"").read().replace(u"\r\n", u"\n").rstrip(u"\n")
    import contextlib as _cl
    # 遮其噪音須用真檔（產生器會 sys.stdout.reconfigure，StringIO 無此法）
    _dn = open(os.devnull, "w", encoding="utf-8")
    with _cl.redirect_stdout(_dn):
        import gen_appendix as G
    _dn.close()
    tong = G._TONG
    bad = []
    if book_apx.replace(u"\n \n", u"\n") != md.replace(u"\n \n", u"\n"):
        n = sum(1 for x, y in zip(book_apx.split(u"\n"), md.split(u"\n")) if x != y)
        bad.append(u"書中附錄與產生器草稿不合（首 %d 行有差／草稿 %d 行）——換版未重算，或書被直改" % (n, len(md.split(u"\n"))))
    if tong not in book_apx:
        bad.append(u"凡例缺產生器現算之『至通數之別』句——md 為舊版")
    print(u"漂移檢｜書附錄 %d 行／草稿 %d 行｜通數句：%s" % (
        len(book_apx.split(u"\n")), len(md.split(u"\n")), u"在" if tong in book_apx else u"缺"))
    if bad:
        for b in bad:
            print(u"  ✗ " + b)
        raise SystemExit(u"附錄漂移：%d 項" % len(bad))


if __name__ == u"__main__":
    main()
    drift()
