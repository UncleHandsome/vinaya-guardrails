# -*- coding: utf-8 -*-
# 印面與建冊當輪之兩向同步覆核（第 179 輪立；重建輪收帳、以及平日宣稱「印面未動」之自證）。
#
# 問：四式建好之後主檔又寫了字——那些字動到印面沒有（冊還須再建否）？
# 法：**不作第二套過濾式，逕跑管線自身的 md 段**（build38 第 1271–1276 行之序，外加 `write_md` 之
#     改標與目錄整段取代），以临时檔承接；再與建冊當輪所出之四份中介檔**逐行對稱差**。
#     兩側同出一源，故底冊・卷首 stray・DROP_QUOTE・SLIM 開關・精簡本削塊與隨改・定本附錄改標
#     等豁免俱由管線自證，我不列名單（列名單即又一筆手工帳，且必腐）。
# 正向（今出而冊無）＝印面新增或改字 ⇒ 候建；反向（冊有而今無）＝印面經有削改而冊未追 ⇒ 候建。
# 兩向俱空，方許宣稱「四式與主檔同步、無待建之動」。
# 負測：argv[1] 給副本；argv[2] 給 'require-fwd'（副本多一行印面）或 'require-rev'（副本削一行印面）。
# 陷阱一則（本器始立即踩）：`_tk.bottom_lines()` 為 **0 起點**索引，以其校 1 起點之行號即錯開一行——
#     今既全交管線取道，此集在本器不復需用（避其坑，非忘其坑）。
import io
import os
import re
import sys

sys.path.insert(0, u'.')
sys.path.insert(0, u'_print')
import build38

CAND = sys.argv[1] if len(sys.argv) > 1 else None
NEED = sys.argv[2] if len(sys.argv) > 2 else None
MASTER = CAND or u'ver38四分律_起心動念心智分析框架_修正版.md'
build38.SRC = MASTER                      # 負測以副本為源：管線之讀源即本器之讀源
TMP = u'_work/_sync_body.md'


def norm(x):
    return re.sub(u"\\s+", u"", x).strip()


def body(mode):
    """跑管線 md 段（不落印、不渲染，僅落地至 TMP），回傳其行。"""
    build38.MODE = mode
    src = build38.read_source()
    hs0 = build38.collect_all_headings(src)
    ls = build38.drop_appendices(build38.drop_blocks(src, hs0), hs0)
    ls = build38.strip_ch6_yuandian(ls, build38.collect_all_headings(ls))
    ls = build38.apply_slim_markers(ls)
    ls = build38.apply_slim_cuts(ls, build38.collect_all_headings(ls))
    build38.MD = TMP
    build38.write_md(ls, build38.collect_all_headings(ls), [])
    return io.open(TMP, encoding=u'utf-8').read().split(u'\n')


def nset(ls):
    return set(x for x in map(norm, ls) if x)


PAIRS = [(u'full', [u'_print/ver38_列印版.md', u'_print/ver38_列印版_screen.md']),
         (u'slim', [u'_print/ver38_列印版_精簡本.md', u'_print/ver38_列印版_精簡本_screen.md'])]

tot_f = tot_r = 0
for mode, ps in PAIRS:
    b = nset(body(mode))
    for p in ps:
        i = nset(io.open(p, encoding=u'utf-8').read().split(u'\n'))
        fwd, rev = sorted(b - i), sorted(i - b)
        tot_f += len(fwd)
        tot_r += len(rev)
        print(u'%-4s %-30s 今 %d｜冊 %d｜正向缺 %d｜反向幽 %d' % (
            mode, os.path.basename(p), len(b), len(i), len(fwd), len(rev)))
        for t in fwd[:5]:
            print(u'   缺→ %s' % t[:62])
        for t in rev[:5]:
            print(u'   幽→ %s' % t[:62])
    print(u'  （同 mode 兩式中介檔應同集：print/screen 之別唯 CSS）')
    a = nset(io.open(ps[0], encoding=u'utf-8').read().split(u'\n')) ^ \
        nset(io.open(ps[1], encoding=u'utf-8').read().split(u'\n'))
    print(u'  print↔screen 中介檔之差集：%d 形%s' % (len(a), u'（須 0）' if mode else u''))

if os.path.exists(TMP):
    os.remove(TMP)

if NEED == u'require-fwd':
    ok = 0 if tot_f else 1
    print(u'負測（正向須有缺）：缺 %d → %s' % (tot_f, u'器能逮' if tot_f else u'器不能逮'))
elif NEED == u'require-rev':
    ok = 0 if tot_r else 1
    print(u'負測（反向須有報）：報 %d → %s' % (tot_r, u'器能逮' if tot_r else u'器不能逮'))
else:
    ok = 0 if not tot_f and not tot_r else 1
    print(u'結果：%s（正向 %d／反向 %d）' % (
        u'印面與建冊當輪兩向全同——四式與主檔同步、無待建之動' if ok == 0
        else u'印面有動未入冊——候建', tot_f, tot_r))
sys.exit(ok)
