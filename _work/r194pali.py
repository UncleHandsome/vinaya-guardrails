# -*- coding: utf-8 -*-
"""r194pali.py —— 印面梵巴轉寫之『一詞兩拼』軸（第 194 輪立・待診・恆退 0）。

緣起：`paligap`（132 輪）校『一詞出兩家字型』（字形分裂），`r177term`（177 輪）校『漢語術語異形』；
**轉寫本身有無一詞兩拼**（如 adhimokṣa 之於 adhimoksa、Smṛti 之於 Smrti）向無器——此族純然可量，
而錯拼一旦入印，讀者依之檢大正／辭書必至無著。

口徑：取印面所有拉丁詞（≥3 字母，容變音符與連字號），**去音符、去連字號、小寫**後歸基形；
      同基形而表面形 >1 者入桶。**四豁免（俱由 194 輪實測之假陽性反推）**：
   丙·對照已交代——**同一行內並列兩形**且该行另有『梵語作／巴利形／梵作／巴利作／又作／異譯／此從／正字』
        之語，則兩形並列乃如實陳述（實例：附錄D『毘舍佉母｜Visākhā｜此從巴利形，梵語作 Viśākhā』）。
        **初版曾以『任一出現行有對照語』為豁免，遂把整詞一筆抹掉**（vedanā／Vedanā 竟不入丁桶而現形）——
        豁免之域須與病同處，不可全詞連坐（151／168 兩輪『器不分層即以常式為病』之誡又一驗）。
   乙·前綴形誤拆——較短形之左鄰若為變音符字母（如 A^nanda 之 'nanda'），是詞被切斷，非異形；
   丁·唯大小寫異——句首大寫屬製式，另桶只報；
   甲·**同基形之兩拼俱含變音符而字母不同，或一有一無**（本軸之的：疑為錯拼）。
**本軸之的之界（194 輪負測第二植照出）**：基形係『去音符・去連字號・小寫』而得，故所較者為**轉寫風格之異**
      （adhimokṣa／adhimoksa、Upekṣā／Upa-kṣā 之屬）；**字母替換之錯拼（Upepṣā）基形已異，本軸不較**——
      那一維須另立近似形之器（編輯距離），非此軸之事，勿誤以為已護。
**近似形一維今已量畢而決定不立軸（第 196 輪）**：取印面帶變音符之基形 87 個兩兩求編輯距離 1（詞長 ≥5），
      僅得三對——pramāda／apramāda（放逸／不放逸）、śraddhā／aśraddhā（信／不信）乃**否定前綴 a- 之最小對**，
      Mahāpajāpatī／Mahāprajāpatī 乃**巴利形與梵語形之如實對照**（附錄D-2 已註明）。**三對俱正當，零真病**；
      要立此軸須手列豁免名單（前綴對、音譯對），即成手工帳且必腐——違『優选自癒勝手工嚴密』與『寧退檢勿湊數』。
      故此一維**如實記為已查、不設器**；來日若有人再提編輯距離之檢，先讀此段。
退出碼：**恆 0**（待診；升閘則對照條與音譯新詞必假陽性——151 輪之戒）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r194pali.py [副本] [require-hit]`；
      副本模式自算底冊界（184 輪之戒）。清冊落 `_work/r194list.txt`。
"""
import io, os, re, sys, unicodedata
from collections import defaultdict

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

# 變音符字母分兩段：Latin-1 補字母＋Latin Extended-A/B（ā–đ）與 Latin Extended Additional
#（ḍṇḷṃṣṭ…，U+1E00–1EFF）——初版只列到 U+024F，遂把 Upekṣā 截成 'Upek'、Saṃjñā 截成 'jñā'，
# 而**恰恰是這些帶下加點/鼻音符号的詞最需要比對**（器無牙之形，由負測與親量雙重現形）。
LAT = u'A-Za-z\\u00c0-\\u024f\\u1e00-\\u1eff'
TOK = re.compile(u'[' + LAT + u'][' + LAT + u'\\-]{2,30}')
DIAC = re.compile(u'[\\u00c0-\\u024f\\u1e00-\\u1eff]')
TOLD = re.compile(u'梵語作|梵作|巴利形|巴利作|又作|異譯|此從|正字|梵文|巴利文|對應')
# 常用外語詞（非轉寫），其大小寫與所有格形不較
STOPW = set(u'trauma icd dsm oecd gdpr pdf docx html css utf api cpu'.split())


def base(s):
    return re.sub(u'-', u'', u''.join(c for c in unicodedata.normalize('NFD', s)
                                      if unicodedata.category(c) != 'Mn')).lower()


fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf

seen = defaultdict(lambda: defaultdict(list))     # 基形 -> 表面形 -> [行號]
left = {}                                          # (基形,表面形) -> 左鄰字元集合
for i, line in enumerate(L):
    if i in BOT or fence[i] or not line.strip():
        continue
    for m in TOK.finditer(line):
        w = m.group(0)
        if w.lower() in STOPW or not re.search(u'[' + LAT + u']{3}', w):
            continue
        b = base(w)
        if len(b) < 3:
            continue
        seen[b][w].append(i + 1)
        left.setdefault((b, w), set()).add(line[max(0, m.start() - 1):m.start()])

rows = {u'甲': [], u'乙': [], u'丙': [], u'丁': []}
for b, forms in seen.items():
    if len(forms) < 2:
        continue
    surf = sorted(forms)
    lines_all = sorted({n for v in forms.values() for n in v})
    # 對照之豁免須『同處並列』：某一行同時出現兩形，且该行有對照語——
    # 若只取『任一出現行有對照語』，則凡心所表中帶『巴利』之註記行會把全詞一筆抹掉（194 輪初版之誤，
    # 由 vedanā／Vedanā 竟不入丁桶現形）。
    pair = [n for n in lines_all if sum(1 for s in surf if s in L[n - 1]) >= 2]
    if pair and any(TOLD.search(L[n - 1]) for n in pair):
        rows[u'丙'].append((b, surf, pair[:4]))
        continue
    # 前綴形：某表面形之左鄰恆為變音符字母 ⇒ 詞被切斷
    tails = [s for s in surf if left[(b, s)] and all(c.strip() and DIAC.search(c) for c in left[(b, s)])]
    if tails and len(tails) < len(surf):
        rows[u'乙'].append((b, surf, lines_all[:4]))
        continue
    if {s.lower() for s in surf} == set(surf[:1]) or len({s.lower() for s in surf}) == 1:
        rows[u'丁'].append((b, surf, lines_all[:4]))
        continue
    rows[u'甲'].append((b, surf, lines_all[:4]))

print(u'印面轉寫一致性（去音符歸基形）：甲·一詞兩拼（本軸之的）%d｜乙·前綴形誤拆 %d｜'
      u'丙·對照已交代 %d｜丁·唯大小寫異 %d'
      % (len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁'])))
for k in (u'甲', u'丁'):
    for b, surf, ln in rows[k]:
        print(u'  %s %-14s %s｜L%s' % (k, b, u'、'.join(surf), ln))
with io.open(u'_work/r194list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙', u'丙', u'丁'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for b, surf, ln in rows[k]:
            f.write(u'%s\t%s\t%s\t%s\n' % (k, b, u'、'.join(surf), ln))
print(u'清冊：_work/r194list.txt（%d 則）' % sum(len(v) for v in rows.values()))
if COP and REQ:
    sys.exit(0 if rows[u'甲'] else 1)
sys.exit(0)
