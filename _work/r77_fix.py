# -*- coding: utf-8 -*-
"""第七十七輪套改甲：印面工程黑話之洗、四塊『卸甲呼吸窗』之刪、精簡本不附附錄K（含隨動）。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, [f for f in os.listdir(ROOT) if f.startswith('ver38') and f.endswith('.md')][0])
BUILD = os.path.join(ROOT, '_print', 'build38.py')
TYPST = os.path.join(ROOT, '_print', 'build38_typst.py')
s = open(MD, encoding='utf-8').read()
log = []


def rep(a, b, label, want=1):
    global s
    got = s.count(a)
    if got != want:
        raise SystemExit(u'中止！%s｜命中 %d != %d｜%s' % (label, got, want, a[:30].encode('unicode_escape').decode()))
    s = s.replace(a, b)
    log.append(u'✓ %s' % label)


# ── 一、卷首凡例與附錄K 凡例：去 CI 黑話（保留其保證之義）──
rep(u'一側改掛而他側未隨動即報 FAIL；處斷欄與定位行二側之差則屬**已知敞口**，未設為不變量（因此差本屬正當），惟得隨時以腳本逐案列出核對',
    u'一側改掛而他側未隨改，查核即退回重修；處斷欄與定位行二側之差則屬**已知敞口**，未列為通例（因此差本屬正當），惟得隨時逐案列出覆核',
    u'卷首凡例洗 FAIL／腳本')
rep(u'**〔回指狀態之實測口徑與本輪校正〕**', u'**〔回指狀態之實測口徑與近輪校正〕**', u'附錄K 去本輪')
rep(u'本輪以腳本逐列覆核五十五列', u'近輪以全書逐列覆核五十五列', u'附錄K 去腳本')
rep(u'4. 覆核方式：以程式檢索全書「第X章第Y節第Z款」字樣，逐條比對本表，缺一即以死鏈論，退回重修。',
    u'4. 覆核方式：取全書「第X章第Y節第Z款」之指向逐條比對本表；有指而其款不存者，以斷鏈論，退回重修。',
    u'附錄K 去程式檢索')
rep(u'為徹底消除「空泛章級索引」與「死鏈」', u'為徹底消除「空泛章級索引」與「斷鏈」', u'附錄K 定位去死鏈')
rep(u'#### 一、心智生態系統全景 ASCII 拓撲結構圖', u'#### 一、心智生態系統全景拓撲圖', u'第七章圖題去 ASCII')
rep(u'精簡本另僅存 A、B、K 三篇，卷首已別立存檔聲明',
    u'精簡本另僅存 A、B 二篇（款級台帳隨定本），卷首已別立存檔聲明', u'結語篇數句隨動（K 出精簡本）')

# ── 二、四塊『卸甲呼吸窗』：其義已錨定於卷首與結語，章末不復重述 ──
def cut_win(cn, label):
    global s
    lines = s.split('\n')
    i = next((k for k, l in enumerate(lines) if l.startswith('> **【第%s章卸甲呼吸窗' % cn)), None)
    if i is None:
        raise SystemExit(u'中止！%s 頭行不可得' % label)
    j = i
    while j < len(lines) and (lines[j].startswith('>') or not lines[j].strip()):
        j += 1
    if j - i < 4:
        raise SystemExit(u'中止！%s 塊過短 %d' % (label, j - i))
    a = i
    while a > 0 and not lines[a - 1].strip():
        a -= 1
    e = j
    if e < len(lines) and not lines[e].strip():
        e += 1
    del lines[a:e]
    s = '\n'.join(lines)
    log.append(u'✓ %s：刪 %d 行' % (label, e - a))


for cn in [u'一', u'二', u'四', u'五']:
    cut_win(cn, u'第%s章卸甲呼吸窗' % cn)

open(MD, 'w', encoding='utf-8').write(s)

# ── 三、列印管線：精簡本不再附附錄K（兩路同步）──
for path, old, new in [
    (BUILD, 'SLIM_KEEP = {"A", "B", "K"}', 'SLIM_KEEP = {"A", "B"}   # 精簡本不附款級台帳（內部查核表，读者無用）'),
    (BUILD, u'K（跨章款級索引）；修訂誌、術語對照', u'修訂誌、術語對照、跨章款級索引'),
    (BUILD, u'僅收附錄 A（宗門心法）、B（壓力測試）、"', u'僅收附錄 A（宗門心法）、B（壓力測試）；"'),
    (BUILD, 'APPS = "附錄 A、B、K　三篇隨冊"', 'APPS = "附錄 A、B　二篇隨冊"'),
    (TYPST, 'SLIM_KEEP = {"A", "B", "K"}', 'SLIM_KEEP = {"A", "B"}'),
    (TYPST, 'APPS = "附錄 A、B、K　三篇隨冊"', 'APPS = "附錄 A、B　二篇隨冊"'),
    (TYPST, u'K（跨章款級索引）；修訂誌、術語對照', u'修訂誌、術語對照、跨章款級索引'),
]:
    t = open(path, encoding='utf-8').read()
    if t.count(old) != 1:
        raise SystemExit(u'中止！管線錨點 %s 命中 %d：%s' % (os.path.basename(path), t.count(old),
                                                            old[:28].encode('unicode_escape').decode()))
    t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)
    log.append(u'✓ 管線 %s：%s' % (os.path.basename(path), old[:22]))

open(os.path.join(HERE, 'r77_fix.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n行數 %d\n' % (s.count('\n') + 1))
print('\n'.join(log))
import py_compile
for p in (BUILD, TYPST):
    py_compile.compile(p, doraise=True)
print('兩路建置腳本編譯通過；正文今 %d 行' % (s.count('\n') + 1))
