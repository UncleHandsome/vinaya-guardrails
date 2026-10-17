# -*- coding: utf-8 -*-
"""r199ellipsis.py —— 凡例第二律『節引必標刪節號』之專軸（第 199 輪立・**升閘**）。

緣起：凡例引文承諾第二律明文『**節引必標刪節號：嚴禁將原文不相鄰之兩句無標記併入同一引號**』。
歷輪此律唯靠人工記性与 `r185orphan` 之旁桶（戊A）守之，而戊A 只取『印面散文行・具律文形貌』之子集——
**引塊・表列・標題三層向無器，短式（6–11 字）亦向無器**。第 199 輪奉作者令（丙桶案外之『⑧ 立即更正』）
先以 `_work/r199probe.py` 放到最寬去量，得候選 7 筆（戊A 舊口徑唯見 2），追改凡 9 處
（十句義四組・L5718 無標併兩處之文・L3089 表列脫『者』两处・L8792 雙重壓縮一处）。
**量過才知：不是書只有兩處，是器只有兩處。**

口徑（較戊A 寬二級，皆由本輪實测定）：
 ① 印面**四層俱較**（散文・『> 』引塊・表列・標題；底冊與圍欄不較——底冊另有 `e`／`c6` 兩口徑，
    圍欄乃圖，其內引號不屬散文承諾）；
 ② 「」之內容 norm 後 **≥6 漢字**（沿用 185 之下限；12 字邊界只免『術語標注被當逐字宣稱』，
    不免『既已掛單層即不得無標拼接』——本軸唯判**片段俱可查得**者，故無濫入之虞）；
 ③ 引號之內**未見刪節號**（…⋯‥ 三式俱認）；
 ④ 全串查無（存在性一以書閘 `_tk.classify()`：省略號分片・最長前綴・他典庫俱依舊，本軸不另起口徑）；
 ⑤ 以頓號／分號／逗號／冒號分片，**≥4 漢字之片段數 ≥2 且片段俱可查得** ⇒ 判為『節引未標』。
    片段非俱查得者不入本軸（那是冒充律語族，由 `r185orphan` 之甲守）。
豁免：同行標界（無從覆核／本地語料未收／未入本書比對用語料／不作逐字）或〔◈本書法式〕自製之文入乙。
量訖而不擴之維（第 211 輪·刪節號之**形**）：本軸只管『標不標』，不管『一枚或兩枚』。今量印面：兩枚『……』861 見、
真單枚『…』唯 12 見（其中 5 見乃 L228 凡例**以符號示符號**之示例〔…〕【…】［…〕，3 見在照錄引文之內，
4 見在附錄F-3 表列之撮述格）；凡例第二律只宣『節引必標刪節號』，**未宣其形**，且單枚俱有職（示例與省格）⇒
**不判、不刀、不擴尺**。（尺之教：初版以『一枚』配『…(?!…)』去數，把兩枚之**第二枚**也算成單枚，得 873 之虛數；
復尺須前後皆不接『…』。）
【第 219 輪改訂】上載『不判、不刀』今不適用——再量證得：同職而兩形並存（L753『壞伊羅鉢樹葉……』乃**末截斷亦作兩枚**，
故一枚非另職），且**本地語料六檔『…』與『……』俱 0 見**（刪節號盡出編者之手，『照錄原形』之說不成立）。
今治其落於「」『』之內者五處（L3081・L11711・L11721・L11789・L11792），形之門改由 `_tk.py` **不變量 89** 司之
（引號內不作單枚；佔位式〔…〕【…】［…］與附錄F 裸列摘句從寬）。本軸仍守『標不標』，職分不改；印面單枚今餘 7 見。
退出碼：**甲 > 0 即退 1**（升閘——此乃書中既有之約，非新增標準；作者令『硬性合規，不必保留』）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r199ellipsis.py`；
      給副本＋`require-hit` 即負測。清冊落 `_work/r199list.txt`。
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
Q = re.compile(u'「([^」]{4,200})」')
ELL = re.compile(u'[…⋯‥]')
NAME_TAG = (u'無從覆核', u'本地語料未收', u'未入本書比對用語料', u'不作逐字')

fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf


def found(q):
    st, _ = t.classify(q)
    return st in (u'hit', u'skip') or st.startswith(u'other:')


def layer(s):
    return (u'引塊' if s.startswith(u'>') else u'表列' if s.startswith(u'|')
            else u'標題' if s.startswith(u'#') else u'散文')


rows = {'甲': [], '乙': []}
seen = {k: 0 for k in (u'散文', u'引塊', u'表列', u'標題')}
for i, line in enumerate(L):
    if i in BOT or fence[i]:
        continue
    lay = layer(line.strip())
    for m in Q.finditer(line):
        q = m.group(1)
        seen[lay] += 1
        if ELL.search(q):
            continue                                # 已如法標節引
        if len(HAN.findall(t.norm(q))) < 6:
            continue
        if found(q):
            continue                                # 全串連續可查得，非節引
        frags = [f for f in re.split(u'[、；，：;]', q) if len(HAN.findall(t.norm(f))) >= 4]
        if len(frags) < 2 or not all(found(f) for f in frags):
            continue                                # 片段亦查無 ⇒ 冒充律語族（185 之甲）
        (rows[u'乙'] if (any(k in line for k in NAME_TAG) or u'〔◈' in line)
         else rows[u'甲']).append((i + 1, lay, q, frags))

print(u'印面單層「」四層俱較（散文 %d・引塊 %d・表列 %d・標題 %d 枚引號有樣）：'
      u'甲·節引未標（本軸之的）%d｜乙·已標界或自製法式 %d'
      % (seen[u'散文'], seen[u'引塊'], seen[u'表列'], seen[u'標題'],
         len(rows[u'甲']), len(rows[u'乙'])))
for ln, lay, q, frags in rows[u'甲']:
    print(u'  甲 L%-6d %s「%s」⟵ 片段：%s' % (ln, lay, q[:52], u'／'.join(f[:14] for f in frags)))
with io.open(u'_work/r199list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for ln, lay, q, frags in rows[k]:
            f.write(u'%s\tL%d\t%s\t%s\t%s\n' % (k, ln, lay, q, u'／'.join(frags)))
print(u'清冊：_work/r199list.txt（%d 則）' % sum(len(v) for v in rows.values()))
if COP and REQ:
    sys.exit(0 if rows[u'甲'] else 1)
sys.exit(1 if rows[u'甲'] else 0)
