# -*- coding: utf-8 -*-
"""第 254 輪・刀十三：第七章第二節四軸之隨動（迎回與新立之案入軸・共N案如實・裸號去重・總數宣稱改正）。

一、入軸：十四案（13・35・51・60・62・93～102）以『迎回與新立之案（重整後補入）』一行加入其軸之適當群，
    生活場域軸則併入該領域行末——不假手猜度其舊有分组。
二、如實：各群『共 N 案』與各領域『（N 案）』一律**改取該群實際之不同案數**（由器自算，不再手載）；
    節內『99 則判例』二處改 102。
三、去重：生活場域軸之裸號行，同線同號重複者留其一（合卡之後舊列兩支者必撞重號）。
四、四諍軸本為『代表清單』，非全書清冊，不補缺、只如實其數。

用法：python -X utf8 _work/r254axis.py         # dry-run
      python -X utf8 _work/r254axis.py apply
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

SHORT = {13: u'落水救拔', 20: u'異分取片', 33: u'棄金銀羯磨', 34: u'功德衣五月',
         35: u'蓮華色覺醒', 40: u'羅睺羅廁夜', 51: u'私度關逃稅', 53: u'水中嬉戲',
         60: u'藏他衣鉢', 62: u'聽諍彈指', 63: u'學家受食', 72: u'兵象猛獸避險',
         75: u'師徒雙向瞻視', 82: u'般陀現神通', 88: u'跋難陀佛滅自在',
         89: u'新空間初坐權', 92: u'安隱尼問倒', 93: u'目連緘默', 94: u'跋提塚間甚樂',
         95: u'親洗病僧', 96: u'守籠那調琴弦', 97: u'金布祇園', 98: u'泉水停供反被舉',
         99: u'難民借衣遣使', 100: u'涅槃日哀慟', 101: u'僧地入己', 102: u'安居聞利背約',
         8: u'誘殺與嚴拒', 9: u'洗瘡雙判'}
AX1 = {1: [51, 102], 2: [98, 60], 3: [62, 101], 4: [96], 9: [13, 35, 93, 94, 95, 97, 99, 100]}
AX2 = {1: [94, 96, 35], 2: [60, 62], 3: [93, 98, 101, 102], 4: [51, 97],
       5: [13, 99, 100], 6: [95]}


def nums(line):
    return [int(x) for x in re.findall(u'〔案例 ?(\\d{1,3})〕', line)]


def main():
    apply = u'apply' in __import__('sys').argv[1:]
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
    i7 = next(i for i, l in enumerate(lines) if l.startswith(u'# 第七章'))
    s2 = next(i for i in range(i7, len(lines)) if lines[i].startswith(u'### 第二節'))
    s3 = next(i for i in range(s2 + 1, len(lines))
              if lines[i].startswith(u'### 第三節') or lines[i].startswith(u'# 第七章　'))
    seg = lines[s2:s3]

    # ── 三、去重（生活場域軸之裸號行）
    n_dedup = 0
    for k, l in enumerate(seg):
        if re.match(u'^\\s+〔案例', l) and u'〕〔案例' in l:
            seen, outl = set(), []
            for m in re.finditer(u'〔案例 ?\\d{1,3}〕', l):
                t = m.group(0)
                n = int(re.findall(u'\\d+', t)[0])
                if n in seen:
                    n_dedup += 1
                    continue
                seen.add(n)
                outl.append(t)
            pre = l[:l.find(u'〔案例')]
            newl = pre + u'、'.join(outl) + l[l.rfind(u'〕') + 1:]
            seg[k] = newl
    print(u'三、裸號去重 %d 處' % n_dedup)

    # ── 一、入軸
    def groups(pat):
        return [i for i, l in enumerate(seg) if re.match(pat, l)]

    n_add = 0
    for gi in sorted(groups(u'^##### (\\d+)\\.[ ]'), reverse=True):   # 由後向前：插入會推移前面的行號
        m = re.match(u'^##### (\\d+)\\.', seg[gi])
        if m is None:
            raise SystemExit(u'##### 群首失配（插入推移所致）：%r' % seg[gi][:24])
        g = int(m.group(1))
        if g not in AX1:
            continue
        end = next((i for i in range(gi + 1, len(seg))
                    if re.match(u'^##### |^#### ', seg[i])), len(seg))
        add = AX1[g]
        seg[end:end] = [u'* **迎回與新立之案（重整後補入）**：  ',
                        u'  ' + u'、'.join(u'〔案例%02d〕%s' % (n, SHORT.get(n, u'')) for n in add) + u'；',
                        u'']
        n_add += len(add)
    for gi in groups(u'^\\* \\*\\*([一二三四五六])、'):
        g = u'一二三四五六'.index(re.match(u'^\\* \\*\\*([一二三四五六])、', seg[gi]).group(1)) + 1
        if g not in AX2:
            continue
        body = gi + 1
        if body < len(seg) and seg[body].strip().startswith(u'〔案例'):
            add = u'、'.join(u'〔案例%02d〕%s' % (n, SHORT.get(n, u'')) for n in AX2[g])
            seg[body] = re.sub(u'；\\s*$', u'', seg[body].rstrip()) + u'；' + add + u'。'
            n_add += len(AX2[g])
    print(u'一、入軸 %d 案次（心所病相軸與生活場域軸）' % n_add)

    # ── 處分階梯軸：繇各卡自身之罪相依序補入
    card_txt = u'\n'.join(lines)
    def grade(n):
        m = re.search(u'(?m)^### 〔案例 %d〕[^\\n]*$' % n, card_txt)
        blk = card_txt[m.start():m.start() + 5200]
        for kw, g in [(u'波羅夷', 1), (u'僧殘', 2), (u'僧伽婆尸沙', 2), (u'偷蘭遮', 3),
                      (u'捨墮', 4), (u'波逸提', 4), (u'提舍尼', 5), (u'突吉羅', 5),
                      (u'無犯', 6)]:
            if kw in blk:
                return g
        return 6
    miss4 = set(range(1, 103)) - set()
    for i, l in enumerate(seg):
        pass
    have4 = set()
    for i, l in enumerate(seg):
        if i >= groups(u'^#### 四、')[0]:
            have4 |= set(nums(l))
    todo4 = sorted(set(range(1, 103)) - have4)
    byG = {}
    for n in todo4:
        byG.setdefault(grade(n), []).append(n)
    gis = groups(u'^\\* \\*\\*第([一二三四五六])階')
    n_ax4 = 0
    for gi in gis:
        g = u'一二三四五六'.index(re.match(u'^\\* \\*\\*第([一二三四五六])階', seg[gi]).group(1)) + 1
        if g not in byG:
            continue
        body = gi + 1
        add = u'、'.join(u'〔案例%02d〕%s' % (n, SHORT.get(n, u'案未具短名')) for n in byG[g])
        seg[body] = re.sub(u'；\\s*$', u'', seg[body].rstrip()) + u'；' + add + u'。'
        n_ax4 += len(byG[g])
    print(u'一b、處分階梯軸依卡身罪相補入 %d 案（其缺由器自算：今 %s）'
          % (n_ax4, {k: len(v) for k, v in sorted(byG.items())}))

    # ── 二、如實計數
    def recount():
        changed = []
        cur = None
        for i, l in enumerate(seg):
            mm = re.match(u'^##### (\\d+)\\.[ ]（?(.*)$', l) or re.match(u'^\\* \\*\\*([一二三四五六]、|第[一二三四五六]階：)(.*)$', l)
            if mm:
                cur = [i, l]
                continue
            if cur and re.match(u'^\\* \\*\\*', l):
                cur = [i, l]
        return changed
    # 逐群計不同案數並改其『共 N 案』/『（N 案）』
    blocks = []
    heads = [i for i, l in enumerate(seg) if re.match(u'^##### \\d+\\.|^\\* \\*\\*[一二三四五六]、|^\\* \\*\\*第[一二三四五六]階', l)]
    for k, h in enumerate(heads):
        end = heads[k + 1] if k + 1 < len(heads) else len(seg)
        got = set()
        for l in seg[h + 1:end]:
            got |= set(nums(l))
        blocks.append((h, sorted(got)))
    n_cnt = 0
    for h, got in blocks:
        l0 = seg[h]
        pat = re.search(u'（([^（）]*?)共 (\\d+) 案', l0) or re.search(u'（(\\d+) 案', l0)
        if not pat:
            continue
        old = pat.group(0)
        new = old.replace(pat.group(pat.lastindex) if pat.lastindex else u'', u'')
        n = len(got)
        if u'共' in old:
            new = re.sub(u'共 \\d+ 案', u'共 %d 案（實際）' % n, old) if u'實際' not in old else old
        else:
            new = old.replace(u'%d 案' % int(re.findall(u'\\d+', old)[0]), u'%d 案' % n)
        if new != old:
            seg[h] = l0.replace(old, new)
            n_cnt += 1
    print(u'二、如實計數 %d 處' % n_cnt)

    # 總數宣稱
    txt = u'\n'.join(seg)
    for a, b in [(u'本節將第六章 99 則判例', u'本節將第六章 102 則判例'),
                 (u'本軸嚴格對應全書 99 則判例之單一主領域歸屬：',
                  u'本軸以全書 102 則判例各就其主要生活場域歸屬（合卡之一案可分見於數域）：')]:
        c = txt.count(a)
        if c:
            txt = txt.replace(a, b)
            print(u'二b、總數宣稱改正：%d 處（%s）' % (c, a[:16]))
        else:
            print(u'  ⚠ 未見宣稱：%s' % a[:16])
    out = lines[:s2] + txt.split(u'\n') + lines[s3:]
    text = u'\n'.join(out)
    for k in (u'99 則判例',):
        print(u'殘留『%s』：%d' % (k, text.count(k)))
    print(u'行數 %d → %d' % (len(lines), len(out)))
    if apply:
        io.open(SRC, 'w', encoding=u'utf-8').write(text)
        print(u'已落檔')
    else:
        print(u'（dry-run）')


main()
