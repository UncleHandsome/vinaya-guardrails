# -*- coding: utf-8 -*-
"""287・記憶檔之帳更新與簡形改正（唯一法源＝本檔之錨點）。"""
import io

P = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------' \
    u'/memory/project-round31-state.md'
raw = io.open(P, encoding='utf-8').read()

SIMP = chr(0x5F53) + chr(0x5834)          # 簡形『当场』
TRAD = chr(0x7576) + chr(0x5834)          # 正字『當場』
print(u'当场：%d｜當場：%d' % (raw.count(SIMP), raw.count(TRAD)))
i = raw.find(SIMP)
if i >= 0:
    print(u'錨：%r' % raw[i - 30:i + 12])
    raw = raw.replace(SIMP, TRAD)

A = u'**印面今制（276 建・284・285・286 三度重建・積輪 0）**'
assert raw.count(A) == 1, u'錨 A 非一：%d' % raw.count(A)
raw = raw.replace(A, u'**印面今制（276 建・284〜287 四度重建・積輪 0）**')

T = u'**歷次**：273＝302 頁（221）、274＝303（220）、276＝251（144）、284＝256（144）、' \
    u'285＝259（143）、286＝261（146）。'
assert raw.count(T) == 1, u'錨 T 非一：%d' % raw.count(T)
raw = raw.replace(T, u'**287 今制：影印・螢幕各 261 頁（大綱 146＝目錄 146・圍欄 75 段全同頁・超閾 0・'
                     u'最細 9.33pt・9pt 以下 0 段・verify39 兩軌不合格 0 處）**——本輪只動冊身，'
                     u'頁數與目錄條數不因文字之改而動，同齡可鑑。' + T.replace(
                         u'286＝261（146）。', u'286＝261（146）、287＝261（146）。'))

io.open(P, 'w', encoding='utf-8', newline='\n').write(raw)
print(u'寫畢：当场餘 %d 枚｜檔長 %d 字' % (raw.count(SIMP), len(raw)))
