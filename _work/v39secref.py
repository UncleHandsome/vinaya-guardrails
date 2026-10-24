# -*- coding: utf-8 -*-
"""268 輪・器：節級指針之『（X）』須落於所靶之節（不變量第 29 目之原型）。

法源：第 10 目只問『第N章第M節』之**節號可達否**，從不問**括號命題說的是否即那一節**——
      267 輪『第二章第四節（衰竭型止犯免責）』節號俱在而文在第三章閘門三，舊尺全綠。
口徑五則：① 靶鍵一律以**漢字序數**求；
      ② 章界**合併上・下兩 H1**，且無節號之『第N章（X）』以**整章**為靶；
      ③ **他靶之池須排除含本行之段**——卷首導航節把對讀索引之指針自己含在正文內，自證必生假錯靶；
         全章之靶亦不入他靶池（其內含本節，必自證）；
      ④ 度量＝X 折標點後取**四字窗**（初版取五字，而冊內『與學羯磨（與波羅夷戒）』之插字即斷窗，
         合法撮述全墮『未證』——尺之單位須與文之單位同寬），own＝見於靶段之窗數，best＝見於他段之最多窗數；
      ⑤ 判語：own>0 ⇒ 中；own=0 且 best≥2 ⇒ **錯靶**；own=0 且 best<2 ⇒ 未證（新造之語，不判）。
     今量：指針 26 處・中 25・錯靶 0・未證 1（『代持、信託與資金穿透稽核』之四字窗於靶內他段俱無，如實不判）。
     ⚠ 牙之所及：唯『靶內一字不著而他段成串』。267 輪那枚『第二章第四節（衰竭型止犯免責）』以四字窗測之
        確報錯靶（負測 r268neg 第一道），然窗口再窄即與合法撮述同形——**本尺檢錯靶，不判描述語之好壞**。
用法：python -X utf8 _work/v39secref.py [書名]（退碼：錯靶或靶不可求即 1）
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith(u'-') else None
if NAME is None:
    NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
            and u'列印' not in q][0]
SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)          # 274 輪・試跑通道
if SRC_PATH:
    NAME = SRC_PATH
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')

PU = re.compile(u'[\\s\\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·／/]')
CH = re.compile(u'^# 第([一二三四五六七八九十]+)章')
SEC = re.compile(u'^### (?:第([一二三四五六七八九十]+)節|閘門([一二三四五六])|【(.+?)】|'
                 u'([一二三四五六七八九十]+)[、・]([^＃\\n]{0,20}))')
PTR = re.compile(u'第([一二三四五六七八九十]+)章(?:第([一二三四五六七八九十]+)節|閘門([一二三四五六]))?'
                 u'[^\\n『「【（）】』]{0,4}[（【「『]([^（）【】「」『』]{4,40})[）】」』]')


def norm(s):
    return PU.sub(u'', s)


H1 = [i for i, l in enumerate(L) if l.startswith(u'# ')] + [len(L)]
CHAP = [i for i, l in enumerate(L) if CH.match(l)]


def chap_of(i):
    prev = [k for k in CHAP if k <= i]
    return u'第%s章' % CH.match(L[prev[-1]]).group(1) if prev else None


# ── 節段：起於 H3（案例卡除外），訖於下一個 **H1／H2／H3**（H4 屬節之內文，不作節界——初版以 `###`
#     一概截斷，遂使每節只餘其下第一根 H4 之前數行，own 恆 0 而全盤假「未證」）
BND = [i for i, l in enumerate(L) if re.match(u'^#{1,3} ', l)]


def span_end(i):
    nxt = [k for k in BND if k > i]
    return nxt[0] if nxt else len(L)


H1L = [i for i, l in enumerate(L) if re.match(u'^# ', l)]


def ch_ranges(n):
    """該章全部 H1 之『起・訖』（上、下兩 H1 合併為一靶）。"""
    out = []
    for i in CHAP:
        if CH.match(L[i]).group(1) == n:
            nxt = [k for k in H1L if k > i]
            out.append((i, nxt[0] if nxt else len(L)))
    return out


sec = {}                                        # 靶鍵 -> [(起, 訖)]（同名多段須併靶）


def add(key, a, b):
    sec.setdefault(key, []).append((a, b))


for i, l in enumerate(L):
    if not l.startswith(u'### ') or l.startswith(u'### 〔'):
        continue
    m = SEC.match(l)
    if not m:
        continue
    lab = ((m.group(1) and u'第%s節' % m.group(1)) or
           (m.group(2) and u'閘門%s' % m.group(2)) or
           (norm(m.group(3))[:16] if m.group(3) else u'%s、%s' % (m.group(4), norm(m.group(5) or u'')[:10])))
    lab = re.sub(u'[（(]續[)）]', u'', lab)      # 『閘門二（續）』屬閘門二之續段：分列則指『閘門二』者看不足其文（網眼）
    ch = chap_of(i)
    add(u'%s・%s' % (ch or u'卷首', lab), i, span_end(i))
for n in {CH.match(L[i]).group(1) for i in CHAP}:
    rs = ch_ranges(n)
    add(u'第%s章・全章' % n, rs[0][0], rs[-1][1])
TXT = {k: norm(u'\n'.join(u'\n'.join(L[a:b]) for a, b in v)) for k, v in sec.items()}
print(u'靶 %d 鍵（其中全章 %d）・冊 %d 行' % (len(TXT), sum(1 for k in TXT if k.endswith(u'全章')), len(L)))


def cover(i):
    return {k for k, rs in sec.items() if any(a <= i < b for a, b in rs)}


hit = mid = wrong = unk = nokey = 0
for i, l in enumerate(L):
    for m in PTR.finditer(l):
        hit += 1
        lab = ((m.group(2) and u'第%s節' % m.group(2)) or
               (m.group(3) and u'閘門%s' % m.group(3)) or u'全章')
        key = u'第%s章・%s' % (m.group(1), lab)
        if key not in TXT:
            nokey += 1
            print(u'L%-5d ✗ 靶不可求：%s' % (i + 1, key))
            continue
        nm = norm(m.group(4))
        wins = [nm[k:k + 4] for k in range(max(1, len(nm) - 3))]     # 四字窗：五字則冊內『與學羯磨（與波羅夷戒）』之插字斷窗，合法撮述遂墮『未證』
        own = sum(1 for w in wins if w in TXT[key])
        cov = cover(i)
        pool = [(sum(1 for w in wins if w in v), k) for k, v in TXT.items()
                if k != key and not k.endswith(u'全章') and k not in cov]
        bn, bk = max(pool) if pool else (0, u'—')
        if own:
            mid += 1
        elif bn >= 2:
            wrong += 1
            print(u'L%-5d ✗ 錯靶 %-20s own=0 best=%d ⟶ %s｜X＝%s' % (i + 1, key, bn, bk, m.group(4)[:26]))
        else:
            unk += 1
            print(u'L%-5d ・未證 %-20s X＝%s' % (i + 1, key, m.group(4)[:26]))
print(u'———— 節級指針 %d 處：中 %d・錯靶 %d・未證 %d・靶不可求 %d' % (hit, mid, wrong, unk, nokey))
sys.exit(1 if (wrong or nokey) else 0)
