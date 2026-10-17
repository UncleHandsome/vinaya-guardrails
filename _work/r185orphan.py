# -*- coding: utf-8 -*-
"""r185orphan.py —— 「律文形貌掛「」而全語料查無」之自掘軸（第 185 輪立・待診・恆退 0）。

緣起：全書引號之守向有兩重，然**兩重相交處有一縫**：
 ① `_tk.py` 之 `bq`／`bqa` 口徑唯校『**冠有出處**』之「」——未冠者不構成逐字宣稱，故不放行比對；
 ② `_work/quotejudge.py` 唯校『引號前 12 字內有**判定類動詞**』者（佛言／此為／謂之 之屬）。
於是『**以律文之形貌入「」、既無判定動詞、又未冠出處**』一類（如「若比丘為賊所護與賊同心同計…波羅夷」
之撮述、或自製之『制辭式』要約）兩檢俱過，讀者卻依凡例第一條（單層角引號＝大正藏逐字）作逐字會。
本軸專堵此縫——**校其形貌，不校其文意**（文意之斷須讀，器不作法官；166／170 兩輪之戒）。

口徑（四限並具方入甲桶）：
 甲① 印面散文行（非表列、非『> 』引塊、非圍欄、非底冊）；
 甲② 單層「」之內容 norm 後 **漢字 ≥6**，分兩級取形貌（第 192 輪擴尺）：**≥12 字**者罪相名或制辭式俱可入
      （與凡例『12 字邊界』同寬）；**6–11 字之短式唯取制辭式**，且擯問句（帶『？』）與含括注之名目——
      短語若一律放開，『善種子戒體論』『他知不知道佛制此戒？』一族名目問目盡入（實測 21 條），
      甲遂成第二個戊B，本軸之的反被淹；而短式之真病確有（「聽與受具足戒」「最初未制戒不為罪」
      「佛先不制今不應制」三處皆 6–11 字之拼接或節引，舊門檻全漏）。
 甲③ 其形求之**全語料**而**不得**——存在性一以本書法源 `_tk.classify()` 判之（省略號分片、最長前綴、
      他典庫俱依書閘之舊），本軸不另起口徑：自製之尺若比書閘寬一級，便成第二套真相（151／184 兩輪之戒）。
 甲④ 具**律文形貌**：罪相名（波羅夷／偷蘭遮／波逸提／僧殘／突吉羅／滅擯／不淨行／惡見／戒體／擯出／不共住）
      或 制辭式（若…者／不應／不聽／聽…作／應作／犯＋律罪之名／結…罪／與…戒／制…戒——
      『犯』後須接律罪之名，現代詞『犯罪』不算，否則心語一族盡入）。
豁免（如實分桶，不硬判）：同行已標界（NAME_TAG 四式）者入『乙·已標界』；〔◈本書法式〕自製文入『丙·自標』；
      他典形（含《論》《經》《律》名者）入『丁·他典』（指向附錄F-3，非本律之逐字宣稱）；
      全串查無、而以其內頓號/分號/逗號分片後**片段俱可查得**者入『戊A·節引未標』——此屬凡例第二律
      『節引必標刪節號』之債，非冒充律語（**第 199 輪起此職已移於專軸 `r199ellipsis`，桶留以看數**）；
      片段亦查無、且無律文形貌者入『戊B·自製標籤與心語』——此屬凡例第一律字面（引號只給逐字）與
      全書慣例（概念標籤與當事人心中語向掛「」）之兩難，**候作者裁**。
⑥之延長線（第 200 輪量畢而**決定不動**，理由如斯）：作者令『121 條「」歸『』』之後，以全層（散文・引塊・
      表列・標題）全長（≥2 漢字）放開再量，印面掛「」而本律查無者共 **791 枚**（散文 590・引塊 106・表列 63・
      標題 32）。其大半乃**判準層之術語標注**——校勘記第 26 輪『引文承諾第一律之可執行化』已明文界定該律
      唯管『標示為引文者』，判準層術語引號不在此限；換裝 791 枚即為整書換裝，逾本案之裁，故報數候令，不擅動。
      本軸之 ≥12 字／制辭式口徑因此保留（它是**病之筛**，不是**貌之筛**）。
退出碼：**恆 0**（待診；升閘則每有要約式制辭即假陽性，反成死法——151 輪之戒）。
負測：`argv[1]` 注副本（**同位換字、不增不刪行**）；`require-hit` 模式須有報方算過。
"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

if COP:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    BOT, inb = set(), False
    for i, l in enumerate(L):                       # 副本自算底冊界（184 輪之戒：勿借來路行號）
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

NORM_ALL = None  # 存在性不另起口徑，俱由 _tk.classify() 判之（見下方 found）

HAN = re.compile(u'[一-鿿]')
Q = re.compile(u'「([^」]{4,200})」')
CRIME = re.compile(u'(波羅夷|偷蘭遮|波逸提|僧殘|突吉羅|滅擯|不淨行|惡見|戒體|擯出|不共住|無犯|得犯|犯已)')  # 187 輪擴『無犯／得犯／犯已』三式（『無罪』too 現代，濫入即假陽性，實測 2 候選中其一為組織心理語，故不取）
# 『犯…罪』須接律罪之名，勿以現代詞「犯罪」濫入（初版即因此把『戒律只在出事、犯罪時方被召喚』
# 一句心語算成律文形貌——器寬一級，退者便混入治數；151／182 兩輪『先修尺』之教）
RULE = re.compile(u'(若[^」]{0,24}者|不應|不聽|聽[^」]{0,8}作|應作|犯[^」]{0,6}(波羅夷|偷蘭遮|波逸提|突吉羅|僧殘|重罪|某罪)'
                  u'|結[^」]{0,4}罪|與[^」]{0,6}戒|制[^」]{0,4}戒)')
FOTH = re.compile(u'《[^》]{1,20}》')
NAME_TAG = (u'無從覆核', u'本地語料未收', u'未入本書比對用語料', u'不作逐字')

# 圍欄行（``` 之內）不屬印面可讀之文
fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf


def found(q):
    """存在性之判一以本書法源為準（`_tk.classify`：省略號分片＋最長前綴＋他典庫），
    不另起口徑——自製之尺比書閘寬一級，便成第二套真相（151／184 兩輪之戒）。"""
    st, _ = t.classify(q)
    return st in (u'hit', u'skip') or st.startswith(u'other:')


rows = {'甲': [], '乙': [], '丙': [], '丁': [], '戊A': [], '戊B': []}
for i, line in enumerate(L):
    if i in BOT or fence[i]:
        continue
    s = line.strip()
    if s.startswith(u'>') or s.startswith(u'|') or s.startswith(u'#'):
        continue
    for m in Q.finditer(line):
        q = m.group(1)
        nq = t.norm(q)
        nh = len(HAN.findall(nq))
        if nh < 6:
            continue
        if found(q):
            continue
        # 甲②之兩級（192 輪擴尺）：≥12 字者罪相名或制辭式俱可入；6–11 字之短式**唯取制辭式**，
        # 且排除問句與含括注之名目——短語一旦放開，『善種子戒體論』『他知不知道佛制此戒？』
        # 一族名目與問目盡入（實測 21 條），甲遂成第二個戊B，本軸之的反被淹。
        if nh >= 12:
            shape = bool(CRIME.search(q) or RULE.search(q))
        else:
            shape = bool(RULE.search(q)) and not re.search(u'[？?（(]', q)
            if not shape:
                continue      # 短名相屬術語標注（凡例 12 字邊界），不入任何桶——戊B 之數不因擴尺而漲
        ctx = line[max(0, m.start() - 24):m.start()]
        # 全串查無，其以頓號/分號/逗號羅列之片段卻俱可查得 ⇒ 是『節引未標刪節』（凡例第二律），非冒充律語
        frags = [f for f in re.split(u'[、；，：]', q) if len(HAN.findall(t.norm(f))) >= 4]
        piecewise = len(frags) >= 2 and all(found(f) for f in frags)
        tag = (u'乙' if any(k in line for k in NAME_TAG) else
               u'丙' if u'〔◈' in line else
               u'丁' if FOTH.search(q) or FOTH.search(ctx) else
               u'甲' if shape and not piecewise else
               u'戊A' if piecewise else u'戊B')
        rows[tag].append((i + 1, q, ctx))

print(u'印面「」查無而具律文形貌者（≥12 字取罪相名或制辭式；6–11 字唯取制辭式、擯問句與括注名目）：'
      u'甲·律文形貌（本軸之的）%d｜乙·已標界 %d｜丙·自製法式 %d｜丁·他典形 %d｜'
      u'戊A·節引未標（片段俱可查得）%d｜戊B·自製標籤/心語 %d'
      % (len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁']),
         len(rows[u'戊A']), len(rows[u'戊B'])))
for k in (u'甲', u'戊A'):
    for ln, q, ctx in rows[k]:
        print(u'  %s %2d字 L%-6d %s ⟵ …%s' % (k, len(HAN.findall(t.norm(q))), ln, q[:66], ctx[-24:]))
out = u'_work/r185list.txt'
with io.open(out, 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙', u'丙', u'丁', u'戊A', u'戊B'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for ln, q, ctx in rows[k]:
            f.write(u'%s\tL%d\t%s\t…%s\n' % (k, ln, q, ctx[-24:]))
print(u'清冊：%s（%d 則）' % (out, sum(len(v) for v in rows.values())))
hit = len(rows[u'甲'])          # require-hit 唯認本軸之的（甲），戊A／戊B 屬旁證不計
if COP and REQ:
    sys.exit(0 if hit else 1)
sys.exit(0)
