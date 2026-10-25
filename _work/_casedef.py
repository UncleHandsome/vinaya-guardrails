# -*- coding: utf-8 -*-
"""276 輪・案號定義載體之唯一法源（輕模組：不載語料，凡尺皆可 import）。

第六章改製為『十三地標＋六雙螺旋＋五集群矩陣』，一案之定義不再僅為卡節，而有三形；
凡問『此案存在否・其名何』之尺一律經 case_defs()，不得各抄一式（名單勿兩抄之印面版）。
"""
import re


CASE_CARD_RE = re.compile(r'^###\s*〔案例\s*([^\]]+?)〕\s*(.+?)\s*$')
CASE_ROW_RE = re.compile(r'^\|\s*\*\*〔案例\s*([^\]]+?)〕\*\*<br>\s*\*\*(.+?)\*\*')
CASE_LANE_RE = re.compile(r'^\*\s+\*\*案號\*\*：(.+)$')
CASE_H_RE = re.compile(r'^#{2,6}\s.*?〔案例\s*([^\]]+?)〕\s*([^（(：:]{2,40})')
CASE_ITEM_RE = re.compile(r'〔案例\s*([^\]]+?)〕\s*([^〔]*)')


def _case_nums(tok):
    """括號內容 ➔ 案號列：純數字者為案號；『遮43／開23／僧27』之類乃台帳代號，非案號。"""
    out = []
    for p in re.split(r'[/、,，\s]+', tok):
        if p.isdigit():
            out.append(int(p))
    return out


def case_defs(lines):
    """回傳 {案號: {'名': 案名, '形': '卡|矩陣|地標列|標題', '行': 行號(1-based)}}。
       同號多形者並存而記首次之形；查『號號相當』者用 keys，查名者用『名』。"""
    out = {}
    for i, l in enumerate(lines):
        m = CASE_ROW_RE.match(l)
        form, body = None, u''
        if m:
            form, body, nm = u'矩陣', m.group(1), m.group(2).strip()
        elif l.startswith(u'### 〔案例'):
            m = CASE_CARD_RE.match(l)
            form, body, nm = u'卡', m.group(1), m.group(2).strip()
        elif l.startswith(u'#'):
            m = CASE_H_RE.match(l)
            if m:
                form, body, nm = u'標題', m.group(1), m.group(2).strip()
        else:
            m = CASE_LANE_RE.match(l)
            if m:
                for it in CASE_ITEM_RE.finditer(m.group(1)):
                    for n in _case_nums(it.group(1)):
                        out.setdefault(n, {'名': it.group(2).strip(u'、・， '),
                                           '形': u'地標列', '行': i + 1})
                continue
        if not form:
            continue
        for n in _case_nums(body):
            out.setdefault(n, {'名': nm, '形': form, '行': i + 1})
    return out


# ── 276・原典欄之形（舊：卡內『#### 【律典原典】』；新：地標／矩陣之『#### …律典原典逐字回查』）
import re as _re
def _verb_head(line):
    """原典欄之題形：舊『#### 【律典原典】』・新『#### 五、律典原典逐字回查』（不用正則，免轉義之坑）。"""
    s = line.strip()
    if not s.startswith(u'#'):
        return False
    body = s.lstrip(u'#').strip()
    return body == u'【律典原典】' or u'律典原典' in body or u'逐字回查' in body
ANY_HEAD = _re.compile(r'^(#{1,6} |---\s*$)')


def verb_blocks(lines):
    """回傳 [(起, 訖, 隸屬名)]——凡原典欄之段，附其最近之 H3／H4 標題為隸屬（舊制為卡題）。"""
    out, label = [], u'卷首'
    i = 0
    while i < len(lines):
        m = _re.match(u'^#{3,4} +(.*)$', lines[i])
        if m and not _verb_head(lines[i]):
            label = m.group(1).strip()[:26]
        if _verb_head(lines[i]):
            j = i + 1
            while j < len(lines) and not ANY_HEAD.match(lines[j]):
                j += 1
            out.append((i, j, label))
            i = j
            continue
        i += 1
    return out


# ── 276 續・逐字宣稱之管轄（凡例第一律第二條：『凡作逐字之宣稱者，必同線冠有出處，或在標明
#     律典原典・逐字回查・◎原典之一欄之內』）
SRC_MARK = _re.compile(u'◎原典|《[^》]{2,}》|卷[0-9〇一二三四五六七八九十]+|犍度|大正藏')
BOUND_MARK = _re.compile(u'照錄未覆核|本地語料未收|未及復核')


def fence_rows(lines):
    """``` 圍欄之內（含其柵行）：乃版面之圖表，其引號作標籤用，不入逐字宣稱之管轄。"""
    out, op = set(), None
    for i, l in enumerate(lines):
        if l.strip().startswith(u'```'):
            if op is None:
                op = i
            else:
                out.update(range(op, i + 1))
                op = None
    if op is not None:
        out.update(range(op, len(lines)))
    return out


def is_quote_line(line):
    """純引行：去『> 』柵・去粗體記號・去句首之對照標籤（『（對照組）』之屬）後，其質即一「……」者。
       凡以冒號引出之『攝述清單』，其行內術語之「」不作逐字宣稱（276 續之負測現形）。"""
    s = line.strip().lstrip(u'>').strip()
    s = _re.sub(u'^（[^）]{1,14}）', u'', s).strip()
    s = s.replace(u'**', u'').strip()
    return s.startswith(u'「') and s.endswith(u'」')


def _decl(line):
    """宣告行之形：以『> 』起（引文之框），或以冒號終（其下即所引之文）。
       出處只夾敘於句中者（如『表中「X」係古代律論（如《毘尼母論》）』）不作宣告——
       否則全段引號皆被拖入逐字之約，術語即成偽供（276 續之負測現形）。"""
    s = line.strip().rstrip(u'*').strip()
    return s.startswith(u'>') or s.endswith(u'：') or s.endswith(u':')


def src_blocks(lines):
    """回傳 [(起, 訖, 隸屬, 依)]——尺二之管轄區，按**句式**劃而不按欄目名劃（兩張名單之縫即無尺之縫）。
       依＝'欄'：原典欄（律典原典／逐字回查）之題，其下至下一標題皆作宣稱；
       依＝'段'：連續非空行之一段（可冠以屬題，段不越圍欄），其**第一行散文**乃宣告行（『> 』起或冒號終）
              且冠出處（◎原典・《…》・卷N・犍度・大正藏）——調部深描十五則之『> ◎原典：』由此入校。
       同線左側已冠出處之引號屬尺三之職，尺二不重校（見 v39quote）。"""
    out = []
    inverb = set()
    for a, b, lab in verb_blocks(lines):
        out.append((a, b, lab, u'欄'))
        inverb.update(range(a, b))
    fen = fence_rows(lines)
    i = 0
    while i < len(lines):
        if not lines[i].strip() or i in fen:
            i += 1
            continue
        j = i
        while j < len(lines) and lines[j].strip() and j not in fen:
            j += 1
        h = i
        while h < j and lines[h].lstrip().startswith(u'#'):
            h += 1                                       # 屬題不計：出處之宣告看第一行散文
        if (not any(k in inverb for k in range(i, j)) and h < j
                and _decl(lines[h]) and SRC_MARK.search(lines[h])):
            lab = lines[i].strip()[:26] if lines[i].lstrip().startswith(u'#') else u''
            if not lab:
                for k in range(i - 1, -1, -1):
                    m = _re.match(u'^#{2,6} +(.*)$', lines[k])
                    if m:
                        lab = m.group(1).strip()[:26]
                        break
            out.append((i, j, lab or u'卷首', u'段'))
        i = j
    return sorted(out)
