# -*- coding: utf-8 -*-
"""279・外路第七報告（論第一〜三章）之校勘級落刀（九處）。

定性：只治『術語誤冠・全稱過度・內部矛盾・指針缺失』四型——所據俱是本書自身已有之律文、正理或他節現文；
      凡屬新增義理命題（新推定・新禁令反坐・新處分路徑・標題改名・結構搬移）一律不入本刀，另列候裁。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r279fix.py [--apply]
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre279.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')


def sha(x):
    return hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]


def cut(ln, old, new, tag):
    """ln 為 1-based 行號；old 須在該行恰見一次；new 內含 old 者須另行斷言。"""
    l = LINES[ln - 1]
    assert l.count(old) == 1, u'%s｜錨非恰一（L%d）：%s' % (tag, ln, l[:80])
    LINES[ln - 1] = l.replace(old, new)
    print(u'%s｜L%-5d ✔' % (tag, ln))


print(u'正本 %d 行・sha %s' % (len(LINES), sha(TXT)))

# ── 一・G1『罪疑唯輕』誤冠行為人之主觀猶疑（程序法則乃審判者之心證）
cut(1704, u'偷蘭遮（罪疑唯輕，阻卻極刑）', u'偷蘭遮（決意動搖、勝解不滿，法定降階中罪）', u'甲1・盜矩陣之疑')
cut(1719, u'偷蘭遮（生疑不免，罪疑唯輕）', u'偷蘭遮（生疑不免、勝解不滿，法定降階中罪）', u'甲2・殺矩陣之疑')

# ── 二・G2 越濟人之全稱過度：與本書『捨戒自由』（閘門一第五款）及〔案例 08〕律文相沖
cut(1610, u'（法統兩度破壞，終身不納；若未受大戒之沙彌退道後悔悟返歸者，得受大戒，不入此難）',
    u'（法統兩度破壞，終身不納；若未受大戒之沙彌退道後悔悟返歸者，得受大戒，不入此難。'
    u'又先已依律如法捨戒、身分原是白衣，事後重發心求受具者，屬『聽捨戒還家、若復欲出家於佛法中修淨行應度令出家』之常道（見〔案例 08〕），'
    u'亦自始不入此難——此難唯指未捨僧籍、身著袈裟而叛投外道受彼法、復來冒戒求供者）', u'乙・越濟人限縮')

# ── 三・D 正理一之定文補入正理五之除外（本書 L832・L3857・正理五定文俱已如此說，定文獨缺此界）
cut(544, u'罪性看心，輕重量事。心染則遮，心淨則開。',
    u'罪性看心，輕重量事。心染則遮，心淨則開（正理五所列不可逆重罪，雖心淨亦不開）。', u'丙・正理一定文')

# ── 四・C 年少受具之下游法效：本書第四章第一節已有『現前清淨擬制與善意信賴保護』，閘門一未連指針
cut(1626, u'此項缺陷不可事後補正，身分仍為沙彌，年滿後須重新如法開壇受具。',
    u'此項缺陷不可事後補正，身分仍為沙彌，年滿後須重新如法開壇受具。'
    u'至其發覺前以比丘身分參預之常態布薩與羯磨，其下游法效依『現前清淨擬制與善意信賴保護』條（第四章第一節）護之，不溯及動搖受者之戒體。',
    u'丁・年少受具指針')

# ── 五・G3 波逸提六十九之連帶隔離：全書既有『五如法／四瑕疵一票否決』（第四章第一節），此處未設前提
cut(1922, u'依《波逸提法》第六十九條（與被舉比丘同宿言語戒），大眾比丘受法規剛性拘束：',
    u'依《波逸提法》第六十九條（與被舉比丘同宿言語戒），大眾比丘受法規剛性拘束'
    u'【前提：原羯磨須具足五如法，犯四瑕疵者自始不成立、不生拘束力——見第四章第一節；其救濟動見閘門六】：',
    u'戊・三舉隔離之前提')

# 279: verbatim slice from corpus (take-again rule) - never retype CJK
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402
_m = re.search(u'或依親厚.力.{1,12}而取初得', _tk.VINAYA)
assert _m, 'corpus slice not found'
GOLD = _m.group(0) + _tk.VINAYA[_m.end():_m.end() + 3]
assert GOLD.endswith(u'波羅夷'), GOLD[-3:].encode('unicode_escape').decode()
print(u'GOLD：%d 字・尾 U+%04X' % (len(GOLD), ord(GOLD[-1])))


# ── 六・A1 暫取想之全稱過度（律制本有『依親厚強力而取也得波羅夷』之防，且僧物不屬私相通融之界）
cut(1707, u'| **有主物** | **暫取想** | 急難借用，缺乏永久霸占意圖 | **無犯（阻卻盜戒；失檢結非威儀）** |',
    u'| **有主物** | **暫取想** | 親厚知識間零星日用品之暫借，缺乏永久霸占意圖 | **無犯（限親厚零碎；阻卻盜戒，失檢結非威儀）。十方常住僧物、巨額資產與未告而取，自始不成立暫取想——律：《四分律》「' + GOLD + u'」** |',
    u'己・暫取想加界')

# ── 七・A2 止犯之『單純』須立界，免與『不作為犯之保證人責任』混同
cut(1864, u'* **止犯不坐別住**：僧團不得對單純之止犯科處僧殘別住等羞辱性處分；',
    u'* **止犯不坐別住**：僧團不得對單純之止犯科處僧殘別住等羞辱性處分'
    u'（『單純』謂所怠者乃制度性作持義務，未涉他人生命法益；若負瞻視救護之責而故以不作為令彼致死，即非止犯，'
    u'須回審殺業與正理五——不作為犯之保證人責任見〔補遺 29〕）；', u'庚・止犯立界')

# ── 八・G5『後世界內別立羯磨一律僅屬僧殘』之全稱過度，與正理五（大妄語）・十三難（賊住）相沖
cut(1949, u'後世界內別立羯磨，一律僅屬破羯磨僧（僧殘）。',
    u'後世界內別立羯磨，就『分裂僧團』這一事相而言僅屬破羯磨僧（僧殘）。'
    u'惟若其人事相更涉：未證言證、自封佛號聖者，則別犯第四波羅夷（大妄語）；本未受大戒而冒稱已受，即屬十三難之賊住——'
    u'此二罪各依其條結處，不在此限縮之內（見正理五與閘門一）。', u'辛・破僧限縮之轉軌')

# ── 九・G1 之術語界說（『疑』之兩義，本書既有正理四與今之矩陣，須一句鎖死）
i = next(k for k in range(1721, 1730)
         if not LINES[k].startswith(u'|') and not LINES[k].strip())
note = (u'\n> **【術語界說・兩『疑』不可互借】**上兩矩陣之『疑』，指**行為人下手當下**之主觀猶豫（拿法益冒險、心存僥倖），'
        u'其所以降階，是唯識層面『審決印可之勝解心所不滿、決意未充』，屬**實體**之減損；'
        u'而正理四（疑罪唯輕）之『疑』，指**審判者**於事後心證對事相仍有合理懷疑，屬**程序**之恩惠。'
        u'二者絕不可互借：行為人事前故意生疑，不得援程序法之『疑罪唯輕』求免；審判者亦不得因行為人自陳『我當時有疑』即逕予降階。\n')
LINES[i] = LINES[i] + note.lstrip(u'\n')
print(u'壬・術語界說 ➔ 插於 L%d' % (i + 1))

out = u'\n'.join(LINES)
print(u'改後 %d 行・sha %s' % (len(out.split(chr(10))), sha(out)))
if not APPLY:
    print(u'（乾跑・未落盤；備份將存 _work/ver39.pre279.md）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(TXT)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・讀回 %d 行・sha %s・同 out=%s' % (len(back.split(chr(10))), sha(back), back == out))
