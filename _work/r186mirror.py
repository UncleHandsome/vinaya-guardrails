# -*- coding: utf-8 -*-
"""r186mirror.py —— 『雙層角引號而本地語料逐字可查得』之鏡像軸（第 186 輪立・待診・恆退 0）。

緣起：第 185 輪堵了反向之縫（自製要約以律文形貌掛「」而語料查無）。凡例第二條第一律乃**雙向之約**：
  『大正藏逐字原文一律用單層角引號；凡白話改寫、作者概括、世傳俗語與本書自製之法式，一律用雙層角引號……
    二者涇渭分明，絕不混用。』
舊諸閘（`bq`／`bqa`／`quotejudge`／`r185orphan`）所校者盡是「掛「」而實非逐字」一側；
**『掛「』而實乃逐字』一側全書無器**——其害與冒充同重：讀者依凡例視『』為本書概括，遂不知此語有律典本文可據，
法據之等級無端自貶一等。本軸補此鏡像。

口徑（與 185 同寬同窄，一一分桶）：
 ① 印面散文行（表列・『> 』引塊・圍欄・底冊不較——彼各有 `e`／`c6` 兩口徑）；
 ② 『』之內容 ≥12 漢字（與出處閘門之 12 字邊界同寬）；**6–11 字之短式唯取『前有引述框架』者**（第 193 輪擴尺，
    與 `r185orphan` 之短 band 對稱）——緊接引號之前須為 律聽／律明／佛言／彼宣／…立 之屬，此乃『我引律文』之宣稱；
    無框架之短『』多屬**戒名引用**（『依「妄作異語惱他」論』之屬），名目非逐字，別立**己桶**報而不治。
 ③ 存在性逕取書閘 `_tk.classify()`（省略號分片・最長前綴・他典庫俱依舊），分兩桶：
    **甲**＝本律（No.1428/1429 語料）逐字可查得；**乙**＝唯他典（佛經/）可查得（屬宗派層，凡例未明其當何引號，報而不治）；
 ④ 豁免：同行含〔◈（本書法式自標）、〔案：…拆聲…〕、『不作逐字／無從覆核』等標界記者不入甲。
量訖而不立之維（第 211 輪·同形引號之**相巢**）：以棧判『開而未閉又見同形之開』，印面得 15 處（L5378・L5671・L6028・
L6030・L7630・L7827 六行）。逐處親量：其形乃**三至四層之交替**「『「『……』」』」——漢文深巢之通例本即『同形隔一層复用』，
非誤；且語料原形同此（`原文/01-10原文.txt`「…語言：『我得上人法！…』」、`31-37 原文.txt`「…求治言：『當與汝如是如是財物。』…」），
照錄者更不得改其標。⇒ **棧判須知『隔層复用乃正格』方能立軸，一口切必盡逐字引文報成病**（175／206『形之所職』之又一形），
故不刀、不立軸，數與理由記此註。
退出碼：**恆 0**（待診；升閘則凡『要約中嵌逐字句』之正格皆假陽性——151 輪之戒）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r186mirror.py`；
      給副本＋`require-hit` 即負測（唯甲桶計入 hit）。清冊落 `_work/r186list.txt`。
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
    for i, l in enumerate(L):                       # 副本自算底冊界（184 輪之戒）
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

HAN = re.compile(u'[一-鿿]')
Q = re.compile(u'『([^』]{4,200})』')
NAME_TAG = (u'無從覆核', u'本地語料未收', u'未入本書比對用語料', u'不作逐字', u'拆聲')
# 引述框架：緊接引號之前之動詞（句末位），謂此語乃引述律文／他人之言，非本書概括
FRAME = re.compile(u'(律聽|律明|律作|律云|律言|律但|律文|佛言|佛云|佛告|經云|又云|彼宣|彼言|僧今|白言|作是言|云|謂|宣|立|制|說)$')

fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf


def grade(q):
    """存在性一以書閘為準：hit＝本律逐字可查得；other:X＝唯他典可查得；餘者查無。"""
    st, _ = t.classify(q)
    if st == u'hit':
        return u'甲'
    if st.startswith(u'other:'):
        return u'乙'
    return None


rows = {'甲': [], '乙': [], '丙': [], '丁': [], '戊': [], '己': []}
for i, line in enumerate(L):
    if i in BOT or fence[i]:
        continue
    s = line.strip()
    if s.startswith(u'>') or s.startswith(u'|') or s.startswith(u'#'):
        continue
    for m in Q.finditer(line):
        q = m.group(1)
        nh = len(HAN.findall(t.norm(q)))
        if nh < 6:
            continue
        g = grade(q)
        if not g:
            continue
        ctx = line[max(0, m.start() - 24):m.start()]
        # 若本『』位於同段「」之**內層**（大正藏原文自有外「」內『』之 nesting），則其雙層非『自製』之謂，不入甲
        pre = line[:m.start()]
        opened = pre.count(u'「') - pre.count(u'」')
        # ②之兩級（193 輪擴尺，與 185 軸之短 band 對稱）：≥12 字者如舊；6–11 字唯取**前有引述框架**者
        #（律聽／律明／佛言／彼宣／…立 之屬，須緊接引號）——短語若一律放開，『妄作異語惱他』一類
        # 『依『X』論』之戒名引用盡入，那是名目而非逐字宣稱（別立己桶報而不治）。
        framed = bool(FRAME.search(line[max(0, m.start() - 10):m.start()]))
        if nh < 12 and not framed:
            rows[u'己'].append((i + 1, q, ctx))
            continue
        if opened > 0:
            rows[u'戊'].append((i + 1, q, ctx))
        elif (any(k in line for k in NAME_TAG) or u'〔◈' in line) and not (nh < 12 and framed):
            rows[u'丙'].append((i + 1, q, ctx))     # 已就地自標或標界，如實交代者不較
        elif u'「' in q or u'」' in q:
            rows[u'丁'].append((i + 1, q, ctx))     # 『』之內又巢「」，形制另有段級引號閘守之
        else:
            rows[g].append((i + 1, q, ctx))

print(u'印面『』而本地語料逐字可查得（≥12 字如舊；6–11 字唯取前有引述框架者）：'
      u'甲·本律逐字（本軸之的）%d｜乙·唯他典 %d｜'
      u'丙·已自標或標界 %d｜丁·內巢「」%d｜戊·乃「」之內層（非自製之謂）%d｜己·短式名目引用（無框架，報而不治）%d'
      % (len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁']), len(rows[u'戊']), len(rows[u'己'])))
for k in (u'甲', u'乙'):
    for ln, q, ctx in rows[k]:
        print(u'  %s L%-6d %s ⟵ …%s' % (k, ln, q[:66], ctx[-24:]))
with io.open(u'_work/r186list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙', u'丙', u'丁', u'戊', u'己'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for ln, q, ctx in rows[k]:
            f.write(u'%s\tL%d\t%s\t…%s\n' % (k, ln, q, ctx[-24:]))
print(u'清冊：_work/r186list.txt（%d 則）' % sum(len(v) for v in rows.values()))
if COP and REQ:
    sys.exit(0 if rows[u'甲'] else 1)
sys.exit(0)
