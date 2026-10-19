# -*- coding: utf-8 -*-
"""節序之治：一書一制。每章之節標題統為「第N節」，並隨手把指針舊序改寫為新序。

法則：凡章內節號已自一連貫且同制者，一字不動（其指針自亦不變）；
      唯混制・跳號・斷頭之章才重編，重編時立｛舊序→新序｝之映射，指針據此改寫，
      故『第N章第M節』之形永不失指。
      又一章之節散置數章者（`refmap.SPAN`），其『第M節』在散置後已不屬於任何單一章次，
      此處另以源節之實文為錨、就冊身量其落點（`resolve_span`），不以節序臆推。
"""
import re
from collections import defaultdict

CN = {c: i for i, c in enumerate(u"零一二三四五六七八九")}


def cnum(s):
    if s in CN:
        return CN[s]
    if s == u"十":
        return 10
    if u"十" not in s:
        return 0
    a, _, b = s.partition(u"十")
    return (1 if not a else CN.get(a, 0)) * 10 + CN.get(b, 0)


def cn_num(n):
    d = u"零一二三四五六七八九"
    if n < 10:
        return d[n]
    if n == 10:
        return u"十"
    if n < 20:
        return u"十" + (d[n % 10] if n % 10 else u"")
    a, b = divmod(n, 10)
    return d[a] + u"十" + (d[b] if b else u"")


H2J = re.compile(u"^## 第([一二三四五六七八九十]+)節[　 ]*(.*)$")
H2N = re.compile(u"^## ([一二三四五六七八九十]+)、[　 ]*(.*)$")


def plan_chapter(lines):
    """返 [(行序, 式, 舊序, 標題)]。"""
    out = []
    for k, l in enumerate(lines):
        m = H2J.match(l)
        if m:
            out.append((k, u"J", cnum(m.group(1)), m.group(2)))
            continue
        m = H2N.match(l)
        if m:
            out.append((k, u"N", cnum(m.group(1)), m.group(2)))
    return out


def needs_fix(items):
    if len(items) < 2:
        return False
    nums = [n for _, _, n, _ in items]
    kinds = set(k for k, _, _, _ in items)
    if len(kinds) > 1:
        return True
    return nums != list(range(1, len(nums) + 1))


def renumber(text):
    """重編節號並回傳指針映射 {(章名, 舊序, 式) : 新序}；舊序在一章之內兩出者，
       其映射即撤（一序兩指則算不得落點），留予『散點歸章』『指名歸位』二尺落之，並列入了帳。"""
    lines = text.split(u"\n")
    h1 = [i for i, l in enumerate(lines) if l.startswith(u"# ") and not l.startswith(u"# 【")]
    h1 = [i for i in h1 if re.match(u"^# 第[一二三四五六七八九十]+章　", lines[i]) or
          re.match(u"^# 附錄|終卷", lines[i])]
    h1p = h1 + [len(lines)]
    refmap = {}
    fixed = []
    clash = []
    blocked = set()
    for a, b in zip(h1p[:-1], h1p[1:]):
        title = lines[a]
        m = re.match(u"^# (第[一二三四五六七八九十]+章　?|附錄[一二三四五]|終卷)", title)
        ch = m.group(1).replace(u"　", u"") if m else u""
        if not ch.startswith(u"第"):
            continue
        if not ch.endswith(u"章"):
            ch = ch + u"章"
        items = plan_chapter(lines[a + 1:b])
        if not needs_fix(items):
            continue
        for k, (off, kind, old, name) in enumerate(items, 1):
            lines[a + 1 + off] = u"## 第%s節　%s" % (cn_num(k), name)
            key = (ch, kind, old)
            if key in refmap and refmap[key] != k:
                clash.append(u"%s 舊%s%s｜先取第%d節 又有第%d節（%s）" % (
                    ch, kind, cn_num(old), refmap[key], k, name[:18]))
                blocked.add(key)
            refmap.setdefault(key, k)
        fixed.append(ch)
    for key in blocked:
        refmap.pop(key, None)
    return u"\n".join(lines), refmap, fixed, clash


def rewrite_refs(text, refmap):
    """據映射改寫『第N章第M節』——舊序不分式，先取 J 式，次取 N 式。"""
    n = [0]

    def one(m):
        ch = u"第%s章" % m.group(1)
        old = cnum(m.group(2))
        new = refmap.get((ch, u"J", old)) or refmap.get((ch, u"N", old))
        if not new:
            return m.group(0)
        n[0] += 1
        return u"%s第%s節" % (ch, cn_num(new))
    t = re.sub(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節", one, text)
    return t, n[0]


# ── 散點歸章：一章之節散置數章者，其『範圍＋節』指針依節身實文算落點 ─────────
CHAP_H1 = re.compile(u"^# (第[一二三四五六七八九十]+章)　")
SEC_H2 = re.compile(u"^## 第([一二三四五六七八九十]+)節[　 ]*(.*)$")
SRC_SEC = re.compile(u"^(?:第)?([一二三四五六七八九十]+)(?:節|、)")


def sec_blocks(lines):
    """冊身節塊索引：[(章名, 節序, 起行, 迄行)]（行序自 1，迄行含下一節或下一章之前一行）。"""
    out = []
    ch = None
    for i, l in enumerate(lines, 1):
        if l.startswith(u"# "):
            if out:
                out[-1][3] = i - 1
            m = CHAP_H1.match(l)
            ch = m.group(1) if m else None
            continue
        m = SEC_H2.match(l)
        if m and ch:
            if out:
                out[-1][3] = i - 1
            out.append([ch, cnum(m.group(1)), i, len(lines)])
    return [tuple(x) for x in out]


def body_anchors(src, a, b):
    """源節之錨：節身内取足八字之實句首段，最多六條，逐條候選。"""
    out = []
    for l in src.lines[a: min(b, a + 40)]:
        t = l.strip()
        if not t or t.startswith((u"#", u"|", u">", u"-", u"*", u"`")):
            continue
        t = re.sub(u"[*_`]+", u"", t).strip()
        m = re.search(u"[\\u3400-\\u9fff]{8,}", t)
        if m:
            out.append(m.group(0)[:12])
        if len(out) >= 6:
            break
    return out


def span_pattern(name):
    """混合名之正则：『第十四、十五章』容『、第十五章』之重迭第字。"""
    parts = re.split(u"([、至])", name)
    return u"".join(p + u"第?" if p in (u"、", u"至") else p for p in parts)


def resolve_span(text, books, span):
    """散置之章既已分隸數章，指其節者必落一章一節——以源節實文為錨，就冊身量其落點。
       錨無著、或落點越出候落之章、或兩處並立者，如實報錯，不代擬一個『看得過去』的章節。"""
    lines = text.split(u"\n")
    blocks = sec_blocks(lines)
    hits = defaultdict(list)
    for c, o, a, b in blocks:
        for i in range(a, b + 1):
            hits[i] = (c, o)
    land = {}
    rows = []
    for name, (key, pat, cands) in span.items():
        obj = books[key]
        top = obj.find_h1(pat)
        if not top:
            raise SystemExit(u"散點歸章：源章佚（%s %s）" % (key, pat))
        _, i = top
        nxt = [j for j, l2, _ in obj.h if l2 <= 1 and j > i]
        e = nxt[0] - 1 if nxt else len(obj.lines)
        for st, sa, sb in obj.secs(i, e, 3):
            m = SRC_SEC.match(st.strip())
            if not m:
                continue
            om = cnum(m.group(1))
            got = None
            for anc in body_anchors(obj, sa - 1, sb):
                found = set()
                for n, l in enumerate(lines, 1):
                    if anc in l and n in hits:
                        found.add(hits[n])
                inb = [f for f in found if f[0] in cands]
                if len(inb) == 1:
                    got = inb[0]
                    break
                if len(inb) > 1:
                    raise SystemExit(u"散點歸章：錨%s 兩出於 %s" % (
                        anc, u"／".join(u"%s 第%s節" % (f[0], cn_num(f[1])) for f in sorted(inb))))
            if not got:
                raise SystemExit(u"散點歸章：%s 源第%s節之錨無著於 %s" % (name, cn_num(om), u"／".join(cands)))
            land[(name, om)] = got
            rows.append(u"%s 源%s → 冊%s第%s節" % (name, cn_num(om), got[0], cn_num(got[1])))
    n = [0]

    def make(name):
        def one(m):
            ords = [cnum(x) for x in re.findall(u"[一二三四五六七八九十]+", m.group(1))]
            got = []
            for o in ords:
                k = (name, o)
                if k not in land:
                    raise SystemExit(u"散點歸章：指針『%s』之第%s節無落點可算" % (m.group(0), cn_num(o)))
                got.append(land[k])
            n[0] += 1
            if len(set(g[0] for g in got)) == 1:
                return u"%s第%s節" % (got[0][0], u"、".join(cn_num(g[1]) for g in got))
            return u"、".join(u"%s第%s節" % (g[0], cn_num(g[1])) for g in got)
        return one

    pats = [(re.compile(u"%s(第[一二三四五六七八九十]+(?:、第?[一二三四五六七八九十]+)*節)" % span_pattern(k)),
             make(k)) for k in span]
    res = []
    for l in lines:
        if not l.startswith(u"#"):
            for rx, fn in pats:
                l = rx.sub(fn, l)
        res.append(l)
    return u"\n".join(res), n[0], rows


# ── 指名之指針：自報節題或款號者，據冊身實題實數歸位（章序算錯者由此糾正）──────
Q1 = re.compile(u"(第[一二三四五六七八九十]+章第[一二三四五六七八九十]+節)"
                u"([（(〔【·、；：， ]*)([『「])([^』」]{3,26})([』」])")
Q2 = re.compile(u"([『「])([^』」]{3,26})([』」])([）)〕】 ]*)"
                u"(第[一二三四五六七八九十]+章第[一二三四五六七八九十]+節)")
KU = re.compile(u"(第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節)(第|其)([一二三四五六七八九十]+)(款|項)")
ITEM_RX = [re.compile(u"^#{3,4} ([一二三四五六七八九十]+)、", re.M),
           re.compile(u"^#{3,4} (?:第)?([一二三四五六七八九十]+)[.．]", re.M),
           re.compile(u"第([一二三四五六七八九十]+)款"),
           re.compile(u"其([一二三四五六七八九十]+)")]


def sec_texts(lines):
    """{(章名, 第N節) : 節身文本}。"""
    st = {}
    for c, o, a, b in sec_blocks(lines):
        st[(c, u"第%s節" % cn_num(o))] = u"\n".join(lines[a - 1:b])
    return st


def flat_texts(lines):
    """以『第五章第二節』这样一字一鍵之形索引節身，供指針直接比對。"""
    return {u"".join(k): v for k, v in sec_texts(lines).items()}


def item_labels(body):
    out = set()
    for rx in ITEM_RX:
        out |= set(cnum(x) for x in rx.findall(body))
    return out


def land_named(text):
    """指針自報其節題（『第X章第Y節「T」』或『「T」（第X章第Y節）』），T 即落點之證：
       T 唯見於一節者，指針歸那一節；T 無著或兩出者不強改，如實列出交由尺退回。
       同法施於款級：所言之款不在其節，而本章他節獨有其款者，即歸他節。"""
    moved = []
    stuck = []
    done = set()

    def halt(msg):
        if msg not in stuck:
            stuck.append(msg)

    def pass_once(t):
        st = sec_texts(t.split(u"\n"))

        def home(nm):
            got = [k for k in st if nm in st[k]]
            if len(got) == 1:
                return got[0], None
            return None, got

        def refix(m, first):
            if first:
                ref, mid, o1, nm, c1 = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            else:
                o1, nm, c1, mid, ref = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            h, many = home(nm)
            if h is None and not many:
                halt(u"「%s」無著（指%s）" % (nm, ref))
                return m.group(0)
            if h is None:
                halt(u"「%s」兩出（指%s）：%s" % (
                    nm, ref, u"／".join(u"".join(k) for k in many)))
                return m.group(0)
            new = u"".join(h)
            if new == ref:
                return m.group(0)
            if (ref, new, nm) not in done:
                done.add((ref, new, nm))
                moved.append(u"%s → %s（据節題「%s」）" % (ref, new, nm))
            return (new + mid + o1 + nm + c1) if first else (o1 + nm + c1 + mid + new)

        t = Q1.sub(lambda m: refix(m, True), t)
        t = Q2.sub(lambda m: refix(m, False), t)

        st = flat_texts(t.split(u"\n"))

        def kfix(m):
            ref, k = m.group(1), cnum(m.group(5))
            if ref not in st:
                halt(u"%s 節佚（欲指其款%s）" % (ref, cn_num(k)))
                return m.group(0)
            if k in item_labels(st[ref]):
                return m.group(0)
            chp = re.match(u"第[一二三四五六七八九十]+章", ref).group(0)
            same = [q for q in st if q.startswith(chp) and k in item_labels(st[q])]
            whole = [q for q in st if k in item_labels(st[q])]
            pick = same if len(same) == 1 else (whole if len(whole) == 1 else [])
            if not pick:
                halt(u"款%s 不在%s（同章候選%d・全冊%d）" % (
                    cn_num(k), ref, len(same), len(whole)))
                return m.group(0)
            new = pick[0]
            if (ref, new, u"款%s" % cn_num(k)) not in done:
                done.add((ref, new, u"款%s" % cn_num(k)))
                moved.append(u"%s → %s（据款%s）" % (ref, new, cn_num(k)))
            return new + m.group(4) + m.group(5) + m.group(6)

        return KU.sub(kfix, t)

    t = pass_once(text)
    t = pass_once(t)          # 兩輪：第一輪歸位之後，節內實數已變，再核一次以免餘漏
    return t, moved, stuck


# ── 章級指針之自證：指針若緊冠某章之章題關鍵語，落點即該章 ─────────────────
CHAPTER_H1 = re.compile(u"^# (第[一二三四五六七八九十]+章)[　 ]+(.*)$")
TITLE_KEY = re.compile(u"[\\u3400-\\u9fff]{4,10}")
SEP_ALL = re.compile(u"[，、・：；（）【】｜—─·與及暨\\s]+")
REF_H = re.compile(u"第(?:[一二三四五六七八九十]+|[一二三四五六七八九十]+、[一二三四五六七八九十]+"
                   u"|[一二三四五六七八九十]+至第?[一二三四五六七八九十]+)章")


def chapter_map(lines):
    """{章名 : （章題, 章身文本)}。"""
    out = {}
    cur = None
    t = u""
    buf = []
    for l in lines:
        m = CHAPTER_H1.match(l)
        if m:
            if cur:
                out[cur] = (t, u"\n".join(buf))
            cur, t, buf = m.group(1), m.group(2), []
            continue
        if l.startswith(u"# ") and cur:
            out[cur] = (t, u"\n".join(buf))
            cur, buf = None, []
            continue
        if cur:
            buf.append(l)
    if cur:
        out[cur] = (t, u"\n".join(buf))
    return out


def title_owners(cmap):
    """{章題關鍵語 : [所屬章]}——章題之詞唯歸其章。"""
    own = {}
    for ch, (t, _) in cmap.items():
        for seg in SEP_ALL.split(t):
            for w in TITLE_KEY.findall(seg):
                own.setdefault(w, [])
                if ch not in own[w]:
                    own[w].append(ch)
    return own


def land_chapter_claims(text, skip=()):
    """指針之後（或之前）若緊接某章之章題關鍵語，該語便是它自我申報的落點；
       所冠之章與關鍵語所屬之章不合者歸其所屬；關鍵語兩屬者不改，如實呈報。"""
    lines = text.split(u"\n")
    own = title_owners(chapter_map(lines))
    moved = []
    stuck = []
    words = sorted(own, key=len, reverse=True)
    words = [w for w in words if w not in skip]

    def fix(l):
        out = u""
        pos = 0
        for m in REF_H.finditer(l):
            out += l[pos:m.start()]
            ref = m.group(0)
            nxt = l[m.end(): m.end() + 3]
            if nxt.startswith(u"案例") or re.match(u"第[0-9]", nxt):
                out += ref          # 案級／條級之指針已由產器落地，此处只治章級之誤冠
                pos = m.end()
                continue
            win = l[max(0, m.start() - 8):m.start()] + l[m.end():m.end() + 28]
            hit = None
            for w in words:
                if w in win:
                    chs = own[w]
                    if len(chs) != 1:
                        continue
                    if chs[0] not in ref:
                        hit = (w, chs[0])
                    break
            if hit:
                moved.append(u"%s → %s（據章題『%s』）" % (ref, hit[1], hit[0]))
                out += hit[1]
            else:
                for w in words:
                    if w in win and len(own[w]) > 1:
                        stuck.append(u"%s 所冠『%s』兩屬：%s" % (ref, w, u"／".join(own[w])))
                        break
                out += ref
            pos = m.end()
        return out + l[pos:]

    res = [l if l.startswith(u"#") else fix(l) for l in lines]
    return u"\n".join(res), moved, stuck
