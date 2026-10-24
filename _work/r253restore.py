# -*- coding: utf-8 -*-
"""第 253 輪・刀八＋刀九＋刀十（v2）：迎回 11 案 → 全案重編號 → 全書指針隨動。

v2 修兩失（v1 落檔後覆核逮得，已回退至迎回前之點再行）：
 ①**卡界須兩牆**：ver38 之卡尾常緊接『### 〔篇末小標〕』之章級註（如【開許篇末・體例例外說明】），
    v1 只以『#### 〔號〕』為界，遂把他章之註吞入卡內；今以『####〔』與『^#{2,3} 』兩牆俱截，
    並棄卡自身之舊標題行（其號已不由它承載）。
 ②**重號只可一基點**：v1 之宿主映射按『宿主序』、卡題改號按『全序（含迎回卡）』，兩基點相差
    即生重號與空穴（覆核報 缺 6・8・10… 與 13・35・60・92… 重）；今一律按『全序之檔序』。

用法：python -X utf8 _work/r253restore.py            # dry-run
      python -X utf8 _work/r253restore.py apply
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
V38 = io.open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'),
              encoding=u'utf-8').read()

MERGED = {u'06': u'05', u'10': u'09', u'08': u'07', u'23': u'22', u'50': u'49',
          u'57': u'56', u'74': u'73', u'55': u'43', u'54': u'02', u'48': u'26',
          u'19': u'18', u'20': u'18'}
RESTORE = [
    (u'開14', u'落水救拔伸手無犯——救命的觸碰不成立婬戒',
     u'調部判例·身相觸疑事（救生開許）', u'15'),
    (u'僧16', u'蓮華色創傷性覺醒——兩度倫變、痛極而出離',
     u'三十捨墮之一·因緣敘事（創傷出離）', u'39'),
    (u'遮7', u'聽諍彈指謦欬——行經暗處二人語處必須發聲',
     u'波逸提第七十七條（聽諍戒）·妨滅諍之防', u'68'),
    (u'開1', u'跋提塚間甚樂——放下才安穩',
     u'初分·釋子出家因緣（無犯之稱樂）', u'100'),
    (u'開4', u'親洗病僧屎尿——供養病人即供養我',
     u'衣犍度之三·作持之極（大醫王體溫）', u'100'),
    (u'遮16', u'守籠那調琴弦——緊不急、緩不廢，是中道力學',
     u'皮革犍度·掉舉與精進之校準', u'100'),
    (u'開25', u'金布祇園名位共享——讓對方也留名',
     u'房舍犍度初·僧俗契約與名位相讓', u'100'),
    (u'遮33', u'泉水停供反被舉——非舉、不成舉、非法舉',
     u'瞻波犍度第十·如法舉罪之邊界', u'100'),
    (u'開10', u'難民借衣與遣使受戒——救人時程序讓位',
     u'衣犍度之三・受戒犍度·急難開許與程序讓位', u'100'),
    (u'開24', u'涅槃日哀慟——眼淚藏不住修為，不犯',
     u'集法毘尼五百·情極失檢之免責', u'100'),
    (u'遮42', u'僧地入己——更無有理以僧地入己',
     u'房舍犍度之餘·四方僧物產權鐵律', u'100'),
]
SECT = [u'事相經過', u'心相照鏡', u'佛陀處斷', u'人間智慧', u'律典原典']


def v38_card(lab):
    m = re.search(u'(?m)^#### 〔%s〕[^\\n]*$' % lab, V38)
    if not m:
        raise SystemExit(u'ver38 查無卡：' + lab)
    tail = V38[m.end():]
    walls = [x.start() for x in [re.search(u'(?m)^#### 〔(?:遮|開|僧)\\d+〕', tail),
                                 re.search(u'(?m)^#{1,3} ', tail),
                                 re.search(u'(?m)^---\\s*$', tail)] if x]
    end = m.end() + (min(walls) if walls else 9000)
    lines = V38[m.end():end].split(u'\n')          # 棄自標題行（號不復由它承載）
    while lines and lines[0].strip() == u'':
        lines.pop(0)
    while lines and lines[-1].strip() in (u'', u'---'):
        lines.pop()
    return lines


def convert(lines, title, nav1):
    loc, out = u'', []
    for l in lines:
        if l.startswith(u'**定位｜'):
            loc = l
            continue
        m = re.match(u'^##### (.+)$', l.strip())
        if m:
            out.append(u'#### 【%s】' % m.group(1).strip())
            continue
        if l.strip() == u'◎原典':
            out.append(u'#### 【律典原典】')
            continue
        out.append(l)
    fields = []
    for seg in loc.strip(u'*').strip().split(u'｜'):
        if seg.startswith(u'根本心'):
            fields.append(u'病相：' + seg.split(u'：', 1)[1])
        elif seg.startswith(u'八大正理'):
            fields.append(seg.replace(u'八大正理', u'正理天平'))
    nav = u'｜'.join([nav1] + fields)
    return [u'### 〔案例 __〕' + title, u'', u'* **法相導航**：' + nav] + out + [u'---']


def main():
    apply = u'apply' in sys.argv[1:]
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')

    def no_at(i):
        m = re.match(u'^### 〔案例\\s*(\\d+|__)〕', lines[i])
        return m.group(1) if m else None

    # ── 刀八：迎回（同錨者依 RESTORE 之序相接；由後向前插，免行號漂移）
    by_anchor = {}
    for lab, title, nav1, anchor in RESTORE:
        by_anchor.setdefault(anchor, []).append((lab, title, nav1))
    for anchor, items in sorted(by_anchor.items(), key=lambda kv: -int(kv[0])):
        idx = next((i for i in range(len(lines)) if no_at(i) == anchor), None)
        if idx is None:
            raise SystemExit(u'插入錨失中：案例 ' + anchor)
        end = next(i for i in range(idx, len(lines)) if lines[i].strip() == u'---')
        blk = []
        for lab, title, nav1 in items:
            blk += [u''] + convert(v38_card(lab), title, nav1)
        lines[end + 1:end + 1] = blk
    print(u'刀八：迎回 %d 卡（每卡六欄俱自查於落檔後）' % len(RESTORE))

    # ── 刀九：全序重編號（一基點）
    order = [(i, no_at(i)) for i in range(len(lines)) if no_at(i)]
    surv = [(i, no) for i, no in order if no != u'__']
    if len(surv) != 88 or len(order) != 99:
        raise SystemExit(u'卡數不合預期：宿主 %d 全 %d' % (len(surv), len(order)))
    old2new = {}
    for k, (i, no) in enumerate(order):
        new = u'%02d' % (k + 1)
        lines[i] = re.sub(u'〔案例\\s*(?:\\d+|__)〕', u'〔案例 %s〕' % new, lines[i])
        if no != u'__':
            old2new[no] = new
    for o, host in MERGED.items():
        old2new[o] = old2new[host]
    print(u'刀九：全章 99 卡（100 −12 合併 +11 迎回）｜舊→新移號 %d 條'
          % len([1 for k, v in old2new.items() if k != v]))

    # ── 刀十：指針隨動（卡題行不動，餘行全改；含無空格與不補零之形）
    text = u'\n'.join(lines)
    out, n_ref = [], 0
    for l in text.split(u'\n'):
        if re.match(u'^### 〔案例 \\d+〕', l):
            out.append(l)
            continue
        nl = re.sub(u'〔案例 (\\d{1,2})〕',
                    lambda m: u'〔案例 %s〕' % old2new.get(m.group(1).zfill(2), m.group(1)), l)
        nl = re.sub(u'〔案例(\\d{1,2})〕',
                    lambda m: u'〔案例%s〕' % old2new.get(m.group(1).zfill(2), m.group(1)), nl)
        if nl != l:
            n_ref += 1
        out.append(nl)
    text = u'\n'.join(out)
    left = sorted(set(re.findall(u'〔((?:遮|開|僧)\\s*\\d+)〕', text)))
    over = sorted(set(int(m.group(1)) for m in re.finditer(u'〔案例 ?(\\d{1,2})〕', text)) - set(range(1, 100)))
    print(u'刀十：受改之行 %d｜越界指針：%s｜舊帳殘留：%s' % (n_ref, over or u'無', left or u'無'))
    io.open(os.path.join(ROOT, u'_work', u'_case_remap.json'), 'w', encoding=u'utf-8').write(
        json.dumps({u'old2new': old2new, u'cards': 99, u'merged_into': MERGED},
                   ensure_ascii=False, indent=1))
    if apply:
        io.open(SRC, 'w', encoding=u'utf-8').write(text)
        print(u'已落檔｜行數 %d｜映射存 _work/_case_remap.json' % len(text.split(u'\n')))
    else:
        print(u'（dry-run，未落檔）映射例：%s'
              % u' '.join(u'%s→%s' % (k, old2new[k]) for k in list(old2new)[:6]))


main()
