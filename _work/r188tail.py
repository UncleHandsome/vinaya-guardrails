# -*- coding: utf-8 -*-
"""r188tail.py —— 『同巢列項之末標不一致』之自掘軸（第 188 輪立・待診・恆退 0）。

緣起：第 168 輪 `r168par` 校列項之**句式平行**（同層混制、有領無續），第 175 輪之閘校**縮排歸屬**；
然『同一巢內兄弟項之句尾標點』一維向無器——甲項以『。』收、乙項以『；』收、丙項**無標點**，
紙上最易為讀者所見（一段列表之末行忽然缺點，或三項而兩式）。此維純然可量，不需讀文意。

口径：
 ① 印面為界（擯 `bottom_lines()` 與圍欄）；表列行（`|` 起）與標題行不預。
 ② 列項 = `^縮排 ( - | * | N. | N)、)` 之形；**同.marker_kind ＋ 同縮排**者為兄弟（異縮排屬異巢，各論）。
 ③ 項之本文含其**續行**（更深縮排之非標記行），以免末標在續行上而誤判為『無末標』。
 ④ 末標之取：先去行尾之 `*`／空格／半形空白；若末字符為**閉括號或閉引號**，則回溯取其前之標點
    （標點在括注／引文之內者仍算該項末標，唯另記『巢內』一欄備查）。
 ⑤  classify：'。'（句號收）｜'；'（分號收）｜'：'（冒號領下）｜'、'（頓號收）｜'引'（破折號收**而其後果有子列**，引列領下之職）｜'無'。
    （'引'乃第 201 輪之尺修：第六章百則處斷欄『1. 初環…。2. 次環…——』+ 其下 * 子項 凡 92 巢盡此式，
     舊口徑讀作『無末標』而與『。』並存遂盡入甲目——**189 輪『冒號領表領圖乃常式，器不分層即以常式為病』之同族**。）
 ⑥ 分桶：甲＝同巢內『有末標』與『無末標』並存（最刺眼之形，**判前先剝去引列項**）；乙＝『。』與『；』並存；
    丙＝其他混式（含 '、'、'：' 之摻雜）；領句之巢（全項皆『：』）與全項一式者不報；
    己＝巢內含引列項者（計數不判，如實交代其制）。
 ⑦ **引塊層之末標：第 209 輪量訖而不擴尺**——印面多行引塊 220 組，取『短行並列（偈與羅列）』之窄式
    再得 6 組混式，逐組親量俱屬正形：標題行以『】』收而無標（L736、L2415）、引文散文逐行各以『。』收（L1000）、
    同一引塊內以空行分兩偈（L9022）、四句偈之中二句以『；』連為一聯（L9841——『走出公堂，重歸林下；托鉢經行，
    坐看松風』乃有意之對句，非漏標）。⇒ **此維之判別須讀文意方能定，非器之事**；強立則須手列四種豁免，
    成手工帳（196 輪近似形錯拼、206 輪疊字同例），故不擴尺、不立軸，數與理由俱記此註。
 ⑧ **表欄之末標：第 210 輪量訖而不可判**——印面 48 張表逐欄校『格內末標兩式並陳』（兩式各≥3 格方報），
    尺修（跳表頭與分隔行、剝行尾星號與閉引閉括、計問號嘆號）後得 5 欄。逐欄親量：其『無標』之格俱為**照錄之
    引文截於原文盡處**（如『……其事若實而不避護』），補標即改動逐字引文、違反引文承諾第一律；『有標』之格多為
    本書自撰之按語或引文內本有句讀。⇒ **一欄之內兩式乃『引文格』與『按語格』之職分不同，非不一致**；此維不擴尺、
    不立軸。**又記尺之教**：初版之尺未跳表頭、未剝行尾 `**`、未計『？！』，於是一張表之表頭本身充當『無標』一票，
    假陽性叢生——**量形制之器，先量其自身之口徑**。
退出碼：恆 0（待診）。`argv[1]` 注副本（同位植字、不增不刪行）＋`require-hit` 即負測。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

if COP:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    BOT, inb = set(), False
    for i, l in enumerate(L):
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

FENCE = chr(96) * 3
fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(FENCE):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf

MARK = re.compile(u'^(\\s*)([-*]|\\d+[.)、])\\s+(.*)$')
CLOSER = u'』」）〕】>》'
PUNCT = u'。；：、！？'
DASH = u'—–－'
TERM = {u'。': u'。', u'；': u'；', u'：': u'：', u'、': u'、'}


def classify(text, followed_by_item=False):
    s = text.rstrip(u' \t')
    s = re.sub(u'\\*+$', u'', s).rstrip()
    s = re.sub(u'[`]+$', u'', s).rstrip()
    nested = False
    while s and s[-1] in CLOSER:
        s = s[:-1].rstrip()
        nested = True
        if s and s[-1] in PUNCT:
            break
    if not s:
        return u'空', nested
    ch = s[-1]
    # 引列式（第 201 輪之尺修）：項末以破折號收**而其後果有子列**者，是『領下』之職，非『無末標』之病
    #（189 輪『冒號領表領圖乃常式，器不分層即以常式為病』之同族——本章百則處斷欄之
    # 『2. **次環安僧伽**：……——』+ 其下 * 子項 凡 92 巢盡此式，歷載誤入甲目）
    if followed_by_item and ch in DASH:
        return u'引', nested
    if ch in TERM:
        return TERM[ch], nested
    if ch in PUNCT:
        return ch, nested
    return u'無', nested


# 逐項收集（含續行）
items = []          # (row0, indent, kind, text, line)
i = 0
while i < len(L):
    l = L[i]
    if i in BOT or fence[i] or not l.strip():
        i += 1
        continue
    s = l.strip()
    if s.startswith(u'|') or s.startswith(u'#'):
        i += 1
        continue
    m = MARK.match(l)
    if m:
        indent = len(m.group(1).replace(u'\t', u'    '))
        kind = u'ol' if m.group(2)[0].isdigit() else u'ul'
        buf = [m.group(3)]
        j = i + 1
        while j < len(L):
            nl = L[j]
            if not nl.strip():
                bk = j + 1
                while bk < len(L) and not L[bk].strip():
                    bk += 1
                if bk < len(L) and (MARK.match(L[bk]) or L[bk].strip().startswith(u'#')
                                    or len(L[bk]) - len(L[bk].lstrip()) <= indent):
                    break
                buf.append(u'')
                j = bk
                continue
            if MARK.match(nl) or nl.strip().startswith(u'#') or nl.strip().startswith(u'|'):
                break
            ind2 = len(nl) - len(nl.lstrip())
            if ind2 <= indent:
                break
            if j in BOT or fence[j]:
                break
            buf.append(nl.strip())
            j += 1
        items.append((i + 1, indent, kind, u' '.join(x for x in buf if x), l, j))
        i = j
        continue
    i += 1

# 兄弟群：同 kind ＋ 同 indent，且**中間只隔空行**（隔有散文行者乃另一清單，不併——初版以 12 行為窗，
# 遂把兩張清單併作一巢，cls 混入他巢之『。』，丁目因此恆不報：負測之植病把此盲照出）
groups = []
cur = None
for it in items:
    if cur and cur[1] == it[2] and cur[2] == it[1] and it[0] - cur[3] <= 2:
        cur[0].append(it)
        cur[3] = it[5]
    else:
        if cur:
            groups.append(cur[0])
        cur = [[it], it[2], it[1], it[5]]
if cur:
    groups.append(cur[0])

def last_row(g):
    return g[-1][0]


def cls_of(it):
    """項之末標類：其後緊接**更深縮排之列項**者為『引』（引列領下之破折號），非『無』。"""
    r, ind, kind, text, _line, jend = it
    sub = (jend < len(L) and bool(MARK.match(L[jend]))
           and (len(L[jend]) - len(L[jend].lstrip())) > ind)
    return classify(text, sub)[0]


def last_in_block(g):
    """巢之末項之後**第一個非空行**若仍是列項 ⇒ 此巢未盡，『；』收乃行文接續之正格，不報；
    若為散文／標題／分隔線 ⇒ 清單已盡，末項仍以『；』收方是病。
    （初版向前掃十行並把淺層列項一律當『未盡』，遂越過本段散文而撞上十行內另一張清單，
    副本植病不報——負測照出此盲，與 183『器不分層則圖讀成白紙』同族。）"""
    r0 = last_row(g)
    j = r0
    while j < len(L) and j < r0 + 20 and not L[j].strip():
        j += 1
    if j >= len(L) or j >= r0 + 20:
        return True
    if j in BOT or fence[j]:
        return False
    if L[j].strip().startswith(u'#'):
        return True
    return not bool(MARK.match(L[j]))


rows = {u'甲': [], u'乙': [], u'丙': [], u'丁': [], u'戊': [], u'己': []}
for g in groups:
    if len(g) < 2:
        continue
    cls = [cls_of(x) for x in g]
    if u'空' in cls:
        continue
    if u'引' in cls:                                  # 引列式另桶如實交代（領下之職，非參差之病）
        rows[u'己'].append((g[0][0], cls, g))
    eff = [c for c in cls if c != u'引']              # 判混式時先剝去引列項（189 輪『常式非病』之誡）
    if not eff or set(eff) == {u'：'} or len(set(eff)) == 1:
        pass
    else:
        has = [c for c in eff if c != u'無']
        none = eff.count(u'無')
        key = (u'甲' if (has and none) else
               u'乙' if (u'。' in eff and u'；' in eff) else u'丙')
        rows[key].append((g[0][0], cls, g))
    # 丁·羅項之末項未收句號（168 輪正格：分號羅項、末項收句號）
    # **巢未盡者不報**：子項之後若仍有同 block 之項（含較淺之兄弟），則此『；』乃行文未盡之正格
    if eff[-1] == u'；' and all(c in (u'；', u'、') for c in eff) and last_in_block(g):
        rows[u'丁'].append((g[0][0], cls, g))
    # 戊·項末誤頓號（頓號乃項內羅列之隔點，不作一行之收）
    for r, ind, kind, text, _a, _b in g:
        if cls_of((r, ind, kind, text, _a, _b)) == u'、':
            rows[u'戊'].append((r, [u'、'], [(r, ind, kind, text, None, None)]))

print(u'列項群：%d 巢｜末標混式：甲·有末標與無末標並存 %d｜乙·。與；並存 %d｜丙·其他混式 %d'
      % (len(groups), len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙'])))
print(u'可逕治之兩式：丁·羅項末項未收句號 %d 巢｜戊·項末誤頓號 %d 項｜己·引列領子列（破折號收，計數不判）%d 巢'
      % (len(rows[u'丁']), len(rows[u'戊']), len(rows[u'己'])))
for ln, cls, g in rows[u'丁'][:8]:
    print(u'  丁 L%-6d 末標序列=%s｜末項：%s' % (ln, u''.join(c if c != u'無' else u'○' for c in cls),
                                            g[-1][3][:60]))
for r, cls, g in rows[u'戊'][:8]:
    print(u'  戊 L%-6d %s' % (r, g[0][3][:70]))
out = u'_work/r188list.txt'
with io.open(out, 'w', encoding=u'utf-8', newline=u'\n') as f:
    for kk in (u'甲', u'乙', u'丙', u'丁', u'戊'):
        f.write(u'═══ %s：%d ═══\n' % (kk, len(rows[kk])))
        for ln, cls, g in rows[kk]:
            f.write(u'%s\tL%d\t%s\n' % (kk, ln, u'|'.join(cls)))
            for r, ind, kind, text, _a, _b in g:
                f.write(u'\t\tL%d\t%s\n' % (r, text))
print(u'清冊：%s（甲 %d／乙 %d／丙 %d／丁 %d／戊 %d）'
      % (out, len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁']), len(rows[u'戊'])))
if COP and REQ:
    sys.exit(0 if (rows[u'丁'] or rows[u'戊']) else 1)
sys.exit(0)
