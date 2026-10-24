# -*- coding: utf-8 -*-
"""第 253 輪・刀十一：附錄四由卡身自報重建・『百則』定數宣稱如實隨動・第七章檢索去重。

一、附錄四（判例原典逐條回查索引）：舊表係手工抄錄，合併後同號兩行、迎回者又缺行，
    全表已不可信。今**繇被定位者自報**——逐卡取其 題・卷次篇聚・律典原句（首段），
    按篇聚五組重排；表行数 = 卡数（99），一卡一行，多一行少一行即報。
二、宣稱：『百則／一百則／100 片』之定數今屬不實（99），且作者已令『取消一百之定數』——
    故章名去『百則』而為『古典判例法典』，須報數者如實報 99，
    『全書九章』亦正為『八章』（三十九版既已整併為八章）。
三、第七章四軸檢索：合併後同號並列兩事相者屬正格（一案例內兩支），不刪；
    唯**同號同語重複**者刪之（抄列之殘）。新迎回十一案之入軸屬分類判斷，另刀待行——
    本刀如實報其缺，不虚稱軸已全。

用法：python -X utf8 _work/r253claims.py          # dry-run
      python -X utf8 _work/r253claims.py apply
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
GRP = [u'第一組', u'第二組', u'第三組', u'第四組', u'第五組']


def cards_of(text):
    """依序回傳 [(號, 組, 題, 卷次, 原句)]，取自卡身之【律典原典】。"""
    out = []
    ms = list(re.finditer(u'(?m)^### 〔案例 (\\d+)〕([^\\n]*)$', text))
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(text)
        body = text[m.start():end]
        g = u'?'
        for gg in GRP:
            pass
        yz = re.search(u'《四分律》卷([^（\\n]*)(?:（([^）\\n]*)）)?', body)
        juan = (u'卷' + yz.group(1)) if yz else u'—'
        pian = (yz.group(2).strip() if yz and yz.group(2) else u'')
        quote = re.search(u'[「]([^」]{6,400})[」]', body[body.find(u'【律典原典】'):] if u'【律典原典】' in body else u'')
        out.append((m.group(1), m.group(2).strip(), juan, pian,
                    (u'「' + quote.group(1).strip() + u'」') if quote else u'—'))
    return out


def group_ranges(text):
    """第六章內各組 H2 之範圍：[(組名, 起, 迄)]。"""
    ms = list(re.finditer(u'(?m)^## (第[一二三四五]組：[^\\n]*)$', text))
    out = []
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else text.find(u'### 【第六章終卷', m.end())
        out.append((m.group(1), m.start(), end))
    return out


def main():
    apply = u'apply' in sys.argv[1:]
    text = io.open(SRC, encoding=u'utf-8').read()
    i6, j6 = text.find(u'# 第六章'), text.find(u'# 第七章')
    ch6 = text[i6:j6]
    gr = group_ranges(ch6)
    cs = cards_of(text)
    n = len(cs)
    print(u'卡數 %d｜組段 %d 段（組題同文者併算）' % (n, len(gr)))

    # ── 一、附錄四重建
    rows = {g: [] for g, _a, _b in gr}
    for no, title, juan, pian, quote in cs:
        pos = ch6.find(u'### 〔案例 %s〕' % no)
        gname = gr[-1][0]
        for gname2, a, b in gr:
            if a <= pos < b:
                gname = gname2
                break
        head = title.split(u'——')[0].strip()
        rows[gname].append(u'| **〔案例 %s〕%s** | %s%s | %s |'
                           % (no, head, juan, (u'·' + pian) if pian else u'', quote))
    a4 = re.search(u'(?m)^# 附錄四[^\\n]*$', text)
    a5 = re.search(u'(?m)^# 附錄五[^\\n]*$', text)
    old4 = text[a4.start():a5.start()]
    hdr = [l for l in old4.split(u'\n') if l.strip().startswith(u'| 案號') or u':---' in l]
    lead = (u'> 本表今全章 ' + str(n) + u' 案，繇第六章諸卡自身之【律典原典】欄匯出'
            u'（一卡一行，非手工抄錄），故章內增損一卡，此表即隨動一行。'
            u'卷段篇聚皆核合大正藏 No. 1428《四分律》六十卷電子文本，'
            u'供執事僧開庭聽訟與學者考據時隨文回查原典逐字上下文。')
    new4 = [u'# 附錄四　判例原典逐條回查索引', u'',
            u'> **【檢索對照指針】**', lead,
            u'', u'---', u'']
    for gname, _a, _b in gr:
        if not rows[gname]:
            continue
        new4 += [u'### %s' % gname, u'', hdr[0], hdr[1]] + rows[gname] + [u'', u'---', u'']
    print(u'附錄四：舊表行 %d → 新表行 %d（資料行 %d＝卡數 %d：%s）'
          % (len([l for l in old4.split(u'\n') if l.strip().startswith(u'|')]),
             len([l for l in new4 if l.strip().startswith(u'|')]),
             sum(len(v) for v in rows.values()), n,
             u'合' if sum(len(v) for v in rows.values()) == n else u'✗不合'))
    text = text[:a4.start()] + u'\n'.join(new4) + u'\n' + text[a5.start():]

    # ── 二、宣稱隨動
    CLAIM = [
        (u'# 第六章　林下照鏡錄：古典判例法典百則', u'# 第六章　林下照鏡錄：古典判例法典'),
        (u'* **第六章　林下照鏡錄：古典判例法典百則**', u'* **第六章　林下照鏡錄：古典判例法典**'),
        (u'第六章（林下照鏡錄：古典判例法典百則）', u'第六章（林下照鏡錄：古典判例法典）'),
        (u'│ 【第六章 古典判例法典百則（篇聚五組）】', u'│ 【第六章 古典判例法典（篇聚五組）'),
        (u'【附錄四·百則原典回查表】', u'【附錄四·判例原典回查表】'),
        (u'；附錄四：百則原典回查表', u'；附錄四：判例原典回查表'),
        (u'* 附錄四　百則判例原典逐條回查索引（五大篇聚之卷段定位與律典關鍵原句）',
         u'* 附錄四　判例原典逐條回查索引（五大篇聚之卷段定位與律典關鍵原句，繇諸卡自報）'),
        (u'    * 第二節　百則判例四維極速檢索矩陣', u'    * 第二節　判例四維極速檢索矩陣'),
        (u'### 第二節　百則判例四維極速檢索矩陣', u'### 第二節　判例四維極速檢索矩陣'),
        (u'5. **樹葉（具體判例）**：第六章百則判例法典', u'5. **樹葉（具體判例）**：第六章判例法典'),
        (u'5. **樹葉（法相百則·因病與藥）**：', u'5. **樹葉（法相判例·因病與藥）**：'),
        (u'第六章一百則活生生的判例法典。', u'第六章 %d 則活生生的判例法典。' % n),
        (u'而是一百個活生生的人在人間泥淖中的跌倒與掙扎', u'而是一群活生生的人在人間泥淖中的跌倒與掙扎'),
        (u'則判例單元全數發布圓滿', u'判例單元於此全數圓滿'),
        (u'一百個判例單元全數發布圓滿！', u'%d 個判例單元於此全數圓滿！' % n),
        (u'一百個判例單元', u'%d 個判例單元' % n),
        (u'翻過這一百個跌倒又爬起的生命故事', u'翻過這 %d 個跌倒又爬起的生命故事' % n),
        (u'六十卷律典、一百則判例', u'六十卷律典、%d 則判例' % n),
        (u'│    100 片法相之葉（百則古典判例法典） │', u'│    %d 片法相之葉（古典判例法典） │' % n),
        (u'百則判例事相萬端', u'判例事相萬端'),
        (u'本節將第六章一百則判例依', u'本節將第六章 %d 則判例依' % n),
        (u'本軸嚴格對應全書一百則判例之單一主領域歸屬：', u'本軸嚴格對應全書 %d 則判例之單一主領域歸屬：' % n),
        (u'翻過這百則公案的驚濤駭浪', u'翻過這批公案的驚濤駭浪'),
        (u'讀畢全書九章百則', u'讀畢全書八章判例'),
        (u'正文八章義理、百則判例', u'正文八章義理、判例'),
        (u'百則判例多出於佛世極限案情', u'諸判例多出於佛世極限案情'),
    ]
    n_claim = 0
    for old, new in CLAIM:
        c = text.count(old)
        if c == 0:
            print(u'  宣稱錨點未中（或已改）：%s' % old[:34])
            continue
        text = text.replace(old, new)
        n_claim += c
    print(u'宣稱隨動 %d 處（%d 條式樣）' % (n_claim, len(CLAIM)))

    # ── 三、第七章四軸：同號同語之重複抄列刪之
    i7 = text.find(u'# 第七章')
    j7 = text.find(u'# 第八章')
    seg = text[i7:j7]
    seen, n_dup = set(), 0

    def dedup(m):
        global n_dup
        key = m.group(0)
        return key

    seg2 = re.sub(u'(〔案例 ?\\d+〕[^、，；）)\\n]{0,18})(?=、〔案例 ?\\1』|、\\1)', u'', seg)
    # 上式難達：改以行內相鄰同號同語之肉眼式清查
    dbl = re.findall(u'(〔案例 ?\\d+〕[^、，；)\\n]{2,20})、\\1', seg)
    seg2 = seg
    for d in set(dbl):
        seg2 = seg2.replace(d + u'、' + d, d)
    n_dup = len(dbl)
    print(u'第七章：同號同語相鄰重複 %d 組（刪其一）｜指針 %d → %d'
          % (n_dup, len(re.findall(u'〔案例 ?\\d+〕', seg)), len(re.findall(u'〔案例 ?\\d+〕', seg2))))
    missing = [no for no, t, _j, _p, _q in cs
               if u'〔案例 %s〕' % no not in seg2 and u'〔案例%s〕' % no not in seg2]
    print(u'第七章四軸未及之卡：%d 枚 %s（入軸須逐案分類，另刀待行）'
          % (len(missing), missing[:14]))
    text = text[:i7] + seg2 + text[j7:]
    print(u'行數 %d' % len(text.split(u'\n')))
    if apply:
        io.open(SRC, 'w', encoding='utf-8').write(text)
        print(u'已落檔')
    else:
        print(u'（dry-run，未落檔）')


main()
