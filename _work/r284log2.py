# -*- coding: utf-8 -*-
"""284・帳（二）：SOP 積輪 7➔8；專案記憶之現況與使用者記憶之新度。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]

# ── SOP
P = os.path.join(ROOT, u'列印SOP.md')
S = io.open(P, encoding=u'utf-8-sig').read()
OLD = (u'- **印面**：**積輪 7**（277〜283 七輪之改俱未出冊；印面四式仍出於 276 換入之初之 8,146 行／251 頁冊形，'
       u'今冊已 8,178 行・sha256（LF 形）`a37ac076d0a9`）。')
NEW = (u'- **印面**：**積輪 8**（277〜284 八輪之改俱未出冊；印面四式仍出於 276 換入之初之 8,146 行／251 頁冊形，'
       u'今冊已 8,178 行・sha256（LF 形）`6b9029f9902d`）。')
assert S.count(OLD) == 1, S.count(OLD)
S = S.replace(OLD, NEW, 1)
TAIL = (u'\n- **第 284 輪・第六章之清創（含兩新目）**：地標 03 段序歸一〜五・地標 07 卷四➔卷六（從附錄四同案）・'
        u'地標 05 兩段生肉自語料原始檔回圖補標點・凡例三枚錯字（樞點／輍／句讀者）除並立**第 35 目黑單**常護・'
        u'凡例補『引中之引三層亦作雙層角引號』與『次碼（/ 遮MM）乃歷版舊次』兩界定・卷首補三約（雙螺旋原典在附錄四・'
        u'案名以號為準・並列不謂同刑）・案 17／100 加對讀標・案 02／08／06／44 名歸一・地標 03 分本案與參引；'
        u'**立第 34 目『經典地標大案之段序須一〜五連貫』**（牙列針 34）、第 35 目黑單（牙列針 35），'
        u'不變量遂 34 ➔ **36**（自對合目順移為 36）。重建後須覆看第六章卷首括注（今加長）與地標 03 案號列之換行。\n')
assert u'第 284 輪・' not in S
S = S.rstrip(u'\n') + TAIL
io.open(P, 'w', encoding=u'utf-8').write(S)
print(u'SOP 今 %d 行・sha %s' % (len(S.split(u'\n')), sha(S)))

# ── 使用者記憶：第五十七度
UM = os.path.join(u'C:', u'\\', u'Users', u'lionc', u'.qoder', u'memory',
                  u'feedback-self-checkers-must-measure-reality.md')
U = io.open(UM, encoding=u'utf-8').read()
ADD = (u'\n\n**第五十七度・記錯不等於改錯；刀之標籤亦是產物（2026-10-25・戒律分析 ver39 第 284 輪）**：'
       u'281 那輪的日誌明文寫下『以記憶構碼位又錯兩枚（**標**誤為**樞**、閾誤為闊）』，可我當時只改了腳本，'
       u'冊身凡例裡那兩枚『樞點』與一枚『輍』照舊活了三輪，直到外部報告揪出。'
       u'**通則：凡帳上記『某字曾誤』，須同時掃冊身有無殘跡，並把該形列入常設黑單**——'
       u'今立 v39chk 第 35 目『印面無歷輪錯字（黑單隨輪增補）』，單中只收**本書絕無正用**之串（樞點・輍・奷・冱・遤・壊・儱・豂・訃），'
       u'故可長掃印面而不生偽陽（合法難字 毘・罽・闊・謚 不入單；簡形之掃另在第 21 目——兩器分工，按形與按串各守一側）。'
       u'同輪另兩課：① 新立的凡例句裡掛了一對裸「」，**自己觸發尺三『未標界之非逐字』而紅**（此同一課第三度現形：'
       u'落筆凡例・補遺・小記之新句，先跑尺再談功）；② 刀腳本的 rep() 引序寫反，19 支刀全印空標籤而 sha 照變——'
       u'**修改器的自我敘述（標籤・命中數・管轄數）也是產物之一部，跑完必核其印字，不得只看哈希。**')
assert u'第五十七度' not in U, u'已記過'
io.open(UM, 'w', encoding=u'utf-8').write(U + ADD)
back = io.open(UM, encoding=u'utf-8-sig').read()
print(u'使用者記憶 今 %d 行・sha %s・含五十七度：%s' % (
    len(back.split(u'\n')), sha(back), u'第五十七度' in back))
