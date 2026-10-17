# -*- coding: utf-8 -*-
"""quotejudge.py —— 「判定語氣之引號」軸（第 135 輪立）。

緣起：全書凡例定「未冠出處之『』屬術語標注、不構成逐字宣稱」，故 `bq`／`bqa` 兩口徑皆放過无出處之
「」；而第六章『事相經過』全區又在 `bqa` 的掃描網外（該口徑逕跳第六章）。兩縫相交之處，
**「佛判：『○○』」一類的撮述／拼接語長期以直角雙引號冒充律語**——本軸專堵此縫。

口徑（三限並具方報病）：
 ① 引號前之 12 字內須有**判定類動詞**（佛言／佛判／判／宣告／確立／加評／加判／推翻／制／立／聽／依，
    及**繫詞一族**：此為／是為／此即／所謂／謂之／意謂／稱作／稱之為／名之為／管的是／說的是——
    第 170 輪補：『此為「以口供換取實體處分」』一类正掛單層引號，舊表唯認『佛判』式動詞而漏之）；
    小說家之对白動詞（喝斥、怒道、笑道、答曰）不列——其文學性一望可知，非冒充律語。
 ② 引號內容須「讀起來是一句話」：句末帶 ！。？ 或含 汝／我／爾／卿 等人稱代詞；
    純名相（如『十種禁肉』之類）屬術語標注，不較。
 ③ 其 norm 形（摺疊標點與 CBETA 拆聲後）須求之**全語料**（原文/ ＋ 佛經/）而不得。
豁免：同行已標〔案：…拆聲…〕者（律文原字係 CBETA 拆聲、書中以今字易之，已如實交代）。
範圍：印面為限——第六章通掃，其餘各章亦掃；附錄C／L／M（編年底冊，不入印本）不較；
      以「> 」起之引用塊與表列俱屬原典區，另有 `c6`／`e` 兩口徑守之。
退出碼：病 > 0 即退 1。
"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

L = t.LINES
NORM_ALL = u'\n'.join(t.norm(t.read(p)) for p in
                      glob.glob(os.path.join(t.ROOT, u'原文', u'*.txt')) +
                      glob.glob(os.path.join(t.ROOT, u'佛經', u'**', u'*.txt'), recursive=True))
Q = re.compile(u'「([^」]{4,80})」')
JUDGE = re.compile(u'(佛言|佛判|判|宣告|宣布|確立|加判|推翻|制|立|聽|依'
                   u'|此為|是為|此即|所謂|謂之|意謂|稱作|稱之為|名之為|管的是|說的是'
                   u')[^「」]{0,12}$')
UTT = re.compile(u'[！。？]$|汝|我|爾|卿')
MIN = 6
s6, e6 = t.sec(u'第六章')
skip = set()
for nm in (u'附錄C', u'附錄L', u'附錄M'):
    if t.sec(nm):
        skip.update(range(*t.sec(nm)))
bad = []
for i, line in enumerate(L):
    if i in skip:
        continue
    if line.strip().startswith('>') or line.strip().startswith('|'):
        continue
    if u'〔案：' in line and u'拆聲' in line:
        continue
    if u'〔◈' in line:
        continue                          # 本書法式之自製文（求聽文、自陳文、白文）已自標，非冒充律語
    for m in Q.finditer(line):
        q = m.group(1)
        if len(t.norm(q)) < MIN or t.norm(q) in NORM_ALL or not UTT.search(q):
            continue
        if not JUDGE.search(line[:m.start()]):
            continue
        bad.append((i + 1, q, line[max(0, m.start() - 24):m.start()]))
print(u'判定語氣掛「」而全語料查無（印面）：%d 處' % len(bad))
for ln, q, ctx in bad:
    print(u'  L%-6d %s ⟵ …%s' % (ln, q[:58], ctx[-20:]))
sys.exit(1 if bad else 0)
