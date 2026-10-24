# -*- coding: utf-8 -*-
"""284・帳（四）：奉令重建訖之記帳——日誌補一段、SOP 印面今制歸實（積輪 8 ➔ 0）、記憶同步。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]

# 一・日誌
LOG = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
TXT = io.open(LOG, encoding=u'utf-8-sig').read()
ADD = (u'\n**284 補・奉令重建四式＋清場＋入庫推送**（2026-10-25）：完整版影印與螢幕**各 256 頁**'
       u'（原 251，八輪之增削淨 35 行➔頁＋5），大綱 144 條＝目錄印出 144 條・定位失敗 0・同級重出跳過 0；'
       u'`_work/r273face.py 列印` 印面覆核**全中**——〇・同期（印晚於冊 7 分）・甲 144/144・乙 相符 255／不合 0／無頁碼 1・'
       u'丙 圍欄 74 段同頁 73＋超閾如實不鎖 1（L2762・62 行・p67→p84）・丁 附錄七篇俱在・戊 最細 6.2pt。'
       u'**新增之目視待察（非紅）**：戊 項 9pt 以下由歷輪之『唯 1 段 7.97pt』增至 **5 段**（L2875 7.54／L3231 6.32／'
       u'L3337 6.2／L3645 6.2／L3751 7.97，俱為流程圖式之 ```text 圍欄自動縮字），最細 6.2pt；'
       u'-build 另報『目錄條目過長，縮至 9.8〜10.4pt（低於下限 10.5）』三條（地標 11・13 與雙螺旋 06 之長題）'
       u'——二者俱屬印面可讀性，若欲治須拆段或縮題（結構區，候裁）。'
       u'**清場**：28 檔大塊快照與歷輪備檔（含 1.35 MB 之舊冊副本五份・830 KB 級 ver39.preNNN 十一份・7.2 MB 試製 PDF 一份）'
       u'移入 gitignore 之 `_archive/備份/`，五個 `.bak` 同移，15 檔 0 byte 與一次性雜檔刪除，'
       u'**共讓出工作區約 33 MB**；逐檔先試跑印名後落手（禁用前綴通配之戒在案）。'
       u'**入庫**：`git add -A` 前逐項覆核（30 刪・2 更名・23 改・275 新，無敏感檔、無巨二進制——印面產物由 .gitignore 隔開），'
       u'提交 `30b689f`『277〜284 八輪清創入冊・重建印面 256 頁・工作區清場（讓出 33 MB）』並推送 origin/main'
       u'（一次推 23 筆，含歷輪未推者），工作樹現為乾淨。**積輪 0**。\n')
assert u'284 補・奉令重建' not in TXT
io.open(LOG, 'a', encoding=u'utf-8').write(ADD)
print(u'日誌今 %d 行' % len(io.open(LOG, encoding=u'utf-8-sig').read().split(u'\n')))

# 二・SOP
P = os.path.join(ROOT, u'列印SOP.md')
S = io.open(P, encoding=u'utf-8-sig').read()
OLD = (u'- **印面**：**積輪 8**（277〜284 八輪之改俱未出冊；印面四式仍出於 276 換入之初之 8,146 行／251 頁冊形，'
       u'今冊已 8,178 行・sha256（LF 形）`6b9029f9902d`）。')
NEW = (u'- **印面**：**積輪 0**（284 輪奉令重建完整版影印與螢幕**各 256 頁**・大綱 144＝目錄印出 144・定位失敗 0；'
       u'冊 8,178 行・sha256（LF 形）`6b9029f9902d`，印面五量 `_work/r273face.py 列印` 全中；'
       u'待察：9pt 以下圍欄由 1 段增至 5 段（最細 6.2pt，俱流程圖式 ```text 自動縮字）與目錄長題三條縮至 9.8〜10.4pt（低於下限 10.5），'
       u'治須拆段或縮題，屬印面結構，候裁）。')
assert S.count(OLD) == 1, S.count(OLD)
S = S.replace(OLD, NEW, 1)
TAIL = (u'\n- **第 284 輪・清場今制**：工作區不留大塊快照——舊冊副本・歷輪 `ver39.preNNN.md`・`*.bak`・試製 PDF 一律移入 '
        u'`_archive/備份/`（已入 .gitignore），0 byte 與一次性雜檔直除；清檔須**逐名列檔、先試跑印名**（禁前綴通配，'
        u'`_work` 兩冊共用）。印面產物（`_print/*`）永不入庫，管線可重建。\n')
assert u'第 284 輪・清場今制' not in S
S = S.rstrip(u'\n') + TAIL
io.open(P, u'w', encoding=u'utf-8').write(S)
print(u'SOP 今 %d 行・sha %s' % (len(S.split(u'\n')), sha(S)))

# 三・記憶（專案檔之積輪與頁數＋索引行）
PM = os.path.join(u'C:', u'\\', u'Users', u'lionc', u'.qoder', u'projects',
                  u'C--Users-lionc-OneDrive-----------------', u'memory')
f1 = os.path.join(PM, u'project-round31-state.md')
M = io.open(f1, encoding=u'utf-8').read()
for a, b in ((u'・**積輪 8**（印面停 251 頁／8,146 行冊形，奉令方重建）',
              u'・**積輪 0**（284 奉令重建：完整版影印與螢幕各 **256 頁**・大綱 144/144・印面五量全中・已提交 `30b689f` 並推送 origin/main）'),
             (u'**積輪 8（印面停 251 頁／8,146 行，奉令方重建）。**', u'**積輪 0（284 重建：各 256 頁，印面五量全中；`30b689f` 已推）。**'),
             (u'**今冊 8,178 行・sha `6b9029f9902d`・十尺全綠（不變量 36/36・牙列 36 目 38 針 逮 38 欠 0・節級 36➔37 全中）・積輪 8。**',
              u'**今冊 8,178 行・sha `6b9029f9902d`・十尺全綠（不變量 36/36・牙列 36 目 38 針 逮 38 欠 0・節級 37/37）。**')):
    n = M.count(a)
    print(u'記憶改 %d 處：%s…' % (n, a[:18]))
    if n:
        M = M.replace(a, b)
TAIL2 = (u'\n\n**284 補・重建與清場（同輪末）**：奉令重建完整版影印・螢幕**各 256 頁**（原 251），`r273face 列印` 印面五量全中'
         u'（〇同期・甲 144/144・乙 255/0/1・丙 73＋超閾 1・丁 七篇俱在・戊最細 6.2pt）；**待察（非紅，屬印面可讀性候裁）**：'
         u'9pt 以下圍欄 1 ➔ **5 段**、目錄長題三條縮至 9.8〜10.4pt（下限 10.5）。清場：28 檔快照與備檔移入 '
         u'`_archive/備份/`（gitignore）、五個 .bak 同移、15 檔雜檔刪除，讓出工作區約 33 MB；'
         u'提交 `30b689f` 並推送 origin/main（一次推 23 筆），工作樹乾淨，**積輪 0**。'
         u'**清檔之戒仍適用：逐名列檔、先試跑印名、禁前綴通配（`_work` 兩冊共用）。**\n')
if u'284 補・重建與清場' not in M:
    M = M.rstrip(u'\n') + TAIL2
io.open(f1, u'w', encoding=u'utf-8').write(M)
f2 = os.path.join(PM, u'MEMORY.md')
X = io.open(f2, encoding=u'utf-8').read()
o = u'・**積輪 8**（印面停 251 頁／8,146 行，奉令方重建）'
n2 = u'・**積輪 0**（284 奉令重建：影印・螢幕各 **256 頁**・印面五量全中・`30b689f` 已推送 origin/main）'
print(u'索引改：%d 處' % X.count(o))
X = X.replace(o, n2)
io.open(f2, u'w', encoding=u'utf-8').write(X)
print(u'記憶三處訖')
