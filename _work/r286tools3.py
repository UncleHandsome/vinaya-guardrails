# -*- coding: utf-8 -*-
"""286・管線之刀（重落版）：五刀皆以『唯一錨點』替換，不取函數區間（前版以此吞掉 table_keep）。"""
import io
import sys

APPLY = u'--apply' in sys.argv
B = u'_print/build39.py'
C = u'_print/print38.css'
LOG = []


def sub(txt, old, new, label, n=1):
    c = txt.count(old)
    assert c == n, u'【%s】命中 %d 見・期 %d' % (label, c, n)
    LOG.append(u'%-26s 命中 %d' % (label, c))
    return txt.replace(old, new, n)


S = io.open(B, encoding=u'utf-8').read()

# ① 終卷隨冊印
S = sub(S, u'      編纂底冊四篇與終卷呈辭之去留一仍舊制（終卷不印）。',
        u'      編纂底冊四篇仍不入主檔；『終卷』自第 286 輪奉令隨冊印（前制不印，致全章缺於冊）。',
        u'①a 卷首註')
S = sub(S, u'# 列印版不錄：上篇前置宣告與「終卷」之竣工呈辭（H1 以關鍵語內含比對）。',
        u'# 列印版不錄：上篇前置宣告。『終卷』自第 286 輪奉令**隨冊印**（外路第十四報告指其全章未出），\n'
        u'#   故 DROP_H1 今空——此器與其反檢仍留，唯不再擲任何 H1。', u'①b 濾註')
S = sub(S, u'DROP_H1 = ("全書竣工呈辭",)', u'DROP_H1 = ()', u'①c 濾單清空')

# ② 卷首頁碼起於自序（今 p2 印「2」而 p3 印「iii」，一卷首內兩制相交）
S = sub(S, u'''    # 為「開卷總提撕」掛 id，供 CSS 重置正文頁碼（封面不編碼、目錄用羅馬數字）
    body = [l.replace("## 【開卷總提撕】",
                       '<h2 id="opening-note">【開卷總提撕】</h2>', 1)
            if l.startswith("## 【開卷總提撕】") else l for l in body]''',
        u'''    # 為卷首第一個 H2 掛 id，供 CSS 具名頁 `toc` 起羅馬頁碼（封面不編碼）。
    # 286 之改：錨自『開卷總提撕』前移至真正之第一頁卷首『【自序…】』——舊制自序一頁落在 .fm
    #   之外，遂印成阿拉伯「2」而次頁作「iii」，一卷首內兩制相交（外路第十四報告逮之）。
    def _anchor_fm(l):
        for pre in (u"## 【自序", u"## 【開卷總提撕】"):
            if l.startswith(pre):
                return u'<h2 id="opening-note">%s</h2>' % l[3:].strip()
        return l
    body = [_anchor_fm(l) for l in body]''', u'② .fm 之錨前移')

# ③ 出處欄之可讐下限（短格門自 24 放寬至 30 半形單位）
S = sub(S, u'        # 今令每行至少容該欄最長『短格』（≤24 半形單位，即標籤類之格）之半，且不少於四個漢字。',
        u'        # 今令每行至少容該欄最長『短格』（≤30 半形單位，標籤與卷次類之格；286 自 24 放寬，\n'
        u'        # 因『卷四十八・初分』一類 25〜30 單位之格舊不入眼，出處欄遂一字一行）之半，且不少於四個漢字。',
        u'③a 下限之註')
S = sub(S, u'            labs = [u[i] for u in units if 0 < u[i] <= 24]',
        u'            labs = [u[i] for u in units if 0 < u[i] <= 30]', u'③b 短格之門')

# ④ 表前標籤歸表為 caption（新函數置於 pali_span 之前——不取區間，免吞鄰函）
NEWFN = (u'def label_table_keep(html):\n'
         u'    r"""表前之短標籤行歸入表體為 <caption>（第 286 輪・外路第十四報告 p55 表題孤留）。\n\n'
         u'    先試之途為鎖框（`blockquote.keep`），然 Chromium 於框高過頁時不執行 break-inside:avoid，\n'
         u'    標籤照樣孤留上頁；今改把標籤搬進表體——caption 屬表之一部，表若跨頁，表題必隨其首段\n'
         u'    同行（且 thead 逐頁重現時表題不重出，caption 唯在表首）。"""\n'
         u"    PAT = re.compile(\n"
         u"        r'(?s)<blockquote>\\s*<p[^>]*>\\s*(?:<strong>)?(【[^<】]{2,40}】)(?:</strong>)?\\s*:?\\s*</p>\\s*<table([^>]*)>')\n"
         u'\n'
         u'    def one(m):\n'
         u"        print(u'  表題入表：%s' % m.group(1)[:22])\n"
         u'        return (u\'<blockquote><table%s><caption class="tbl-lbl">%s</caption>\'\n'
         u"                % (m.group(2), m.group(1)))\n"
         u'\n'
         u'    return PAT.sub(one, html)\n\n\n')
S = sub(S, u'def pali_span(html):', NEWFN + u'def pali_span(html):', u'④a 新函數')
S = sub(S, u'    html = quote_keep(html)',
        u'    html = label_table_keep(html)      # 先入 caption，再論鎖框\n    html = quote_keep(html)',
        u'④b 注冊')
S = sub(S, u'PRINT_CSS = """', u'PRINT_CSS = """\n'
        u'/* 286・表題入表（見 label_table_keep）：表題與表身同命，不孤留上頁 */\n'
        u'caption.tbl-lbl { caption-side: top; text-align: left; font-weight: 700;\n'
        u'                  padding: .18em 0 .1em; break-after: avoid; }', u'④c PRINT_CSS')
CSS = io.open(C, encoding=u'utf-8').read()
CSS = sub(CSS, u'pre.keep { break-inside: avoid; page-break-inside: avoid; }',
          u'pre.keep { break-inside: avoid; page-break-inside: avoid; }\n'
          u'/* 286・表前標籤歸表為 caption（見 build39.label_table_keep） */\n'
          u'caption.tbl-lbl { caption-side: top; text-align: left; font-weight: 700;\n'
          u'                  padding: .18em 0 .1em; break-after: avoid; }', u'④d print38.css')

for k in (u'def table_keep', u'def quote_keep', u'def retune_tables', u'def pali_span'):
    assert S.count(k) == 1, u'器之諸函數有失：%s＝%d' % (k, S.count(k))
print(u'\n'.join(LOG))
print(u'校：函數俱在・DROP_H1 空 %s' % (u'DROP_H1 = ()' in S))
if APPLY:
    io.open(B, 'w', encoding=u'utf-8', newline=u'\n').write(S)
    io.open(C, 'w', encoding=u'utf-8', newline=u'\n').write(CSS)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
