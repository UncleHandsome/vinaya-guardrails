# -*- coding: utf-8 -*-
"""新冊解析器：讀 `_archive/舊本/` 兩冊（只讀一字不動），切成章・節・案例卡之可用塊。

章＝H1・節＝H3・框架卡＝H4（欄目 H5）・護欄案＝H4（欄目為項目符標籤）。
框架卡之標題層唯 H4 一線可斷卡，其 H5 欄目屬卡身（第三十八輪之實測教訓）。
"""
import io, re, os

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


def read(path):
    return io.open(path, encoding="utf-8").read().replace(u"\r\n", u"\n").split(u"\n")


def head_blocks(lines, lvl, pat):
    """某層標題依正則切塊，返 [(標題, 起, 迄)]（迄含至下一同層或更淺層前）。"""
    hs = [(i, re.match(r"^(#{%d}) (.*)$" % lvl, l)) for i, l in enumerate(lines, 1)]
    marks = [(i, m.group(2)) for i, m in hs if m and re.search(pat, m.group(2))]
    allmarks = [i for i, m in hs if m and len(m.group(1)) <= lvl]
    out = []
    for k, (i, t) in enumerate(marks):
        nxt = [j for j in allmarks if j > i]
        out.append((t, i, nxt[0] - 1 if nxt else len(lines)))
    return out


class Book(object):
    """一冊之切塊器。"""

    def __init__(self, lines):
        self.lines = lines
        self.h = [(i, len(m.group(1)), m.group(2))
                  for i, l in enumerate(lines, 1) for m in [re.match(r"^(#{1,6}) (.*)$", l)] if m]

    def slice(self, a, b):
        return u"\n".join(self.lines[a - 1:b]).rstrip()

    def find_h1(self, pat):
        for i, lvl, t in self.h:
            if lvl == 1 and re.search(pat, t):
                return (t, i)
        return None

    def block(self, pat, lvl=1):
        """首個命中之標題塊，返 (標題, 該塊文本)。"""
        marks = [(i, t) for i, l2, t in self.h if l2 == lvl and re.search(pat, t)]
        if not marks:
            return None
        i, t = marks[0]
        nxt = [j for j, l2, _ in self.h if l2 <= lvl and j > i]
        return (t, self.slice(i, nxt[0] - 1 if nxt else len(self.lines)))

    def secs(self, a, b, lvl=3):
        """塊內某層標題清單 [(標題, 起, 迄)]。"""
        ms = [(i, t) for i, l2, t in self.h if l2 == lvl and a <= i <= b]
        out = []
        for k, (i, t) in enumerate(ms):
            e = ms[k + 1][0] - 1 if k + 1 < len(ms) else b
            out.append((t, i, e))
        return out

    def sec(self, a, b, sub, lvl=3):
        for t, i, e in self.secs(a, b, lvl):
            if sub in t:
                return self.slice(i, e)
        return None

    def minus(self, text, seg):
        """從整塊中挖去其中一段（挖後以空行補位，不留殘行）。"""
        if not seg or seg not in text:
            return text
        return text.replace(seg, u"").replace(u"\n\n\n\n", u"\n\n")


FW_PATH = u"ver38四分律_起心動念心智分析框架_修正版.md"
HL_PATH = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"


def load(root):
    fw = Book(read(os.path.join(root, u"_archive", u"舊本", FW_PATH)))
    hl = Book(read(os.path.join(root, u"_archive", u"舊本", HL_PATH)))
    return fw, hl


# ── 框架卡 ──────────────────────────────────────────────────────────────────
CARD_RE = re.compile(r"^#### 〔(遮|開|僧|補遺)(\d+)〕(.*)$")
FIELD_RE = re.compile(r"^##### (.+)$")


def fw_cards(fw):
    """返 {碼: dict(title, head, body, fields{}, quote)}。"""
    out = {}
    marks = [(i, CARD_RE.match(l)) for i, l in enumerate(fw.lines, 1)]
    marks = [(i, m) for i, m in marks if m]
    for k, (i, m) in enumerate(marks):
        code = u"〔%s%s〕" % (m.group(1), m.group(2))
        nxt = [j for j, _ in marks[k + 1:]]
        shallower = [j for j, l2, _ in fw.h if l2 <= 4 and j > i]
        e = min([x for x in [nxt[0] - 1 if nxt else None] + [shallower[0] - 1 if shallower else None]
                 if x is not None] + [len(fw.lines)])
        body = fw.slice(i + 1, e)
        fields, cur, buf = {}, None, []
        quote = []
        for l in body.split(u"\n"):
            fm = FIELD_RE.match(l)
            if fm:
                if cur:
                    fields[cur] = u"\n".join(buf).strip()
                cur, buf = fm.group(1).strip(), []
                continue
            if l.startswith(u"◎"):
                if cur:
                    fields[cur] = u"\n".join(buf).strip()
                cur, buf = u"律藏原文", []
                continue
            buf.append(l)
        if cur:
            fields[cur] = u"\n".join(buf).strip()
        out[code] = dict(title=m.group(3).strip(), fields=fields, body=body)
    return out


# ── 護欄案 ──────────────────────────────────────────────────────────────────
HL_CASE_RE = re.compile(r"^#### 案例([一二三四五六七八九十]+)：(.*)$")
HL_FIELD_RE = re.compile(r"^\*\s*\*\*【([^】]{2,18})】：\*\*(.*)$")


def hl_cases(hl, chap_a, chap_b):
    """某章內之案例卡 [(序, 題, {欄: 文}, 律文引)]。"""
    marks = []
    for i in range(chap_a, chap_b + 1):
        m = HL_CASE_RE.match(hl.lines[i - 1])
        if m:
            marks.append((i, m))
    out = []
    for k, (i, m) in enumerate(marks):
        e = (marks[k + 1][0] - 1) if k + 1 < len(marks) else chap_b
        body = hl.slice(i + 1, e)
        parts, cur, buf, quotes = {}, None, [], []
        for l in body.split(u"\n"):
            fm = HL_FIELD_RE.match(l)
            if fm:
                if cur:
                    parts[cur] = u"\n".join(buf).strip()
                cur, buf = fm.group(1), [fm.group(2).strip()]
                continue
            if cur is None and l.startswith(u">"):
                quotes.append(l)
                continue
            if cur is not None:
                buf.append(l)
        if cur:
            parts[cur] = u"\n".join(buf).strip()
        out.append((cnum(m.group(1)), m.group(2).strip(), parts, u"\n".join(quotes).strip(), body))
    return out
