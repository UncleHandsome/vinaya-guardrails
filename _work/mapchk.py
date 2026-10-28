# -*- coding: utf-8 -*-
"""十線地圖指針尺（mapchk・第 75 輪立）：卷首《十線地圖》之行・指針・宣稱・形制四目對合。
一、指針：每一表格行之『書中位置』須為書中實存之案例或小節；其『條號』須與附錄倒排所指同一位置
    （法源＝書中附錄《全戒本歷條總表》，本尺不另立第二套落點）。
二、宣稱：①導言「十線共X行，點名Y案」須等於實數；②「第N章（M案）」須等於該章案例實數；
    ③標題與導引中以「N 場／N 樁」計該線行數者，須等於該線實有之表格行數。
三、形制：十線之 H2 序號連貫（一〜十）；每一線須有導引段（題與表之間有文）與『現代維度』段。
四、《附記》之『抽哪幾線』須覆蓋一〜十，不得有線無所歸（語義之當否非尺所能判，只判有無所歸）。
口徑兩則（豁免亦是宣稱，故記於此）：①散句中之『一樁／一場』多作冠詞（如『禁了一樁』），不計為行數宣稱；
②『點名Y案』唯計指到案例之行之去重者，指到小節者（『第N章第X節』）不算一案。
管轄自印：線數・資料行數・點名句數・涉章數・附錄鍵數俱當場印出（殭尺之綠非綠）。
用法：python -X utf8 _work/mapchk.py [-v]
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
        if ch == u"千":
            tot += (cur or 1) * 1000
            cur = 0
        elif ch == u"百":
            tot += (cur or 1) * 100
            cur = 0
        elif ch == u"十":
            tot += (cur or 1) * 10
            cur = 0
        elif ch in S:
            cur = S.index(ch)
    return tot + cur


def _cn(n):
    """漢字數詞（與 cn2int 互逆，刀之宣稱即取此形）。"""
    D = u"一二三四五六七八九"
    if n == 0:
        return u"零"
    if n < 0 or n > 999:
        return str(n)
    parts = []
    h, r = divmod(n, 100)
    if h:
        parts.append(D[h - 1] + u"百")
    t, o = divmod(r, 10)
    if t:
        parts.append((D[t - 1] if (t > 1 or h) else u"") + u"十")
    elif r and h:
        parts.append(u"零")
    if o:
        parts.append(D[o - 1])
    return u"".join(parts)


CH = re.compile(u"^# 第([一二三四五六七八九十百]+)章")
SEC = re.compile(u"^### ([一二三四五六七八九十]+)、 ?(.*)")
CASE = re.compile(u"^#### 案例([一二三四五六七八九十百]+)[：:]")
ROW = re.compile(u"^\\|\\s*([^|]+?)\\s*\\|\\s*([^|]+?)\\s*\\|\\s*([^|]+?)\\s*\\|")
MPCASE = re.compile(u"^第([一二三四五六七八九十百]+)章案例([一二三四五六七八九十百]+)$")
MPSEC = re.compile(u"^第([一二三四五六七八九十百]+)章第([一二三四五六七八九十百]+)"
                   u"(?:、([一二三四五六七八九十]+))?(?:節)?(.*)$")
HDR = re.compile(u"^## ([甲乙])、比丘尼?戒本：(.+?)（戒本")
NUM = re.compile(u"^(\\d+)(?:～(\\d+))?\\.\\s")
POS = re.compile(u"書中：(.+?)\\s*$")
KEYS = (u"波羅夷", u"僧殘", u"二不定", u"捨墮", u"單提", u"提舍尼", u"眾學", u"七滅諍")


def nums_of(tiao):
    seg = tiao[tiao.index(u"第") + 1:]
    if u"條" in seg:
        seg = seg[:seg.rindex(u"條")]
    ns = []
    for part in seg.split(u"、"):
        part = part.strip()
        if u"～" in part:
            x, y = part.split(u"～")
            if x.isdigit() and y.isdigit():
                ns.extend(range(int(x), int(y) + 1))
        elif part.isdigit():
            ns.append(int(part))
    return ns


def structure(L):
    apx = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
    mlo = next(i for i, s in enumerate(L) if s.startswith(u"# 十線地圖"))
    mhi = next(i for i in range(mlo + 1, len(L)) if L[i].startswith(u"# 【"))
    cases, secs, cur = {}, {}, None
    for i in range(mhi, apx):
        s = L[i]
        m = CH.match(s)
        if m:
            cur = cn2int(m.group(1))
            continue
        if cur is None:
            continue
        m = SEC.match(s)
        if m:
            secs[(cur, cn2int(m.group(1)))] = m.group(2)
        m = CASE.match(s)
        if m:
            cases[(cur, cn2int(m.group(1)))] = m.group(0)
    inv, curp = {}, None
    for s in L[apx:]:
        h = HDR.match(s)
        if h:
            curp = (u"尼" if h.group(1) == u"乙" else u"比", h.group(2))
            continue
        m = NUM.match(s)
        if not (curp and m):
            continue
        p = POS.search(s)
        a = int(m.group(1))
        vals = [x.strip() for x in re.split(u"、", p.group(1))] if p else []
        for n in range(a, int(m.group(2) or m.group(1)) + 1):
            inv[(curp[0], curp[1], n)] = vals
    h2 = [(i, L[i]) for i in range(mlo, mhi) if L[i].startswith(u"## ")]
    lines = []
    for k, (i, t) in enumerate(h2):
        j = h2[k + 1][0] if k + 1 < len(h2) else mhi
        body = L[i:j]
        rows = []
        tab = next((q for q, s in enumerate(body) if s.startswith(u"|")), None)
        for q, s in enumerate(body):
            cells = [x.strip() for x in s.strip().strip(u"|").split(u"|")]
            if len(cells) < 2 or set(cells[0]) <= set(u"- ") or cells[0].startswith(u"書中位置") or cells[0] == u"想談的事":
                continue
            rows.append((i + 1 + q, cells[0], cells[1], cells[2] if len(cells) > 2 else u"".join(cells[1:])))
        intro = [s for s in body[1:tab] if s.strip()] if tab is not None else [s for s in body[1:] if s.strip()]
        lines.append({"ln": i + 1, "k": k + 1, "title": t[3:].strip(), "rows": rows,
                      "intro": intro, "has_mod": any(u"現代維度" in s for s in body),
                      "end": j})
    return mlo, mhi, apx, lines, cases, secs, inv


def row_problems(L):
    """每一表格行：位置須實存，條號須與附錄倒排同一落點。刀與尺同取此函（單一法源）。"""
    mlo, mhi, apx, lines, cases, secs, inv = structure(L)
    data = [r for x in lines if not x["title"].startswith(u"附記") for r in x["rows"]]
    bad = []
    for ln_, pos, tiao, _d in data:
        m = MPCASE.match(pos)
        m2 = None if m else MPSEC.match(pos)
        if not m and not m2:
            bad.append((ln_, u"位置形制", u"%s｜%s" % (pos, tiao)))
            continue
        if m:
            if (cn2int(m.group(1)), cn2int(m.group(2))) not in cases:
                bad.append((ln_, u"案例查無", pos))
                continue
        else:
            c = cn2int(m2.group(1))
            js = [cn2int(m2.group(2))] + ([cn2int(m2.group(3))] if m2.group(3) else [])
            if any((c, j) not in secs for j in js):
                bad.append((ln_, u"小節查無", pos))
        if u"第" in tiao and u"條" in tiao:
            who = u"尼" if tiao.startswith(u"尼") else u"比"
            key = next((x for x in KEYS if x in tiao), None)
            if not key:
                bad.append((ln_, u"篇名未識", tiao))
                continue
            hit = set()
            for n in nums_of(tiao):
                got = [v for (w, p, k2), v in inv.items() if w == who and key in p and k2 == n]
                if not got:
                    bad.append((ln_, u"號查無", u"%s 第%s條" % (tiao, n)))
                for g in got:
                    hit |= set(g)
            if pos not in hit:
                bad.append((ln_, u"與附錄不合", u"%s｜附錄指：%s" % (pos, u"／".join(sorted(hit)) or u"查無")))
    return bad


def check():
    L = load()
    mlo, mhi, apx, lines, cases, secs, inv = structure(L)
    xian = [x for x in lines if not x["title"].startswith(u"附記")]
    data = [r for x in xian for r in x["rows"]]
    bad = []
    for x in xian:
        if not x["title"].startswith(u"%s、" % _cn(x["k"])):
            bad.append((x["ln"], u"線序", u"第 %d 之題作『%s』" % (x["k"], x["title"][:12])))
        if not x["intro"]:
            bad.append((x["ln"], u"導引", u"%s線無導引段（題與表直接相連）" % _cn(x["k"])))
        if not x["has_mod"]:
            bad.append((x["ln"], u"現代維度", u"%s線缺『現代維度』段" % _cn(x["k"])))
        for m in re.finditer(u"([一二三四五六七八九十百]+)(場|樁)", x["title"] + u"".join(x["intro"])):
            # 口徑：『一樁／一場』在散句中多作冠詞（『禁了一樁』），不計為行數宣稱——此即本尺之豁免，如實記於此。
            if cn2int(m.group(1)) <= 1:
                continue
            if cn2int(m.group(1)) != len(x["rows"]):
                bad.append((x["ln"], u"行數宣稱", u"稱『%s%s』而%s線實 %d 行" %
                            (m.group(1), m.group(2), _cn(x["k"]), len(x["rows"]))))
    bad += row_problems(L)
    it = u"".join(L[mlo:xian[0]["ln"] - 1])
    m = re.search(u"十線共([一二三四五六七八九十百]+)行，點名([一二三四五六七八九十百]+)案", it)
    # 『案』唯計指到案例者；指到小節（『第N章第X節』）之行不算一案——程序之落點不得冒充案例之戶口。
    ncase = len({r[1] for r in data if MPCASE.match(r[1])})
    if not m:
        bad.append((mlo + 1, u"導言無數", u"未見『十線共X行，點名Y案』之如實自報"))
    elif (cn2int(m.group(1)), cn2int(m.group(2))) != (len(data), ncase):
        bad.append((mlo + 1, u"導言行案宣稱", u"稱 %d 行・%d 案｜實 %d 行・%d 案" %
                    (cn2int(m.group(1)), cn2int(m.group(2)), len(data), ncase)))
    for mm in re.finditer(u"第([一二三四五六七八九十百]+)章（([一二三四五六七八九十百]+)案）", it):
        c = cn2int(mm.group(1))
        per = len([k for k in cases if k[0] == c])
        if cn2int(mm.group(2)) != per:
            bad.append((mlo + 1, u"章案宣稱", u"稱第%s章（%s案）｜實 %d 案" % (mm.group(1), mm.group(2), per)))
    for mm in re.finditer(u"([一二三四五六七八九十]+)章合計([一二三四五六七八九十百]+)案", it):
        chs = {cn2int(x) for x in re.findall(u"第([一二三四五六七八九十百]+)章", it[max(0, mm.start() - 120):mm.start()])}
        ssum = sum(len([k for k in cases if k[0] == c]) for c in chs)
        if cn2int(mm.group(1)) != len(chs) or cn2int(mm.group(2)) != ssum:
            bad.append((mlo + 1, u"合計宣稱", u"稱 %s 章合計 %s 案｜窗口內 %d 章實 %d 案" %
                        (mm.group(1), mm.group(2), len(chs), ssum)))
    fu = [x for x in lines if x["title"].startswith(u"附記")]
    if not fu:
        bad.append((mhi, u"附記查無", u"末段《附記》不在"))
    else:
        cov = set()
        for _l, a, b, _c in fu[0]["rows"]:
            for t in re.findall(u"[一二三四五六七八九十]+", b):
                v = cn2int(t)
                if 1 <= v <= 10:
                    cov.add(v)
        missx = [i for i in range(1, 11) if i not in cov]
        if missx:
            bad.append((fu[0]["ln"], u"附記未覆蓋", u"第 %s 線無所歸" % u"、".join(_cn(i) for i in missx)))
    print(u"管轄｜十線 %d・資料行 %d・點名 %d 案・涉章 %d・案例戶口 %d・附錄鍵 %d" % (
        len(xian), len(data), ncase, len({r[1][:r[1].index(u"章") + 1] for r in data}), len(cases), len(inv)))
    if u"-v" in sys.argv:
        for x in xian:
            print(u"  L%-5d %-32s 行 %d・導引 %d 段・現代維度 %s" % (
                x["ln"], x["title"][:28], len(x["rows"]), len(x["intro"]),
                u"有" if x["has_mod"] else u"無"))
    print(u"判：指針・宣稱・形制・附記四目俱中" if not bad else u"判：%d 目病" % len(bad))
    for x in bad:
        print(u"  L%-5d %s｜%s" % (x[0], x[1], x[2]))
    return len(data), ncase, bad


def load():
    return io.open(BOOK, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")


if __name__ == u"__main__":
    _r, _c, b = check()
    sys.exit(1 if b else 0)
