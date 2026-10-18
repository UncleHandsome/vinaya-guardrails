# -*- coding: utf-8 -*-
"""ver37 校勘工具箱（可重現查核器）

  python _tk.py verify [scope]   # scope: c6 | e | bq | all   → _work/verify_<scope>.txt
  python _tk.py check            # 結構不變量               → _work/check.txt
  python _tk.py probe <子字串>   # 語料回查（原典／佛經）
  python _tk.py apply <tag>      # 安全套改 _work/patch_<tag>.json（old 全文唯一才套）
  python _tk.py stat             # 基本盤點
"""
import os, re, sys, glob, json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, '_work')
os.makedirs(WORK, exist_ok=True)
_CANDS = [q for q in glob.glob(os.path.join(ROOT, 'ver[0-9]*.md')) + glob.glob(
              os.path.join(ROOT, '_archive', u'\u820a\u672c', 'ver[0-9]*.md'))     # 舊本層（舊＝U+820A）
          if u'\u5217\u5370' not in os.path.basename(q) and re.search(r'^ver\d+', os.path.basename(q))]
SRC = os.environ.get('TKSRC') or (
    max(_CANDS, key=lambda q: int(re.match(r'ver(\d+)', os.path.basename(q)).group(1))) if _CANDS else None)
if not os.path.isabs(SRC):
    SRC = os.path.join(ROOT, SRC)

VARIANT_GROUPS = [
    '虫蟲', '缽鉢', '麁麤粗', '衆眾', '説說', '裏裡', '毗毘', '証證', '无無',
    '华華', '宝寶', '乱亂', '离離', '愿願', '禅禪', '观觀', '忆憶', '莲蓮',
    '恶惡', '难難', '为為', '达達', '悳德', '迴回', '畝畒',
    '恒恆', '药藥', '诃呵', '线線', '净淨凈', '卻却',
]
FOLD = {}
for g in VARIANT_GROUPS:
    for ch in g:
        FOLD[ch] = g[-1] if g[-1] in g else ch

KEEP = re.compile(r'[一-鿿㐀-䶿0-9]')
BRACKET = re.compile(r'\[([^\[\]]{1,14})\]')
# CBETA 組字碼之定字：形義俱定者直接折入正字，兩側同一口徑（語料作『[真/心]』即上真下心之瞋），
# 故書中排「瞋」仍可過逐字閘——否則印面留一組字碼，通俗書即成校對事故。
BRACKET_MAP = {u'真/心': u'瞋'}


def _decomp(m):
    g = m.group(1)
    if g in BRACKET_MAP:
        return BRACKET_MAP[g]
    for sep in ('*', '/'):
        if sep in g:
            return g.split(sep)[-1]
    return g


def unfold(s):
    return BRACKET.sub(_decomp, s)


def norm(s):
    return ''.join(KEEP.findall(unfold(''.join(FOLD.get(c, c) for c in s))))


def read(p):
    return open(p, encoding='utf-8-sig').read()


SEPCH = chr(0)          # 計頻之界標：標點不消失，故不致黏出原典所無之詞


def norm_sep(s):
    """計頻專用之歸一：異體折一、括注展開一如 `norm`，惟標點改塞界標而非刪去。"""
    t = unfold(''.join(FOLD.get(c, c) for c in s))
    return ''.join(c if KEEP.match(c) else SEPCH for c in t)


def term_count(term):
    """某詞於本律語料之逐字出現數（與附錄D-3『逐字檢索統計』之口徑合）。"""
    return VINAYA_SEP.count(term)


def load_corpus():
    vin = []
    for f in sorted(glob.glob(os.path.join(ROOT, '原文', '*.txt'))):
        vin.append(norm(read(f)))
    other = {}
    for f in glob.glob(os.path.join(ROOT, '佛經', '**', '*.txt'), recursive=True):
        other[os.path.relpath(f, ROOT).replace('\\', '/')] = norm(read(f))
    return '\n'.join(vin), other


VINAYA, OTHER = load_corpus()
VINAYA_SEP = SEPCH.join(norm_sep(read(f)) for f in sorted(glob.glob(os.path.join(ROOT, '原文', '*.txt'))))
# 底冊（附錄C 修訂誌・K 款級台帳・L 十維驗收・M 全書校勘記）今另存內部備檔，不入書檔以遠讀者之目
#   （第 250 輪奉令）。查核之 corpus 仍須見其文，故於此串接：DOC／LINES ＝ 主檔 ＋ 備檔，
#   諸軸之 `sec('附錄X')` 與 `bottom_lines()` 一律照舊，印面之行號分毫不動。
BSRC = os.environ.get('TKBOTTOM') or os.path.join(ROOT, '_archive', u'編纂底冊.md')
DOC_MAIN = read(SRC)
DOC_BOTTOM = read(BSRC) if os.path.exists(BSRC) else ''
N_MAIN = len(DOC_MAIN.split('\n'))
MAIN_LINES = DOC_MAIN.split('\n')      # 只此主檔——凡欲整串寫回 `SRC` 之器必取此，取 `LINES` 則把備檔倒進主檔（第 250 輪之失）
DOC = DOC_MAIN + (u'\n' + DOC_BOTTOM if DOC_BOTTOM else '')
LINES = DOC.split('\n')


def path_of(name):
    """某 H1 篇題今存何檔：主檔或底冊備檔。凡欲寫檔之器（如 `rows2.py`）一律取此，勿假設在主檔。"""
    for i, l in enumerate(LINES):
        if l.startswith(u'# ') and name in l:
            return SRC if i < N_MAIN else BSRC
    return SRC

# 三十格矩陣所在之章：章號隨「第五章前移」之重編而動，故依章題語義定位，不退硬編。
MAT_CH = next((re.match(r'#\s*(第[一二三四五六七八九]章)', l).group(1) for l in LINES
               if re.match(r'#\s*第[一二三四五六七八九]章', l) and u'六大領域' in l), u'第五章')

CASE_RE = re.compile(r'^####\s*〔(遮|開|僧)(\d+)〕\s*(.*)$')
POS_RE = re.compile(r'^\*\*定位｜根本心：(.+?)｜三環：(.+?)｜八大正理：(.+?)\*\*')
Q_RE = re.compile(r'「(.+?)」', re.S)
ELL = re.compile(r'…+|\.{3,}')


def bounds():
    b = {}
    for i, l in enumerate(LINES):
        if l.startswith('# 第') or l.startswith('# 附錄') or l.startswith('# 結語') or l.startswith('# 終卷'):
            b.setdefault(re.match(r'#\s*(\S+)', l).group(1), i)
    order = [i for h, i in b.items()]
    return b


B = bounds()


def sec(name):
    """(start, end) line index range for a top-level section heading."""
    starts = sorted([(i, h) for h, i in B.items()])
    for k, (i, h) in enumerate(starts):
        if h == name:
            j = starts[k + 1][0] if k + 1 < len(starts) else len(LINES)
            return i, j
    return None


# 底冊之行索引（修訂誌・款級台帳・十維驗收・全書校勘記・終卷）——凡「不預編年」之軸一律取此，
#   勿再以篇名关键字劃區：第 123 輪附錄M 去『工程』二字改名後，九支以『全書工程校勘記』為鑰之軸
#   （freq88・motif89・phrase89・r102d 等）其底冊排除即靜默失效，四十筆編年自述遂充作印面之病。
BOTTOM_NAMES = (u'附錄C', u'附錄K', u'附錄L', u'附錄M', u'終卷')

# 底冊四篇（終卷不在此列——它仍屬書檔，唯不入印本）：第 250 輪奉作者令另檔 `_archive/編纂底冊.md`，
#   故卷首目錄不列其目、其 H3 子目亦不由目錄校；`build38` 另立反向閘，主檔再見此四題即全建擲回。
LEDGER_NAMES = (u'附錄C', u'附錄K', u'附錄L', u'附錄M')


def bottom_lines():
    idx = set()
    for nm in BOTTOM_NAMES:
        r = sec(nm)
        if r:
            idx.update(range(*r))
    if DOC_BOTTOM:                      # 第 250 輪起：備檔之文全屬底冊（含其檔頭凡例）
        idx.update(range(N_MAIN, len(LINES)))
    return idx


def longest_prefix(frag_norm):
    lo, hi = 0, len(frag_norm)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if frag_norm[:mid] in VINAYA:
            lo = mid
        else:
            hi = mid - 1
    return lo


def classify(raw):
    parts = [norm(p) for p in ELL.split(raw)]
    parts = [p for p in parts if len(p) >= 4]
    if not parts:
        return 'skip', []
    bad = []
    for p in parts:
        if p in VINAYA:
            continue
        if len(p) >= 6:
            lp = longest_prefix(p)
            bad.append((p, lp))
        else:
            bad.append((p, 0))
    if not bad:
        return 'hit', []
    for k, v in OTHER.items():
        if all(p in v for p, _ in bad):
            return 'other:' + k, []
    return 'miss', bad


def emit(path, text):
    open(path, 'w', encoding='utf-8').write(text)
    print(text[-2000:])


# ---------------- verify ----------------
def fragments_c6():
    s, e = sec('第六章')
    out = []
    case = None
    in_orig = False
    for i in range(s, e):
        l = LINES[i]
        m = CASE_RE.match(l)
        if m:
            case = m.group(1) + m.group(2)
            in_orig = False
            continue
        if l.strip().startswith('◎原典'):
            in_orig = True
            continue
        if in_orig and (l.strip() == '---' or l.startswith('##')):
            in_orig = False
        if in_orig and l.lstrip().startswith('>'):
            for q in Q_RE.findall(l):
                out.append((case, i + 1, q))
    return out


def fragments_c6n():
    """第六章・◎原典區塊以外（敘事／處斷／人間智慧）之 「」 片段。"""
    s, e = sec('第六章')
    out = []
    in_orig = False
    case = None
    for i in range(s, e):
        l = LINES[i]
        m = CASE_RE.match(l)
        if m:
            case = m.group(1) + m.group(2)
            in_orig = False
            continue
        if l.strip().startswith('◎原典'):
            in_orig = True
            continue
        if in_orig and (l.strip() == '---' or l.startswith('##')):
            in_orig = False
        if in_orig:
            continue
        for q in Q_RE.findall(l):
            out.append((case, i + 1, q))
    return out


def fragments_e():
    s, e = sec('附錄E')
    out = []
    case = None
    for i in range(s, e):
        l = LINES[i]
        if not l.startswith('|'):
            continue
        m = re.match(r'^\|\s*\*{0,2}〔(遮|開|僧)(\d+)〕\*{0,2}\s*\|', l)
        if not m:
            continue
        case = m.group(1) + m.group(2)
        cells = [c.strip() for c in l.split('|')]
        for c in cells:
            for q in Q_RE.findall(c):
                out.append((case, i + 1, q))
    return out


def fragments_f():
    s, e = sec('附錄F')
    out = []
    for i in range(s, e):
        l = LINES[i]
        if not l.lstrip().startswith('|'):
            continue
        for q in Q_RE.findall(l):
            out.append(('F', i + 1, q))
    return out


def f3_rows():
    """附錄F-3 揭露清單之表列數（自算，不手載）。
    『筆數』與『列數』本是兩口徑：此表以典籍・版本為列，一列可攝同段之數筆
    （如〈維摩詰〉與〈中阿含〉兩列各標三筆），另攝一列非逐字之骨架術語，故列數不必等於筆數。"""
    s, e = sec('附錄F')
    s3 = e3 = None
    for i in range(s, e):
        if LINES[i].startswith('### ') and 'F-3' in LINES[i]:
            s3 = i
        elif s3 is not None and LINES[i].startswith('### '):
            e3 = i
            break
    if s3 is None:
        return 0
    e3 = e3 or e
    n = 0
    for i in range(s3, e3):
        l = LINES[i]
        if not l.lstrip().startswith('|') or l.count('|') < 6:
            continue
        if l.split('|')[1].strip().isdigit():
            n += 1
    return n


def f3_map():
    """附錄F-3 之『列』與本表（F-1・F-2）之『筆』兩向相攝（第 235 輪立，為不變量之證）。
       列之以『所在』欄括號內之法理位置回指本表某行；『F-1 以外』之名相列不指筆，
       一行同段之數筆可歸一列（一列亦同攝之），故列數與筆數本非一口徑，不得強使相等。"""
    s, e = sec('附錄F')
    s3 = next((i for i in range(s, e)
               if LINES[i].startswith('### ') and 'F-3' in LINES[i]), None)
    if s3 is None:
        return dict(rows=0, npen=0, row_orphan=['無 F-3 篇界'], pen_orphan=[], multi=0)
    e3 = next((i for i in range(s3 + 1, e) if LINES[i].startswith('### ')), e)
    pen = {}
    for case, ln, q in fragments_f():
        if ln - 1 >= s3:
            continue
        st, _ = classify(q)
        st = st_adjust(st, ln, q)
        if st in ('miss', 'disclosed'):
            pen.setdefault(ln - 1, []).append(q)
    rows = 0
    row_orphan = []
    covered = set()
    cells = {j: LINES[j].split('|')[1].replace('**', '').strip() for j in pen}
    for i in range(s3, e3):
        l = LINES[i]
        if not l.lstrip().startswith('|') or l.count('|') < 6:
            continue
        c = [x.strip() for x in l.split('|')]
        if not c[1].isdigit():
            continue
        rows += 1
        mm = re.search(u'（([^）]+)）', c[2])
        if not mm or u'以外' in c[2]:
            continue
        hit = [j for j in pen if cells[j].startswith(mm.group(1))]
        if hit:
            covered.add(hit[0])
        else:
            row_orphan.append(c[1])
    return dict(rows=rows, npen=sum(len(v) for v in pen.values()),
                row_orphan=row_orphan, pen_orphan=sorted(j + 1 for j in pen if j not in covered),
                multi=sum(1 for j in covered if len(pen[j]) > 1))


CN_NUM = '一二三四五六七八九十'
_CD = {c: i + 1 for i, c in enumerate(CN_NUM)}
REF_PAT = re.compile(u'第([%s]+)章第([%s、至]+)節' % (CN_NUM, CN_NUM))


def cn_num(s):
    if not s:
        return None
    if s in _CD:
        return _CD[s]
    m = re.match(u'^([一二三四五六七八九])?十([一二三四五六七八九])?$', s)
    if not m:
        return None
    return _CD.get(m.group(1), 1) * 10 + _CD.get(m.group(2), 0)


def ref_pairs(line):
    """一行之內的『章·節』指針；範圍式（『第二、三節』『第二至四節』）展開成集合。
       （第 236 輪：舊口徑以字面子串求之，遂把寫作範圍式的真指針判為查無——器病非書病。）"""
    out = set()
    for m in REF_PAT.finditer(line):
        ch = cn_num(m.group(1))
        for part in re.split(u'[、至]', m.group(2)):
            v = cn_num(part)
            if v:
                out.add((ch, v))
    return out


def kref_loc_range(loc):
    """『第五章第三節第六款』→（起, 迄）行索引；不可解者回 None。"""
    m = re.match(u'^第([%s]+)章第([%s]+)節(?:第(%s)款)?' % (CN_NUM, CN_NUM, CN_NUM), loc)
    if not m:
        return None
    chap, jie, kuan = m.groups()
    ch = [i for i, l in enumerate(LINES) if re.match(u'^# 第%s章' % chap, l)]
    if not ch:
        return None
    ci = ch[0]
    hi = next((i for i in range(ci + 1, len(LINES)) if LINES[i].startswith(u'# ')), len(LINES))
    js = [i for i in range(ci, hi) if LINES[i].startswith(u'### 第%s節' % jie)]
    if not js:
        return None
    s0 = js[0]
    e0 = next((i for i in range(s0 + 1, hi) if LINES[i].startswith(u'### ')), hi)
    if kuan:
        ks = [i for i in range(s0, e0) if LINES[i].startswith(u'#### %s、' % kuan)]
        if ks:
            k0 = ks[0]
            return (k0, next((i for i in range(k0 + 1, e0) if LINES[i].startswith(u'#### ')), e0))
    return (s0, e0)


def kref_check_rows():
    """附錄K 之逐列嚴覆核：回傳（可校列數, 落點之內查無目標指針之列）。
       可校者＝狀態作『已回指』且落點與目標皆可解者；『已回指（範圍式）』與『未回指』俱不校
       （前者之落點多不可解，後者本就存目待補，第 48 輪判令③ 如實保留）。"""
    sK, eK = sec('附錄K')
    bad, n = [], 0
    for i in range(sK, eK):
        l = LINES[i]
        if l.count('|') != 5 or not l.lstrip().startswith('|'):
            continue
        c = [x.strip() for x in l.split('|')]
        if re.match(r'^:?-{2,}', c[1]) or c[1] in ('正文落點', ''):
            continue
        tg, st = c[3], c[4]
        rng = kref_loc_range(c[1])
        want = ref_pairs(tg)
        if not rng or not want or st != '已回指':
            continue
        n += 1
        if not any(ref_pairs(LINES[j]) & want for j in range(*rng)):
            bad.append((i + 1, c[1], tg[:40]))
    return n, bad


def fragments_bq():
    """公布口徑：第六章以外、以引用塊（> ）呈現之宣稱引文（書中合規率即依此測得）。"""
    out = []
    s6, e6 = sec('第六章')
    for i, l in enumerate(LINES):
        if s6 <= i < e6:
            continue
        if not l.lstrip().startswith('>'):
            continue
        for q in Q_RE.findall(l):
            out.append(('bq', i + 1, q))
    return out


def fragments_bqa():
    """診斷口徑：第六章以外全行掃描（含表列與列條式引文），校勘附錄與 E／F 另計。

    立此口徑之因由：舊式 bq 僅取 blockquote 行，附錄H 之列條式「佛陀判語」長期在
    掃描網外，故全書引文宣稱之敞口須以此口徑另測並如實揭露。
    """
    out = []
    s6, e6 = sec('第六章')
    skip = set()
    for nm in ('附錄C', '附錄D', '附錄E', '附錄F', '附錄L', '附錄M'):
        if sec(nm):
            skip.update(range(*sec(nm)))
    for i, l in enumerate(LINES):
        if s6 <= i < e6 or i in skip:
            continue
        for q in Q_RE.findall(l):
            out.append(('bqa', i + 1, q))
    return out


SRC_MARK = re.compile(r'《[^》]{1,20}》|卷\s*[一二三四五六七八九十0-9]{1,4}|犍度|No\.\s*14[0-9]{2}|戒本|摩訶僧祇|五百|七百')


SRC_STRICT = re.compile(r'《[^》]{1,20}》|卷\s*[一二三四五六七八九十0-9]{1,4}|犍度|毘尼增一|律雲|此律文|佛言告|大正藏')


def has_source(idx):
    """引號段是否「冠有出處」——依凡例，只有冠出處者構成逐字宣稱。"""
    for j in range(idx, max(-1, idx - 4), -1):
        if SRC_MARK.search(LINES[j]):
            return True
    return False


def has_source_strict(idx):
    """嚴格版：出處記號須與引號同句（當行或前行），避免現代法條與自創語誤判為引文。"""
    for j in (idx - 1, idx):
        if 0 <= j < len(LINES) and SRC_STRICT.search(LINES[j]):
            return True
    return False


NAME_TAG = ('無從覆核', '本地語料未收', '未入本書比對用語料', '不作逐字')


def term_ok(q):
    """名相有據：短名相（含、／之列舉）去戒字後每一項均可於語料查得者，不作非逐字論。"""
    for part in ELL.split(q):
        for sub in re.split(r'[、/，（）()]', part):
            s2 = norm(sub)
            if len(s2) < 3 or s2 in VINAYA:
                continue
            if s2.endswith('戒') and s2[:-1] in VINAYA:
                continue
            if s2.endswith('羯磨') and s2[:-2] in VINAYA:
                continue
            return False
    return True


def st_adjust(st, ln, q):
    """非逐字之兩類豁免：同行（或次行）已標界之無從覆核者；名相有據而辭形稍異者。"""
    if not st.startswith('miss'):
        return st
    ctx = LINES[ln - 1] + (LINES[ln] if ln < len(LINES) else '')
    if any(k in ctx for k in NAME_TAG):
        return 'disclosed'
    if term_ok(q):
        return 'name_ok'
    return st


def do_verify(scope):
    fn = {'c6': fragments_c6, 'e': fragments_e, 'bq': fragments_bq, 'f': fragments_f,
           'bqa': fragments_bqa}[scope]
    o = []
    hits = misses = skips = others = 0
    term_only = term_hit = 0
    n_disc = n_name = 0
    frag_total = 0
    miss_cases = set()
    case_frag = {}
    meta_lo = min([sec(x)[0] for x in ('附錄C', '附錄L', '附錄M') if sec(x)] or [10 ** 9])
    meta_set = set()
    meta_cnt = 0
    for nm in ('附錄C', '附錄L', '附錄M'):
        if sec(nm):
            meta_set.update(range(*sec(nm)))
    for case, ln, q in fn():
        if scope == 'bq' and (ln - 1) in meta_set:
            meta_cnt += 1
            continue
        claimed = scope in ('c6', 'e') or (has_source_strict(ln - 1) if scope in ('bq', 'bqa') else has_source(ln - 1))
        st, bad = classify(q)
        st = st_adjust(st, ln, q)
        if st in ('disclosed', 'name_ok'):
            if st == 'disclosed':
                n_disc += 1
            else:
                n_name += 1
            continue
        if not claimed:
            term_only += 1
            if st == 'hit':
                term_hit += 1
            continue
        case_frag.setdefault(case, [0, 0])
        if st == 'hit':
            hits += 1
            case_frag[case][0] += 1
            frag_total += 1
        elif st.startswith('other:'):
            others += 1
            o.append('OTHER %-6s L%-6d [%s] %s' % (case, ln, st[6:], q[:70]))
        elif st == 'skip':
            skips += 1
        else:
            misses += 1
            frag_total += 1
            case_frag[case][1] += 1
            miss_cases.add(case)
            p, lp = bad[0]
            o.append('MISS  %-6s L%-6d 片段長%d 前綴命中%d :: %s' % (case, ln, len(p), lp, q[:90]))
    o.append('')
    o.append('=' * 70)
    o.append('scope=%s  逐字命中=%d  非逐字=%d  他典命中=%d  過短略=%d  片段計=%d  合規率=%s'
             % (scope, hits, misses, others, skips, frag_total,
                ('%.1f%%' % (100.0 * hits / frag_total)) if frag_total else 'n/a'))
    o.append('（未冠出處之標注用語，不構成逐字宣稱：%d 處，其中語料可查得 %d 處）' % (term_only, term_hit))
    if scope in ('bq', 'bqa'):
        o.append('（豁免不計入未合規：已標界之本地無從覆核 %d 段；名相有據而辭形稍異 %d 段）'
                 % (n_disc, n_name))
    if meta_cnt:
        o.append('（附錄C/L/M 校勘引述，屬說明舊誤之後設語，不列逐字宣稱：%d 處）' % meta_cnt)
    o.append('含非逐字之案例(%d): %s' % (len(miss_cases), '、'.join('〔%s〕' % c for c in sorted(miss_cases))))
    o.append('全逐字案例數=%d / 有引文案例數=%d' % (sum(1 for v in case_frag.values() if v[1] == 0 and v[0]), len(case_frag)))
    txt = '\n'.join(o)
    emit(os.path.join(WORK, 'verify_%s.txt' % scope), txt)


# ---------------- check ----------------
def do_check():
    inv = []
    def ck(name, ok, info=''):
        inv.append((name, bool(ok), info))

    ids = [m.group(1) + m.group(2) for l in LINES if (m := CASE_RE.match(l))]
    ck('ch6 案例數=100', len(ids) == 100 and len(set(ids)) == 100, str(len(ids)))
    exp = ['遮%d' % i for i in range(1, 46)] + ['開%d' % i for i in range(1, 26)] + ['僧%d' % i for i in range(1, 31)]
    ck('ch6 編號連續無缺', ids == exp, str([x for x in exp if x not in ids][:8]))

    pos = {}
    for i, l in enumerate(LINES):
        m = POS_RE.match(l)
        if m:
            pos.setdefault(i, m)
    n6 = sum(1 for i in range(*sec('第六章')) if POS_RE.match(LINES[i]))
    nJ = sum(1 for i in range(*sec('附錄J')) if POS_RE.match(LINES[i]))
    ck('第六章定位行=100', n6 == 100, str(n6))
    ck('定位行總數=100+附錄J(設計內)', len(pos) == 100 + nJ, 'all=%d J=%d' % (len(pos), nJ))

    s6, e6 = sec('第六章')
    case_pos = {}
    cur = None
    for i in range(s6, e6):
        m = CASE_RE.match(LINES[i])
        if m:
            cur = m.group(1) + m.group(2)
        p = POS_RE.match(LINES[i])
        if p and cur:
            case_pos[cur] = (p.group(1), p.group(2), p.group(3), i + 1)
    ck('定位行綁案=100', len(case_pos) == 100, str(len(case_pos)))

    # ch7 master table（欄序唯表頭是問，欄數可增損——第56輪去『事相簡述』欄後由七欄變六欄）
    s7, e7 = sec('第七章')
    rows = {}
    hdr = None
    ncol = 0
    for i in range(s7, e7):
        l = LINES[i]
        if l.startswith('| 編號 |'):
            cells = [x.strip() for x in l.split('|')]
            if '條目法定正名' in cells and '正理對位' in cells:
                hdr = {name: k for k, name in enumerate(cells)}
                ncol = len(cells)
            continue
        m = re.match(r'^\|\s*〔(遮|開|僧)(\d+)〕\s*\|', l)
        if m and hdr:
            c = [x.strip() for x in l.split('|')]
            if len(c) == ncol:
                rows[m.group(1) + m.group(2)] = (c[hdr['條目法定正名']], c[hdr['根本心']],
                                                 c[hdr['領域']], c[hdr['正理對位']], i + 1)
    ck('ch7 總表列=100', len(rows) == 100, str(len(rows)))
    ck('ch7 與 ch6 同集', set(rows) == set(ids), str((list(set(ids) - set(rows)) + list(set(rows) - set(ids)))[:6]))

    # 正理 tally from ch7
    tally = {i: 0 for i in range(1, 9)}
    for cid, (title, root, dom, zl, ln) in rows.items():
        for n in re.findall(r'正理([一二三四五六七八])', zl):
            tally['一二三四五六七八'.index(n) + 1] += 1
    tot = sum(tally.values())
    # —— 台帳解綁（第九十二輪・著者命「盡量解綁，往後勿再耗力於數」）——
    # 舊此處錨定 133 與 42/33/12/11/8/14/8/5 兩條硬數，改一綁則四處皆須手工隨動。
    # 今分計與總計唯由定位行自算（`_work/ledger.py --go`），帳不再為定數；
    # 下表只驗「印面所印之帳 ＝ 定位行自算之帳」，不合者一跑即平，不復逐處改帳。
    exp_t = None

    # 第七章第三節台帳之逐案枚舉須與總表綁定集合全等
    truth = {i: set() for i in '一二三四五六七八'}
    for cid, (title, root, dom, zl, ln) in rows.items():
        for n in re.findall(r'正理([一二三四五六七八])', zl):
            truth[n].add(cid)
    enum_bad = []
    for i in range(s7, e7):
        m = re.match(r'^\|\s*\*\*正理([一二三四五六七八])\*\*', LINES[i])
        if not m:
            continue
        eids = set(re.findall(r'〔(遮\d+|開\d+|僧\d+)〕', LINES[i]))
        if eids != truth[m.group(1)]:
            enum_bad.append((m.group(1), sorted(truth[m.group(1)] ^ eids)[:6]))
    ck('第七章台帳枚舉＝總表綁定集合', not enum_bad, str(enum_bad[:4]))

    # 根本心 / 正理 parity ch6 定位行 vs ch7
    CN = '一二三四五六七八'
    mm = []
    for cid, (root, ring, zl, ln) in case_pos.items():
        if cid not in rows:
            continue
        r7 = rows[cid][1]
        if root.strip() != r7:
            mm.append((cid, '根本心', root, r7))
        a = re.findall(r'正理([一二三四五六七八])', zl)
        b = re.findall(r'正理([一二三四五六七八])', rows[cid][3])
        if a != b:
            mm.append((cid, '正理', a, b))
    ck('定位行↔ch7 根本心/正理一致', not mm, str(mm[:6]))

    # —— 本輪新增：以人工查證成立、改為不變量守護之結構宣稱 ——
    DOM = ('個人修煉', '人際互動', '僧團事務', '社會邊界', '危機', '照護')
    badr = [(cid, ring) for cid, (root, ring, zl, ln) in case_pos.items()
            if not re.search(r'初環|次環|終環', ring) or any(d in ring for d in DOM)]
    ck('定位行三環欄只載初/次/終環', not badr, str(badr[:4]))
    nm1 = {}
    for cid, (root, ring, zl, ln) in case_pos.items():
        for m in re.finditer(r'([一-鿿]{4})（正理([一二三四五六七八])）', zl):
            nm1.setdefault(m.group(2), set()).add(m.group(1))
    ck('定位行正理法定名單一', all(len(v) == 1 for v in nm1.values()),
       str({k: sorted(v) for k, v in nm1.items() if len(v) > 1}))
    cg = ''.join(re.findall(r'[一-鿿]{4}', LINES[25] + LINES[27]))
    ck('卷首略戒憲綱恰三十二字', len(cg) == 32, '%d 字' % len(cg))
    gates = re.findall(r'(?m)^### 閘門([一二三四五六])', DOC)
    ck('六重心智閘門標題齊備', gates == list('一二三四五六'), str(gates))
    s5, e5 = sec(MAT_CH)
    i0m = next((i for i in range(s5, e5) if LINES[i].startswith('### 第五節')), e5)
    mrows = [i for i in range(i0m, e5) if LINES[i].lstrip().startswith('| **') and '、' in LINES[i][:12]]
    widths = set(LINES[i].count('|') for i in mrows)
    ck('三十格矩陣六列且欄數齊', len(mrows) == 6 and len(widths) == 1, '列=%d 欄=%s' % (len(mrows), sorted(widths)))

    # 法定正名 parity: ch6 heading vs ch7 col2
    titles = {}
    for i in range(s6, e6):
        m = CASE_RE.match(LINES[i])
        if m:
            titles[m.group(1) + m.group(2)] = m.group(3).strip()
    nm = [(c, titles[c], rows[c][0]) for c in titles if c in rows and titles[c] != rows[c][0]]
    ck('條目法定正名 ch6↔ch7 一致', not nm, str(nm[:6]))

    per = {'遮': 0, '開': 0, '僧': 0}
    sd = [0, 0, 0]
    for cid, (title, root, dom, zl, ln) in rows.items():
        n = len(re.findall(r'正理[一二三四五六七八]', zl))
        per[cid[0]] += n
        if 1 <= n <= 3:
            sd[n - 1] += 1
    # 台帳與諸帳之同步，一律交 `_work/ledger.py` 自判（第九十二、九十三輪解綁令）：
    # 綁定分計／篇計／總計、四諍案數、七階支數、三十格矩陣落點、複統攝則數——
    # 器若報差，修法只有一条：`python _work/ledger.py --go`。此處不再另寫一套算帳之法。
    try:
        import importlib.util as _iu
        _sp = _iu.spec_from_file_location('_ledger', os.path.join(ROOT, '_work', 'ledger.py'))
        _lg = _iu.module_from_spec(_sp)
        _sp.loader.exec_module(_lg)
        ck('諸帳印面＝自算（勿手改帳，跑 _work/ledger.py --go）',
           not _lg.changes, '; '.join(_lg.changes[:4]))
    except Exception as _e:
        ck('諸帳印面＝自算（勿手改帳，跑 _work/ledger.py --go）', False, '自算器不可用：%r' % _e)
    try:
        ds = corpus_tiaobu()
        ck('調部語料復算 348/326/198/152/99/92',
           [ds['段落數'], ds['疑'], ds['波羅夷'], ds['無犯'], ds['佛問言'], ds['汝以何心']]
           == [348, 326, 198, 152, 99, 92], str(ds))
    except Exception as e:
        ck('調部語料可復算', False, 'ERR %s' % e)
    ck('正文已無「99 次汝以何心」舊式', '99 次「佛問言：汝以何心' not in DOC)

    # 附錄E
    se, ee = sec('附錄E')
    er = {}
    for i in range(se, ee):
        m = re.match(r'^\|\s*\*{0,2}〔(遮|開|僧)(\d+)〕\*{0,2}\s*\|', LINES[i])
        if m:
            er.setdefault(m.group(1) + m.group(2), []).append(i + 1)
    ck('附錄E 列=100 且每案一列', len(er) == 100 and all(len(v) == 1 for v in er.values()),
       'cols=%d dup=%s' % (len(er), [k for k, v in er.items() if len(v) > 1]))
    ck('附錄E 與 ch6 同集', set(er) == set(ids), str(list(set(ids) ^ set(er))[:6]))

    # 編號五處一致（目錄不逐案列目，故不參與；改以矩陣為第五處）
    s5, e5 = sec(MAT_CH)
    mstart = next((i for i in range(s5, e5) if LINES[i].startswith('### 第五節')), e5)
    mend = next((i for i in range(mstart + 1, e5) if LINES[i].startswith('### ')), e5)
    mid = set()
    for i in range(mstart, mend):
        if LINES[i].lstrip().startswith('|'):
            mid |= {a + b for a, b in re.findall(r'〔(遮|開|僧)(\d+)〕', LINES[i])}
    ck('第五章矩陣編號=100', mid == set(ids), 'n=%d miss=%s' % (len(mid), sorted(set(ids) - mid)[:6]))
    pid = set()
    for i in range(s6, e6):
        m = POS_RE.match(LINES[i])
        if not m:
            continue
        for j in range(i, max(s6, i - 12), -1):
            mm = CASE_RE.match(LINES[j])
            if mm:
                pid.add(mm.group(1) + mm.group(2))
                break
    ck('第六章定位行編號=100', pid == set(ids), 'n=%d' % len(pid))
    ck('第七章總表編號=100', set(rows) == set(ids))
    ck('附錄E 編號=100', set(er) == set(ids))
    ck('正名五處（標題/總表）逐字一致', not nm, 'ch6標題↔ch7正名差異 %d 筆' % len(nm))

    # 附錄引用死鏈
    heads = set(re.findall(r'^#\s*(附錄[A-N])', DOC, re.M))
    refs = set(re.findall(r'附錄\s*([A-N])\b', DOC))
    dead = sorted(r for r in refs if ('附錄' + r) not in heads)
    ck('附錄引用無死鏈', not dead, 'heads=%s dead=%s' % (sorted(heads), dead))

    # 章節引用死鏈
    ch_titles = re.findall(r'^#\s*(第[一二三四五六七八九]章)\s*\S*', DOC, re.M)
    ck('九章齊備', len(ch_titles) == 9, str(len(ch_titles)))
    sec_heads = set()
    cur = None
    for i, l in enumerate(LINES):
        m = re.match(r'^#\s*(第[一二三四五六七八九]章)', l)
        if m:
            cur = m.group(1)
        if cur and re.match(r'^###\s*第([一二三四五六七八九十]+)節', l):
            sec_heads.add(cur + '第' + re.match(r'^###\s*第([一二三四五六七八九十]+)節', l).group(1) + '節')
    bad_sec = []
    for m in re.finditer(r'第([一二三四五六七八九])章第([一二三四五六七八九十]+)節', DOC):
        k = '第%s章第%s節' % (m.group(1), m.group(2))
        if k not in sec_heads:
            bad_sec.append(k)
    ck('章節交叉引用無死鏈', not bad_sec, str(sorted(set(bad_sec))[:10]))

    # —— 款級死鏈：各節實際款號集合（含「十至十三、」合併編號與 H5「款N」標記）——
    NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
           '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18,
           '十九': 19, '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25}
    CN = '|'.join(NUM)
    kuans = {}
    chap = secn = None
    for l in LINES:
        m = re.match(r'^#\s*第([一二三四五六七八九])章', l)
        if m:
            chap, secn = '第%s章' % m.group(1), None
            continue
        if re.match(r'^#\s*(附錄|結語|終卷)', l):
            chap = secn = None
            continue
        if not chap:
            continue
        m = re.match(r'^###\s*第(%s)節' % CN, l)
        if m:
            secn = '第%s節' % m.group(1)
            kuans.setdefault((chap, secn), set())
            continue
        if secn:
            s = set()
            m = re.match(r'^#{4,5}\s*(?:第)?(%s)(?:\s*至\s*(%s))?[、.．]' % (CN, CN), l)
            if m:
                a = NUM[m.group(1)]
                b = NUM[m.group(2)] if m.group(2) else a
                s |= set(range(a, b + 1))
            for mm in re.finditer(r'款(%s)（' % CN, l):
                s.add(NUM[mm.group(1)])
            kuans[(chap, secn)] |= s
    bad_kuan = []
    for m in re.finditer(r'第([一二三四五六七八九])章第(%s)節第(%s)款' % (CN, CN), DOC):
        key = ('第%s章' % m.group(1), '第%s節' % m.group(2))
        z = NUM.get(m.group(3))
        if key not in kuans:
            bad_kuan.append((key[0], key[1], '無此節'))
        elif z not in kuans[key]:
            bad_kuan.append((key[0], key[1], '第%s款（實有 %s）' % (m.group(3), sorted(kuans[key]))))
    ck('款級交叉引用無死鏈', not bad_kuan, str(bad_kuan[:5]))

    # 相對指針之範圍（第 144 輪立）：『本節第N款』『本章第N節』不落章名，舊死鏈檢（其鑰為
    #   『第X章第Y節第Z款』全式）全無感。兩遍為之：先算各章實有之節數、各節實有之款數，
    #   再核引語之序號（底冊與圍欄內不較——編年文字引述舊稱，非當今之指針）。
    _fnc, _bot = set(), bottom_lines()
    _fc = False
    for i, l in enumerate(LINES):
        if l.startswith(u'```'):
            _fc = not _fc
            _fnc.add(i)
        elif _fc:
            _fnc.add(i)

    def _live(i):
        return i not in _fnc and i not in _bot

    _of, _seccnt, _kuancnt = {}, {}, {}
    _cch = _cse = None
    for i, l in enumerate(LINES):
        if not _live(i):
            continue
        m = re.match(u'^#\\s*(第[一二三四五六七八九]章)', l)
        if m:
            _cch, _cse = m.group(1), None
            _seccnt.setdefault(_cch, 0)
            _of[i] = (_cch, _cse)
            continue
        if re.match(u'^#\\s*(附錄|結語|終卷)', l):
            _cch = _cse = None
            continue
        _of[i] = (_cch, _cse)
        if not _cch:
            continue
        m = re.match(u'^###\\s*第(%s)節' % CN, l)
        if m:
            _cse = u'第%s節' % m.group(1)
            _seccnt[_cch] += 1
            _kuancnt.setdefault((_cch, _cse), 0)
            continue
        m = re.match(u'^#{4,5}\\s*(?:第)?(%s)(?:\\s*至\\s*(%s))?[、.．]' % (CN, CN), l)
        if m and _cse:
            _kuancnt[(_cch, _cse)] += ((NUM[m.group(2)] - NUM[m.group(1)] + 1)
                                       if m.group(2) else 1)
    _rp = []
    for i, l in enumerate(LINES):
        if not _live(i):
            continue
        ch, se = _of.get(i, (None, None))
        if not ch:
            continue
        for m in re.finditer(u'本節第(%s|[0-9]+)款' % CN, l):
            z = int(m.group(1)) if m.group(1).isdigit() else NUM.get(m.group(1))
            cnt = _kuancnt.get((ch, se), 0)
            if z is None or not (1 <= z <= cnt):
                _rp.append(u'L%d『本節第%s款』%s 實 %d 款' % (i + 1, m.group(1), se, cnt))
        for m in re.finditer(u'本章第(%s|[0-9]+)節' % CN, l):
            z = int(m.group(1)) if m.group(1).isdigit() else NUM.get(m.group(1))
            cnt = _seccnt.get(ch, 0)
            if z is None or not (1 <= z <= cnt):
                _rp.append(u'L%d『本章第%s節』%s 實 %d 節' % (i + 1, m.group(1), ch, cnt))
    ck(u'相對指針（本節第N款／本章第N節）不越界', not _rp, u'%d 筆 %s' % (len(_rp), _rp[:4]))

    # 第六章百則之欄位齊（第 144 輪立）：每則必具四欄。歷輪只校編號五處相扣與根本心之詞彙，
    #   於『案內缺欄』全無感——削欄、搬遷、合併案例最易致缺，而缺一欄於冊上無跡可尋。
    _LB4 = (u'事相經過', u'心相照鏡', u'佛陀處斷', u'人間智慧')
    _s6, _e6 = sec(u'第六章')
    _blk = {lb: 0 for lb in _LB4}
    for i in range(_s6, _e6):
        if LINES[i].startswith(u'##### '):
            for lb in _LB4:
                if lb in LINES[i]:
                    _blk[lb] += 1
    _ncase = len([i for i in range(_s6, _e6) if re.match(u'^#### 〔[遮開僧]', LINES[i])])
    ck(u'第六章百則四欄齊備（每則各一）',
       _ncase == 100 and all(v == 100 for v in _blk.values()),
       u'%d 則｜%s' % (_ncase, u' '.join(u'%s=%d' % (lb, _blk[lb]) for lb in _LB4)))

    # 篇題之數與篇內之實（第 145 輪立兩條）：
    # 一、附錄L 自題『十維驗收』，其清單須恰有第一維至第十維十列而無缺號——歷輪只校該篇第三節
    #     之實測列，於『宣稱十維而表列不足十』無感；
    # 二、附錄M 校勘記乃編年之錄，條目所標『第N輪』須依時單調遞增（第 145 輪即由此逮得
    #     第二十四輪誤置於第二十六輪之後——編年一亂，後之檢索者無從知其真次）。
    def _cn(s):
        d = {c: k for k, c in enumerate(u'零一二三四五六七八九')}
        d[u'兩'] = 2      # 第 219 輪察：編年自建條之『第兩百X輪』用『兩』，舊尺只認二…九，遂盡數不解（142 條之盲）
        m = re.match(u'^(?:([一二三四五六七八九兩])?百)?(零?[一二三四五六七八九十]*)$', s)
        if not m:
            return None
        hi = d.get(m.group(1), 0) if m.group(1) else 0
        rest = m.group(2) or u''
        if rest in (u'', u'零'):
            return hi * 100
        if hi and rest.startswith(u'零'):          # 一百零四之屬
            return hi * 100 + d.get(rest[1:], 0)
        mm = re.match(u'^([一二三四五六七八九])?十([一二三四五六七八九])?$', rest)
        if mm:
            return hi * 100 + (d.get(mm.group(1), 1) if mm.group(1) else 1) * 10 + \
                (d.get(mm.group(2), 0) if mm.group(2) else 0)
        return d.get(rest, None) if len(rest) == 1 else None
    _sL, _eL = sec(u'附錄L')
    _dims = [_cn(m.group(1)) for i in range(_sL, _eL)
             if (m := re.match(u'^\\|\\s*\\*{0,2}第([一二三四五六七八九十百]+)維', LINES[i]))]
    _claim = re.search(u'附錄L\\s*十維', DOC) or re.search(u'^# 附錄L　十維', DOC, re.M)
    ck(u'附錄L 維度列數＝篇題所題之十維',
       bool(_claim) and _dims == list(range(1, 11)),
       u'%d 列：%s' % (len(_dims), _dims))
    _sM, _eM = sec(u'附錄M')
    _rounds = [(_cn(m.group(2)), int(m.group(1)), i + 1) for i in range(_sM, _eM)
               if (m := re.match(u'^(\\d+)\\. \\*\\*第([零一二三四五六七八九十百兩]+)輪', LINES[i]))]
    _unconv = [(i, n) for (n, _, i) in _rounds if n is None]
    _rin = [(a, b) for (a, _, _), (b, _, _) in zip(_rounds, _rounds[1:])
            if a is not None and b is not None and b < a]
    _nin = [(a, b) for (_, a, _), (_, b, _) in zip(_rounds, _rounds[1:]) if b <= a]
    ck(u'校勘記編年依時單調（輪名與條號俱不逆）',
       len(_rounds) >= 80 and not _rin and not _nin and not _unconv,
       u'%d 條｜輪逆 %s｜號逆 %s｜不解 %s' % (len(_rounds), _rin[:3], _nin[:3], _unconv[:3]))

    # 引號配對
    ck('「」 配對', DOC.count('「') == DOC.count('」'), '%d/%d' % (DOC.count('「'), DOC.count('」')))
    ck('『』 配對', DOC.count('『') == DOC.count('』'), '%d/%d' % (DOC.count('『'), DOC.count('』')))
    # 空引號：舊只校「」一式且通掃全書，故『』之空對（如「改掛『』」）歷輪無聲——
    #   今三式俱校而唯掃印面；底冊（附錄C／K／L／M、終卷）以符號自述編年，依「編年不回改」不較。
    _ip_doc = '\n'.join(l for i, l in enumerate(LINES) if i not in bottom_lines())
    _empty_q = [nm for nm, rx in ((u'「」', u'「\\s*」'),
                                  (u'『』', u'『\\s*』'),
                                  (u'〔〕', u'〔\\s*〕')) if re.search(rx, _ip_doc)]
    ck('印面無空引號（「」『』〔〕三式）', not _empty_q, str(_empty_q))
    s8b, e8b = sec('第八章')
    nq = len(re.findall(r'\*\*捫心自省\*\*', '\n'.join(LINES[s8b:e8b])))
    # 全書之計舊連底冊——第 232 輪校勘記引『捫心自省』一枚入底冊，印面一字未動而此檢遂 17 見。底冊以自述編年，依『編年不回改』不較（784 之 `_ip_doc` 同基），故改取印面口徑。
    ck('第八章捫心自省=16（十六觀心問；印面別處不許冒此語，底冊自述不較）',
       nq == 16 and _ip_doc.count('捫心自省') == 16,
       '章內 %d、印面 %d' % (nq, _ip_doc.count('捫心自省')))
    CN2N = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    body_to_end = sec('附錄A')[0]
    body = '\n'.join(LINES[:body_to_end])
    gates = {CN2N[m] for m in re.findall(r'【道岔([一二三四五六七八九十]+)', DOC) if m in CN2N}
    mx = max(gates) if gates else 0
    claim = {CN2N[m] for m in re.findall(r'([一二三四五六七八九十])大道岔', body) if m in CN2N}
    ck('「N大道岔」宣稱＝實立道岔數（卷首與正文）', claim in ({mx}, set()), '實立 %s 宣稱 %s' % (sorted(gates), sorted(claim)))
    bad_sec = []
    for ch in ('第一章', '第二章', '第三章', '第四章', '第五章', '第六章', '第七章', '第八章', '第九章'):
        s0, e0 = sec(ch)
        nums = [m for l in LINES[s0:e0] if (m := re.match(r'^###\s*第([一二三四五六七八九十]+)節', l))]
        nn = sorted(CN2N[m.group(1)] for m in nums if m.group(1) in CN2N)
        if nn != list(range(1, len(nn) + 1)):
            bad_sec.append((ch, nn))
    ck('各章節號自一連續無缺', not bad_sec, str(bad_sec))
    try:
        sT = next(i for i, l in enumerate(LINES) if l.startswith('## 【全書開卷標準目錄】'))
        eT = next(i for i, l in enumerate(LINES) if i > sT and l.startswith('# 第一章'))
        flat = ''.join(re.sub(r'[\s*]', '', l) for l in LINES[sT:eT])
        orph = []
        for ch in ('第一章', '第二章', '第三章', '第四章', '第五章', '第六章', '第七章', '第八章', '第九章'):
            s0, e0 = sec(ch)
            for i in range(s0, e0):
                m = re.match(r'^###\s*第([一二三四五六七八九十]+)節\s*(.*)', LINES[i])
                if not m:
                    continue
                key = '第%s節' % m.group(1) + re.sub(r'[\s*]', '', m.group(2)).split('（')[0][:10]
                if key not in flat:
                    orph.append((ch, i + 1))
        miss_h1 = [l[:12] for l in LINES[sT:eT] and [] or []]
        _H1K = re.compile(r'^#\s*(附錄[A-Z]|結語|終卷)')
        _SKIPLEDGER = tuple(u'# ' + x for x in LEDGER_NAMES)   # 底冊四篇已另檔（第 250 輪），目錄不列其目
        tops = [m.group(1) for l in LINES if (m := _H1K.match(l)) and not l.startswith(_SKIPLEDGER)]
        notoc = [x for x in dict.fromkeys(tops) if x not in ''.join(LINES[sT:eT])]
        ck('卷首目錄與章節標題雙向對齊', not orph and not notoc, '目錄缺 %s；章目錄而無實際節 %s' % (notoc, orph[:4]))
    except StopIteration:
        ck('卷首目錄與章節標題雙向對齊', False, '找不到目錄區間')
    sK, eK = sec('附錄K')
    krows = 0
    for i in range(sK, eK):
        l = LINES[i]
        if not l.lstrip().startswith('|') or l.count('|') != 5:
            continue
        c = [x.strip() for x in l.split('|')]
        if re.match(r'^:?-{2,}', c[1]) or c[1] in ('正文落點', ''):
            continue
        krows += 1
    ck('附錄K 索引條目=55', krows == 55 or '55 條' not in DOC, '實數 %d' % krows)
    m6 = measure('c6')
    mE = measure('e')
    PRE = ('| 第六章「◎原典」逐字宣稱片段數', '| 逐字可查得片段數', '| **第六章引文逐字合規率**',
           '| 案內引文全數逐字之案例', '| 仍含非逐字片段之案例', '| 附錄 E「案例引文一覽」',
           '| 第六章以外冠出處之引號段', '| 敞口診斷（全行掃描', '| 附錄 F 經論互證引文')
    mB, mA, mF = measure('bq'), measure('bqa'), measure('f')
    want = {'| 第六章「◎原典」逐字宣稱片段數': [str(m6['tot'])],
            '| 逐字可查得片段數': [str(m6['hit'])],
            '| **第六章引文逐字合規率**': ['%.1f' % m6['rate']],
            '| 案內引文全數逐字之案例': [str(m6['full']), str(m6['n'])],
            '| 仍含非逐字片段之案例': [str(m6['n'] - m6['full'])],
            '| 附錄 E「案例引文一覽」': [str(mE['hit']), str(mE['tot']), '%.1f' % mE['rate']],
            '| 第六章以外冠出處之引號段': [str(mB['hit']), str(mB['tot']), str(mB['term']), str(mB['meta']),
                                      str(mB['disc']), str(mB['namok'])],
            '| 敞口診斷（全行掃描': [str(mA['tot']), str(mA['hit']), str(mA['miss']), str(mA['disc'])],
            '| 附錄 F 經論互證引文': [str(mF['hit']), str(mF['other']), str(mF['miss']),
                                       str(mF['disc'] + mF['namok']), str(f3_rows())]}
    tbl = [l for l in LINES if l.startswith(PRE)]
    tblbad = []
    for pre, nums in want.items():
        row = next((v for v in tbl if v.startswith(pre)), None)
        if not row:
            tblbad.append((pre, '缺列'))
            continue
        found = re.findall(r'\*{0,2}(\d+(?:\.\d)?)\*{0,2}', row)
        # （歷輪曾在此寫死一枚『消去名單』以免噪音——它只會吞掉本該存在的實測數，
        #   第 128 輪即因『83』被消去而誤報一筆 FAIL；本檢只問 want⊆found，多出的數字無害，故去之。）
        for wnum in nums:
            if wnum not in found:
                tblbad.append((pre[:18], '表內 %s 缺 %s' % (found, wnum)))
    ck('附錄L 實測表數字＝當場復測', not tblbad, str(tblbad[:3]))
    # 第一百二十輪：實測表有檢，表外散文無守——〔驗收裁決〕一段向以「174/174」「120/120」作擔保，
    # 歷輪皆手抄；同段又曾手載「F-3 共 11 筆」而與實測表之 19 互異（今已去其數）。故立此檢。
    dec = next((l for l in LINES if u'〔驗收裁決〕' in l), u'')
    decbad = []
    if dec:
        for lab, mm in ((u'第六章', (m6['hit'], m6['tot'])), (u'附錄E', (mE['hit'], mE['tot']))):
            if ('%d/%d' % mm) not in dec:
                decbad.append(u'%s 實測 %d/%d 未見於裁決' % (lab, mm[0], mm[1]))
        if re.search(r'F-3[^。]{0,60}共\s*[\d一二三四五六七八九十百]{1,4}\s*[筆條]', dec):
            decbad.append(u'裁決內手載 F-3 筆數')
    ck('〔驗收裁決〕散文之實測數＝當場復測', not decbad, str(decbad[:3]))
    # 第 235 輪：外路以 F-3 之『19 列』代『23 筆』而報『差 4』——實乃兩口徑（一列可攝同段數筆，
    #   另有名相列不攝筆）。數既兩式，便立兩向之攝：列列須有所指、筆筆須有所列，脫節即退。
    m3 = f3_map()
    ck('附錄F-3 與本表兩向相攝（列有所指·筆有所列；列數不強等於筆數）',
       not m3['row_orphan'] and not m3['pen_orphan'] and m3['rows'] == f3_rows(),
       '列 %d（無所指 %s）｜筆 %d（無所列 %s）｜攝多筆之列 %d' % (
           m3['rows'], m3['row_orphan'][:3], m3['npen'], m3['pen_orphan'][:3], m3['multi']))
    eng = [i + 1 for i, l in enumerate(LINES)
           if re.search(r'TODO|FIXME|XXX|TBD|WIP|占位|待回填|【占', l)]
    ck('無英文工程殘留', not eng, str(eng[:8]))
    SIMP_ONLY = set('实从个国们来这对经视见请许设让还钱铁传递记录灭举处声复断书马鸟鱼东风飞当应专长阳阴队阶阵陆随难极样类产无为说变关边钟网电' + chr(0x573a)+chr(0x5c3d)+chr(0x663e)+chr(0x5e9f)+chr(0x6c47)+chr(0x8bcd)+chr(0x865a)
    + chr(0x6570) + chr(0x65ad) + chr(0x51c6) + chr(0x95ed) + chr(0x5C61) + chr(0x5956) + chr(0x76D6) + chr(0x987B) + chr(0x4F63) + chr(0x866B) + chr(0x4F59) + chr(0x95A2) + chr(0x95EE) + chr(0x7EC8) + chr(0x65F6) + chr(0x56FE) + chr(0x53D1)
    + chr(0x8F66) + chr(0x8F68) + chr(0x8F69) + chr(0x8F6C) + chr(0x8F6E) + chr(0x8F6F) + chr(0x8F74) + chr(0x8F7B) + chr(0x8F7D) + chr(0x8F83) + chr(0x8F86) + u"\u5f20\u7ebf\u636e\u5199\u8f6c\u5934\u9875\u987e\u60ac\u95fb\u672f\u5355\u53f7\u62e5\u62a4\u62a5\u8bfb\u6444\u70b9\u6837\u6784\u5907\u5212\u5ba1\u8bae\u8bc6\u8bc9\u8bef\u8c03\u8c08\u8c22\u534f\u8d22\u8d28\u8d23\u8d26\u8d39\u8d44\u5f00\u5bfc\u8fd0\u8be5\u6807\u8bb0\u7ed3\u8111\u8f7b" + u"与么亚仓仪价众优会伤伦储儿军农况冻净减凑凤击刘删剂区医县参双叶吗启员团园圣坏块夹夺妇孙宁屿师帐帘帮广庄庆彦彻晓枢枣枪柜栈档桥梦检楼问冲决栏带" \
    + "强册听层纲织纪则称没确级统义习违连续丛压历怀态愿战觉绝艺镜竞独迈门圆络叠职虽两码软语谁极亩圣图钟镜启众兴创厂" + chr(0x5398) + chr(0x8BC1) + chr(0x4E25) + chr(0x987B) + chr(0x6267) + chr(0x6251) + chr(0x8D34)
    + chr(0x5E76) + chr(0x5F52) + chr(0x62DF) + chr(0x65E7) + chr(0x6761) + chr(0x6B8B) + chr(0x90BB) + chr(0x5C4A) + chr(0x8BF8)) - {chr(0x51C6)}   # 0x8BF8＝『諸』之簡形一枚，第 226 輪補（底冊校勘記落此，入表前兩名單俱無）｜嚴／須／執之簡形第 125、127 輪補（入表前書中零見或豁免在案）；『扑』之簡形第 147 輪補（書中僅底冊兩見「扑空」，正作「撲空」，入表前印面零見）；『两』之簡形第 174 輪補（印面一枚落於附錄I 三十格第 20 行「法域邊界两款」，歷輪名單無此字，閘遂無聲——『名單之外』之又一例，第 61 輪之教）；**『准』一枚第 149 輪移出名單**——准非簡形，乃『許可、核准』義之正字（ ROC 公文與法條作准：不准、特准、准予、准駁），前此誤以為簡體而『全面歸準』，實則簡轉繁工具將准準合流，遂使『方準開庭』『不準動』『特準』『準予』『準入』諸語盡成法學字傷；今由第 69 檢兩向守之；**『贴』(U+8D34) 一枚第 180 輪補**——外路第二十三批之記錄自查時由我新寫之規画文落此形（『轮』則早已在車部十一之列，是我記錄檔之 scanner 未收，非書閘之盲——**名冊有無先查後說**）；入單前量全書二字俱零見   # 0x8BC1＝證之簡形，第 121 輪補（入表前書中零見）
    # 第 220 輪改：引號之豁免須辨巢套與跨行——舊以同線正則剝「」『』，遇外層「」跨行而內層同線成對者，
    #   配對即錯位，遂把引文內之字露在『引號外』（L5671 之『并』即其證）。今以深度帶走，兩族各自計數。
    _q1 = _q2 = 0
    _pl = []
    for _qc in DOC:
        if _qc == u'「':
            _q1 += 1
        elif _qc == u'」':
            _q1 = max(0, _q1 - 1)
        elif _qc == u'『':
            _q2 += 1
        elif _qc == u'』':
            _q2 = max(0, _q2 - 1)
        elif _q1 == 0 and _q2 == 0:
            _pl.append(_qc)
    # 第 220 輪補八字『并归拟旧条残邻届』——本輪自查簡形名單之差集：recordsimp 之鍵多於 `_tk.SIMP_ONLY` 達 195 枚，
    #   逐字查印面唯『并』一枚屬編者手筆（L5645，引文外），餘『归拟旧条残邻』14 枚俱在附錄M 記錄之編者文，『届』一枚在印面
    #   釋義（L11425）——俱已就地歸正（并→並、届→屆、归→歸、拟→擬、旧→舊、条→條、残→殘、邻→鄰），入單前引文外俱 0 見。
    #   『并』於引文內餘 5 見屬照錄（語料『并』100 見／『並』6 見），由上之巢套狀態機豁免——舊同線剝法會露其一，故先修口徑後補單。
    plain = u''.join(_pl)
    simp = sorted(set(plain) & SIMP_ONLY)
    ck('引號外無簡體孤立字', not simp, str(simp[:8]))
    # 日本新字体三形（缽＝鉢、裏＝裡、証＝證）——簡形閘只收簡體故向漏此族（第 102 輪掃得『缽』91 見歸正為『鉢』，
    # 其後歷輪新文又落兩見於第四章與第六章，第 135 輪由 jp74c 之待診旗逮出，今升為長檢）。
    # 底冊四篇（修訂誌、款級台帳、十維驗收、全書校勘記）不入印本，其舊形與異體之自述依「編年不回改」之例不較。
    JP_BAD = set(u'\u7f3d\u88cf\u8a3c')      # 缽／裏／証（日新字体；正體作鉢、裡、證）
    _jd = set()
    for _jn in (u'附錄C', u'附錄K', u'附錄L', u'附錄M'):
        if sec(_jn):
            _jd.update(range(*sec(_jn)))
    _jplain = re.sub(r'「[^」]*」|『[^』]*』', '', u'\n'.join(
        l for i, l in enumerate(LINES) if i not in _jd))
    _jbad = sorted(set(_jplain) & JP_BAD)
    ck(u'印面無日新字体（U+7F3D·88CF·8A3C）', not _jbad, str(_jbad[:6]))
    n6long = []
    for c, ln, q in fragments_c6n():
        k, bad = classify(q)
        if k == 'miss' and bad and max(len(p) for p, _ in bad) >= 12:
            n6long.append('%s L%d' % (c, ln))
    ck('第六章敘事層長句引號逐字可查', not n6long, '%d 處 %s' % (len(n6long), n6long[:6]))
    h2bad = [i + 1 for i, l in enumerate(LINES) if l.startswith('## ') and not l[3:].startswith('【')]
    ck('二級標題一律以【】起（凡例體例）', not h2bad, str(h2bad[:6]))
    AREA_K = [('個人', '個人修煉'), ('人際', '人際互動'), ('事務', '僧團事務'),
              ('邊界', '僧團與社會邊界'), ('危機', '危機與特殊時刻'), ('照護', '照護與護生專業')]
    s5a, e5a = sec(MAT_CH)
    s7a, e7a = sec('第七章')
    mxs = {}
    for i in range(s5a, e5a):
        l = LINES[i]
        if not l.startswith('|'):
            continue
        cells = [c.strip() for c in l.split('|')]
        if len(cells) < 3 or not re.match(r'^\*\*[一二三四五六]、', cells[1]):
            continue
        dom = next((v for k, v in AREA_K if k in cells[1]), None)
        if not dom:
            continue
        for c in cells[2:]:
            for mm in re.finditer(r'〔(遮|開|僧)(\d+)〕', c):
                mxs.setdefault(mm.group(1) + mm.group(2), set()).add(dom)
    bad = []
    n7 = 0
    for i in range(s7a, e7a):
        l = LINES[i]
        mm = re.match(r'^\|\s*〔(遮|開|僧)(\d+)〕\s*\|', l)
        if not mm:
            continue
        n7 += 1
        case = mm.group(1) + mm.group(2)
        dom = None
        for c in [x.strip() for x in l.split('|')][1:]:
            if len(c) <= 12:
                dom = next((v for k, v in AREA_K if k in c), None)
                if dom:
                    break
        if not dom or dom not in mxs.get(case, set()):
            bad.append('%s 總表=%s 矩陣=%s' % (case, dom, sorted(mxs.get(case, []))))
    ck('第五章矩陣落點涵蓋第七章主領域', not bad and n7 == 100 and len(mxs) == 100,
       '%d 案不符 %s' % (len(bad), bad[:4]))
    oldnum = [i + 1 for i, l in enumerate(LINES)
              if re.search(r'舊[〔](遮|開|僧)\d+[〕]', l)]
    ck('舊版編號不得使用案例括號', not oldnum, str(oldnum[:6]))
    s6c, e6c = sec('第六章')
    heads = [i for i in range(s6c, e6c) if CASE_RE.match(LINES[i])]
    NEED6 = ('##### 事相經過', '##### 心相照鏡', '##### 佛陀處斷', '##### 人間智慧')
    struct_bad = []
    for n, i in enumerate(heads):
        stop = heads[n + 1] if n + 1 < len(heads) else e6c
        body = LINES[i:stop]
        cid = CASE_RE.match(LINES[i]).group(1) + CASE_RE.match(LINES[i]).group(2)
        lack = [x for x in NEED6 if not any(b.startswith(x) for b in body)]
        if not any(b.strip().startswith('◎原典') for b in body):
            lack.append('◎原典')
        duan = [re.match(r'^\d+\.\s+\*\*(初環|次環|終環)', b).group(1) for b in body
                if re.match(r'^\d+\.\s+\*\*(初環|次環|終環)', b)]
        nums = [int(re.match(r'^(\d+)\.', b).group(1)) for b in body
                if re.match(r'^\d+\.\s+\*\*(初環|次環|終環)', b)]
        pos = next((b for b in body if b.startswith('**定位｜')), '')
        declared = re.findall(r'(初環|次環|終環)[\u4e00-\u9fff]{0,6}', pos)
        if lack or duan != ['初環', '次環', '終環'] or nums != [1, 2, 3] or set(declared) - set(duan):
            struct_bad.append('%s:%s%s%s' % (cid, lack, '' if duan == ['初環', '次環', '終環'] else '環序' + str(duan),
                                             '' if nums == [1, 2, 3] else '序' + str(nums)))
    ck('第六章百案六段完備三環相符', not struct_bad and len(heads) == 100,
       '%d 案異常 %s' % (len(struct_bad), struct_bad[:5]))
    sK2, eK2 = sec('附錄K')
    CN2 = '一二三四五六七八九十'
    # 回指之證唯取正文，不取底冊：修訂誌・台帳・驗收・校勘記・終卷乃編年自述，
    #   其行間偶現之節次字樣不是「他處引用」（第 174 輪一筆校勘記遂令四列虛報已回指）。
    _knot = set(bottom_lines()) | set(range(sK2, eK2))
    kbad = []
    for i in range(sK2, eK2):
        l = LINES[i]
        if l.count('|') != 5 or not l.lstrip().startswith('|'):
            continue
        c = [x.strip() for x in l.split('|')]
        if re.match(r'^:?-{2,}', c[1]) or c[1] in ('正文落點', ''):
            continue
        tg, st = c[3], c[4]
        mm = re.search(r'第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)至([一二三四五六七八九十]+)節', tg)
        if mm:
            ch2, a2, b2 = mm.group(1), CN2.index(mm.group(2)) + 1, CN2.index(mm.group(3)) + 1
            refs = ['第%s章第%s節' % (ch2, CN2[k - 1]) for k in range(a2, b2 + 1)]
            exp = '已回指（範圍式）'
        else:
            m2 = re.search(r'第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節(?:第([一二三四五六七八九十]+)款)?', tg)
            if not m2:
                continue
            base = '第%s章第%s節' % (m2.group(1), m2.group(2))
            kuan = m2.group(3)
            refs = [base]
            exp = '已回指'
            hit = False
            for j, l2 in enumerate(LINES):
                if j in _knot or base not in l2:
                    continue
                if not kuan:
                    hit = True
                    break
                for mz in re.finditer(re.escape(base), l2):
                    win = l2[mz.end():mz.end() + 60]
                    if re.search(r'[:：、（(]?\s*第%s款' % kuan, win) or re.search(r'%s、' % kuan, win):
                        hit = True
            if not hit:
                exp = '未回指（存目待補）'
        if exp.startswith('已回指（'):
            hit2 = any(any(r in l2 for r in refs) for j, l2 in enumerate(LINES) if not (sK2 <= j < eK2))
            exp = '已回指（範圍式）' if hit2 else '未回指（存目待補）'
        if st != exp:
            kbad.append('%s→%s' % (st or '(空)', exp))
    ck('附錄K 回指狀態＝實測', not kbad, '%d 列不符 %s' % (len(kbad), kbad[:5]))
    # 第 236 輪：上一檢只問『目標之章·節在全書任何一處出現』——近於恆真，故容得下『落點之內全無指針』
    #   之假回指（今查得六列，俱補自然指針而清）。本檢以落點為牢，範圍式指針（『第二、三節』）展開為集合再取交集。
    kn, kbad2 = kref_check_rows()
    ck('附錄K 已回指之列須落點之內實見其指針（嚴口徑・範圍式展開）', not kbad2,
       '可校 %d 列｜查無 %d 列 %s' % (kn, len(kbad2), kbad2[:3]))
    subheads = set()
    for l in LINES:
        m = re.match(r'^#{3,5}\s*([A-N])-(\d+)\b', l)
        if m:
            subheads.add(m.group(1) + '-' + m.group(2))
    subbad = []
    for i2, l2 in enumerate(LINES):
        for m in re.finditer(r'附錄\s*([A-N])-(\d+)', l2):
            k = m.group(1) + '-' + m.group(2)
            if k not in subheads:
                subbad.append('%s(L%d)' % (k, i2 + 1))
    ck('附錄子目引用無死鏈', not subbad, str(subbad[:6]))
    # 附錄F-3「所在」欄之定位：舊載本檔行號（一.edit 即漂移），今以 F-1／F-2 表首欄之行標為準
    f3lab = {u'1': set(), u'2': set()}
    zone = None
    for l in LINES:
        if l.startswith(u'### F-1'):
            zone = u'1'
        elif l.startswith(u'### F-2'):
            zone = u'2'
        elif l.startswith(u'### ') or l.startswith(u'## ') or l.startswith(u'# '):
            zone = None
        if zone and l.startswith(u'|'):
            cs = [c.strip() for c in l.split(u'|')]
            if len(cs) > 2 and cs[1]:
                f3lab[zone].add(re.sub(u'（[^）]*）', u'', cs[1]).strip(u'* ').strip())
    f3bad = []
    for i2, l2 in enumerate(LINES):
        for m in re.finditer(u'F-([12])（([^（）]{2,26})）行', l2):
            if m.group(2) not in f3lab[m.group(1)]:
                f3bad.append('%s(L%d)' % (m.group(0), i2 + 1))
    ck(u'附錄F-3 所在欄＝篇內行標（勿載本檔行號）', not f3bad, str(f3bad[:5]))
    # 附錄F-3 首欄序號：須自一起而連貫，且全屬阿拉伯數字（第 127 輪立——歷輪增補曾留「12a」之補丁痕，
    # 而此种痕在印刷定本中即屬工作檔之外洩；序欄一有字母尾或跳號，本檢即報）
    f3seq, z3 = [], False
    for l in LINES:
        if l.startswith(u'### F-3'):
            z3 = True
            continue
        if z3 and l[:1] in ('#',) and l.strip():
            z3 = False
        if z3 and l.startswith(u'|'):
            cs = [c.strip() for c in l.split(u'|')]
            if len(cs) > 2 and re.match(u'^\\*{0,2}[0-9]+[a-z]?\\*{0,2}$', cs[1]):
                f3seq.append(cs[1].strip(u'*'))
    f3ok = f3seq == [str(k) for k in range(1, len(f3seq) + 1)]
    ck(u'附錄F-3 首欄序號＝1..N 連續無字母尾', f3ok,
       u'%d 筆%s' % (len(f3seq), u'' if f3ok else u'｜今序 ' + u','.join(f3seq[:24])))
    # 卷首『全書開卷標準目錄』乃手寫之目，須逐條對合實有標題（節名之括註係目錄自有之撮述，不較）
    def _nm(t):
        t = re.split(r'[（(]', t)[0]
        t = t.replace('**', '').replace(u'【', '').replace(u'】', '')
        return re.sub(u'[　 :：、，—-]', '', t).strip()

    _t0 = next(i for i, l in enumerate(LINES) if l.startswith(u'## 【全書開卷標準目錄】'))
    _t1 = next(i for i, l in enumerate(LINES) if i > _t0 and l.startswith(u'# 第一章'))
    _hd = {_nm(m.group(1)) for l in LINES for m in [re.match(r'^#{1,5}\s+(.*)$', l)] if m}
    _tocbad = []
    for i2 in range(_t0, _t1):
        m = re.match(r'^\s*\*\s+(.+)$', LINES[i2])
        if not m:
            continue
        t = _nm(m.group(1))
        if t and t not in (u'附錄', u'目錄') and t not in _hd:
            _tocbad.append('L%d %s' % (i2 + 1, t[:16]))
    ck(u'卷首目錄＝實有標題', not _tocbad, '%d 條不合 %s' % (len(_tocbad), _tocbad[:4]))

    # 上檢只校『列其目→有其題』之正向。第 142 輪補其反向兩條（今日方悟『凡立一向之檢必問其反向』）：
    # 一、印面九章與結語之內，凡 H3 標題須見於卷首目錄——第四章【章末指針】、第六章【開許篇末·體例
    #    例外說明】兩插片與第七／八章『### ——副題』俱是實有其題而目錄不列，歷輪無器問及（副題今降為
    #    粗體副標題，不入標題層；他章向無副題之標題層）；
    # 二、目錄括注所列之附錄子目（如『A-1至A-6』『F-1…F-3』）須與該篇實有之 H3 子目齊一——
    #    第 141 輪目錄漏 F-3 即此類病之現形，彼時出以人工，今使自校。
    _tocset = set()
    for i2 in range(_t0, _t1):
        m = re.match(r'^\s*\*\s+(.+)$', LINES[i2])
        if m:
            _tocset.add(_nm(m.group(1)))
    _orph = []
    for _ch in (u'第一章', u'第二章', u'第三章', u'第四章', u'第五章',
                u'第六章', u'第七章', u'第八章', u'第九章', u'結語'):
        s0, e0 = sec(_ch)
        for i in range(s0, e0):
            m = re.match(u'^### (.*)$', LINES[i])
            if not m:
                continue
            t = _nm(m.group(1))
            if t and t not in _tocset:
                _orph.append(u'%s L%d『%s』' % (_ch, i + 1, t[:16]))
    ck(u'章內 H3 俱列於卷首目錄（目錄之反向檢）', not _orph,
       u'%d 條未列 %s' % (len(_orph), _orph[:4]))

    _subact = {}
    for _i, l in enumerate(LINES):
        if _i in bottom_lines():          # 底冊四篇已另檔，其 H3 子目不復由目錄求之（第 250 輪）
            continue
        m = re.match(u'^###\\s*([A-M])-([0-9]+)', l)
        if m:
            _subact.setdefault(m.group(1), set()).add(u'%s-%s' % (m.group(1), m.group(2)))
    _subbad = []
    for _a in sorted(_subact):
        _ln = next((LINES[i] for i in range(_t0, _t1)
                    if re.match(u'^\\s*\\*\\s*附錄%s' % _a, LINES[i])), u'')
        got = set(re.findall(u'[A-M]-[0-9]+', _ln))
        for x, m1, m2 in re.findall(u'([A-M])-([0-9]+)至[A-M]-([0-9]+)', _ln):
            if x == _a:
                got.update(u'%s-%d' % (x, k) for k in range(int(m1), int(m2) + 1))
        miss = sorted(_subact[_a] - got)
        ghost = sorted(got - _subact[_a])
        if miss or ghost:
            _subbad.append(u'附錄%s 目錄未列%s｜目錄虛列%s' % (_a, miss[:4], ghost[:4]))
    ck(u'目錄括注之附錄子目＝實有子目', not _subbad,
       u'%d 篇不合 %s' % (len(_subbad), _subbad[:3]))

    # 日式間隔號 U+30FB（・）之除（第 142 輪立）：全書隔號通例作 U+00B7『·』（1068 見），
    #   而歷輪新文屢誤落『・』（母數 30 枚、封面 build38.py 另 5 枚）——此族非簡體、非日新字体，
    #   故簡形閘與第 57 檢俱不較，是『名單之外』之又一例。
    _jp35 = [u'L%d' % (i + 1) for i, l in enumerate(LINES) if u'・' in l]
    ck(u'全書無日式間隔號 U+30FB（隔號通例作『·』）', not _jp35,
       u'%d 行 %s' % (len(_jp35), _jp35[:5]))

    # 印面之工程指涉與不隨冊之底冊死指針（第 147 輪立）：附錄F-3 一行舊云『一以附錄L 某行為準——
    #   該行由 `_tk.py` 當場復測』，而附錄L 屬編纂底冊本就不入印本，腳本名更非讀者所有，
    #   遂成冊內死指針與工務口語（第 86 輪治精簡本之幽靈指針，未治此類『指往不印之底冊』者）。
    #   卷首目錄之存目行與結語之存檔聲明係如實交代何者不隨冊，不在病數，故目錄區塊免掃。
    _b147 = set(bottom_lines())
    _toc0 = next((i for i, l in enumerate(LINES) if l.startswith(u'### 目錄')), None)
    _toc1 = next((i for i in range((_toc0 or 0) + 1, len(LINES))
                  if LINES[i].startswith(u'# ')), len(LINES))
    _ENG = re.compile(r'_tk|_work|_archive|\.py\b|\.md\b|build38|verify38|ledger|rows2|pandoc|typst'
                      r'|腳本|一跑即平'
                      # 第 154 輪益：編務自用之詞不得入印（外路第二十批「語域」一節，量得印面本零見，
                      #   唯「查核器」「印面」「實測」舊各一二見，今已改從書中本語，此守其不回流）
                      r'|查核器|印面|負測|不變量|機械查核')
    _BOT = re.compile(r'附錄\s*[CKLM]|終卷')
    _engbad = []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or (_toc0 is not None and _toc0 <= _i < _toc1):
            continue
        if _ENG.search(_l):
            _engbad.append(u'L%d 工程語' % (_i + 1))
        elif _BOT.search(_l):
            _engbad.append(u'L%d 底冊指針' % (_i + 1))
    ck(u'印面無工程指涉與不隨冊之底冊指針（目錄存目行免）', not _engbad,
       u'%d 處 %s' % (len(_engbad), _engbad[:6]))

    # 准／準之分工（第 149 輪立）：許可義（准許、核准、不准、特准、准予、准入）須作『准』，
    #   標準義（標準、準則、基準、校準、精準、準繩、準確、準備、準用、準據）須作『準』。
    #   簡轉繁工具將兩字合流為『準』，故許可義諸語歷輪盡成字傷（第 148 輪來報始指之，覆核俱屬實）。
    #   兩向俱校：印面見許可義之『準』即報；全書引號外見標準義之『准』亦報（引號內為法條逐字，從寬）。
    _PERM_R = re.compile(u'方準|不準|特準|準予|準入|準其|獲準|準隨|準前|仍準依|後準受|唯準')
    _KEEP_R = re.compile(u'不準確|不準則')
    _zbad = []
    for _i, _l in enumerate(LINES):
        if _i in _b147:
            continue
        _m = [x.group(0) for x in _PERM_R.finditer(_l) if not _KEEP_R.match(_l[max(0, x.start()):x.start() + 3])]
        if _m:
            _zbad.append(u'L%d %s' % (_i + 1, u'、'.join(sorted(set(_m)))[:14]))
    _plain69 = re.sub(r'「[^」]*」|『[^』]*』', '', u'\n'.join(LINES))
    _zhbad = [w for w in (u'標准', u'准則', u'准據', u'水准', u'精准', u'准確', u'准備', u'基准', u'校准', u'准時')
              if w in _plain69]
    ck(u'准／準之分工（許可義作准、標準義作準；印面校前者、全書校後者）',
       not _zbad and not _zhbad, u'許可義之『準』%d 處｜標準義之『准』%s' % (len(_zbad), _zhbad[:4]))

    # 印面標點與引號之形制兩檢（第 150 輪自掘立）：
    #  70 半形標點夾入漢字之間——簡轉繁與 markdown 手習最易落下「漢字,漢字」「漢字?漢字」之形，
    #     於印面為體例之傷（全書標點通例作全形）；圍欄內（ASCII 圖、表單、程式性文字）從寬不校。
    #  71 段內引號不得交叉、不得失配——逐行校則跨行之引文盡成假陽性（實測印面有五處如此），
    #     故以「段」（空行所隔之連續行块）為位，唯求其「『「與』』之次序各如其.stack，不少閉、不多閉、不交叉。
    _f70 = [False] * len(LINES)
    _in70 = False
    for _i, _l in enumerate(LINES):
        if _l.strip().startswith(u'```'):
            _in70 = not _in70
            _f70[_i] = True
            continue
        _f70[_i] = _in70
    _CJ = u'\u3400-\u4dbf\u4e00-\u9fff'
    _P70 = re.compile(u'[%s][,;:?!.(]|[,;:?!.)][%s]' % (_CJ, _CJ))
    _p70 = []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _f70[_i]:
            continue
        _m70 = _P70.search(_l)
        if _m70:
            _p70.append(u'L%d[%s]' % (_i + 1, _m70.group(0)))
    ck(u'印面無半形標點夾入漢字之間（圍欄內從寬）', not _p70, u'%d 處 %s' % (len(_p70), _p70[:5]))

    def _seg71():
        cur = []
        for _i, _l in enumerate(LINES):
            if _i in _b147:
                if cur:
                    yield cur
                    cur = []
                continue
            if _l.strip() == u'':
                if cur:
                    yield cur
                cur = []
            else:
                cur.append(_l)
        if cur:
            yield cur
    _p71 = []
    for _si, _seg in enumerate(_seg71()):
        _txt = u''.join(_seg)
        _st = []
        _e = u''
        for _ch in _txt:
            if _ch in (u'「', u'『'):
                _st.append(_ch)
            elif _ch in (u'」', u'』'):
                if not _st:
                    _e = u'多閉'
                    break
                if _st[-1] == (u'「' if _ch == u'」' else u'『'):
                    _st.pop()
                else:
                    _e = u'交叉'
                    break
        if _e or _st:
            _p71.append(u'%s@段%d' % (_e or u'未閉', _si + 1))
    ck(u'印面引號以段為位不交叉不失配（「」『』）', not _p71, u'%d 段 %s' % (len(_p71), _p71[:5]))

    # 第 151 輪自掘立兩檢：
    #  72 標點不得疊用或錯置相接——「。，」「，：」「、、」之類多為套改時刪留不全所致；
    #     基線全書（含底冊）為零，故不設區之例外：底冊編年亦不得有（第 151 輪即由此清創修訂誌一枚）。
    #  73 印面世俗法條之引用一律疏排——書中今制作「第 75 條第 2 項」（數字兩側各一空格），
    #     而附錄J 舊全作「第75條」緊排（一冊之內兩式並出）；律條之漢字式（第十九條）不在此校。
    _P72 = re.compile(u'([，。、；：！？])\\1|[，。、；：！？](?:[。，、；：！？])')
    _p72 = []
    for _i, _l in enumerate(LINES):
        _m72 = _P72.search(_l)
        if _m72:
            _p72.append(u'L%d[%s]' % (_i + 1, _m72.group(0)))
    ck(u'全書標點不疊用、不錯置相接（，。、；：！？）', not _p72, u'%d 處 %s' % (len(_p72), _p72[:5]))

    _P73 = re.compile(u'第(\\s*)(\\d+)(\\s*)([條項款])')
    _p73 = []
    for _i, _l in enumerate(LINES):
        if _i in _b147:
            continue
        for _m73 in _P73.finditer(_l):
            if _m73.group(1) != u' ' or _m73.group(3) != u' ':
                _p73.append(u'L%d[%s]' % (_i + 1, _m73.group(0)))
    ck(u'印面世俗法條引用俱作疏排（第 N 條；律條漢字式不校）', not _p73, u'%d 處 %s' % (len(_p73), _p73[:5]))

    # 第 152 輪立：74 尼部之條不得但云『波逸提法第N條』——本律比丘部與比丘尼部**各自編號**，
    #   同號別戒（比丘波逸提第七十二條＝輕訶戒；尼波逸提第七十二條＝問比丘義戒），敘述層逸「比丘尼」
    #   三字即錯指全案。部別之判取附錄E 條次欄：以**最近的卷段標記**定部（22-30 屬尼分）或段前缀明現
    #   「比丘尼」者屬尼；唯取「戒名只見於尼部」者校之（兩名同見兩部者擱置不判，免生假陽性）。
    def _ni_part_map():
        try:
            _e0 = next(k for k, _l in enumerate(LINES) if _l.startswith(u'# 附錄E'))
            _e1 = next(k for k in range(_e0 + 1, len(LINES)) if LINES[k].startswith(u'# '))
        except StopIteration:
            return {}
        _vol = re.compile(u'(01-10|11-21|22-30|31-37|38-49|50-60)卷段')
        _num = re.compile(u'(比丘尼)?(八波羅夷法|波逸提法|波逸提|僧殘|波羅夷|尼薩耆波逸提|提舍尼)(?:法)?'
                          u'第([一二三四五六七八九十百零〇]{1,8}?)條(?:（([^）]{1,22}?)）)?')
        _m = {}
        for _k in range(_e0, _e1):
            _l0 = LINES[_k]
            if not _l0.strip().startswith(u'| **〔'):
                continue
            _cs = [c.strip() for c in _l0.strip().strip(u'|').split(u'|')]
            if len(_cs) < 2:
                continue
            _cur, _tk = None, []
            _tk += [(x.start(), u'v', x.group(1)) for x in _vol.finditer(_cs[1])]
            _tk += [(x.start(), u'n', x) for x in _num.finditer(_cs[1])]
            for _p, _kd, _v in sorted(_tk):
                if _kd == u'v':
                    _cur = _v
                elif _v.group(4):
                    _m.setdefault(_v.group(4), set()).add(
                        u'尼' if (_cur == u'22-30' or _v.group(1) == u'比丘尼') else u'比丘')
        return {k: v for k, v in _m.items() if v == set([u'尼'])}

    _ni74 = _ni_part_map()
    _CIT74 = re.compile(u'((?:比丘尼)?)((?:八波羅夷法|波逸提法|波逸提|僧殘|波羅夷|尼薩耆波逸提|提舍尼)'
                        u'第[一二三四五六七八九十百零〇]{1,8}?條)([^，。；：、\\s｜|（〕)]{0,22}?)戒')
    _p74 = []
    for _i, _l in enumerate(LINES):
        if _i in _b147:
            continue
        for _m74 in _CIT74.finditer(_l):
            _nm = _m74.group(3)
            if (_nm in _ni74 or (_nm + u'戒') in _ni74) and _m74.group(1) != u'比丘尼':
                _p74.append(u'L%d【%s】' % (_i + 1, _m74.group(2)))
    ck(u'印面引尼部之戒俱冠「比丘尼」（部別不逸；尼部戒名自附錄E 取）', not _p74,
       u'%d 處｜尼部戒名庫 %d 名 %s' % (len(_p74), len(_ni74), _p74[:4]))

    # 第 153 輪立：75 卷首目錄區塊內不得夾散文——管線以點線目錄**整段取代**該區
    #   （`build38.write_md`：自建目錄起點至「# 第一章」前止），故區內任何非列表之行永不入印。
    #   由來：第 148 輪於目錄附錄區塊之末補『附錄收編之界』一行以實結語之自指，歷五輪全綠而冊上無字。
    _t0 = None
    for _i75, _l75 in enumerate(LINES):
        if _l75.startswith(u'## \u3010全書開卷標準目錄') or _l75.strip() in (u'## 目錄', u'### 目錄'):
            _t0 = _i75
            break
    _p75 = []
    if _t0 is not None:
        _OK75 = re.compile(u'^(?:\\s*#|\\s*\\*|\\s*$|-{3,}|\\s*-{3,}\\s*$)')
        for _i75 in range(_t0, len(LINES)):
            if LINES[_i75].startswith(u'# 第一章'):
                break
            if not _OK75.match(LINES[_i75]):
                _p75.append(u'L%d[%s]' % (_i75 + 1, LINES[_i75][:24]))
    ck(u'卷首目錄區塊內無散文行（管線整段取代，區內散句永不入印）', not _p75,
       u'%d 行 %s' % (len(_p75), _p75[:3]))


    # 以篇名劃區者，篇名一動即斷鏈（第 143 輪立）。第 123 輪附錄M 去『工程』二字改名，
    #   `build38.DROP_H1` 當時隨改，而 `_work` 下九支軸仍以舊名為鑰——其『底冊不入掃』之界
    #   自彼輪起靜默失效，四十筆編年自述遂被當印面之病報出（freq88 不中 46 筆即此）。
    #   今管線一側立檢守之，本檔一側則改用 `bottom_lines()`（以 H1 篇界取之，改名不致失守）。
    _bp = os.path.join(ROOT, u'_print', u'build38.py')
    _dropk = []
    if os.path.exists(_bp):
        _bsrc = open(_bp, encoding='utf-8').read()
        _dm = re.search(u'DROP_H1\\s*=\\s*[\\(\\[]([^\\)\\]]*)[\\)\\]]', _bsrc, re.S)
        if _dm:
            _dropk = [x for x in re.findall(u'[\'"]([^\'"]+)[\'"]', _dm.group(1)) if x]
    _h1t = [l[2:].strip() for l in LINES if l.startswith(u'# ')]
    _deadk = [k for k in _dropk if not any(k in h for h in _h1t)]
    _deadn = [nm for nm in BOTTOM_NAMES if not sec(nm)]
    # 同一病之全域掃：凡工具端以篇名关键字劃區者（字串內含下列語），其語須配得實有 H1——
    #   第 123 輪改名後，九支軸之底冊排除俱靜默失效，歷二十輪無人覺，今使當場報。
    _WATCH = (u'修訂誌', u'款級', u'十維驗收', u'校勘記', u'竣工呈辭')
    _stale = []
    for _tf in [os.path.join(ROOT, u'_tk.py'), _bp] + sorted(
            glob.glob(os.path.join(WORK, u'*.py'))):
        if not os.path.exists(_tf):
            continue
        try:
            _src = open(_tf, encoding='utf-8').read()
        except Exception:
            continue
        _lits = []
        # ① 劃區名單之賦值（變數名含 DROP／BOTTOM／NOPRINT／EXCL／SKIP／NO）
        for _m2 in re.finditer(
                u'\\b([A-Za-z0-9_]*(?:DROP|BOTTOM|NOPRINT|EXCL|SKIP)[A-Za-z0-9_]*)\\s*=\\s*'
                u'[\\(\\[](.{0,400}?)[\\)\\]]', _src, re.S):
            _lits += re.findall(u'[\'"]([^\'"\\n]{2,20})[\'"]', _m2.group(2))
        # ② 行內比較（"X" in l ／ "X" in title 之類就地劃區）
        _lits += re.findall(u'[\'"]([^\'"\\n]{2,20})[\'"]\\s*in\\s+\\w+', _src)
        for _lit in _lits:
            # 只問『關鍵語之形』者（短且無句讀）；散文敘述不入此制
            if not (2 <= len(_lit) <= 12) or re.search(u'[、，。；：！？（）「」『』【】/]', _lit):
                continue
            if any(k in _lit for k in _WATCH) and not any(_lit in h for h in _h1t):
                _stale.append(u'%s:%s' % (os.path.basename(_tf), _lit[:16]))
    ck(u'工具端以篇名劃區之關鍵語俱配實有篇名（改名斷鏈之防）',
       bool(_dropk) and not _deadk and not _deadn and not _stale,
       u'管線 %d 語｜死語 %s｜本檔不著 %s｜工具死語 %s' % (
           len(_dropk), _deadk[:2], _deadn[:2], sorted(set(_stale))[:4]))

    # 『第X章第Y節第Z款』類指針須落在實有標題之上（款號兼收『十至十三、』之併列款）
    _CN = {c: n for n, c in enumerate(u'零一二三四五六七八九')}

    def _c2n(s):
        if not s:
            return None
        m = re.fullmatch(r'([一二三四五六七八九])?十([一二三四五六七八九])?', s.strip())
        if m:
            return _CN.get(m.group(1), 1) * 10 + _CN.get(m.group(2), 0)
        return _CN.get(s.strip())

    def _num(t, pats):
        for p in pats:
            m = re.match(p, t)
            if m:
                if m.lastindex == 2:
                    return list(range(_c2n(m.group(1)), _c2n(m.group(2)) + 1))
                v = _c2n(m.group(1))
                return [v] if v else []
        return []

    _SP = [u'^第([一二三四五六七八九十]+)節', u'^閘門([一二三四五六七八九十]+)', u'^（([一二三四五六七八九十]+)）',
           u'^([一二三四五六七八九十]+)、']
    _KP = [u'^([一二三四五六七八九十]+)至([一二三四五六七八九十]+)[、，]', u'^([一二三四五六七八九十]+)、',
           r'^(\d+)[\.、]', u'^（([一二三四五六七八九十]+)）']
    _cb = [i for i, l in enumerate(LINES) if re.match(r'^# 第[一二三四五六七八九]章', l)]
    _cb.append(next(i for i, l in enumerate(LINES) if l.startswith(u'# 結語')))
    _tree, _span2 = {}, {}
    for _k in range(len(_cb) - 1):
        _nmch = u'第%s章' % u'一二三四五六七八九'[_k]
        _span2[_nmch] = (_cb[_k], _cb[_k + 1])
        _secs, _cur = [], None
        for j in range(_cb[_k] + 1, _cb[_k + 1]):
            _lt = LINES[j]
            if _lt.startswith('### '):
                _cur = {'n': _num(_lt[4:].strip(), _SP), 'i': j}
                _secs.append(_cur)
            elif _lt.startswith('#### ') and _cur is not None:
                _cur.setdefault('k', []).extend(_num(_lt[5:].strip(), _KP))
        _tree[_nmch] = _secs
    _pbad = []
    for i2, l2 in enumerate(LINES):
        _own = next((n for n, (s0, e0) in _span2.items() if s0 <= i2 < e0), None)
        for m in re.finditer(u'(?:第([一二三四五六七八九])章|本章|此章)'
                             r'\s*(?:第([一二三四五六七八九十]+)節|閘門([一二三四五六七八九十]+))?'
                             u'(?:第([一二三四五六七八九十]+)款)?', l2):
            _ch = (u'第%s章' % m.group(1)) if m.group(1) else _own
            if _ch not in _tree:
                continue
            _sn = _c2n(m.group(2)) if m.group(2) else _c2n(m.group(3))
            _kn = _c2n(m.group(4))
            if _sn is None or _kn is None:
                continue
            _sc = next((x for x in _tree[_ch] if _sn in x['n']), None)
            if _sc is None:
                _pbad.append('%s(L%d)' % (m.group(0), i2 + 1))
            elif _kn not in _sc.get('k', []):
                _pbad.append('%s→款缺(L%d)' % (m.group(0), i2 + 1))
    ck(u'章節款指針無死鏈', not _pbad, '%d 處 %s' % (len(_pbad), _pbad[:5]))
    # —— 指針須具節級：卷首凡例第七條明定『章直轄節，節下為款』，故書中不得有「某章某款」之越級縮寫
    #    （第 128 輪立：附錄F-3 一行舊作「第二章款七」，上條以節號為鑰，故於此類縮寫全無感。
    #     底冊兩篇免掃：附錄C 修訂誌與全書校勘記乃歷輪實錄，依『編年不回改』之例不較。）
    _bot = bottom_lines()
    _abbr = []
    for i2, l2 in enumerate(LINES):
        if i2 in _bot:
            continue
        for m in re.finditer(u'(?:第[一二三四五六七八九]章|本章|此章)(?:款|第[一二三四五六七八九十]+款)', l2):
            _abbr.append('%s(L%d)' % (m.group(0), i2 + 1))
    ck(u'指針具節級（嚴禁『某章某款』式縮寫）', not _abbr, str(_abbr[:5]))
    # 八大正理之定名：卷首標尺、第一章定文、第七章總表等處須同名（第一章第二節為唯一法定定文）
    _z = {}
    for m in re.finditer(r'^> \*\*正理([一二三四五六七八])[：:]([^*\n]{2,20})\*\*', DOC, re.M):
        _z0 = re.split(r'[（(—\s]', m.group(2).strip())[0]
        if len(_z0) >= 3 and m.group(1) not in _z:
            _z[m.group(1)] = _z0
    _zbad = []
    for i2, l2 in enumerate(LINES):
        # 『』與「」之內係提及舊名（如編年引昔日之誤寫），非今之宣稱——與簡形閘口同一豁免之例
        l2 = re.sub(u'「[^」]*」|『[^』]*』', '', l2)
        for m in re.finditer(r'正理([一二三四五六七八])[：:]\**([^（()、，。；：|*\n]{2,20})', l2):
            nm = re.split(r'[—\s]', m.group(2))[0]
            par = _z.get(m.group(1))
            if par and nm != par:
                _zbad.append(u'%s≠%s(L%d)' % (m.group(0)[:14], par, i2 + 1))
    ck(u'八大正理定名不兩樣', not _zbad, '%d 處 %s' % (len(_zbad), _zbad[:4]))
    L1V = {u'貪', u'瞋', u'癡', u'慢', u'清淨', u'無記',
           u'懈怠', u'判準態', u'總則', u'無'}
    L2V = {u'覆', u'慳', u'掉舉', u'悔'}
    vbad, vcnt = [], 0
    for vi, vl in enumerate(LINES):
        if not vl.strip().startswith(u'**定位'):
            continue
        vm = POS_RE.match(vl.strip())
        if not vm:
            continue
        vcnt += 1
        vhead = re.split(u'對比', vm.group(1))[0]
        for vk, vt in enumerate(re.split(u'加', vhead)):
            vb = re.split(u'（', vt)[0].strip()
            if vb in L1V or (vb in L2V and vk > 0):
                continue
            vbad.append(u'%s(L%d)' % (vb, vi + 1))
    ck(u'定位行根本心須在宣告詞彙內',
       not vbad and vcnt >= 100, u'%d 越詞 %s' % (len(vbad), vbad[:5]))

    # 全書 Markdown 表：凡有分隔列之真表，其每一資料列之管數須與表頭同、行末必閉管、行尾無空白
    # （第 134 輪立。舊制僅點驗數個特定表之「五行四欄」定型式，其餘表一筆未校；
    #  外路第十三批改 F-1 時落一行缺尾管，恰在舊過濾之外，md 檢與印面六軸俱未接到）
    _tb, _ntab, _k = [], 0, 0
    while _k < len(LINES):
        if not LINES[_k].lstrip().startswith(u'|'):
            _k += 1
            continue
        _j = _k
        while _j < len(LINES) and LINES[_j].lstrip().startswith(u'|'):
            _j += 1
        if _j - _k >= 2 and re.match(u'^\\s*\\|[\\s:|-]+\\|\\s*$', LINES[_k + 1]):
            _ntab += 1
            _h = LINES[_k].count(u'|')
            for _r in range(_k + 1, _j):
                _t = LINES[_r]
                if (_t.count(u'|') != _h or not _t.rstrip().endswith(u'|')
                        or _t.rstrip() != _t):
                    _tb.append(u'L%d(%d≠%d)' % (_r + 1, _t.count(u'|'), _h))
        _k = _j
    ck(u'全書表格欄數與表頭齊（閉管·無尾空白）',
       not _tb and _ntab >= 50, u'%d 表不合格 %s' % (len(_tb), _tb[:6]))

    # 印面無懸空標題（第 141 輪立。第二章第六節第一款之正文於歷輪搬遷中遺落，
    #   只餘一光題直連下一光題，而卷首目錄仍列其目——舊檢唯校指針之死鏈，
    #   於「有目無文」之另一向（链接尚在、內容已空）全無感）。
    #   法：各級標題（H1–H5，柵欄內不計）之下、下一同級或更粗之標題之前，必實有內文。
    #   （第 189 輪由 H4 扩至 H5：第七章第三節九個「板塊」H5 光題直連同級子題，
    #     因本檢止於 H4 而歷輪無聲——懸空之形不因級別而減，故扩之；先補九句板塊導言，再扩閘。）
    _inf, _fc = set(), False
    for _i, _l in enumerate(LINES):
        if _l.startswith(u'```'):
            _fc = not _fc
            _inf.add(_i)
            continue
        if _fc:
            _inf.add(_i)
    _hs = [(_i, len(re.match(u'^(#{1,5}) ', _l).group(1)))
           for _i, _l in enumerate(LINES)
           if _i not in _inf and re.match(u'^#{1,5} ', _l)]
    _dang = []
    for _a in range(len(_hs) - 1):
        _i, _lv = _hs[_a]
        _j, _lv2 = _hs[_a + 1]
        if _lv2 > _lv:
            continue
        if not [1 for _k in range(_i + 1, _j) if LINES[_k].strip()]:
            _dang.append(u'L%d(h%d)' % (_i + 1, _lv))
    ck(u'全書標題不懸空（H1–H5 之下必實有內文）',
       not _dang, u'%d 處 %s' % (len(_dang), _dang[:6]))

    # 列表序號不得合寫（第 141 輪立。第五章第四節第一款舊作「1-2.」，
    #   CommonMark 不認此式為清單項，故其下之「3.」成列表首項——印面階梯遂自三起算）
    _combo = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
              if _i not in _inf and re.match(u'^\\s*\\d+\\s*[-\u2013\u2014]\\s*\\d+\\.[\\s\u3000]', _l)]
    ck(u'列表序號無「N-M.」合寫式', not _combo, u'%d 處 %s' % (len(_combo), _combo[:6]))

    # ── 76／77（第 173 輪立，俱由產物層實排逮得，非源層目測所能見）──
    # 76 『---』緊接文字行：pandoc 認作 setext 二級標題而非分隔線。書中因此多出一枚 h2
    #     （並入 PDF 大綱），另有兩處在段末印出一個多餘的「—」。
    # 77 引言塊末行為有內容之「> …」而次行未留空行：lazy continuation 將次行吸入框內
    #     （實測：第五章『逆向制衡』一段被吞入上方法益框，紙上成引文而實非引文）。
    _setext, _swallow = [], []
    for _i in range(1, len(LINES)):
        if _i in _b147 or _i in _inf:
            continue
        _s = LINES[_i].strip()
        _p = LINES[_i - 1].strip()
        if _s in (u'---', u'***') and _p and not _p.startswith((u'#', u'|', u'`')):
            # 『> …』之行首亦在劫持之列（第八章『留白』即被吸成框內 h2），故不排『>』
            _setext.append(u'L%d' % (_i + 1))
        if (_p.startswith(u'>') and _p.strip(u'> \u3000') and _s
                and _s not in (u'---', u'***')
                and not _s.startswith((u'>', u'#', u'|', u'`', u'<'))
                and LINES[_i - 1].startswith(u'>') and not LINES[_i].startswith(u' ')):
            # 唯『行首之 >』方會吞下一步同行首之文；縮排於列項內的引文（如第八章定音叉
            # 諸條之「  > …」）其後同層列項本屬並列，非被吞——不收此形即七筆假陽性。
            _swallow.append(u'L%d(%s)' % (_i + 1, u'列' if re.match(u'^[-*+] |^\\d+[.)、]', _s) else u'文'))
    ck(u'印面無 setext 標題劫持（『---』之前須留空行）',
       not _setext, u'%d 處 %s' % (len(_setext), _setext[:6]))
    ck(u'印面引言塊不吞後段（『>』有內容者，次行須留空行）',
       not _swallow, u'%d 處 %s' % (len(_swallow), _swallow[:6]))
    # 78 篇題（H1）之前須有分隔線：全書 24 篇之界，歷輪搬遷中遺落一枚（附錄D 舊直續附錄C 末行，
    #    紙上兩篇之間無界）——首篇之前乃封面題辭，不較。
    _h1 = [i for i, _l in enumerate(LINES) if _l.startswith(u'# ')]
    _nosep = []
    for _i in _h1[1:]:
        _j = _i - 1
        while _j > 0 and (LINES[_j].strip() == u'' or LINES[_j].lstrip().startswith(u'<!--')):
            _j -= 1
        if LINES[_j].strip() not in (u'---', u'***'):
            _nosep.append(u'L%d(%s)' % (_i + 1, LINES[_i][2:9].replace(u'　', u' ')))
    ck(u'篇題之前一律有分隔線（H1 不直貼前篇末行）',
       not _nosep, u'%d 處 %s' % (len(_nosep), _nosep[:6]))
    # 79 列項續行之縮排：CommonMark 以『標記 indent＋標記寬』為項之內容欄；續段欲屬本項，
    #    縮排須恰等於該欄，歸零則出巢自立——介乎其間者為野縮排，印面或黏為上項之尾（軟換行）
    #    或脫巢為 flush 段，全憑解析器寛容。第 175 輪掃得十二處，其中閘門五『佛滅後劃界』之兩注
    #    一在巢內一在巢外，紙上裂為兩層（即 173 輪『斜體碎裂』之半治）。
    _mk = re.compile(u'^(\\s*)(?:([-*+])[ \u3000]{1,4}|\\d{1,3}[.)、][ \u3000]{1,4})(\\S)')
    _cols, _stray = [], []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _i in _inf or not _l.strip():
            continue
        _m = _mk.match(_l)
        if _m:
            _c = len(_m.group(0)) - 1
            while _cols and _cols[-1] >= _c:
                _cols.pop()
            _cols.append(_c)
            continue
        if re.match(u'^\\s*(\\||#|<|`|>\\s*$)', _l):
            continue
        _w = len(_l) - len(_l.lstrip(u' \u3000'))
        while _cols and (len(_l) - len(_l.lstrip(u' '))) < _cols[-1]:
            _cols.pop()
        if _w and _w not in _cols:
            _stray.append(u'L%d(縮%d)' % (_i + 1, _w))
    ck(u'印面無野縮排（續行須在巢欄或歸零）',
       not _stray, u'%d 處 %s' % (len(_stray), _stray[:8]))
    # 80／81 以『段』為位數粗體記號之奇偶與六族括號之平衡（第 176 輪立）。
    #    80 之病緣：173 輪『洗白。** 惟』之接縫星號落單，紙上印出字面記號——彼時唯人眼逮得；
    #    81 之病緣：歷輪之誤落單括（如案語末之『）』）向由 `mdlint` 之成對檢兼_capture，
    #    今以段為位，跨段之正格嵌套不誤傷（同行計之則「（如…（嫉）…）」盡成假陽性）。
    _blk, _bc, _inc = [], [], False
    for _i, _l in enumerate(LINES):
        if _l.lstrip().startswith(u'```'):
            _inc = not _inc
            if _bc:
                _blk.append(_bc); _bc = []
            continue
        if _inc or _i in _b147 or _l.strip().startswith((u'<!--', u'-->')):
            continue
        if _l.strip() == u'' or _l.startswith(u'#'):
            if _bc:
                _blk.append(_bc); _bc = []
            continue
        if _l.lstrip().startswith(u'|'):
            if _bc:
                _blk.append(_bc); _bc = []
            _blk.append([(_i, _l)])
            continue
        _bc.append((_i, _l))
    if _bc:
        _blk.append(_bc)
    _odd, _unal = [], []
    for _b in _blk:
        _tx = re.sub(u'<[^>]{1,60}>', u'', re.sub(u'`[^`]*`', u'        ',
                     u'\n'.join(_x for _, _x in _b)))
        _tx = re.sub(u'⁽\\\\?\\*[^⁾]*⁾', u'', _tx)          # 腳注符 ⁽*¹⁾ 乃字面星號，不入計
        _n = len(re.findall(u'(?<!\\\\)\\*\\*', _tx))
        if _n % 2:
            _odd.append(u'L%d(%d)' % (_b[0][0] + 1, _n))
        for _a, _z in ((u'（', u'）'), (u'〔', u'〕'), (u'「', u'」'),
                       (u'『', u'』'), (u'《', u'》'), (u'［', u'］')):
            if _tx.count(_a) != _tx.count(_z):
                _unal.append(u'L%d(%s%d/%s%d)' % (_b[0][0] + 1, _a, _tx.count(_a), _z, _tx.count(_z)))
    ck(u'印面粗體記號段內成對（『**』不落單）',
       not _odd, u'%d 處 %s' % (len(_odd), _odd[:6]))
    ck(u'印面六族括號段內平衡', not _unal, u'%d 處 %s' % (len(_unal), _unal[:6]))
    # 82 四制括號各司其形（第 177 輪立。凡例第七條：〔〕主考證標籤、【】主標題與通道、
    #    ［］主圍欄圖內心所切片、[ ] 主檢核框與問序）。病緣：問序歷輪以半形 [N] 為制（印面 94 處），
    #    卻有三處掛成六角『第〔10〕問』——形制既倒，`qindex` 據半形取鑰，遂於無形中漏計其引用。
    _badbr = []
    _rxs = [(u'問序掛錯形', re.compile(u'[〔［【]\\d+[〕］】]問|問[〔［【]\\d+[〕］】]')),
            (u'案號掛錯形', re.compile(u'[\\[［【](?:遮|開|僧)\\d+[\\]］】]')),
            (u'通道掛數字', re.compile(u'【\\d+】')),
            # 第 206 輪補第四形之防：印面舊有 15 行以 Markdown 跳脫『\(N\)』為編序（第五章『非法足數
            # 十五類』一處獨有，全書餘處皆全形（）或半形 [] 問序），既非『括號四制』所載之職，
            # 又於全形語中夾半形之形——今歸全形（N），此式不許再入印面。
            # 口徑只禁『\(數字\)』整體，不禁單枚『\)' 或『\*』：印面 L2080–2083 之腳注作『⁽\*²⁾』，
            # 其 backslash 乃跳脱星號所必需（實測 191 輪之產物 HTML 已吞 backslash 而只印『⁽*²⁾』，非病）——
            # **一口刀切必把正字讀成病**（175 輪『族內各有其制』同例）。
            (u'編序掛跳脱', re.compile(r'\\\(\d{1,2}\\\)'))]
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _i in _inf:
            continue
        for _n, _rx in _rxs:
            for _m in _rx.finditer(_l):
                _badbr.append(u'L%d(%s:%s)' % (_i + 1, _n, _m.group(0)[:8]))
    ck(u'印面四制括號各司其形（問序半形・案號六角・編序不跳脱）',
       not _badbr, u'%d 處 %s' % (len(_badbr), _badbr[:6]))
    # 85 標題末不帶句讀（第 207 輪立。自掘七維之測：印面 H1–H5 有三十行以全形冒號收——二十九枚乃案例
    #    卡片之 H5 欄名、一枚乃第九章款題；標題職在分節，領句乃正文之責，且同一欄名在諸卡間因尾冒之有無
    #    而成兩式並存。今削之並守其制。圍欄與底冊從寬。）
    _hd = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
           if _i not in _b147 and _i not in _inf and _l.startswith(u'#')
           and _l.rstrip(u' ')[-1:] in (u'：', u'。', u'，', u'、', u'；', u'！')]
    ck(u'印面標題末不帶句讀（H1–H5）', not _hd, u'%d 處 %s' % (len(_hd), _hd[:6]))
    # 86 行末空白不是一枚（第 207 輪立。硬換行須兩枚空格：一枚既不成換行、又不可見，歷輪引塊空行所積
    #    之尾枚空格俱屬半宣言之噪音（本輪削 72 枚，全在引塊行）。圍欄內之圖從寬、底冊舊錄從寬。）
    _tl = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
           if _i not in _b147 and _i not in _inf and _l.strip()
           and len(_l) - len(_l.rstrip(u' ')) == 1]
    ck(u'印面行末空白不是一枚（零枚或兩枚硬換行）', not _tl, u'%d 處 %s' % (len(_tl), _tl[:6]))
    # 87 篇題之譯字異形不回流（第 215 輪立。自掘名相維：印面篇題通作『犍度』196 見，別錄三處括註與一處底冊
    #    作『揵度』——本律原文兩式俱有（揵度 54／犍度 14），書中自定其一為正（犍度），異形唯許見於逐字引文之內。
    #    尺須取**兩字之整體**：單字『揵』於書中有職（尼揵子、目揵連皆律文正形，見附錄D-3），一刀切即把正字讀成病
    #    （本輪初版即如此，負測⓪③三路同報不中現形）。此門與簡形閘同法：先剝引號再搜。）
    _kd = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
           if _i not in _b147 and _i not in _inf
           and u'揵度' in re.sub(u'「[^」]*」|『[^』]*』', u'', _l)]
    ck(u'印面引號外無篇題異形『揵度』（通作犍度）', not _kd, u'%d 處 %s' % (len(_kd), _kd[:6]))
    # 88 考證案語之括號與標籤畫一（第 218 輪立。卷首『括號之四制』明定〔…〕主考證與標籤、四制各司其形
    #    不得互易；實測印面〔案：61／〔編者X17 俱六角，別有『（編者按：…）』三處置考證於全形圓括號、
    #    又『〔按：』一處與通例『〔案：』異字同職（本輪已歸位）。此閘只校**標籤之形**，不校何語當為案語
    #    （『（』包夾注乃全書通例，其職不同，故唯點名此二式）；引號之內從寬——如它日有照錄之文自帶此形，不犯。）
    _an = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
           if _i not in _b147 and _i not in _inf
           and re.search(u'[（(]\\s*編者按|〔\\s*按[：:]',
                         re.sub(u'「[^」]*」|『[^』]*』', u'', _l))]
    ck(u'印面考證案語不作『（編者按』與『〔按：』兩式（當從六角〔編者按：／〔案：）', not _an, u'%d 處 %s' % (len(_an), _an[:6]))
    # 89 節引之刪節號在引號之內須作兩枚（第 219 輪立。實測印面：『……』861 見（引號內 844），單枚『…』
    #    12 見——其中 5 見乃 L228 凡例『以符號示符號』之示例〔…〕【…】［…］，2 見在附錄F-3 引文欄之裸列
    #    摘句（該欄本無引號），餘 5 見散入「」『』為節引（L3081・L11711・L11721・L11789・L11792，本輪歸位）。
    #    211 輪曾以『凡例第二律只宣標不宣形』而全數從寬；今再量，見同職而异形——末截斷亦作兩枚（L753
    #    『壞伊羅鉢樹葉……』即其證），故知一枚非另一職，只是形制分歧（國標標點用法亦作兩枚）。
    #    從寬三域：佔位式括號（〔〕【】［］）內之 …、引號外之裸列摘句、圍欄與底冊（附錄M 記錄如實登載舊形）。
    #    尺之教（亦載 r199ellipsis 碼內註）：數單枚須前後皆不接『…』，否則把兩枚之第二枚算成單枚（虛數 873 之失）。）
    _el = []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _i in _inf:
            continue
        for _m in re.finditer(u'「[^」]*」|『[^』]*』', _l):
            _sg = re.sub(u'〔[^〕]*〕|【[^】]*】|\\[[^\\]]*\\]', u'', _m.group(0))
            if re.search(u'(?<!…)…(?!…)', _sg):
                _el.append(u'L%d' % (_i + 1))
                break
    ck(u'印面引號內之節引不作單枚『…』（當從通例『……』；佔位式括號與裸列摘句從寬）', not _el, u'%d 處 %s' % (len(_el), _el[:6]))
    # 90 印面標題行內不摻粗體記號（第 219 輪立。H1–H5 之粗乃版式之職，行內再加 ** 於產物層得
    #    <h5><strong>…</strong></h5> 之重疊（實測 _print/ver38_列印版.html，故非字面外洩而是冗記），
    #    於源層則是 markdown 標記混入標題——第 8 輪『源碼外洩』之族。全書標題 1,238 枚（H1 19／H2 4／
    #    H3 111／H4 435／H5 669）唯 L2240 一枚摻粗（本輪歸位），通例明確。）
    _hb = [u'L%d' % (_i + 1) for _i, _l in enumerate(LINES)
           if _i not in _b147 and _i not in _inf
           and re.match(u'^#{1,5} ', _l) and u'**' in _l]
    ck(u'印面標題行內不摻粗體記號（『**』不入 H1–H5）', not _hb, u'%d 處 %s' % (len(_hb), _hb[:6]))
    # 91 印面引號外且圍欄外不作半形圓括號（第 221 輪立。實測印面引號外之半形圓括號凡 37 見，其職有兩：
    #    ① 圍欄圖層 21 見——ASCII 圖之邊標籤，半形乃就欄格之緊縮式（其中 13 見之右側另有節點或箭頭須守列，
    #       改全形則欄位右移而破框；同層之全形括號 275 行俱為不涉欄格之括注，故兩式之別在格不在職），從寬不刀，
    #       其『一職兩式』連欄格重排者候與四式重建併辦；② 表列拉丁子題 16 見——『中文名＋br＋半形括拉丁』
    #       與同表鄰行之『＋br＋全形括 Samodhāna＋全形括』異形同職（全書含拉丁之括號：全形 183、半形 16，
    #       而表列一格之內全形已 24 見），本輪十六處歸全形。豁免之界由『容器』定，不由『字形』定——與 206 輪
    #    之腳注跳脫星號、215 輪之『揵度』同法：閘之單位須與病之單位同寬，一刀切即把正字讀成病。引號之剝除
    #    走遍全檔以度計（第 220 輪之制：同線正則遇跨行巢套即錯配）；底冊從寬——附錄M 之記錄如實登載舊形。）
    _n1 = _n2 = 0
    _nl = 0
    _hp = []
    for _wc in DOC:
        if _wc == u'\n':
            _nl += 1
            continue
        if _wc == u'「':
            _n1 += 1
        elif _wc == u'」':
            _n1 = max(0, _n1 - 1)
        elif _wc == u'『':
            _n2 += 1
        elif _wc == u'』':
            _n2 = max(0, _n2 - 1)
        elif _n1 == 0 and _n2 == 0 and _wc == u'(' and _nl not in _b147 and _nl not in _inf:
            _hp.append(u'L%d' % (_nl + 1))
    ck(u'印面引號外且圍欄外不作半形圓括號（圍欄以半形就欄格，有職從寬）', not _hp, u'%d 處 %s' % (len(_hp), _hp[:6]))
    # 92 印面漢字並列不作半形斜線（第 222 輪立。實測印面・引號外・圍欄外之『漢斜線漢』凡 11 見，其職有兩：
    #    ① 表欄名『互見索引／備註』之舊形六枚（附錄E 三表與附錄F 三表之末欄）＋括號內之並列四枚（L9134 三鏡、
    #    L9288 境想三問）——並列與選擇之義以全形為通例（印面・非圍欄之漢漢：全形 92 對半形 11；散文 62 對 0；
    #    表列 30 對 11），此十枚無欄格之職（表列自換行），與 221 輪之表列拉丁子題同科 ⇒ 一刀歸全形；
    #    ② 字構拆描一枚（L11465『阿[少／兔]樓陀』之舊形）——拆部件之對照假半形方括號而立，與 L7066
    #    『[(殼-一)／牛]』同職（218、206 之誡：同一形有兩職，一刀切即把正字讀成病），故豁免之域取半形方括號之內。
    #    半形斜線之存者八見俱有職：HTML 閉標 2、外語名 2（Zoom 斜線 Teams、Benefit 斜線 Remediation）、比值 2
    #    （120/120、No.1428/1429）、路徑 2（『原文/』『佛經/』——右隨反引號故本不入漢漢之尺，且俱在行內程式碼段內）。
    #    圍欄之內另有半形斜線 33 見（221 之容器法：圖中緊縮就欄格）、引號之內 12 見（照錄側）、底冊 709 見（記錄從寬）。
    #    方括號之巢以行為界——實測全書半形方括號無一行不成對，跨行之巢不存在，故逐行重置其深度不失真；
    #    引號之巢則須跨行走（220 之誡）。此尺之兩側皆逐字符走深度：先剝後判會錯位（221 之教），故不剝而標位。
    #    閘名不用『・』——彼號乃全書所禁而記錄須照引閘名（221 之教，此器之註內亦不帶其形，唯述其碼位）。）
    _s1 = _s2 = 0
    _hs = []
    for _i, _l in enumerate(LINES):
        _bb = 0
        _ms = []
        for _c in _l:
            _ms.append(_s1 == 0 and _s2 == 0 and _bb == 0)
            if _c == u'「':
                _s1 += 1
            elif _c == u'」':
                _s1 = max(0, _s1 - 1)
            elif _c == u'『':
                _s2 += 1
            elif _c == u'』':
                _s2 = max(0, _s2 - 1)
            elif _c == u'[':
                _bb += 1
            elif _c == u']':
                _bb = max(0, _bb - 1)
        if _i in _b147 or _i in _inf:
            continue
        for _j, _c in enumerate(_l):
            if _c != chr(0x2F) or _j == 0 or _j + 1 >= len(_l) or not _ms[_j]:
                continue
            if 0x4E00 <= ord(_l[_j - 1]) <= 0x9FFF and 0x4E00 <= ord(_l[_j + 1]) <= 0x9FFF:
                _hs.append(u'L%d' % (_i + 1))
                break
    ck(u'印面漢字並列不作半形斜線（並列通例作全形『／』；路徑、比值、外語名、字構拆描從寬）', not _hs, u'%d 處 %s' % (len(_hs), _hs[:6]))
    # 93 印面引號之問嘆號後不重疊句號（第 231 輪立）。外路報第七章 L8362 一枚作『「汝以何心？」。樹幹』，
    #    親量印面（先剝粗體星、略圍欄與底冊）：「？」後一字凡 15 式 40 見、「！」後凡 15 式 49 見，
    #    而「？」加「。」、「！」加「。」、『？』加「。」、『！』加「。」四式俱 0 見 ⇒ 問號即句末、
    #    引號外不再著句號乃印面之通例，一枚即病（207『標題尾冒』、219『節引單枚』之同族）。
    #    剝星之必要：書中作粗體包引號，閉星落在引號與句讀之間，不剝則錯位（220 之細形）。
    _ov = []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _i in _inf:
            continue
        _s = _l.replace(u'**', u'')
        for _m in (u'？」', u'！」', u'？』', u'！』'):
            _p = 0
            while True:
                _j = _s.find(_m, _p)
                if _j < 0:
                    break
                if _s[_j + 2:_j + 3] == u'。':
                    _ov.append(u'L%d' % (_i + 1))
                    break
                _p = _j + 2
    ck(u'印面引號之問嘆號後不重疊句號（問號即句末；先剝粗體星再逐行搜）', not _ov, u'%d 處 %s' % (len(_ov), _ov[:6]))
    # 83 表段必帶分隔行（第 178 輪立。分隔行一缺，pandoc 不認其為表——第 110 輪『34 張表化為連寫文字』
    #    即此族之產物層大病，其時病在管線，今日防其病在源檔）：相鄰之『|』行連段，第二段須為
    #    由 -／:／空格組成分隔行，且欄數與表頭同。
    _runs, _k = [], 0
    while _k < len(LINES):
        if _k not in _b147 and _k not in _inf and LINES[_k].lstrip().startswith(u'|'):
            _j = _k
            while (_j + 1 < len(LINES) and _j + 1 not in _b147 and _j + 1 not in _inf
                   and LINES[_j + 1].lstrip().startswith(u'|')):
                _j += 1
            _runs.append((_k, _j))
            _k = _j + 1
        else:
            _k += 1
    _norun = []
    for _a, _b in _runs:
        if _b == _a:
            _norun.append(u'L%d(孤行)' % (_a + 1))
            continue
        if not re.match(u'^\\s*\\|[\\s:|-]+$', LINES[_a + 1]) or u'-' not in LINES[_a + 1]:
            _norun.append(u'L%d(二行非分隔)' % (_a + 1))
        elif LINES[_a].count(u'|') != LINES[_a + 1].count(u'|'):
            _norun.append(u'L%d(欄數不合)' % (_a + 1))
    ck(u'印面表格必帶分隔行且欄數與表頭合',
       not _norun, u'表段 %d 處｜病 %d 處 %s' % (len(_runs), len(_norun), _norun[:6]))
    # 84 標題不無端跨級（第 178 輪立）：全書之制為『章（H1）直入節（H3）』，此外不得跨兩級
    #    （跨則目錄縮排與分頁之算式失據）。今印面 H1..H5 凡 1,238 枚，跨級唯 H1→H3 十八處。
    _pre, _jump = None, []
    for _i, _l in enumerate(LINES):
        if _i in _b147 or _i in _inf:
            continue
        _m = re.match(u'^(#{1,6})\\s', _l)
        if not _m:
            continue
        _n = len(_m.group(1))
        if _pre and _n > _pre + 1 and not (_pre == 1 and _n == 3):
            _jump.append(u'L%d(H%d→H%d)' % (_i + 1, _pre, _n))
        _pre = _n
    ck(u'印面標題不無端跨級（唯章可直入節 H1→H3）',
       not _jump, u'%d 處 %s' % (len(_jump), _jump[:6]))


    # 「書中所載不變量項數＝實測」一條已退（第九十二輪・解綁令）：
    # 舊制須於附錄L 自報「52/52」，於是每增損一查即須改書；且其取文式不辨區，
    # 連編年舊檔之「共 52/52 項結構不變量全綠」亦作現況宣稱計之——一數之動，兩處隨。
    # 今書中不自錄項數（改由本器當場報數），此檢無可校，遂並退之。
    n_ok = sum(1 for _, ok, _ in inv)
    claims = []
    exp = (str(n_ok + 1), str(len(inv) + 1))
    badc = [c for c in claims if c != exp]
    _ = (badc, exp, n_ok)  # 項數自報之檢已退，見上註

    o = []
    npass = 0
    for n, ok, info in inv:
        npass += ok
        o.append('%s %-34s %s' % ('PASS' if ok else 'FAIL', n, ('' if ok and not info else ('| ' + info))))
    o.append('=' * 70)
    o.append('不變量 %d/%d PASS' % (npass, len(inv)))
    # 第 178 輪之治：emit 只印末 2000 字，故長報告之先段（含多數檢）在 stdout 中不可見；
    #   歷輪我以 `check > _work/check.txt` 收報，反把完整檔覆寫成尾段——於是有 FAIL 而 grep 不見。
    #   今於報告之**尾**再列 FAIL 清冊（尾段必入 stdout），並教以『stdout 丟棄、只讀 emit 檔』之收法。
    _bad = [(n, info) for n, ok, info in inv if not ok]
    if _bad:
        o.append(u'▼ 失敗清冊（%d 條）——勿以 stdout  redirection 覆寫本檔：收報請用 '
                 u'`python _tk.py check >/dev/null; grep -c "^FAIL" _work/check.txt`' % len(_bad))
        for n, info in _bad:
            o.append(u'   ✗ %s｜%s' % (n, info))
        txt = '\n'.join(o)
        emit(os.path.join(WORK, 'check.txt'), txt)
        return len(inv) - npass
    txt = '\n'.join(o)
    emit(os.path.join(WORK, 'check.txt'), txt)
    return len(inv) - npass        # 回 FAIL 數；第 120 輪前此值被丟棄，rc 恆零


# ---------------- probe ----------------
def do_probe(s):
    n = norm(s)
    o = ['probe raw=%s norm=%s len=%d' % (s[:60], n[:60], len(n))]
    o.append('四分律語料命中: %s' % ('YES @%d' % VINAYA.find(n) if n in VINAYA else 'NO (長前綴 %d/%d)' % (longest_prefix(n), len(n))))
    for k, v in OTHER.items():
        if n in v:
            o.append('佛經命中: %s' % k)
    if n not in VINAYA:
        for p, raw in [(k, None) for k in OTHER]:
            pass
        # fuzzy: report first divergent char position against best window
        o.append('提示: 以 longest_prefix 定位首個不符字符，必要時逐段縮小比對。')
    emit(os.path.join(WORK, 'probe.txt'), '\n'.join(o))


# ---------------- apply ----------------
def do_apply(tag, dry=False):
    path = os.path.join(WORK, 'patch_%s.json' % tag)
    patches = json.loads(read(path))
    src = read(SRC)
    o, applied, skipped = [], 0, 0
    for i, p in enumerate(patches):
        old, new = p['old'], p['new']
        c = src.count(old)
        if c == 1:
            src = src.replace(old, new)
            applied += 1
            o.append('OK   %2d %s' % (i + 1, old[:60]))
        else:
            skipped += 1
            o.append('SKIP %2d count=%d :: %s' % (i + 1, c, old[:60]))
        if 'note' in p:
            o.append('     note: %s' % p['note'])
    if not dry:
        open(SRC, 'w', encoding='utf-8').write(src)
    o.append('=' * 70)
    o.append('tag=%s applied=%d skipped=%d dry=%s' % (tag, applied, skipped, dry))
    emit(os.path.join(WORK, 'apply_%s.txt' % tag), '\n'.join(o))


def do_diff(raw):
    """對單段宣稱逐字之引文，逐段找出與語料首個不符處並排顯示。"""
    o = ['RAW: %s' % raw.strip()[:200]]
    for k, part in enumerate([p for p in ELL.split(raw)]):
        n = norm(part)
        if len(n) < 2:
            continue
        if n in VINAYA:
            o.append('  [%d] OK   (%d) %s' % (k + 1, len(n), n[:38]))
            continue
        lp = longest_prefix(n)
        at = VINAYA.find(n[:lp]) if lp else -1
        o.append('  [%d] MISS len=%d prefix=%d' % (k + 1, len(n), lp))
        if at >= 0:
            o.append('       文書端: %s' % n[lp - 6:lp + 34])
            o.append('       語料端: %s' % VINAYA[at + lp - 6: at + lp + 34])
        else:
            o.append('       起首即不符: %s' % n[:40])
    txt = '\n'.join(o)
    emit(os.path.join(WORK, 'diff.txt'), txt)


def do_order():
    idx = {}
    for i, l in enumerate(LINES):
        m = re.match(r'^#\s*(第[一二三四五六七八九]章)', l)
        if m:
            idx.setdefault(m.group(1), i)
    order = [h for h, _ in sorted(idx.items(), key=lambda kv: kv[1])]
    o = ['【物理章序】 ' + ' → '.join('%s(L%d)' % (h, idx[h] + 1) for h in order)]
    o.append('【章號序】 ' + '、'.join(h for h, _ in sorted(idx.items())))
    o.append('')

    # 目錄章條目次序
    toc_pos = []
    for i, l in enumerate(LINES[:400]):
        m = re.match(r'^\s*\*\s*\*\*(第[一二三四五六七八九]章)', l) or re.match(r'^#\s*(第[一二三四五六七八九]章)', l)
        if m and (m.group(1), i) not in toc_pos:
            toc_pos.append((m.group(1), i))
    seen = []
    for h, i in toc_pos:
        if h not in seen:
            seen.append(h)
    o.append('【目錄章序】 ' + ' → '.join(seen))
    o.append('目錄章序與物理章序 %s' % ('一致' if seen == order else '★不一致'))
    o.append('')

    BACK = ('上一章', '前章', '前一章', '前述', '前文', '上文', '已述', '前所', '前六章', '前五章', '前四章',
            '前三章', '前兩章', '前二章', '上章')
    FWD = ('下一章', '後章', '後一章', '後述', '下文', '詳後', '後出', '次章', '下接', '續章')
    o.append('【前後指涉語診斷】（BACK 指向物理在後之章／FWD 指向物理在前之章＝可疑）')
    def chap_of(i):
        cur = None
        for h in order:
            if idx[h] <= i:
                cur = h
        return cur
    sus = 0
    for i, l in enumerate(LINES):
        ch = chap_of(i)
        back = any(k in l for k in BACK)
        fwd = any(k in l for k in FWD)
        if not (back or fwd):
            continue
        refs = [h for h in re.findall(r'第[一二三四五六七八九]章', l)]
        for h in refs:
            if h not in idx:
                continue
            if back and idx[h] > idx[ch]:
                o.append('  可疑BACK  %s@L%-6d 指 %s(在後) :: %s' % (ch, i + 1, h, l.strip()[:110]))
                sus += 1
            if fwd and idx[h] < idx[ch] and ch not in ('第九章',):
                o.append('  可疑FWD   %s@L%-6d 指 %s(在前) :: %s' % (ch, i + 1, h, l.strip()[:110]))
                sus += 1
    o.append('  可疑計 %d 处' % sus)
    o.append('')

    # 章末引橋 / 下章預告
    o.append('【章末引橋對位】（各章末段所指「下一章」是否確為物理下一章）')
    for k, h in enumerate(order):
        nxt = order[k + 1] if k + 1 < len(order) else None
        s = idx[h]
        e = idx[nxt] if nxt else len(LINES)
        seg = LINES[max(s, e - 60):e]
        hits = [l.strip()[:120] for l in seg if re.search(r'下一章|次章|下接|轉入|進入第', l)]
        o.append('  %s → %s' % (h, nxt))
        for x in hits[-3:]:
            o.append('      %s' % x)
    txt = '\n'.join(o)
    emit(os.path.join(WORK, 'order.txt'), txt)


def corpus_tiaobu():
    """調部（卷55–57）語料復算：以「調部之一」起、「毘尼增一之一」止。"""
    s = read(os.path.join(ROOT, '原文', '50-60 原文.txt'))
    i1, i2 = s.index('調部之一'), s.index('毘尼增一之一')
    g = s[i1:i2]
    paras = [p.strip() for p in re.split(r'\n\s*\n', g) if p.strip()]
    return {'起訖': 'L%d-L%d' % (s[:i1].count('\n') + 1, s[:i2].count('\n') + 1),
            '段落數': len(paras), '疑': g.count('疑'), '波羅夷': g.count('波羅夷'),
            '無犯': g.count('無犯'), '佛問言': g.count('佛問言'), '汝以何心': g.count('汝以何心')}


def do_data():
    """調部（卷55-57）四大數據復算：檢索式依書方附錄 H 所訂。"""
    st = corpus_tiaobu()
    o = ['【調部復算】 ' + '、'.join('%s=%s' % (k, v) for k, v in st.items())]
    o.append('書中宣稱：348 案、326 疑、198 波羅夷、152 無犯、佛問言 99 次、汝以何心 92 次')
    for pat in ('348 案', '326 疑', '198 波羅夷', '92 次'):
        o.append('  正文含 %-10s → %d 處' % (pat, DOC.count(pat)))
    for pat in ('99 次', '99 次之多', '九十九次'):
        o.append('  正文殘留 %-10s → %d 處 %s' % (pat, DOC.count(pat),
                   [i + 1 for i, l in enumerate(LINES) if pat in l][:6]))
    emit(os.path.join(WORK, 'data.txt'), '\n'.join(o))


def measure(scope):
    fn = {'c6': fragments_c6, 'e': fragments_e, 'f': fragments_f, 'bq': fragments_bq,
           'bqa': fragments_bqa}[scope]
    meta = set()
    if scope in ('bq', 'bqa'):
        for nm in ('附錄C', '附錄L', '附錄M'):
            meta.update(range(*sec(nm)))
    hit = miss = other = skip = term = nmeta = 0
    disc = namok = 0
    cases = {}
    for case, ln, q in fn():
        if scope in ('bq', 'bqa') and (ln - 1) in meta:
            nmeta += 1
            continue
        claimed = scope in ('c6', 'e') or (has_source_strict(ln - 1) if scope in ('bq', 'bqa') else has_source(ln - 1))
        st, _ = classify(q)
        st = st_adjust(st, ln, q)
        if st == 'disclosed':
            disc += 1
            continue
        if st == 'name_ok':
            namok += 1
            continue
        if not claimed:
            term += 1
            continue
        c = cases.setdefault(case, [0, 0])
        if st == 'hit':
            hit += 1
            c[0] += 1
        elif st.startswith('other:'):
            other += 1
        elif st == 'skip':
            skip += 1
        else:
            miss += 1
            c[1] += 1
    tot = hit + miss
    return dict(hit=hit, miss=miss, other=other, skip=skip, term=term, meta=nmeta, tot=tot,
                disc=disc, namok=namok,
                rate=(100.0 * hit / tot) if tot else 0.0,
                full=sum(1 for v in cases.values() if v[1] == 0 and v[0]), n=len(cases))


def do_stat():
    o = ['SRC=%s chars=%d lines=%d' % (os.path.basename(SRC), len(DOC), len(LINES))]
    o.append('四分律語料(剔標點)=%d 字；佛經檔=%d' % (len(VINAYA), len(OTHER)))
    o.append('「」 對數=%d' % len(Q_RE.findall(DOC)))
    o.append('◎原典 區塊數=%d' % sum(1 for l in LINES if l.strip().startswith('◎原典')))
    o.append('> blockquote 行數=%d' % sum(1 for l in LINES if l.lstrip().startswith('>')))
    o.append('案例標題=%d 定位行=%d' % (sum(1 for l in LINES if CASE_RE.match(l)), sum(1 for l in LINES if POS_RE.match(l))))
    emit(os.path.join(WORK, 'stat.txt'), '\n'.join(o))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stat'
    if cmd == 'verify':
        for s in (['c6', 'e', 'bq'] if len(sys.argv) < 3 or sys.argv[2] == 'all' else [sys.argv[2]]):
            do_verify(s)
    elif cmd == 'check':
        # 第 120 輪之治：舊此處丟回傳值，故有 FAIL 亦退 0——歷輪以 `RC=$?` 為閘者皆假綠。
        n_bad = do_check() or 0
        if n_bad:
            sys.exit(1)
    elif cmd == 'probe':
        do_probe(' '.join(sys.argv[2:]))
    elif cmd == 'apply':
        do_apply(sys.argv[2], dry='--dry' in sys.argv)
    elif cmd == 'diff':
        do_diff(' '.join(sys.argv[2:]))
    elif cmd == 'order':
        do_order()
    elif cmd == 'data':
        do_data()
    elif cmd == 'stat':
        do_stat()
    else:
        print(__doc__)
