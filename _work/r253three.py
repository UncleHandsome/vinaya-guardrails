# -*- coding: utf-8 -*-
"""第 254 輪・刀十二：自 ver38 合卡拆出三案，各立一卡 → 重編號 → 指針再隨動。

三案（作者令『解開大雜燩、各自獨立』）：
  私度關逃稅（波逸提第六十七條·知是賊伴結要共同道行）
  安居聞利背約（安居犍度·憂陀延王請跋難陀夏安居）
  藏他衣鉢坐具針筒（波逸提第五十八條·下至戲笑者）
事相取 ver38 遮2／遮36 合卡內之原文分段，心相與處斷依其本有之科判拆出，**不添新義**；
【律典原典】之逐字引一律先斷語料可查（norm 折標點後求之），查無即不引——
『安居背約』一事律中唯有因緣文而無結戒句（其罪相依『失安居歲』之科判），故如實不掛逐字制辭。

用法：python -X utf8 _work/r253three.py            # dry-run
      python -X utf8 _work/r253three.py apply
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
sys.path.insert(0, ROOT)
import _tk                                                    # noqa: E402

V = _tk.norm(_tk.VINAYA)
SIMP = set(u'两当强随关个国为说对经视见运还这')

CARDS = [
    dict(
        anchor=(u'before', u'打搏高喚'),
        title=u'藏他衣鉢坐具針筒——下至戲笑的欺凌',
        nav=u'波逸提第五十八條（藏他衣鉢戒）·戲笑為掩之侵犯｜病相：瞋加癡（以彼憂惱為戲樂）｜正理天平：正理一（心事相應）',
        事=[u'六群比丘伺候十七群少年比丘經行背向之際，取其三衣、瓦鉢、坐具、針筒藏於草叢暗室。',
             u'少年比丘聞犍槌而欲赴說戒，翻覓不得，哭泣崩潰；六群比丘拍手戲笑，辯稱『開玩笑耳』。',
             u'佛集僧審問，知而故問，六群伏承。佛以無數方便呵責，遂立第五十八條：藏他衣鉢坐具針筒，'
             u'下至為戲笑者，波逸提。'],
        心=[u'你把自己一時的興致，建立在同修失去資生之物的慌張之上。',
             u'『鬧著玩』三個字從來不能洗白一個事實：一人笑而一人哭者，其笑便是欺凌。'
             u'僧格之防，不在重罪之初犯，而在微損之不惜。'],
        斷=[u'**初環見真實**：主觀具足令彼憂惱之惡意（雖自稱戲笑），客觀成辦藏他資具之表業，要件俱足。',
             u'**次環安僧伽**：依正理一心事相應——動機之輕慢不減表業之成立，故制曰『下至戲笑』，'
             u'明心跡之無可藉口；三衣鉢具為道器，非戲具。',
             u'**終環入無事**：歸還衣鉢，向受害同修當面發露懺悔，對首除罪，案卷備查。'],
        智=u'玩笑的分界，在被捉弄者能不能同笑。藏人衣鉢而自樂，是把同修的焦慮當燃料；'
            u'僧中之樂，當生於彼此護念，不當生於一人失物。',
        quotes=[(u'《四分律》卷十六（波逸提法第五十八條·藏他衣鉢戒）',
                 u'若比丘，藏比丘衣鉢、坐具、針筒，若自藏、若教人藏，下至戲笑者，波逸提。')],
    ),
    dict(
        anchor=(u'after', u'觀軍陣營中過宿'),
        title=u'私度關逃稅——以法服為走私之掩護',
        nav=u'波逸提第六十七條（知賊伴結要同道戒）·僧服作關卡之屏障｜病相：貪加癡（圖利便而忘王法）｜正理天平：正理二（世間信心）、正理五（不可逆底線）',
        事=[u'眾多比丘欲從舍衛國往毘舍離，路次有賈客伴擬私度關卡、不輸王稅。',
             u'賈客問知比丘所詣，遂求『與諸尊共伴』；比丘貪途中之照應，許其結要同行，藉法服以掩走私。',
             u'守關者捕得，押至波斯匿王所。王審知比丘事前明曉其逃稅之情，痛斥沙門知法犯法；'
             u'念其身披法服，呵責驅逐而不加刑。'],
        心=[u'你以為同行一段路只是順水人情，其實你出的不是力氣，是三寶的門面。',
             u'關吏見沙門而緩其盤查，商賈便借你一身法服作護身符——所圖者小利，所損者一代之信。'],
        斷=[u'**初環見真實**：『知是賊伴』而『結要』（先共期要）同行，明知之與要契二者俱備，'
             u'方成結罪；不知者不犯，疑者有輕重之判。',
             u'**次環安僧伽**：律結波逸提，世俗關稅之刑責自負——律不代王法免其罪，唯就其污僧相而制；'
             u'村間一道、空曠十里，各有結罪之階梯，防其以『只走一步』自寬。',
             u'**終環入無事**：發露懺除，退出商旅之伴，歸阿蘭若。'],
        智=u'捷徑之旁必有關卡，關卡之旁必有代價。出家人的信用是眾生交給三寶的，'
            u'拿去替人遮一次稅，賠的是千夫對法服的信心。',
        quotes=[(u'《四分律》卷十七（波逸提法第六十七條·知賊伴結要同道戒）',
                 u'若比丘知賊伴，結要共同道行，乃至一村間，波逸提。')],
    ),
    dict(
        anchor=(u'before', u'【第六章終卷圓滿宣告】'),
        title=u'受請安居聞利背約——信約不隨供養漲落',
        nav=u'安居犍度·受請住夏而聞利輒徙（違要失歲）｜病相：貪（利養）加癡（謂無損於人）｜正理天平：正理二（世間信心）、正理七（更生復權）',
        事=[u'拘睒彌王憂陀延與跋難陀釋子為舊親友，請跋難陀於國中結夏安居。',
             u'安居期中，跋難陀聞餘住處大得利養、大得衣物，即往彼住處小住分物，復還拘睒彌。',
             u'王聞而嫌：『云何跋難陀釋子受我請在此住夏安居，聞彼住處大得利養大得衣物便往至彼，'
             u'在彼住已復還來此？』諸比丘以是呵責，白佛。佛集僧呵責跋難陀，如文廣說。'],
        心=[u'信約在你不吃虧時总是莊嚴的；一旦別處供養更厚，條文便成了可以擱下的外衣。',
             u'你自以為只是『去去就回』，並未失卻安居之體，但受請之家已在你的離坐裡看見了自己在僧團天秤上的重量。'],
        斷=[u'**初環見真實**：受請住夏而心在異處之利養，動機為貪，表業為輒徙，客觀已破所要之信。',
             u'**次環安僧伽**：律於安居有『處所決定』之制，無難輒去者依其日數判失歲與不失歲之界；'
             u'此案所損尤在僧俗信約——主人供養一季，買的是『安心住此』一句，故亦涉正理二世間信心。',
             u'**終環入無事**：發露懺悔，如法補其處分之儀，此後不復以利養擇居。'],
        智=u'道場留人，靠的是守約，不是出价。為供養而移錫的人，永遠在找下一個更高的供養；'
            u'為本願而安住的人，一缽一坐處即是道場。',
        quotes=[(u'《四分律》卷三十七（安居犍度·憂陀延王請跋難陀夏安居）',
                 u'云何跋難陀釋子受我請在此住夏安居，聞彼住處大得利養大得衣物便往至彼，在彼住已復還來此？')],
    ),
]


def body_of(c):
    out = [u'### 〔案例 __〕' + c[u'title'], u'', u'* **法相導航**：' + c[u'nav'], u'',
           u'#### 【事相經過】']
    out += [l + (u'  ' if k + 1 < len(c[u'事']) else u'') for k, l in enumerate(c[u'事'])]
    out += [u'', u'#### 【心相照鏡】']
    out += [l + u'  ' for l in c[u'心'][:-1]] + [c[u'心'][-1]]
    out += [u'', u'#### 【佛陀處斷】']
    for k, l in enumerate(c[u'斷']):
        out.append(u'%d. ' % (k + 1) + l + (u'  ' if k + 1 < len(c[u'斷']) else u''))
    out += [u'', u'#### 【人間智慧】', c[u'智'], u'', u'#### 【律典原典】']
    for i, (head, q) in enumerate(c[u'quotes']):
        out.append(u'> %s：  ' % head if i == 0 else u'> 又%s：  ' % head)
        out.append(u'> 「%s」' % q)
    out.append(u'---')
    return out


def main():
    apply = u'apply' in sys.argv[1:]
    text = io.open(SRC, encoding=u'utf-8').read()
    # 語料之斷（先量後刀：引文不中即不許落檔）
    for c in CARDS:
        for _h, q in c[u'quotes']:
            if _tk.norm(q) not in V:
                raise SystemExit(u'語料查無逐字，不得掛單層引號：%s' % q[:36])
        for fld in (u'事', u'心', u'斷'):
            for l in c[fld]:
                bad = sorted(set(l) & SIMP)
                if bad:
                    raise SystemExit(u'新文帶簡形 %s：%s' % (bad, l[:30]))
        for l in c[u'斷']:
            if u'\u6076\u610f' in l or u'Hide' in l:
                raise SystemExit(u'新文帶汙字：%s' % l[:24])
    lines = text.split(u'\n')
    n_add = 0
    for pos, key in [(u'before', 0), (u'after', 1), (u'before', 2)]:
        c = CARDS[key]
        want, kw = c[u'anchor']
        idx = next((i for i, l in enumerate(lines)
                    if re.match(u'^### 〔案例 \\d+〕', l) and kw in l), None)
        if idx is None:
            if kw.startswith(u'【'):
                idx = next((i for i, l in enumerate(lines) if l.strip().startswith(u'### ' + kw)), None)
            if idx is None:
                raise SystemExit(u'插入錨失中：' + kw)
        tgt = idx if want == u'before' else None
        if tgt is None:
            nxt = [i for i in range(idx + 1, len(lines))
                   if re.match(u'^### 〔案例 \\d+〕', lines[i]) or lines[i].strip().startswith(u'### 【')]
            tgt = nxt[0] if nxt else len(lines)
            tgt = next(i for i in range(idx + 1, len(lines)) if lines[i].strip() == u'---') + 1
        lines[tgt:tgt] = [u''] + body_of(c)
        n_add += 1
    print(u'刀十二：立卡 %d 枚（引文俱經語料斷驗）' % n_add)

    order = [(i, re.match(u'^### 〔案例 (\\d+|__)〕', lines[i]).group(1))
             for i in range(len(lines)) if re.match(u'^### 〔案例 (\\d+|__)〕', lines[i])]
    old2new = {}
    for k, (i, no) in enumerate(order):
        new = u'%02d' % (k + 1)
        lines[i] = re.sub(u'〔案例 (?:\\d+|__)〕', u'〔案例 %s〕' % new, lines[i])
        if no != u'__':
            old2new[no] = new
    print(u'刀十二：全章 %d 卡｜補零位數：%s' % (len(order), u'三位' if len(order) > 99 else u'兩位'))
    text = u'\n'.join(lines)
    out, n_ref = [], 0
    for l in text.split(u'\n'):
        if re.match(u'^### 〔案例 \\d+〕', l):
            out.append(l)
            continue
        nl = re.sub(u'〔案例 (\\d{1,3})〕',
                    lambda m: u'〔案例 %s〕' % old2new.get(m.group(1).zfill(2), m.group(1)), l)
        nl = re.sub(u'〔案例(\\d{1,3})〕',
                    lambda m: u'〔案例%s〕' % old2new.get(m.group(1).zfill(2), m.group(1)), nl)
        if nl != l:
            n_ref += 1
        out.append(nl)
    text = u'\n'.join(out)
    over = sorted(set(int(m.group(1)) for m in re.finditer(u'〔案例 ?(\\d{1,3})〕', text))
                  - set(range(1, len(order) + 1)))
    print(u'刀十二：指針隨動 %d 行｜越界：%s' % (n_ref, over or u'無'))
    mp = json.load(open(os.path.join(ROOT, u'_work', u'_case_remap.json'), encoding=u'utf-8'))
    for k in mp[u'old2new']:
        if k in old2new:
            mp[u'old2new'][k] = old2new[k]
    mp[u'cards'] = len(order)
    mp[u'note254'] = [c[u'title'][:12] for c in CARDS]
    if apply:
        io.open(SRC, 'w', encoding=u'utf-8').write(text)
        json.dump(mp, open(os.path.join(ROOT, u'_work', u'_case_remap.json'), 'w',
                           encoding=u'utf-8'), ensure_ascii=False, indent=1)
        print(u'已落檔｜行數 %d' % len(text.split(u'\n')))
    else:
        print(u'（dry-run，未落檔）')


main()
