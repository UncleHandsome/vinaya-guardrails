# -*- coding: utf-8 -*-
"""276 續・刀：形制之宣稱歸實（第六章改製後『一案一卡・卡內【律典原典】』之形已廢，
   冊中三處舊宣稱遂與載體不合；尺三之自報亦同病，另於器側改）。

三處：甲・凡例【引號給予標準】之『同線或近行』——『近行』不可驗，改與尺二・尺三同一口徑；
      乙・凡例【原典層】之『一百零二卡各立【律典原典】一欄』——今為三形載體＋十四回查欄；
      丙・附錄四表頭之『繇諸卡自身之【律典原典】欄匯出（一卡一行）』——今一案一行，匯自定義載體。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276word.py [apply]
"""
import hashlib
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)

EDITS = [
    (u'甲・凡例：出處閘門之界如尺',
     u'——**凡作逐字之宣稱者，必同線或近行冠有出處**（《……》・卷N・犍度之類），'
     u'無出處者一依撮述論，不列入就地覆核之數。',
     u'——**凡作逐字之宣稱者，必冠出處於引號同線之左，或標於其段之首**'
     u'（《……》・卷N・犍度・◎原典之類；標於段首者，其段須以『> 』起或以冒號引出，'
     u'其下引文方接連作一宣稱），無出處者一依撮述論，不列入就地覆核之數。'),

    (u'乙・凡例：原典層之落點如今制',
     u'**今冊之落點如實記**：第六章一百零二卡各立【律典原典】一欄（另有一站於附錄四之說明），'
     u'附錄六之十五則補遺另以 `◎原典` 標起，卡外之逐字，則依第一節之出處閘門判之。',
     u'**今冊之落點如實記**：第六章一百零二案以集群矩陣・經典地標之案號列・節題三形載其定義，'
     u'逐字之文匯於各節標明『律典原典逐字回查』之欄（今十四欄，一欄可覆數案，非一案一欄）；'
     u'附錄六十五則補遺則於【佛陀判語】下自標 `◎原典` 以起引文；'
     u'凡此欄・段之外之逐字，一依第一節之出處閘門判之。'),

    (u'丙・附錄四表頭：匯出之載體如今制',
     u'> 本表今全章 102 案，繇第六章諸卡自身之【律典原典】欄匯出（一卡一行，非手工抄錄），'
     u'故章內增損一卡，此表即隨動一行。',
     u'> 本表今全章 102 案，一案一行，繇第六章案號之定義載體（集群矩陣・經典地標之案號列・節題）匯出，'
     u'非手工抄錄，故章內增損一案，此表即隨動一行。'),
]

# 補遺引文之實數（乙則之宣稱須自量，不硬寫）
sys.path.insert(0, ROOT)
sys.path.insert(0, WORK)
import _casedef as CD                                              # noqa: E402
import _tk                                                     # noqa: E402
_L = _tk.MAIN_LINES
_bq = sum(1 for a, b, lab, dep in CD.src_blocks(_L) if dep == u'段'
          for j in range(a, b) if CD.is_quote_line(_L[j]))
print(u'量｜補遺段內純引行 %d 行（宣稱段數由尺二報，凡例只稱『其引文若干段』者須合此量）' % _bq)


def main():
    apply = u'apply' in sys.argv
    raw = io.open(SRC, encoding=u'utf-8-sig').read()
    L = raw.replace(u'\r\n', u'\n').split(u'\n')
    print(u'正本｜%d 行・sha256 %s' % (len(L), hashlib.sha256(raw.encode(u'utf-8')).hexdigest()[:12]))
    out = list(L)
    for tag, old, new in EDITS:
        n = sum(x.count(old) for x in out)
        if n != 1:
            raise AssertionError(u'%s｜錨見 %d 次（須 1）：%s' % (tag, n, old[:24]))
        out = [x.replace(old, new) for x in out]
        print(u'  ✓ %s' % tag)
    txt = u'\n'.join(out)
    if not apply:
        print(u'———— 乾跑畢（加 apply 方落刀）・字數差 %+d' % (len(txt) - len(raw)))
        return 0
    bak = os.path.join(WORK, u'r276word.bak')
    shutil.copyfile(SRC, bak)
    io.open(SRC, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    new = io.open(SRC, encoding=u'utf-8').read()
    print(u'落刀｜備份 %s｜新 %d 行・%d B・sha256 %s' % (
        bak, new.count(u'\n') + 1, len(new.encode(u'utf-8')),
        hashlib.sha256(new.encode(u'utf-8')).hexdigest()[:12]))
    return 0 if new == txt else 2


if __name__ == u'__main__':
    sys.exit(main())
