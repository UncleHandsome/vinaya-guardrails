# -*- coding: utf-8 -*-
"""第 253 輪・刀七：第六章十二組『同案正反支』合卡（100 卡 → 88 卡）。

作者裁：同為一事而強split 者合還，以復『一案例內兩極對照』之法理張力。
合卡之法：**一字不刪原卡之文**，只以（甲）（乙）〔（丙）〕分支同置於六欄之內，
        欄末補一行『雙判合參』（純本書斷語，不掛單層引號，免墮逐字之宣稱）。
法相導航＝兩支之字段取並集（去重而連寫），不另立說。
本刀不重編號——全案重編號與指針隨動另刀行之（刀九）。

用法：python -X utf8 _work/r253merge.py            # dry-run（印一組範例與總計）
      python -X utf8 _work/r253merge.py apply
      python -X utf8 _work/r253merge.py apply only=05,06
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
SECT = [u'事相經過', u'心相照鏡', u'佛陀處斷', u'人間智慧', u'律典原典']

# (主號, [支號...], 合併後之題（不含『〔案例 NN〕』與主號前）, [支名...], 合參語)
SPEC = [
    (u'05', [u'05', u'06'], u'解牛雙判——同一樹下，慈心放生與盜心牽走的生死兩極',
     [u'慈心放生支', u'盜心牽走支'],
     u'同一樹下、同一解繩，佛以『汝以何心』一句判出兩極：心無盜思者，正理四阻卻故意而無犯，'
     u'然仍加第三值教誡『不應作如是事』以防後世假放生而行偷盜；心起盜思而牛已離處者，'
     u'正理五守死客觀死線，後念放還不能逆向消滅已成之重罪。兩支合觀，乃見『以心定性、以事定量』全句。'),
    (u'09', [u'09', u'10'], u'洗瘡雙判——同一鉢酸漿，殺心致死與慈心救難的一念之隔',
     [u'殺心致死支', u'慈心救難支'],
     u'同一漿水、同一死result，生死之界只在當前一念：以『令彼早死』之心施漿，即屬以口業與身業成辦之殺人，'
     u'斷頭滅擯；純為止痛而施，死非所願，無犯——佛仍制『與洗瘡』之預防禁令，使後人不得以救護為名試探死線。'),
    (u'07', [u'07', u'08'], u'誘殺與嚴拒——勸病夫早死之毒口與夜半推門之骨氣',
     [u'勸死謀害支', u'金剛嚴拒支'],
     u'同為探病之因緣，一染一淨：以淫欲心而勸人死者，殺業成辦；遇婦夜奔而推門不納、露地端坐至明者，'
     u'身處嫌疑之地而心無一毫動搖，佛皆以『何心』定之。兩支合讀，方知殺戒與淫戒同守一念之防。'),
    (u'22', [u'22', u'23'], u'前妻示根——以瞋治貪仍結瞋罪，與正念疾避之中道',
     [u'折辱結罪支', u'正念避出支'],
     u'面對故二示根挑逗，諸煩惱各自獨立結算：瞋心潑漿、以石砸、出惡言，婬戒雖犯不成，打人與惡語之突吉羅歷歷各結；'
     u'佛隨開中道之方——『不應以瞋恚石打惡言，應當自攝諸根，疾疾避去』。折辱不是清白，避出方是解脫。'),
    (u'49', [u'49', u'50'], u'露地敷僧坐具——責任分散之公物之殃與二俱不收之連帶鐵律',
     [u'一人不收支', u'二人俱不收支'],
     u'本制與隨語同條：一人敷坐具而不收，結波逸提；二人各作『他會收』之想而俱不收，二俱波逸提。'
     u'隨語之所重在破僥倖——心期他人代責，不能減自己之責；此為常住公物管理最古之連帶條文。'),
    (u'56', [u'56', u'57'], u'迦留陀夷三度移座——強坐、門後、露地的空間擦邊球',
     [u'堂屋強坐支', u'門後露地支'],
     u'三日三徙座，人未離此家，心已三度自我說服：堂屋不可坐則避於門後，門後不可則對坐露地。'
     u'佛逐段結之，示『形式之退让不消滅實質之逼近』；行者當於第一念動時便走，不待第三度自欺。'),
    (u'73', [u'73', u'74'], u'佛塔二但書——為守護故止宿與為堅牢故藏物',
     [u'止宿守護支', u'藏物堅牢支'],
     u'同出眾學法，同為盜亂之歲：形式之清規讓於常住重財之保全，佛立『除為守護故』『除為堅牢故』兩但書。'
     u'二但書皆以客觀危難為要件，非以個人安逸為理由——此乃開許之防濫界。'),
    (u'43', [u'43', u'55'], u'阿那律兩次清白——同室宿與同道行，聖者自清亦不破外在防線',
     [u'同室宿支', u'同道行支'],
     u'聖者心無染污，佛仍制戒：一比丘與女同室宿、一比丘與女同行，皆以『外相可嫌』結罪。'
     u'清白不能替代避嫌，此二案合為『僧俗邊界之客觀防線』最硬之註腳。'),
    (u'02', [u'02', u'54'], u'檀尼迦取官木——離處波羅夷與未離處偷蘭遮的一條死線',
     [u'離處既遂支', u'未離處前方便支'],
     u'同一檀尼迦、同一官木：既移離本處，即成波羅夷；若方斫截牽掣而物未離處，唯結偷蘭遮。'
     u'两支合觀，『離處』二字乃盜戒既遂與未遂之唯一客觀死線，不随心之强弱而移動。'),
    (u'26', [u'26', u'48'], u'闡陀連環抗拒——庭上顧左右而言他，到三勸不受諫成僧殘',
     [u'不受諫支', u'妄作異語支'],
     u'同一場管教之連續升級：先於眾中拒受勸諫（『何用教我，我應教汝』），繼於庭審問東答西、喚來故不來、語時故喧嘩，'
     u'終至白四三諫不從而成僧殘。小动作乃大病之前相，程序抗拒與慢心不受諫本是一事之兩段。'),
    (u'18', [u'18', u'19', u'20'], u'迦留陀夷七度試探——摩觸、褻語與自讚索供的欲望微觀改裝',
     [u'身相摩觸支', u'口吐褻語支', u'自讚索供支'],
     u'同一精舍門外、同一執鑰之人，欲望三度換裝：身不得觸則以口，口不可褻則假神聖——『我是第一大阿羅漢，'
     u'供養我淫欲得大福』。三支合為一案例，方見第二至第四僧殘同一病理之遞進。'),
]


def parse(lines):
    """回傳 [(起行, 止行, 號, 題, {欄名: [行]})]。"""
    out = []
    idxs = [i for i, l in enumerate(lines) if re.match(u'^### 〔案例\\s*\\d+〕', l)]
    for k, i in enumerate(idxs):
        end = idxs[k + 1] if k + 1 < len(idxs) else len(lines)
        m = re.match(u'^### 〔案例\\s*(\\d+)〕(.*)$', lines[i])
        sec, cur = {None: []}, None
        for l in lines[i + 1:end]:
            mm = re.match(u'^#### 【(.+)】\\s*$', l)
            if mm:
                cur = mm.group(1)
                sec[cur] = []
            elif l.strip() == u'---':
                break
            else:
                sec.setdefault(cur, []).append(l)
        out.append((i, end, m.group(1), m.group(2).strip(), sec))
    return out


def nav_of(sec):
    for l in sec.get(None, []) + sec.get(None, []):
        pass
    for l in sec[None]:
        if l.startswith(u'* **法相導航**'):
            return l
    return u''


def merge_card(main_no, title, branches, parts, hecan):
    navs = []
    for p in parts:
        for l in p[4][None]:
            if l.startswith(u'* **法相導航**'):
                fields = l.split(u'：', 1)[1]
                navs.append(fields)
    def uni(key):
        got = []
        for nv in navs:
            for seg in nv.split(u'｜'):
                if seg.startswith(key):
                    v = seg.split(u'：', 1)[1] if u'：' in seg else seg
                    if v not in got:
                        got.append(v)
        return got
    kill = set([u'病相', u'正理天平'])
    body_nav = []
    for src in navs:
        for s in src.split(u'｜'):
            head = s.split(u'：')[0]
            if s not in body_nav and head not in kill:
                body_nav.append(s)
    for key in [u'病相', u'正理天平']:
        vs = uni(key)
        if vs:
            body_nav.append(u'%s：%s' % (key, u'／'.join(vs)))
    out = [u'### 〔案例 %s〕%s' % (main_no, title), u'',
           u'* **法相導航**：' + u'｜'.join(body_nav),
           u'']
    for s in SECT:
        out.append(u'#### 【%s】' % s)
        for k, p in enumerate(parts):
            txt = [x for x in p[4].get(s, [])]
            while txt and txt[-1].strip() == u'':
                txt.pop()
            if not txt:
                continue
            out.append(u'**（%s）%s**' % (u'甲乙丙丁'[k], branches[k]))
            out.extend(txt)
            out.append(u'')
        if s == u'佛陀處斷':
            out.append(u'**雙判合參**：' + hecan)
            out.append(u'')
    out.append(u'---')                      # 每卡之尾分隔（原卡尾者已隨整段吃掉，此處補回）
    return out


def main():
    apply = u'apply' in sys.argv[1:]
    only = None
    for a in sys.argv[1:]:
        if a.startswith(u'only='):
            only = a[5:].split(u',')
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
    cards = parse(lines)
    by_no = {c[2]: c for c in cards}
    todo = [s for s in SPEC if (only is None or s[0] in only)]
    kill, build = set(), []
    for main_no, members, title, branches, hecan in todo:
        parts = []
        for mm in members:
            if mm not in by_no:
                raise SystemExit(u'案例 %s 查無卡（%s 組）' % (mm, main_no))
            parts.append(by_no[mm])
        for p in parts:
            kill.update(range(p[0], p[1]))
        build.append((parts[0][0], merge_card(main_no, title, branches, parts, hecan)))
    # 主卡起點之前之空行保留；其餘支卡整段刪除
    out, i = [], 0
    ins = {pos: txt for pos, txt in build}
    while i < len(lines):
        if i in kill:
            if i in ins:
                out.extend(ins[i])
            i += 1
            continue
        out.append(lines[i])
        i += 1
    print(u'合卡組數 %d｜涉及舊卡 %d 枚｜淨減 %d 枚｜新行數 %d（舊 %d）'
          % (len(todo), sum(len(s[1]) for s in todo),
             sum(len(s[1]) - 1 for s in todo), len(out), len(lines)))
    for g in todo[:1]:
        merged = ins[[p[0] for p in [by_no[x] for x in g[1]]][0]]
        print(u'—— 範例（合併後之全卡）——')
        for l in merged[:16]:
            print(u'  %.100s' % l)
        print(u'  …共 %d 行' % len(merged))
    bad = []
    for s in todo:
        for mm in s[1]:
            if re.search(u'〔案例\\s*%s〕' % mm, u'\n'.join(out)) and mm != s[0]:
                pass
    if apply:
        io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(out))
        print(u'已落檔')
    else:
        print(u'（dry-run，未落檔）')


main()
