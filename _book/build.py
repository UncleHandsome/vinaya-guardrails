# -*- coding: utf-8 -*-
"""《佛陀的護欄：四分律行為心理學與現代僧伽治理》・全冊合成。

產序：章身（填 CASE_MAP）→ 卷首與路標（據 CASE_MAP 重算指針）→ 通卷清創 → 冊身自生總目錄 → 落盤。
"""
import os, re, sys, io, datetime
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parse as P
import clean as CL
import assemble as A
import texts as T
import refmap as CM
import sequence as SQ
CM_NAMES = CM.NAMES

OUT = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
for a in sys.argv[1:]:
    if a.startswith("--out="):
        OUT = a.split("=", 1)[1]

PARTS = [(u"第一部", u"理論奠基——懸崖邊的修道要塞（體・哲學與立法本懷）",
          [u"第一章", u"第二章", u"第三章", u"第四章"]),
         (u"第二部", u"深層心相——起心動念的心智解剖室（相・唯識心所與微觀動機）",
          [u"第五章", u"第六章"]),
         (u"第三部", u"比丘戒防禦體系與古典判例法典（用・男眾學處與行為設計）",
          [u"第七章", u"第八章", u"第九章", u"第十章", u"第十一章", u"第十二章", u"第十三章"]),
         (u"第四部", u"比丘尼戒的鋼鐵防護網（用・女眾學處與性別防暴工程）",
          [u"第十四章", u"第十五章", u"第十六章", u"第十七章", u"第十八章"]),
         (u"第五部", u"僧伽司法程序——法權、證據與復權（法・正當程序與制度救急）",
          [u"第十九章", u"第二十章", u"第二十一章"]),
         (u"第六部", u"法意深探——歷史爭議與世界律學（源・法統傳承與跨域共振）",
          [u"第二十二章", u"第二十三章", u"第二十四章"]),
         (u"第七部", u"現代啟示——從個人自律到組織治理（化・古老智慧之當代落地）",
          [u"第二十五章", u"第二十六章", u"第二十七章", u"第二十八章"])]

TITLES = {
    u"第一章": u"為什麼現代人讀不懂戒律？——法條主義與立法本懷的千年斷裂",
    u"第二章": u"正統律學的核心密碼——什麼是「以遮衛性」？",
    u"第三章": u"城郭宮殿之喻——同心圓防禦工程與五重陣地模型",
    u"第四章": u"結戒十句義與八大正理——僧伽要塞的母法中樞與四大神聖邊界",
    u"第五章": u"樹根與枝幹：微觀心所動力學與六大領域換裝之則",
    u"第六章": u"照鏡察心：三軸病灶、六重心智閘門與四大臨界標尺（但書）",
    u"第七章": u"四波羅夷——斷頭之罪：王城的四次失守與不可逆客觀死線",
    u"第八章": u"十三僧殘——身受重傷的宮牆、欲望改裝與僧中復健制度",
    u"第九章": u"三十捨墮——斬斷物質貪婪，以物理沒收打造極簡真空",
    u"第十章": u"九十單提（上）——言語、獨處與微環境行為管理（第 1～45 條）",
    u"第十一章": u"九十單提（下）——暴力阻斷、思想防毒與司法正義（第 46～90 條）",
    u"第十二章": u"威儀最前哨與調部極限裁判——提舍尼、眾學法與邊緣疑難判例法",
    u"第十三章": u"二十犍度——僧團憲典與組織運作現場（行舍羅、安居與分衣）",
    u"第十四章": u"為什麼比丘尼戒更多？——古印度生存深淵與女性自衛工程",
    u"第十五章": u"比丘尼八波羅夷與十七僧殘——觸電即死的高壓護欄與獨立自治",
    u"第十六章": u"比丘尼三十捨墮——五衣裝甲、器物自戀祛魅與公義信託",
    u"第十七章": u"109 條不共單提（上）——身體純化、斷除自慰與防暴機制（第 70～124 條）",
    u"第十八章": u"109 條不共單提（下）——招生風控、二部僧治理與尊卑秩序（第 125～178 條）",
    u"第十九章": u"如法推尋——自言治、結界管轄與控辯正義（反逼供與吹哨防禦）",
    u"第二十章": u"四諍與七滅諍體系——僧團最高憲法法院與如草覆地和解法式",
    u"第二十一章": u"解縛還淨——處分、可懺性、僧殘別住算法與出罪復權閉環",
    u"第二十二章": u"阿難的困惑——「微細戒可捨」公案、五百結集與歷史代價",
    u"第二十三章": u"歷代祖師的智慧——南山律宗的千年接力",
    u"第二十四章": u"南北傳的交匯——世界律學視角下的「情境選擇架構」共振",
    u"第二十五章": u"當欲望來臨時，意志力為何不堪一擊？——神經科學與前額葉叛變",
    u"第二十六章": u"個人生活的「四重護欄工程指南」——空間除蔽、多巴胺延遲、情感邊界與微細威儀",
    u"第二十七章": u"現代道場與機構治理會通指南——三線模型、雙軌解耦、長照防線與寺產信託",
    u"第二十八章": u"重新定義自由——法架自捨，重歸林下（繳械印：「 歇 」）",
}

CASE_SRC = {u"第七章": u"第五章", u"第八章": u"第六章", u"第九章": u"第七章",
            u"第十章": u"第八章", u"第十一章": u"第九章", u"第十二章": u"第十章",
            u"第十三章": u"第十一章", u"第十五章": u"第十二章", u"第十六章": u"第十三章",
            u"第十七章": u"第十四章", u"第十八章": u"第十五章"}


def body_of(ch):
    """每章之正文（未清創之原文・已重算指針）。"""
    j = []
    if ch == u"第一章":
        j = [A.hch(u"一"), A.vch(u"一", u"第一節")]
    elif ch == u"第二章":
        j = [A.hch(u"二")]
    elif ch == u"第三章":
        j = [A.hch(u"三")]
    elif ch == u"第四章":
        j = [A.hch(u"四"), T.RULING_INTENT, A.vdaodu_part(u"動機審查主幹"),
             A.vdaodu_part(u"八大正理總綱標尺"), A.vminus(u"一", u"第一節")]
    elif ch == u"第五章":
        j = [A.vch(u"七", u"第一節"), A.vch(u"二"), A.vappx_sec(u"I", u"I-2")]
    elif ch == u"第六章":
        j = [A.vch(u"三")]
    elif ch in CASE_SRC or ch == u"第十四章":
        if ch == u"第十四章":
            j = [A.hch(u"十二", before=u"### 三、"), T.RULING_ANNI, A.cases_of(ch)[0]]
        else:
            hc = CASE_SRC[ch]
            cut = u"### 三、" if ch == u"第十五章" else None
            pre = A.hprose(hc, before=cut if ch == u"第十四章" else None,
                           after=u"### 三、" if ch == u"第十五章" else None,
                           drop_sec=u"七滅諍" if ch == u"第十二章" else None)
            txt, n = A.cases_of(ch)
            j = [pre, txt] if n else [pre]
            if ch == u"第七章":
                j.insert(1, u"## 【三篇立言之總意】\n\n" + A.fw6_intro())
                j.append(T.RULING_GARMA)
            if ch == u"第十三章" or ch == u"第十二章":
                pass
        if ch == u"第十二章":
            j.append(A.vappx_minus(u"H", [u"〔補遺"]))
    elif ch == u"第十九章":
        j = [A.vminus(u"四", u"第五節"), T.RULING_SELF]
    elif ch == u"第二十章":
        j = [A.vch(u"四", u"第五節"), A.hsec(u"十", u"七滅諍")]
    elif ch == u"第二十一章":
        j = [A.vch(u"五"), T.EDGE_SMALL]
    elif ch in (u"第二十二章", u"第二十三章", u"第二十四章"):
        j = [A.hch({u"第二十二章": u"十六", u"第二十三章": u"十七", u"第二十四章": u"十八"}[ch])]
    elif ch == u"第二十五章":
        j = [A.hch(u"十九")]
    elif ch == u"第二十六章":
        j = [A.hprose(u"二十", cut=u"### 尾聲"), T.TOOLBOX_NOTE, T.SELF_FIVE,
             A.vch(u"八", u"第三節"), A.vch(u"八", u"第四節"), A.vch(u"八", u"第一節")]
    elif ch == u"第二十七章":
        j = [A.vch(u"九"), T.RULING_FORENSIC, A.vch(u"八", u"第二節"), A.vappx_sec(u"I", u"I-1")]
    elif ch == u"第二十八章":
        j = [A.vbody(u"^結語"), A.vch(u"八", u"第五節"), A.hsec(u"二十", u"尾聲")]
    return u"\n\n".join(x for x in j if x and x.strip())


# ── 大悲商主・義理之校（指南模組三・四）───────────────────────────────────
OVERRIDES = [
    (u"《瑜伽師地論·菩薩地》明示，菩薩為救五百商人，以大悲增上發心斷彼惡人性命，寧自墮地獄受苦，"
     u"於菩薩戒「無所違犯、生多功德」。",
     u"《瑜伽師地論·菩薩地》許菩薩於此際寧自墮地獄，所言者是因果上之自擔，**非律庭上之免罪**；"
     u"後世援引此段作「為眾生故」之免罪藉口者，本冊不許（別見第七章【本冊之斷】）。"),
    (u"菩薩以捨身受罰之極限代價成全大悲，僧團以寸步不讓之極刑護持教法；兩者互不退讓，方成佛法圓滿。",
     u"菩薩之代價自己承擔，僧團之底線寸步不讓；因果歸因果，法權歸法權——二者不相通約，"
     u"方不致以玄談毀戒相。"),
    (u"外自宣稱修持無上清淨梵行，內裡全是聚眾通姦生子的淫窟！袈裟之下，生兒育女，無恥之尤！",
     u"外自稱修持清淨梵行，內則聚眾生子，是毀如來名聞之根。"),
]


OVERRIDES += [
    (u"（三十格矩陣中依近癡之相歸入癡欄）", u"（依近癡之相歸入癡欄）"),
    (u"，並列出三十格檢索總表。**先明此表之分際：它是分類之輔具", u"之則。**先明此處之分際：它是分類之輔具"),
    (u"心中本無一張六乘五的方格；今以表撮取其分佈，唯為檢索與教學之便。",
     u"心中本無一張预设的方格；今隨事指其分佈，唯為教學之便。"),
    (u"，對位三十格矩陣中之 14 標籤——", u"——"),
    (u"故不列道岔之數", u"故不列通道之數"),
    (u"（循四階漏斗道岔排查心所病根", u"（循四階漏斗排查心所病根"),
    (u"正式入編百則後之綜合三環與正理對位，一律以**第六章定位行及第七章總表**為準",
     u"正式入編之後之綜合三環與正理對位，一律以各案『心相照鏡』與『佛陀處斷』兩欄為準"),
    (u"完整正理組合見第六章定位行與第七章總表", u"完整正理組合見各案『佛陀處斷』之欄"),
    (u"〔正理參照凡例〕十五則專題案例之正理參照僅為研讀指引，各案暫不佔第七章綁定台帳之點；綁定以第六章百則台帳為準。",
     u"〔正理參照之例〕十五則專題案例之正理參照僅為研讀指引，不另立全書之綁定清冊。"),
    (u"（上篇·遮止四十五則基準台帳）", u"（上篇·遮止四十五則出處回查）"),
    (u"（下篇·開許二十五則＋僧伽三十則基準台帳）", u"（下篇·開許二十五則＋僧伽三十則出處回查）"),
    (u"文獻出處回查台帳", u"文獻出處回查表"),
    (u"**〔合編說明〕** 本單元由", u"本單元由"),
    (u"檢索得一百九十八次「波羅夷」、一百五十二次「無犯」，而世尊開庭審查動機之垂問「汝以何心」，竟出現九十二次之多。",
     u"「波羅夷」與「無犯」之判往復交見，而世尊開庭審查動機之垂問「汝以何心」，尤為數數見之。"),
    (u"本地語料未收", u"本冊未據原藏覆核"),
    (u"本地語料無此明文", u"本冊所據律文無此明文"),
    (u"查無本律與本地語料之逐字出處", u"查無本律及本冊所據藏經之逐字出處"),
    (u"本地語料", u"本冊所據藏經"),
    (u"不能出具原始載體、不可變之檔案雜湊值與未中斷之證據鏈者",
     u"不能出具原始載體與未中斷之證據鏈者"),
    (u"撤除公堂法架，平常無事吃茶", u"撤除公堂法架，平常無事"),
    (u"行者收工洗鉢，林下安詳吃茶，整座法庭徹底消融於空閑寂靜之中",
     u"行者收工洗鉢，整座法庭徹底消融於空閑寂靜之中"),
    (u"（此案律庭無別斷之文，制戒之斷即上件事相。）", u""),
    (u"* **各案例的【條文】欄，或直引律文，或以今語轉寫。**", u"* **各案例的戒文欄，或直引律文，或以今語轉寫。**"),
    (u"【結語·隨身三印】", u"【第二十八章·隨身三印】"),
    (u"第五章（總表與終極壓縮） ──► 第二十六章至二十八章（隨身工具與法庭淨空） ──► 結語（斷有漏與隨身三印）",
     u"第二十一章（解縛還淨：處分與可懺性） ──► 第二十六至二十八章（隨身工具與法庭淨空） ──► 第二十八章（斷有漏與隨身三印）"),
    (u"第五章（總表與終極壓縮） ──► 第二十六至二十八章（隨身工具與法庭淨空） ──► 結語（斷有漏與隨身三印）",
     u"第二十一章（解縛還淨：處分與可懑性） ──► 第二十六至二十八章（隨身工具與法庭淨空） ──► 第二十八章（斷有漏與隨身三印）"),

    (u"**「大貴價功德衣的處理方式最值得抄。** 面對", u"**「大貴價功德衣的處理方式最值得抄。」** 面對"),
    (u"凡標註 `◎原典` 者", u"凡冠『律藏原文』之目者"),
    (u"『復問：「從誰得耶？』報言", u"『復問：「從誰得耶？」』報言"),
    (u"前章出公堂，入本章則唯即案而觀心。", u"公堂之制既明，入本章則唯即案而觀心。"),
    (u"第五至第十一章與第十三至第十八章是案例最密之處，四章合計逾百案",
     u"第七至第十三章與第十四至第十八章是案例最密之處，合計百有餘案"),
    (u"再回頭讀該章的矩陣圖**；其餘條目俱已由篇末之歷條總表（唯全本有之）逐號登記",
     u"再回頭讀該章的結構圖**；其餘條目俱已由卷末附錄三之歷條總表逐號登記"),
    (u"唯篇末之歷條總表（唯全本有之）所收戒文不加粗體而仍是逐字，其例見該篇凡例。",
     u"唯卷末附錄三之歷條總表所收戒文不加粗體而仍是逐字，其例見該表之表凡例。"),
    (u"心中本無一張预设的方格", u"心中本無一張預設的方格"),
    (u"**六段式剛性結構**：每案嚴格遵奉『定位行 ＋ 事相經過 ＋ 心相照鏡 ＋ 佛陀處斷 ＋ 人間智慧 ＋ 文末原典』六段式規格，順序固定，各司其職。",
     u"**案例之六段**：每案依『事相經過・心相照鏡・法相剖析・佛陀處斷・人間智慧與行持・律藏原文』為序；有則著之，無則闕其名，不拘定式。"),
    (u"真正看錯想錯的人，在被叫住的一瞬間，心頭坦蕩，當場放手歸還。",
     u"你若真正看錯想錯，只被人叫住那一瞬間，心頭坦蕩，當場放手歸還。"),
    (u"法堂燈熄，公堂淨空；林下無事，天下太平。", u"法堂燈熄，公堂淨空。"),
]
OVERRIDES = [(a, bb) for a, bb in OVERRIDES if a and a != bb]

CL.DROP_HEAD += [u"挫折慢心療法"]

# ── 章身先成（填 CASE_MAP）─────────────────────────────────────────────────
CH_BODY = {ch: body_of(ch) for _, _, chs in PARTS for ch in chs}


def hlfix(text):
    """護欄側之指針落地：先按新序改『第N章案例M』，再改章次。"""
    return A.relink(A.case_refs(text), u"h")


# ── 卷首 ────────────────────────────────────────────────────────────────────
HEAD = []
HEAD.append(u"# 佛陀的護欄\n\n## ——四分律行為心理學與現代僧伽治理\n\n"
            u"> 四分律比丘與比丘尼戒之行為心理學解析・僧伽司法程序與現代僧伽治理之全解")
FRONT = hlfix(u"\n".join(A.hl.lines[9:76]).strip())
FRONT = re.sub(u"^### ", u"## ", FRONT, flags=re.M)
FRONT = FRONT.replace(u"## 【凡例】本書引文之四例", u"## 【引文四例】（兩源舊約・本冊沿用其例）")
ROAD = hlfix(u"\n".join(A.hl.lines[441:626]).strip())
ROAD = re.sub(u"^# 十線地圖.*$", u"# 【全書路標】十線地圖——跨章合併閱讀指引", ROAD, count=1, flags=re.M)
HEAD.append(FRONT)
HEAD.append(T.FANLI)
HEAD.append(A.vfanli_part(u"引文承諾"))
HEAD.append(A.vfanli_part(u"正名"))
HEAD.append(A.vdaodu_part(u"四種讀者"))
HEAD.append(A.vdaodu_part(u"修學次第"))
HEAD.append(A.vfanli_part(u"外語轉寫"))
HEAD.append(A.vfanli_part(u"心智標籤"))
HEAD.append(ROAD)
HEAD.append(A.vfront(u"開卷總提撕"))

# ── 卷末 ────────────────────────────────────────────────────────────────────
APX = [(u"附錄一", u"宗門心法——禪案與自性觀照輯要", A.vappx(u"A")),
       (u"附錄二", u"極限情境壓力測試矩陣", A.vappx(u"B")),
       (u"附錄三", u"全戒本歷條總對照表（比丘 250・比丘尼 348）", A.jieben()),
       (u"附錄四", u"現代深水實務案例推演", A.vappx(u"J")),
       (u"附錄五", u"文獻存檔與經論互證", A.vappx(u"D") + u"\n\n" + A.vappx(u"E") + u"\n\n" + A.vappx(u"F"))]
TAIL = [u"\n\n".join(u"## %s　%s\n\n%s" % (k, tt, re.sub(u"^## # ", u"# ", x)) for k, tt, x in APX)]
TAIL.append(u"# 終卷　全書竣工呈辭與終局迴向偈\n\n" + A.vbody(u"^終卷"))

# ── 合成 ────────────────────────────────────────────────────────────────────
O = [u"\n\n".join(x for x in HEAD if x and x.strip())]
for pname, ptitle, chs in PARTS:
    O.append(u"# 【%s：%s】" % (pname, ptitle))
    for ch in chs:
        O.append(u"# %s　%s\n\n%s" % (ch, TITLES[ch], CH_BODY[ch]))
O.append(u"# 【卷末・工具與附錄】（息・隨身法器與考據底冊）")
O += TAIL
book = u"\n\n".join(x for x in O if x and x.strip())

STATS = defaultdict(int)
book = CL.apply_rules(book, STATS, ref_fn=A.ref_fn,
                      name_pairs=CM_NAMES,
                      overrides=OVERRIDES)




def post_fix(text):
    # 指針成形之後的末道修整：『案例九（之三正理）』之類乃缝合所致之病句
    n = len(re.findall(u"案例[一二三四五六七八九十]+（之", text))
    t = re.sub(u"案例([一二三四五六七八九十]+)（之([^）]{1,12})）",
               lambda m: u"案例%s（其%s）" % (m.group(1), m.group(2)), text)
    print(u"末道修整：缝合病句 %d 處" % n)
    return t


book = post_fix(book)
book, refmap, fixed = SQ.renumber(book)
book, nref = SQ.rewrite_refs(book, refmap)
print(u"節序之治：重編 %s｜指針改序 %d 條" % (u"、".join(fixed) or u"無", nref))

def make_toc(text):
    out = [u"## 【本書總目錄】（由書身實題生成・改書即改目）", u""]
    fence = False
    for l in text.split(u"\n"):
        if l.startswith(u"```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^# 【(.+?)】$", l)
        if m:
            out.append(u"")
            out.append(u"**%s**" % m.group(1))
            continue
        m = re.match(r"^# (第[一二三四五六七八九十]+章　.+)$", l)
        if m:
            out.append(u"- %s" % m.group(1))
        elif l.startswith(u"# 終卷") or re.match(r"^## 附錄[一二三四五]", l):
            out.append(u"- %s" % l.lstrip("# "))
    return u"\n".join(out)


toc = make_toc(book)
book = book.replace(u"# 【第一部：", toc + u"\n\n" + u"# 【第一部：", 1)

# 册題清冊：產器自報其結構標題，尺據以核冊身——規則若誤傷標題，此處即對不上
KEEP_H1 = re.compile(u"^# (第[一二三四五六七八九十]+章　|【第|【卷末|【全書路標|終卷|佛陀的護欄)")
rows = [l.rstrip() for l in book.split("\n") if l.startswith(u"# ") and KEEP_H1.match(l)]
rows += [l.rstrip() for l in book.split("\n") if re.match(u"^## 附錄[一二三四五]　", l)]
io.open(os.path.join(HERE, u"册題清冊.tsv"), "w", encoding="utf-8", newline="\n").write(
    "\n".join(rows) + "\n")

io.open(OUT, "w", encoding="utf-8", newline="\n").write(book + u"\n")
n = len(book.split("\n"))
cjk = len(re.findall(u"[\\u3400-\\u9fff]", book))
print(u"落成：%s｜%d 行｜%d 字｜漢字 %d" % (os.path.basename(OUT), n, len(book), cjk))
fused = sum(1 for t, items in A.PLAN.items() for _, code, hc in items if code and hc)
print(u"案例：%d（框架 115＋護欄 164－同案合一 %d）｜人稱 你 %d／缺 %d｜指針重算 %d｜戒本表落地 %d" % (
    A.SENT[u"case"], fused, A.SENT[u"second_ok"], A.SENT[u"second_missing"],
    A.RELINK[u"n"], A.RELINK[u"case"]))
for k in sorted(STATS):
    print(u"　規則 %-10s %d" % (k, STATS[k]))
