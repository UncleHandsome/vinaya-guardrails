# -*- coding: utf-8 -*-
"""附錄產生器：自《四分律》原文逐篇擷取各條之「結戒宣說」，配上本書既有案例之落點，
   生成「全戒本歷條總表」之 markdown 塊（寫入 _work/appendix_jieben.md，不徑改書檔）。
   律文錨點：每條戒之制戒宣告「集十句義乃至正法久住，欲說戒者當如是說：X。」——X 即該條戒文。
   自證：逐篇計數並與戒本之數相符者全收；律文以數條合宣一篇者（眾學法、尼諸篇之一部），
         如實標為「律文合宣 N 條」，不虚報為全。
用法：python -X utf8 _work/gen_appendix.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk  # noqa: E402  —— 組字碼折正字之單一法源在其 BRACKET_MAP（逐字閘兩側同一口徑）
DISP = [(u"[" + k + u"]", v) for k, v in _tk.BRACKET_MAP.items()]


def disp(t):
    """印面之形：語料之 CBETA 組字碼折為正字（『[真/心]』→『瞋』），無正字可折者存其形。"""
    for a, b in DISP:
        t = t.replace(a, b)
    return t


def inner_q(t):
    """戒文內之引號折為『』：本表以「」為戒文之外框，律文原有之引號須降一層（甲部多已作『』，
       尼部新收之條（八波羅夷六～八・三十捨墮七條）則原文件用「」，不折則兩套書中形不一致。"""
    out = []
    for ch in t:
        out.append({u"「": u"『", u"」": u"』"}.get(ch, ch))
    return u"".join(out)


BOOK = HP.SRC
U = u"零一二三四五六七八九"
DECLARE = re.compile(u"如是說(?:戒)?[：:]")
SPLIT = re.compile(u"集十句義")
# 尾標：『(N)』『(N竟)』之半形全形俱收；容『(N竟』反括號佚失一處（01-10「痛惱所纏。(五竟三十捨墮法之二」）；
# 亦容『(N篇名竟)』——二不定法之末標作「(二不定法竟)」，缺此式則第二條之界不立。
# 「竟」在而反括號佚者方許無閉，故篇內列舉之「(一)」「(三」之屬仍不入界（界之真偽另有閘）。
TAIL = re.compile(u"[(（]([〇零一二三四五六七八九十百]{1,5})[^()]{0,10}?(?:竟[)）]|竟|[)）])")
# 界後另起之因緣語（隨制並宣之條，其界唯以此件與篇內戒文列舉分別）
NIYUAN = re.compile(u"^\\s*(?:爾時|時有|時諸|復次)")
RUN_MIN = 8                             # 連段全同之歷號行，滿此數方合為「a～b.」一行
ENDS = [(u"波羅夷", u"不共住。"), (u"僧殘", u"僧伽婆尸沙。"), (u"捨墮", u"尼薩耆波逸提。"),
        (u"提舍尼", u"波羅提提舍尼。"), (u"學法", u"式叉迦羅尼。"), (u"單提", u"波逸提。"),
        (u"不定", u"不定法。")]

# 篇序：(部, 篇名, 章標題, 罪級, 戒本應有條數, 原文檔)
PLAN = [
    (u"甲、比丘戒本", u"四波羅夷法", u"四波羅夷（斷頭罪）", u"波羅夷", 4, u"01-10"),
    (u"甲、比丘戒本", u"十三僧殘法", u"十三僧殘（僧伽婆尸沙）", u"僧殘", 13, u"01-10"),
    (u"甲、比丘戒本", u"二不定法", u"二不定法（隨所犯而治，不立定名）", u"不定", 2, u"01-10"),
    (u"甲、比丘戒本", u"三十捨墮法", u"三十捨墮（尼薩耆波逸提）", u"捨墮", 30, u"01-10"),
    (u"甲、比丘戒本", u"九十單提法", u"九十單提（波逸提）", u"單提", 90, u"11-21"),
    (u"甲、比丘戒本", u"四提舍尼", u"四提舍尼（波羅提提舍尼）", u"提舍尼", 4, u"11-21"),
    (u"甲、比丘戒本", u"百眾學法", u"百眾學法（式叉迦羅尼）", u"學法", 100, u"11-21"),
    (u"乙、比丘尼戒本", u"八波羅夷法", u"八波羅夷（斷頭罪）", u"波羅夷", 8, u"22-30"),
    (u"乙、比丘尼戒本", u"十七僧殘法", u"十七僧殘（僧伽婆尸沙）", u"僧殘", 17, u"22-30"),
    (u"乙、比丘尼戒本", u"三十捨墮法", u"三十捨墮（尼薩耆波逸提）", u"捨墮", 30, u"22-30"),
    (u"乙、比丘尼戒本", u"一百七十八單提法", u"一百七十八單提（波逸提）", u"單提", 178, u"22-30"),
]
def mie_names():
    """七滅諍之名與次第一律取戒本之宣告句（「應與X，當與X」七番），不從後人科判，亦不手打——
       手打必與律文異次（南傳傳本以多人語為第五，《四分律》戒本以覓罪相為第五）。"""
    s = corpus(u"11-21")
    k = s.find(u"七滅諍法")
    assert k >= 0, u"戒本『七滅諍法』段不可得"
    nm = re.findall(u"應與([^，；]{2,8})，當與\\1", s[k:k + 800])
    assert len(nm) == 7, u"宣告句得 %d 名（應 7）：%s" % (len(nm), nm)
    return nm


rows = []

def cn2int(s):
    if s == u"十":
        return 10
    if u"百" in s:
        a, b = s.split(u"百", 1)
        v = (U.index(a) if a else 1) * 100
        if b:
            if u"十" in b:
                c, d = b.split(u"十", 1)
                v += (U.index(c) if c else 1) * 10 + (U.index(d) if d else 0)
            elif b in U:
                v += U.index(b)
        return v
    if s.startswith(u"十"):
        return 10 + (U.index(s[1]) if len(s) > 1 else 0)
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s) if s in U else -1


def corpus(tag):
    f = [p for p in glob.glob(os.path.join(ROOT, u"原文", u"*.txt")) if tag in os.path.basename(p)]
    s = io.open(f[0], encoding="utf-8").read().replace("\r\n", "\n")
    return s


def pick(chunk, cat):
    """界內取該條戒文，四层退路：結戒宣說 → 任何「說：」宣說 → 「若X…罪級」句 → 學法之「不得X」句。

    上限 420 字：僧殘第十二（污他家行惡行）之結戒宣說含三諫驅出之全文，實測 340 字，
    舊上限 240 遂使此條淪為『合見前條』——非律文未別宣，是尺太短（用戶所引外審即指此）。
    """
    term = dict(ENDS)[cat]
    bare = term.rstrip(u"。")
    terms = [term, bare] + ([u"突吉羅。", u"突吉羅"] if cat == u"學法" else [])
    m = list(re.finditer(u"集十句義[^：]{0,40}[：:]", chunk))
    for pat in ([m[-1]] if m else []):
        tail = chunk[pat.end():pat.end() + 900]
        p = tail.find(term)
        cut = len(term)
        if p < 0:
            # 律文有未斷句者：尼波羅夷六～八作「…是比丘尼波羅夷不共住犯此八事故…」，句末無圓點，
            # 舊口徑強求「不共住。」遂整條丟棄，附錄反報『律文合見前條，未別宣』——非律不別宣，是尺太苛。
            bare = term.rstrip(u"。")
            p = tail.find(bare)
            cut = len(bare)
            if p >= 0:
                nx = re.search(u"[。；]", tail[p + cut:p + cut + 7])
                if nx:
                    cut += nx.end()
        if p >= 0:
            t = tail[:p + cut].replace(u"\n", u"").replace(u"\u3000", u"").strip().strip(u"『「』」 ")
            # 宣說前段不入戒文：附錄凡例明言戒文乃「欲說戒者當如是說」之後所宣之原句，
            # 而十句義之列舉常與宣說句同段（『一、攝取於僧……當如是說：若比丘…』），
            # 不削則此格以結戒動機冒充戒文（實測四波羅夷第1、尼八波羅夷第1 兩格）。
            dm = list(re.finditer(u"(?:如是|如此)說[：:]", t))
            if dm:
                t = t[dm[-1].end():]
            if 8 <= len(t) <= 420:
                return t
    best = None
    for mm in re.finditer(u"(?:如是|如此)說(?:戒)?[：:]([^：]{4,420}?" + re.escape(term) + u")", chunk):
        t = mm.group(1).replace(u"\n", u"").replace(u"\u3000", u"").strip().strip(u"『「』」 ")
        if 8 <= len(t) <= 420:
            best = t
    if best:
        return best
    # 尾標所切之界本身就是戒文者（尼端多段不作「集十句義」，只宣一句）：舊口徑至此只剩
    # 「若過，尼薩耆波逸提。」之零頭（實測尼捨墮第3・5・6・7・12・15・17 七條），
    # 今先認全段——以「若」起、以罪級收、段中無「義如上」者，即以此段為戒文（仍是語料之連續子串）。
    cc = chunk.replace(u"\n", u"").replace(u"\u3000", u"").strip(u"｜|『「』」 \r\n\t ")
    for tt in (term, bare):
        if cc.startswith(u"若") and cc.endswith(tt) and u"義如上" not in cc and 8 <= len(cc) <= 420:
            return cc
        if cc.startswith(u"若") and u"義如上" not in cc:
            q = cc.find(tt)                       # 段末若另接細判或「此是時。」之屬，取至第一處罪級止
            if q >= 0 and 8 <= q + len(tt) <= 420:
                nx = re.search(u"[。；]", cc[q + len(tt):q + len(tt) + 4])
                return cc[:q + len(tt) + (nx.end() if nx else 0)]
    if cat == u"學法":                                 # 眾學法多作「不得X，式叉迦羅尼（如上）」之別宣
        p = chunk.rfind(u"式叉迦羅尼")
        if p >= 0:
            w = chunk[max(0, p - 90):p]
            st = max(w.rfind(u"。"), w.rfind(u"\n"), w.rfind(u"；"))
            t = ((w[st + 1:] if st >= 0 else w) + u"式叉迦羅尼").replace(u"\n", u"")
            t = re.sub(u"[，,]?\\s*(如上|亦如是)[^。]*$", u"", t).strip(u" ，。") + u"。"
            if 6 <= len(t) <= 90 and (t.startswith(u"不得") or t[0] in u"當應"):
                return t
    for tt in terms:
        for mm in re.finditer(u"若[^。\n]{4,200}?" + re.escape(tt), chunk):
            t = mm.group(0).replace(u"\n", u"")
            if 10 <= len(t) <= 240:
                return t
    return None


def rules_of(s, stem, cat, exp=0):
    """篇題（含其「之子卷」）定範圍 → 尾標定條界 → 界內取戒文；行號以界之序為準。"""
    alias = {u"百眾學法": u"百[眾種]學法", u"四提舍尼": u"四(?:波羅提|波提)?提舍尼(?:法)?"}
    pats = [(u"四波羅夷法", u"四波羅夷法"), (u"十三僧殘法", u"十三僧殘法"), (u"二不定法", u"二不定法"),
            (u"三十捨墮法", u"三十捨墮法"),
            (u"九十單提法", u"九十單提法"), (u"四提舍尼", u"四(?:波羅提)?提舍尼(?:法)?"),
            (u"百眾學法", u"百[眾種]學法(?:之一)?"), (u"七滅諍法", u"七滅諍法"),
            (u"八波羅夷法", u"八波羅夷法"), (u"十七僧殘法", u"十七僧殘法"),
            (u"一百七十八單提法", u"一百七十八單提法")]
    pts = []
    for key, rx in pats:
        for m in re.finditer(u"(?:^|\n)" + rx + u"(?:之[〇零一二三四五六七八九十]+)?[ \t）)]*", s):
            pts.append((m.start(), key, m.end()))
    pts.sort()
    mine = [p for p in pts if p[1] == stem]
    if not mine:
        return []
    a = mine[0][0]
    after = [p for p in pts if p[1] != stem and p[0] > a]
    b = after[0][0] if after else len(s)
    seg = s[a:b]
    if os.environ.get(u"JDBG"):
        n_jing = len([m for m in TAIL.finditer(seg) if u"竟" in m.group(0)])
        print(u"  DBG %s｜段 %d 字｜尾標 %d（含竟 %d）" % (stem, len(seg), len(list(TAIL.finditer(seg))), n_jing))
    out, prev = [], 0
    off, prevn = 0, 0
    term = dict(ENDS)[cat]
    for m in TAIL.finditer(seg):
        n = cn2int(m.group(1))
        if n <= 0:
            continue
        before = seg[max(0, m.start() - 24):m.start()]
        # 條界之真伪：帶「竟」、前文以「痛惱所纏」收（因緣之例）、或前文即以罪級收「且後文另起因緣」——
        # 第三式乃「隨前條並宣」之條（尼單提第118號教人誦習呪術，全篇唯此一見）：律但宣戒文，
        # 不附犯相與不犯段，故無「痛惱所纏」可據；舊口徑不認此式，遂使該號別宣之戒文佚於前條界內，
        # 附錄反報『未別宣』。必兼「後文另起因緣」者，以篇內戒文之列舉「(一)(二)(三)」亦以罪級收，
        # 不兼此件則增 61 偽界（實測），反噬其後之號。
        real = ((u"竟" in m.group(0)) or before.endswith(u"痛惱所纏。")
                or (before.rstrip(u"\n\r\t ").endswith(term)
                    and NIYUAN.match(seg[m.end():m.end() + 12])))
        if not real:
            continue                      # 篇內列舉之括號（如「(一)」）非條界；條界帶「竟」或以「痛惱所纏」收
        if n == 1 and prevn >= 50:          # 唯篇之後半自一重數者還其連號（小數列之「(一)」乃條內列舉，非重數）
            off += prevn
        prevn = n
        nn = off + n
        if exp and nn > exp:
            if n <= exp:                    # 篇末之標本已作全域號（「(一百七十八波逸提法竟)」即第178條，非重數78），
                nn = n                      # 加偏移反成 278 而逾篇——故先退偏移，不退則實據此標所宣之戒文即佚
            else:
                prev = m.end()              # 既逾全域之數又非本篇之號者（卷次括號）不立界
                continue
        t = pick(seg[prev:m.start()], cat)
        prev = m.end()
        if t:
            out.append((nn, t))
    dedup, seen = [], set()
    for n, t in out:                      # 同號重出（界之偽）者唯留其先
        if n in seen or n < 1:
            continue
        seen.add(n)
        dedup.append((n, t))
    return sorted(dedup)


def int2cn(n):
    if n < 10:
        return U[n]
    if n == 10:
        return u"十"
    if n < 20:
        return u"十" + U[n - 10]
    return U[n // 10] + u"十" + (U[n % 10] if n % 10 else u"")


def book_index():
    """書中條次索引：{(族, 罪級, 條次): 「第N章案例M」或「第N章第X節」}；章→族類之配屬依本書今制。

    標記不止於案例：第十章四提舍尼乃以小節逐條陳述（『#### 1. …（第N條）』），
    若只取『#### 案例』則此四條於附錄反成『－』——收而未列，是附錄之誤，非書之缺。
    故凡帶『第N條』式標記者一律入索引，案例歸案例、非案例者歸其所在之節。
    """
    L = io.open(BOOK, encoding="utf-8", newline="").read().split(u"\r\n")
    CHH = re.compile(u"^# 第(.+?)章")
    st = [(cn2int(m.group(1)), i) for i, l in enumerate(L) for m in [CHH.match(l)] if m]
    kind = {5: (u"比", u"波羅夷"), 6: (u"比", u"僧殘"), 7: (u"比", u"捨墮"),
            8: (u"比", u"單提"), 9: (u"比", u"單提"), 10: (u"比", u"提舍尼"),
            12: (u"尼", u"波羅夷"), 13: (u"尼", u"捨墮"), 14: (u"尼", u"單提"), 15: (u"尼", u"單提")}
    NUM = re.compile(u"[〇零一二三四五六七八九十百]{1,4}|\\d{1,3}")
    RNG = re.compile(u"(\\d{1,3}|[〇零一二三四五六七八九十百]{1,4})\\s*(?:[～~–—-]|至)\\s*(?:第)?(\\d{1,3}|[〇零一二三四五六七八九十百]{1,4})")
    SECH = re.compile(u"^### ([〇零一二三四五六七八九十]+)、")
    SPLIT = re.compile(u"[、，：:；;（）()·—／\\s]+")
    # 一篇之主而章兼他篇者（第十章有提舍尼、眾學法、七滅諍），其號須由標記旁之篇名定歸屬：
    # 「（眾學法第26～48條）」之「學法」在「第」字前六字內，或標記以篇名收尾（「第十、十一僧殘」）者從之；
    # 無篇名可據者仍從本章主篇。此即第十章食組二十三条於附錄不作『－』之故。
    KW = [(u"學法", u"學法"), (u"眾學", u"學法"), (u"式叉迦羅尼", u"學法"), (u"波羅夷", u"波羅夷"),
          (u"僧殘", u"僧殘"), (u"僧伽婆尸沙", u"僧殘"), (u"捨墮", u"捨墮"), (u"尼薩耆", u"捨墮"),
          (u"提舍尼", u"提舍尼"), (u"不定", u"不定"), (u"單提", u"單提"), (u"波逸提", u"單提")]
    famcat = {}
    for b, st_, ti, c_, e_, tg in PLAN:
        famcat.setdefault(u"尼" if u"尼" in b else u"比", set()).add(c_)
    idx, idxr, names = {}, {}, []

    def num(s):
        return int(s) if s.isdigit() else cn2int(s)
    for j, k in enumerate([x[0] for x in st]):
        if k not in kind:
            continue
        fam, cat = kind[k]
        a = st[j][1]
        z = st[j + 1][1] if j + 1 < len(st) else len(L)
        sec = None
        for i in range(a, z):
            l = L[i]
            m = SECH.match(l)
            if m:
                sec = m.group(1)
            if not l.startswith((u"### ", u"#### ")):
                continue
            isc = l.startswith(u"#### 案例")
            tt = l[5:].strip() if isc else l[4:].strip()
            if isc:
                label = u"第%s章%s" % (int2cn(k), tt.split(u"：")[0].strip())
            elif sec:
                label = u"第%s章第%s節" % (int2cn(k), sec)
            else:
                continue
            for mm in re.finditer(u"第[^。；）]{0,40}?(?:條|波羅夷|僧殘|提舍尼)", tt):
                run = mm.group(0)
                # 篇名之取：以『括注為句』——回看至最近的句界（（「：；。）而非定長六字。
                # 舊口徑六字窗會漏掉同一括注內之第二段範圍（『（眾學法第2～25條、第49～100條）』
                # 之第二段遂歸本章主篇『提舍尼』，遂使眾學法 49～52、60～61 六號於附錄成『－』）。
                # 取窗內『離錨最近』之篇名，而非 KW 表之最前者——一名兩現之句自此有定準。
                clause = max([tt.rfind(ch, 0, mm.start()) for ch in u"（「：；。（("] + [-1]) + 1
                near = tt[max(clause, mm.start() - 24):mm.start()] + run
                cat2, pd = cat, -1
                for kw, c2 in KW:
                    p = near.rfind(kw)
                    if p > pd and c2 in famcat[fam]:
                        cat2, pd = c2, p
                # 範圍（『第20～23條』『第一至第四僧殘』）分兩種：在案例標題下，該段之
                # 每一條俱屬此案，故展開；在小節總覽（『矩陣（第1～45條）』）則只點全段、
                # 非逐條解剖，故不列——若列，其端點反以 setdefault 搶去真正案例之指針。
                # 並列之數（『第七、八波羅夷』『第12、13、14條』）為實指諸條，兩處俱收。
                # 範圍所推之號只為弱指針（idxr）：一案例自「第26～48條」者，其中三六、四二
                # 二條實由案例一以戒名解剖，強指針（明列之號與戒名）須優先，否則連列吞單條。
                sp = [(num(x), num(y)) for x, y in RNG.findall(run)]
                if sp:
                    if not isc:
                        continue
                    for x, y in sp:
                        for q in range(min(x, y), max(x, y) + 1):
                            idxr.setdefault((fam, cat2, q), label)
                    for x in NUM.findall(run):      # 範圍之外常並列他號（『第150～155、157、158條』），
                        n2 = num(x)                 # 只展開範圍便漏掉並列者，故兩類俱收
                        if n2 > 0:
                            idx.setdefault((fam, cat2, n2), label)
                    continue
                for x in NUM.findall(run):
                    n = num(x)
                    if n > 0:
                        idx.setdefault((fam, cat2, n), label)
            for piece in SPLIT.split(tt):
                if len(piece) >= 5 and piece.endswith(u"戒"):
                    core = re.sub(u"^(不得|若|故|聽|得)", u"", piece)[:-1]
                    if len(core) >= 4:
                        names.append((fam, core, label))
    return idx, names, idxr


rows = []
idx, NAMES, IDXR = book_index()
BKL = io.open(BOOK, encoding="utf-8", newline="").read().split(u"\r\n")
滅諍 = mie_names()


def book_hit(fam, cat, n, txt):
    """該條於書中之位置：先查條號標記（明列者），再查戒名，最後才退到範圍所推之弱指針。
       案例標題只用傳統戒名而未註條號者（第十章案例一『不得大摶飯食戒、不得嚼飯作聲戒』屬此），
       若全篇不列即成『－』，是收而未列；其名之相符須在戒文**起句**：「惡見不捨」亦見於
       第 69 條文中段，只查含有便誤認，故截起句而比。"""
    lab = idx.get((fam, cat, n), u"")
    if lab:
        return lab
    if txt:
        head = re.sub(u"^若比丘尼?|^若|^不得|^故|^聽", u"", txt)[:10]
        for f, core, lb in NAMES:
            if f == fam and core in head:
                return lb
    return IDXR.get((fam, cat, n), u"")


for bu, stem, title, cat, exp, tag in PLAN:
    s = corpus(tag)
    rs = rules_of(s, stem, cat, exp)
    rows.append((bu, stem, title, cat, exp, rs))
    fam = u"尼" if u"尼" in bu else u"比"
    have = dict(rs)
    hit = sum(1 for n in range(1, exp + 1) if book_hit(fam, cat, n, have.get(n)))
    print(u"%-14s｜%-12s｜列 %3d／戒本 %3d｜別宣 %3d｜書中已展開 %3d" % (
        bu, stem, exp, exp, len(have), hit))


def mie_ptr(nm):
    """七滅諍之書中落點（自書中標題實算，非手打名單）：案例標題含其名者優先——案例乃現行犯之解剖；
       次取小節標題（『#### N. …』）所在之節。第十章第三節今具六小節，七條俱有落點。"""
    a = next(i for i, l in enumerate(BKL) if l.startswith(u"# 第十章"))
    z = next(i for i, l in enumerate(BKL[a + 1:], a + 1) if re.match(u"^# 第.+章", l))
    sec, weak = None, None
    for i in range(a, z):
        l = BKL[i]
        m = re.match(u"^### ([一二三四五六七八九十]+)、", l)
        if m:
            sec = m.group(1)
        if not l.startswith(u"#### ") or nm not in l:
            continue
        if l.startswith(u"#### 案例"):
            return u"第十章" + l[5:].split(u"：")[0].strip()
        if weak is None and sec:
            weak = u"第十章第%s節" % sec
    return weak or u""


def _sum_line():
    """篇數之算式自 PLAN 算出（勿手打：手打必於改 PLAN 時滯後）。"""
    tot = sum(p[4] for p in PLAN) + len(滅諍)
    out = []
    for bu, nm in ((u"甲、比丘戒本", u"比丘"), (u"乙、比丘尼戒本", u"比丘尼")):
        ns = [p[4] for p in PLAN if p[0] == bu]
        if bu.startswith(u"甲"):
            ns.append(len(滅諍))
        out.append(u"%s %s＝%d 條" % (nm, u"＋".join(str(x) for x in ns), sum(ns)))
    return (u"%s，共 %d 號；比戒之數恰合『比丘二百五十戒』之通數（含二不定法）"
            % (u"、".join(out), tot), tot)


# 誦本之通數（非本表之法源）：比丘尼戒舊稱三百四十八條，其超出本表乙部之數者，
# 乃尼部之八悔過・百眾學・七滅諍——律於尼犍度但云如前而未別宣，本表故不另立號。
NITONG = [(u"八悔過（提舍尼）", 8), (u"百眾學法", 100), (u"七滅諍法", 7)]
_sum, _TOT = _sum_line()
_ni = sum(p[4] for p in PLAN if p[0].startswith(u"乙"))
_ja = sum(p[4] for p in PLAN if p[0].startswith(u"甲")) + len(滅諍)   # PLAN 之外別有一篇，與 _sum_line 同一口徑
_ni_extra = sum(v for _k, v in NITONG)
NI_TONG = _ni + _ni_extra
_TONG = (u"至通數之別：比丘二百五十，本表恰合（含二不定法）；比丘尼舊稱三百四十八，"
         u"本表乙部列 %d 號，其餘 %d 條即%s（＝%d＋%d＝%d），"
         u"此三者律於尼犍度但云如前、不逐條別宣，誦本方列其號——本表不另立號，非刪削，乃此文無句可抄。") % (
    _ni, _ni_extra, u"＋".join(u"%s%d" % (k, v) for k, v in NITONG), _ni, _ni_extra, NI_TONG)
md = [u"# 附錄　全戒本歷條總表", u"",
      # 附錄扉頁（第 78 輪・外路第廿八報之裝幀案）：H1 照為卷首之題（目錄條・書籤・印面反查俱指此頁，
      # 故其位不動），唯於產物層升作整頁封面（見 `_print/build_hulan.py` 之 `h1.apx-open`）；
      # 此處只補副題兩行，其號數一依本表自算之 _ja・_ni・_TOT，不另手打（手打即來日必漂移）。
      u"<div class=\"apxcover\">",
      u"<div class=\"arule\"></div>",
      u"<p class=\"ac2\">甲、比丘戒本 %d 號　乙、比丘尼戒本 %d 號　合 %d 號</p>"
      % (_ja, _ni, _TOT),
      u"<p class=\"ac3\">逐條登其結戒原句，並標本書解剖此條之處</p>",
      u"</div>",
      u"",
      u"本表**列盡兩部戒本之每一條**（%s；連段全同者以號段列一行，如『1～69.』，其間逐號之狀態即該行所云，"
      u"非省號、非漏號），"
      u"故任何一號有無收入、收入何章何案，一望可核。戒文一律取該條「欲說戒者當如是說」之後所宣"
      u"的原句（無別宣者取其結戒句或犯相句），不從後人科判轉抄，故任何一行都可回到律文對照。"
      u"其後經佛重制者，正文另標【重制戒文】以列定本，本表但錄初制原句，兩不相代。"
      u"電子檔之缺字組字碼能定字者已折為正字（如『[真/心]』作『瞋』），無正字可折者"
      # 第 78 輪・外路第廿七報曾建議以『造字碼位』代此缺字，實測不取：所擬之 U+27655 於
      # Ext-B 字圖中現形為『衣＋末』，與此字之構形不合；且全冊內非 BMP 之字實測 0 枚
      # （`_work/hlnonbmp78.py`），故亦不附加 Ext-B 之伴字體——無靶之刀，來日徒亂字級之量。
      # 此處唯如實述其為 CBETA 述字之法。
      u"（如『[袖-由+宁]』）姑存其形，非排印之誤——此記乃 CBETA 述字之法，以其字之左右構件序於"
      u"括號之內（上例即衣旁加一構件），其碼位未得，故存其記最誠，不以形近之字冒充。" % _sum, u"",
      u"「書中」欄給出本書解剖此條之位置——『第N章案例M』為案例現行犯之解剖，『第N章第X節』為該條於小節內"
      u"逐條陳述者。律文常將數條合為"
      u"一宣（尼戒諸篇與百眾學法尤多），無別宣之號只列號與對應，不強造戒文，故標『律文合見前條』；"
      u"百眾學法一篇之號次依律文匯宣之先後，不依後人科判所編百法之次（彼以『當齊整著涅槃僧』等五威儀為首），"
      u"兩者不必盡合——此亦『不從後人科判轉抄』一句之落處，讀者按號求文，請即本表之次為準。"
      u"另須辨明：篇首數號乃與前部共通之條，律文但云「義如上」而不別宣，本表遂不指落點——"
      u"今作『－』者凡@@DASHR@@行，其號計@@DASHN@@（@@DASHL@@），俱此類也，非缺漏、非刪削；"
      u"其義見前部同篇之號，不可於此部另指。除上數處外，諸號悉有落點。", u"",
      _TONG, u""]
for bu, stem, title, cat, exp, rs in rows:
    fam = u"尼" if u"尼" in bu else u"比"
    got = dict(rs)
    # 篇首若干號乃與前部共通之條，律文但云「義如上」而不別宣（乙部尤多）——此非抽取之失，亦非書中之缺。
    # 篇中之散缺者另報其數（舊口徑只報篇首之連段，遂使百眾學法之表頭作「其第1～1號」此等病句）。
    first = min(got) if got else 1
    np_ = [x for x in range(1, exp + 1) if x not in got]
    sc = [y for y in np_ if y >= first]
    parts = []
    if first > 1:
        parts.append(u"其第1號與前部共戒，律文不別宣" if first == 2
                     else u"其第1～%d號與前部共戒，律文不別宣" % (first - 1))
    if sc:
        parts.append(u"另有第%s號律文未別宣" % u"、".join(str(y) for y in sc) if len(sc) <= 12
                     else u"另有 %d 號律文未別宣" % len(sc))
    note = (u"｜" + u"；".join(parts)) if parts else u""
    md += [u"## %s：%s（戒本 %d 條，律文別宣 %d 條%s）" % (bu, title, exp, len(got), note), u""]
    prev = u""
    lines = []
    for n in range(1, exp + 1):
        txt = got.get(n)
        hit = book_hit(fam, cat, n, txt)
        if txt:
            prev = hit
        elif not hit and prev:
            hit = prev            # 律文既合宣，書中亦無從另指——其落點即其所合見之前條之落點
        if txt:
            cell = u"「%s」" % inner_q(disp(txt))
        else:
            cell = (u"（與前部共戒，律文但云義如上，不別宣）" if n < first
                    else u"（律文合見前條，未別宣）")
        lines.append((cell, hit if hit else u"－"))
    # 連段全同者以號段列一行（如「1～69.」）：此類行除號以外別無異文，逐行重出徒費印面（69 行≈2.6 頁）。
    # 唯長段方合（RUN_MIN），小段仍逐號立行以存「某號是否有落點」一望可核之便；稽核之尺（apxchk）自展開。
    k = 0
    while k < len(lines):
        j = k
        while j + 1 < len(lines) and lines[j + 1] == lines[k]:
            j += 1
        if (j - k + 1) >= RUN_MIN:
            md.append(u"%d～%d. %s　｜書中：%s" % (k + 1, j + 1, lines[k][0], lines[k][1]))
        else:                           # 短段不合——一合則連段之內佚號（apxchk 之歷號核即報缺）
            for q in range(k, j + 1):
                md.append(u"%d. %s　｜書中：%s" % (q + 1, lines[q][0], lines[q][1]))
        k = j + 1
    md.append(u"")
    if bu.startswith(u"甲") and u"百眾學法" in title:
        # 七滅諍法乃甲部之殿（戒本次第：波羅夷→僧殘→不定→捨墮→單提→提舍尼→眾學→七滅諍）。
        # 舊版因抽取之便把它甩在全表之最末，遂成『甲未卒業而乙部插在其前、甲之尾條另擱書尾』之倒裝
        # （外路第廿八報指為結構大病，屬實）。今隨甲部百眾學法之後如次 emit，兩部各自完整。
        md += [u"## 甲、比丘戒本：七滅諍法（戒本 7 條）", u"",
               u"七滅諍法不以「若比丘…」之禁語立文，而以七種滅諍之程序為戒；律文結云：「若有諍事起，即應除滅。」",
               u""]
        md += [u"%d. %s　｜書中：%s" % (mi, x, mie_ptr(x) or u"－") for mi, x in enumerate(滅諍, 1)]
        md.append(u"")
# 『－』之數須自算：篇首共戒之號本無別宣之文，故不指落點。舊帳只舉乙部（尼單提前 69 號），
# 而甲部百眾學法首號亦屬此類，遂成「作『－』者其條尚未展開」之誤說——今由本表之實形取數，不復手抄。
_dr, _dn, _dl, _pian = 0, 0, [], u""
for _s in md:
    if _s.startswith(u"## "):
        _pian = _s[3:]
        continue
    if _s.endswith(u"｜書中：－"):
        mm = re.match(u"^(\\d+)(?:～(\\d+))?\\. ", _s)
        a, b = int(mm.group(1)), int(mm.group(2) or mm.group(1))
        _dr += 1
        _dn += b - a + 1
        nm = _pian.split(u"：")[-1].split(u"（")[0]
        _dl.append(u"%s第%d%s號" % (nm, a, (u"～%d" % b) if b > a else u""))
md = [s.replace(u"@@DASHR@@", str(_dr)).replace(u"@@DASHN@@", str(_dn))
        .replace(u"@@DASHL@@", u"，".join(_dl)) for s in md]
print(u"『－』自算：%d 行・%d 號（%s）" % (_dr, _dn, u"，".join(_dl)))
txt = u"\r\n".join(md) + u"\r\n"
OUT = os.path.join(ROOT, u"_work", u"appendix_jieben.md")
if u"--go" in sys.argv:
    io.open(OUT, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已出附錄草稿：%s｜%d 行｜%d 條戒文" % (OUT, len(md), sum(len(r[5]) for r in rows) + 7))
else:
    print(u"（覆核模式，未寫檔；加 --go 即寫 _work/appendix_jieben.md）")
