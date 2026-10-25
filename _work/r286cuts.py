# -*- coding: utf-8 -*-
"""286・冊身之刀（外路第十四報告兩批之實病）：
   ① 第三章交付殘跡除 ② 附錄六舊編次之編者小記除 ③【新增專款】×2 除
   ④ 第四章結案戒文歸逐字 ⑤ 卷首索引之案名歸一 ⑥ 第七章四軸散落行併項
   ⑦ 62 行全流程圖折為甲乙兩段（免腰斬）。
   用法：python -X utf8 _work/r286cuts.py [--apply]"""
import io
import re
import shutil
import sys

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
T = S.replace(u'\r\n', u'\n')
LOG = []


def rep(old, new, label, n=1):
    global T
    c = T.count(old)
    assert c == n, u'【%s】命中 %d 見・期 %d' % (label, c, n)
    LOG.append(u'%-24s 命中 %d' % (label, c))
    T = T.replace(old, new, n)


# ── ① 第三章交付殘跡（含其上空行）
rep(u'\n*(第三章修正定本第一部分在此告一段落，第二部分將續接閘門三、閘門四與閘門五之完整純化文本)*\n',
    u'\n', u'① 交付殘跡除')

# ── ② 附錄六之舊編次備忘（285 改號後已成誤导性陈述）
i = T.find(u'> *〔編者小記〕本則以前之編次止於卅五')
assert i > 0, u'② 之錨不可求'
j = T.find(u'\n', i) + 1
seg = T[i:j]
back = T.rfind(u'\n', 0, i)
LOG.append(u'%-24s 除 %d 字・其首 %s' % (u'② 編者小記除', len(seg), seg[:14]))
T = T[:back + 1] + T[j:]

# ── ③【新增專款】之版本標籤（兩處）
rep(u'#### 五、【新增專款】僧伽內部侵權傷害之同儕求謝與實質修復',
    u'#### 五、僧伽內部侵權傷害之同儕求謝與實質修復', u'③ 款五標籤除')
rep(u'#### 八、【新增專款】惡意突襲捨戒之財產追索與歷史宣告阻卻',
    u'#### 八、惡意突襲捨戒之財產追索與歷史宣告阻卻', u'③ 款八標籤除')

# ── ④ 第四章結案戒文：報告令『補引號』，然冊文乃撮述（語料無此連綴）➔ 改歸逐字
rep(u'律有明敕：**如法諍事滅已而後更發起者，得波逸提**。',
    u'律有明敕：**「若比丘如法諍事滅已，後更發起者，得波逸提。」**', u'④ 戒文歸逐字')

# ── ⑤ 卷首對讀索引之案名（285 已刷附錄四，此為另一載體）
rep(u'〔案例87〕賓頭盧寧令王失位', u'〔案例87〕賓頭盧起迎王失位', u'⑤ 案名歸一')

# ── ⑥ 第七章四軸之散落行（同項之內隔一空行，共四處）
L = T.split(u'\n')
P2 = u'  ' + chr(0x3014)
kills = [i for i in range(1, len(L) - 1)
         if L[i].strip() == u'' and L[i - 1].startswith(P2) and L[i + 1].startswith(P2)]
assert len(kills) == 4, u'⑥ 散落行量得 %d（期 4）' % len(kills)
for i in reversed(kills):
    del L[i]
LOG.append(u'%-24s 併項 %d 處' % (u'⑥ 散落行併項', len(kills)))
T = u'\n'.join(L)

# ── ⑦ 62 行全流程圖：折為甲乙兩段（各 ≤31 行，得鎖於單頁）
L = T.split(u'\n')
st = next(i for i, x in enumerate(L) if x.startswith(u'```text') and u'【訴訟發動雙軌】' in L[i + 1])
en = next(i for i in range(st + 1, len(L)) if L[i].strip() == u'```')
body = L[st + 1:en]
assert len(body) == 62, u'⑦ 圖行數量得 %d（期 62）' % len(body)
cut = next(i for i, x in enumerate(body) if u'【心證階梯與證據調查】' in x)   # 0-based within body
A = body[:cut]                                       # 至匯流線與 ▼ 止
B = body[cut:]                                       # 自【心證階梯與證據調查】起
assert A[-1].strip() in (u'▼', u'▼') or u'▼' in A[-1], u'⑦ 甲段之末非箭頭：%r' % A[-1]
assert not (set(A) & set(B)), u'⑦ 甲乙兩段有重行（接縫雙載）'
newb = ([u'【甲・訴訟發動雙軌與求聽審查】'] + A[1:] + [u'```', u'', u'```text',
        u'【乙・心證審理、滅諍與出站】'] + B)
LOG.append(u'%-24s 甲 %d 行・乙 %d 行' % (u'⑦ 大圖折兩段', len(A), len(B)))
L[st:en + 1] = [u'```text'] + newb + [u'```']
T = u'\n'.join(L)
mx = 0
for m in re.finditer(u'(?s)^```text\\n(.*?)^```', T, re.M):
    mx = max(mx, len(m.group(1).split(u'\n')))
print(u'校：最長圍欄 %d 行（逾 45 即仍可能腰斬）・『新增專款』餘 %d・『卅』餘 %d・『在此告一段落』餘 %d'
      % (mx, T.count(u'新增專款'), T.count(u'卅'), T.count(u'在此告一段落')))
assert T.count(u'新增專款') == 0 and T.count(u'卅') == 0 and T.count(u'在此告一段落') == 0
print(u'\n'.join(LOG))
print(u'行數 %d ➔ %d（%+d）' % (len(S.split(u'\n')), len(T.split(u'\n')),
                              len(T.split(u'\n')) - len(S.split(u'\n'))))
if APPLY:
    shutil.copyfile(P, u'_archive/備份/ver39.pre286a.md')
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T)
    print(u'已寫入・備份 _archive/備份/ver39.pre286a.md')
else:
    print(u'（試跑・未寫檔）')
