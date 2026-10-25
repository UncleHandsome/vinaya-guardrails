# -*- coding: utf-8 -*-
"""285・批六甲（修）：#59 四段圍欄之折行＋#60 三條目錄長題精簡。
   折行以『行內找鑰・指定斷點・加縮排』三事為之，不靠空白數之硬匹配。
   用法：python -X utf8 _work/r285cuts6a.py [--apply]"""
import io
import sys
import unicodedata

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
L = S.replace(u'\r\n', u'\n').split(u'\n')
LOG = []


def w(s):
    return sum(2 if unicodedata.east_asian_width(c) in u'WF' else 1 for c in s)


def fold(key, before, after, indent=None, label=u''):
    """唯一含 key 之行，在 before|after 之界斷為兩行；續行縮排默認承原行之首。"""
    idx = [i for i, x in enumerate(L) if key in x]
    assert len(idx) == 1, u'【%s】鑰見 %d 行' % (label or key, len(idx))
    i = idx[0]
    line = L[i]
    assert before + after in line, u'【%s】斷點不在行內' % (label or key)
    ind = (indent if indent is not None else line[:len(line) - len(line.lstrip(u' '))])
    new = [line.replace(before + after, before + u'\n' + ind + after, 1)]
    if w(new[0]) > 105:                                        # 折一次仍超寬，再折一次
        parts = new[0].split(u'\n')
        for k, seg in enumerate(parts):
            if w(seg) <= 105:
                continue
            mid = seg[:len(seg) // 2]
            cut = max(mid.rfind(u'；'), mid.rfind(u'，'), mid.rfind(u'（'))
            assert cut > 0, u'【%s】再斷無點' % (label or key)
            parts[k:k + 1] = [seg[:cut + 1], ind + u'  ' + seg[cut + 1:]]
        new = [u'\n'.join(parts)]
    L[i] = new[0]
    LOG.append(u'%-22s L%-5d 寬 %d➔%d' % (label or key, i + 1, w(line),
                                          max(w(x) for x in new[0].split(u'\n'))))


# ── #59 四段之折行
fold(u'唯獨住無人之難緣始得暫行責心自誓', u'為正，', u'唯獨住無人之難緣始得暫行責心自誓',
     indent=u' ' * 26, label=u'四態損益')
fold(u'非佛陀親口逐字定法）', u'直入六夜摩那埵', u'（此級乃本書依正理四所設之引申，非佛陀親口逐字定法）',
     indent=u' ' * 32, label=u'覆藏四級')
# 急難凍結：一行三段，以 partition 兩刀（自動再折之式在此不適用）
i3 = [i for i, x in enumerate(L) if u'於原本暫停之刻度接續起算' in x]
assert len(i3) == 1, u'急難凍結鑰見 %d 行' % len(i3)
ln = L[i3[0]]
p1, s1, r1 = ln.partition(u'乃得接續（受別住是眾法')
p2, s2, p3 = r1.partition(u'   ──► 於原本')
assert s1 and s2, u'兩刀皆須在行內：%r' % ln[:40]
p1 = p1 + u'乃得接續'
NLN = chr(10)
L[i3[0]] = p1 + NLN + u' ' * 37 + p2 + NLN + u' ' * 26 + u'──► ' + p3.lstrip(u'─► ')
LOG.append(u'%-22s L%-5d 三段折畢➔寬 %d' % (u'急難凍結', i3[0] + 1,
    max(w(x) for x in L[i3[0]].split(NLN))))
# 非法足數第 12 類：一行三段
i4 = [i for i, x in enumerate(L) if u'不溯及推翻已成之羯磨' in x]
assert len(i4) == 1, u'非法足數鑰見 %d 行' % len(i4)
ln4 = L[i4[0]]
head4 = ln4[:len(ln4) - len(ln4.lstrip(u' '))]
a1, s14, r14 = ln4.partition(u'（個人隱密、大會當下無從得知者，')
a2, s24, a3 = r14.partition(u'『現前清淨擬制與善意信賴保護』，')
assert s14 and s24, u'兩刀皆須在行內：%r' % ln4[:40]
L[i4[0]] = (a1 + chr(10) + head4 + u'    ' + s14 + chr(10) + head4 + u'    ' + s24 + a3)
LOG.append(u'%-22s L%-5d 三段折畢➔寬 %d' % (u'非法足數', i4[0] + 1,
    max(w(x) for x in L[i4[0]].split(chr(10)))))

# ── #60 三條長題（副標題落正文）


def rep(old, new, label):
    global L
    c = u'\n'.join(L).count(old)
    assert c == 1, u'【%s】命中 %d' % (label, c)
    txt = u'\n'.join(L).replace(old, new, 1)
    LOG.append(u'%-22s 題寬 %d➔%d' % (label, max(w(x) for x in old.split(u'\n')),
                                      max(w(x) for x in new.split(u'\n'))))
    L = txt.split(u'\n')


rep(u'### 【經典地標深描 11】耶舍七百結集斷十事——面對全員腐敗時，吹哨人的跨界非常救濟\n',
    u'### 【經典地標深描 11】耶舍七百結集斷十事——全員腐敗時之吹哨救濟\n\n'
    u'本案之題旨在：當僧團多數已腐，異見者如何自處——**面對全員腐敗時，吹哨人的跨界非常救濟**。'
    u'此其副題，正文一依此判。\n', u'地標 11 短題')
rep(u'### 【經典地標深描 13】大迦葉五百結集責阿難——個人名譽在群體和合面前退讓的大悲自誓\n',
    u'### 【經典地標深描 13】大迦葉五百結集責阿難——群體和合前的大悲自誓\n\n'
    u'本案之題旨在：**個人名譽在群體和合面前退讓的大悲自誓**。此其副題，正文一依此判。\n',
    u'地標 13 短題')
rep(u'### 【雙螺旋對照專題 06】目連神足遭控緘默 vs 富羅那堅持少數異議——沉默與堅守的二諦張力\n',
    u'### 【雙螺旋對照專題 06】目連遭控緘默 vs 富羅那堅持異議——沉默與堅守之二諦\n\n'
    u'本組之題旨在：**目連神足遭控時的沉默**與**富羅那少數異議的堅守**，二諦之張力各極其邊。'
    u'此其副題，正文一依此判。\n', u'雙螺旋 06 短題')

T = u'\n'.join(L)
BLK = []
i = 0
while i < len(L):
    if L[i].startswith(u'```'):
        j = next((k for k in range(i + 1, len(L)) if L[k].strip() == u'```'), None)
        if j:
            mx = max((w(y) for y in L[i + 1:j]), default=0)
            if mx > 105:
                BLK.append((mx, i + 1))
            i = j + 1
            continue
    i += 1
print(u'\n'.join(LOG))
print(u'校：仍逾 105 之圍欄 %d 段 ➔ %s' % (len(BLK), BLK))
if APPLY:
    io.open(u'_archive/備份/ver39.pre285i.md', 'w', encoding=u'utf-8', newline=u'\n').write(S)
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
