# -*- coding: utf-8 -*-
# 記錄檔之『重複黏貼／兩條併為一條』偵測器（第 180 輪立，長駐；改完 SOP 或日誌之後即掃）。
#
# 緣起：第 179 輪以腳本補寫 SOP 時未重吐錨點，事後又以另一腳本『原樣補回』164 輪之『欄寬之制』條，
#   補回之身卻**同時留在兩條之內**（164 條本體完好，其 427 字之後段又黏進 179 輪『抽驗單須隨印面而動』條之末）。
#   歷輪只斷言『今制頁數各恰 1 條』——那查的是**標題**之重，查不到**內文**之重；此病藏一日，
#   到第 180 輪改用『欄寬之制』為鍵計條目數（得 2）才現形。同日上線即再逮兩組：
#   ①『簡形閘口之擴』與『探針可重跑』兩條**並存兩處**（condensed 版錯置於『台帳今制』之末、
#      wrapped 舊版在其當位『套改公約』），②L286 兩條併一行（152 輪『部別』條末黏上 164 輪『表內空格』條）。
#   **凡靠多處手工隨動之嚴密，皆是待解之債**——今立此器，一輪一掃，不待人工翻檢。
#
# 三口徑（行內正規化後取 60 字滑窗；窗長足以避體例性短句之偶同）：
#   甲 跨行重複窗：同一窗見於兩行（一條之內黏了他條之身）；
#   乙 行內自覆窗：同一窗在同一行見兩處（同段重寫之徵）；
#   丙 併條之形：行內見『。- **』（兩條被併成一行）。
# 白名單：純記號窗（盡為 |-: # * 空格引號者）不計。
# 分檔之體：SOP／規画／企画＝**條列檔**，三徑俱判（病→退 1）；編年日誌＝**記錄檔**，
#   其逐輪自報『終測：不變量 N/N、五口徑 c6 174/174…』之套語跨條同文乃其體（記錄之真），故**只報不判**
#   ——口徑須隨檔案之體而分，一刀切即把體例讀成缺陷（175 輪『族內各有其制』同例）。
# 負測：argv[1] 給副本（植一段重複黏貼）＋ 'require-hit' → 須有報方算過。
import io
import re
import sys

FILES = [u'列印SOP.md', u'文意梳理規劃.md', u'3D體例另冊與正文重排企畫.md']
INFO = [u'_archive/編年工程日誌.md']
W = 60
SIGN = re.compile(u'^[|\\-:\\s#*·．.。』『「』（）〔〕\\[\\]\\(）]*$')

args = [a for a in sys.argv[1:] if a != u'require-hit']
NEED = u'require-hit' in sys.argv[1:]
strict_list = args if args else FILES
info_list = [] if args else INFO


def scan(p):
    try:
        raw = io.open(p, encoding=u'utf-8').read()
    except IOError:
        return None
    lines = raw.split(u'\n')
    norm = [re.sub(u'\\s+', u'', l) for l in lines]
    # 表列（'| … |'）之「同一原文登兩行」乃清冊之體（一目一行、同句可屬兩目），不屬黏貼——不預
    keep = [i for i, l in enumerate(norm)
            if len(l) >= W and not SIGN.match(l) and not lines[i].strip().startswith(u'|')]
    win = {}
    for i in keep:
        for s in range(0, len(norm[i]) - W + 1):     # 步長取 1——初版以 7 取樣，兩處同文而起點非同餘於 7 時遂不漏報（負測現形）
            w = norm[i][s:s + W]
            if SIGN.match(w):
                continue
            win.setdefault(w, set()).add(i)
    pairs = {}
    for w, v in win.items():
        if len(v) < 2:
            continue
        key = tuple(sorted(v))
        e = pairs.setdefault(key, [0, w])
        e[0] += 1
    jia = sorted(pairs.items(), key=lambda x: (-x[1][0], x[0]))
    yi = []
    for i in keep:
        seen = set()
        for s in range(0, len(norm[i]) - W + 1):     # 步長取 1——初版以 7 取样，兩處同文而起點非同餘於 7 時遂不漏報（負測現形）
            w = norm[i][s:s + W]
            if SIGN.match(w):
                continue
            if w in seen:
                yi.append((i + 1, w))
                break
            seen.add(w)
    bing = [(i + 1, l[:64]) for i, l in enumerate(lines) if u'。- **' in l]
    print(u'%-30s 甲 跨行重複 %d 組｜乙 行內自覆 %d｜丙 併條 %d' % (p, len(jia), len(yi), len(bing)))
    for key, (cnt, w) in jia[:5]:
        print(u'   甲 L%s｜同文窗 %d 個｜例：%s…' % (u'＋L'.join(str(x + 1) for x in key[:4]), cnt, w[:34]))

    for i, w in yi[:4]:
        print(u'   乙 L%d｜窗：%s…' % (i, w[:34]))
    for i, t in bing[:4]:
        print(u'   丙 L%d｜%s' % (i, t))
    return len(jia) + len(yi) + len(bing)


TOT = 0
for p in strict_list:
    r = scan(p)
    if r is not None:
        TOT += r
if info_list:
    print(u'（以下乃記錄檔，套語跨條同文屬其體，只報不判）')
    for p in info_list:
        scan(p)

if NEED:
    ok = TOT > 0
    print(u'負測：strict 檔報 %d → %s' % (TOT, u'器有牙' if ok else u'器無牙'))
    sys.exit(0 if ok else 1)
print(u'結果：%s（條列檔合計 %d）' % (u'條列檔無重複黏貼' if TOT == 0 else u'條列檔有重複黏貼——須修', TOT))
sys.exit(0 if TOT == 0 else 1)
