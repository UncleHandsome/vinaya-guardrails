# -*- coding: utf-8 -*-
"""281・外路第九報告（論第七章下〜附錄六）之校勘級落刀（五處）。
   另四段『生肉引文』之標點已由 r281punct.py／r281tail.py 自語料原始檔回圖重敷，不在本刀。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r281fix.py [--apply]
"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre281b.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')


def sha(x):
    return hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]


def find(sub, cnt=1):
    hits = [i for i, l in enumerate(LINES) if sub in l]
    assert len(hits) == cnt, u'錨非恰一：%s ➔ %s' % (sub[:24], [h + 1 for h in hits])
    return hits[0]


def cut(sub, new_sub, tag, ln=None):
    i = find(sub) if ln is None else ln
    LINES[i] = LINES[i].replace(sub, new_sub)
    print(u'%s｜L%-5d ✔' % (tag, i + 1))
    return i


print(u'正本 %d 行・sha %s' % (len(LINES), sha(TXT)))

# ── 一・案號之奇形：矩陣行作『〔案例 02 未遂支〕』，與全書定號之式相異（案名已自明『未遂』）
cut(u'| **〔案例 02 未遂支〕**', u'| **〔案例 02〕**', u'甲・定號之形')

# ── 二・法域中立：第八章自設之【法域中立之註】明言不預設特定地區條號，本句卻舉『三十日』
cut(u'人資法務必須於**知悉違失事實後之法定短期除斥期間內（如勞動法規之三十日）**，正式送達世俗解僱公文。',
    u'人資法務必須於**知悉違失事實後，於當地勞工實定法所定之短期除斥期間內**（部分法域定為三十日，'
    u'逾期不行使即失其效；此舉其例，非定各地皆然），正式送達世俗解僱公文。', u'乙・除斥期間之去地區化')

# ── 三・附錄五之異文校語：补外來校語之出處，並如實標本地未覆核（凡例【未收之典須自標其界】）
cut(u'（校：本地所收《首楞嚴》檔作『狂性自歇』，通行大正藏本作『狂心若歇』，異文並存待覆核。）',
    u'（校：本地所收《首楞嚴》檔作『狂性自歇』；通行大正藏本（T19, no. 945, p. 121b）作『狂心若歇』——'
    u'此據外來校語，本地未及覆核；宋明禪錄多引作『狂性自歇』。異文並存而義不相礙，冊文從本地檔。）',
    u'丙・異文校語之標界')

# ── 四・第六章：案號主屬與對照引證之clarifier（免讀者清點時生『重號』之疑）
i = find(u'本章不再採用 102 個平鋪直敘的卡片')
LINES[i] = LINES[i].rstrip() + (
    u'  （**案號之主屬**：一案以其在集群矩陣之條目為歸屬之準；同一案號再見於他戰場之矩陣・地標・雙螺旋者，'
    u'係**對照引證**，非另立一案。全書判例之總數與回查之權準，俱以附錄四之一百零二條為準。）')
print(u'丁・主屬之clarifier ➔ L%d' % (i + 1))

# ── 五・附錄六：補遺 35／37 交界之再次提醒（導言已言於前，此為閱覽時之就近提示）
j = find(u'### 〔補遺 37〕')
NOTE = (u'> *〔編者小記〕自此以上為〔補遺 29〕〜〔補遺 35〕，其下為〔補遺 37〕〜〔補遺 44〕：'
        u'〔補遺 36〕乃歷次整理所遺之虛位，非漏印；〔補遺 01〕〜〔補遺 28〕之法理已全數重構吸收入第六章百零二案。*'
        u'\n\n')
LINES[j] = NOTE + LINES[j]
print(u'戊・交界小記 ➔ 插於 L%d 之前' % (j + 1))

out = u'\n'.join(LINES)
for ph in [u'〔案例 02 未遂支〕', u'如勞動法規之三十日', u'異文並存待覆核']:
    assert ph not in out, u'%s 猶在冊' % ph
print(u'改後 %d 行・sha %s' % (len(LINES), sha(out)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding='utf-8').write(TXT)
io.open(BOOK, 'w', encoding='utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・%d 行・sha %s・同=%s' % (len(back.split(chr(10))), sha(back), back == out))
