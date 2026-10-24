# -*- coding: utf-8 -*-
"""276 續・刀：尺二新管轄所逮六段『逐字宣稱』之真逐字回填。

口徑：（一）新句一律先對語料核過（依 `_tk.classify` 之 segmentation：刪節號切段・norm 折異體），
      核不過者不落刀；（二）錨在冊中須恰見一次，非一即擲；（三）改畢以尺二同一口徑覆核全書，
      仍有未中者即回退不寫（寫檔在核後）；（四）先備份 + SHA，一步可退。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276verb3.py        # 乾跑（只印差）
      PYTHONIOENCODING=utf-8 python -X utf8 _work/r276verb3.py apply   # 落刀寫檔
"""
import hashlib
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
sys.path.insert(0, ROOT)
sys.path.insert(0, WORK)
import _casedef as CD                                              # noqa: E402
import _tk                                                     # noqa: E402

NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
BAK = os.path.join(WORK, u'r276verb3.bak')

EDITS = [
    # (標，舊句，新句，語料之據)
    (u'蘇毘羅第二案・奪『而』字',
     u'有比丘尼持蘇毘羅去彼不遠行，比丘尼作是念',
     u'有比丘尼持蘇毘羅去彼不遠而行，比丘尼作是念',
     u'有比丘尼持蘇毘羅去彼不遠而行，比丘尼作是念'),

    (u'迦留陀夷初條・首句歸語料（冊衍『爾時・祇樹給孤獨園』）',
     u'「爾時佛在舍衛國祇樹給孤獨園。時迦留陀夷聞佛所制不得弄陰墮精，便手執戶鑰在門外立，'
     u'伺諸婦女居士家婦女童女來，語言：『大妹！可來入房看。』將至房中，捉捫摸嗚口',
     u'「佛在舍衛國，時迦留陀夷聞佛所制不得弄陰墮精，便手執戶鑰在門外立，'
     u'伺諸婦女居士家婦女童女來，語言：『大妹！可來入房看。』將至房中捉捫摸嗚口',
     u'佛在舍衛國，時迦留陀夷聞佛所制不得弄陰墮精，便手執戶鑰在門外立，'
     u'伺諸婦女居士家婦女童女來，語言：「大妹！可來入房看。」將至房中捉捫摸嗚口'),

    (u'迦留陀夷・初條戒文與二條因緣之間補刪節號',
     u'若觸一一身分者，僧伽婆尸沙。』  ',
     u'若觸一一身分者，僧伽婆尸沙。』……  ',
     None),

    (u'迦留陀夷・二條戒文與三條因緣之間補刪節號',
     u'隨所說麁惡婬欲語，僧伽婆尸沙。』  ',
     u'隨所說麁惡婬欲語，僧伽婆尸沙。』……  ',
     None),

    (u'跋難陀・捉金銀戒衍一『若』字，且其下接『此應捨』乃第十九條捨法，中間補刪節號',
     u'> 若比丘，自手捉金銀若錢，若教人捉，若置地受，尼薩耆波逸提。  ',
     u'> 若比丘自手捉金銀若錢，教人捉，若置地受，尼薩耆波逸提。……  ',
     u'若比丘自手捉金銀若錢，教人捉，若置地受，尼薩耆波逸提。'),

    (u'跋難陀・末二句（酥油蜜持來僧中食／無行跡處棄之）語料無文，改結於有據之淨法段',
     u'> 若買得酥油蜜物，持來僧中食，犯戒比丘不得噉，餘比丘得食。若彼人不肯受者，'
     u'當語彼人言：『汝持去棄之。』……若無人者，應差比丘持去，在無行跡處棄之。」',
     u'> 若得淨衣鉢、坐具、針筒，得持貿易持之。……若彼人不肯與者，餘比丘當語其人言：'
     u'『佛有教，為淨故與汝，應還彼比丘物。』」',
     u'若得淨衣鉢、坐具、針筒，得持貿易持之。……若彼人不肯與者，'
     u'餘比丘當語其人言：「佛有教，為淨故與汝，應還彼比丘物。」'),

    (u'兩舌戒・『欲令鬪諍』乃攝述，歸語料之『如是不息…』',
     u'傳彼屏語向此說，欲令鬪諍……',
     u'傳彼屏語向此說，如是不息，遂至眾中，未有鬪事而生鬪事，已有鬪事而不滅……',
     u'傳彼屏語向此說，如是不息，遂至眾中，未有鬪事而生鬪事，已有鬪事而不滅'),

    (u'七百集法・此處語料作『耶舍伽那子』（他處之『迦』自有據，不并改）',
     u'聞耶舍迦那子比丘往人間求索伴黨',
     u'聞耶舍伽那子比丘往人間求索伴黨',
     u'聞耶舍伽那子比丘往人間求索伴黨'),

    (u'補遺 39・相隔两段無標併入一引號，補刪節號（凡例第三律）',
     u'於夢中失精，不犯。若比丘故弄陰失精',
     u'於夢中失精，不犯。……若比丘故弄陰失精',
     None),
]


def verify(piece, tag):
    """新句须逐段在語料（依 classify 之切段與 norm），否即擲。"""
    for p in _tk.ELL.split(piece):
        pn = _tk.norm(p)
        if len(pn) >= 4 and pn not in _tk.VINAYA:
            raise AssertionError(u'%s｜語料無此段：%s' % (tag, p[:40]))


def recheck(lines):
    """以尺二同一口徑覆核：回傳未中之段 [(行, 引文首 30)]。"""
    bad = []
    for a, b, lab, dep in CD.src_blocks(lines):
        txt = u'\n'.join(lines[a:b])
        for m in _tk.Q_RE.finditer(txt):
            ln = a + txt[:m.start()].count(u'\n')
            col = m.start() - (txt.rfind(u'\n', 0, m.start()) + 1)
            if _tk.SRC_STRICT.search(lines[ln][:col]):
                continue
            if dep == u'段' and not CD.is_quote_line(lines[ln]):
                continue
            k, _d = _tk.classify(m.group(1))
            if k == u'miss':
                bad.append((ln + 1, m.group(1)[:30].replace(u'\n', u'')))
    return bad


def main():
    apply = u'apply' in sys.argv
    raw = io.open(SRC, encoding=u'utf-8-sig').read()
    L = raw.replace(u'\r\n', u'\n').split(u'\n')
    print(u'正本｜%d 行・sha256 %s' % (len(L), hashlib.sha256(raw.encode(u'utf-8')).hexdigest()[:12]))
    out = list(L)
    for tag, old, new, ev in EDITS:
        n = sum(x.count(old) for x in out)
        if n != 1:
            raise AssertionError(u'%s｜錨見 %d 次（須 1）：%s' % (tag, n, old[:30]))
        if old in new:
            raise AssertionError(u'%s｜新句仍含舊句（替無所獲）' % tag)
        if ev:
            verify(ev, tag)
        out = [x.replace(old, new) for x in out]
        print(u'  ✓ %s%s' % (tag, u'（語料已核）' if ev else u'（刪節號／界語，不校）'))
    bad = recheck(out)
    print(u'改後以尺二覆核｜未中 %d 段%s' % (len(bad), u'' if not bad else u'：%s' % bad[:6]))
    if bad:
        print(u'———— 未中者猶在，不寫檔（先補據或另刀）')
        return 1
    if not apply:
        print(u'———— 乾跑畢（加 apply 方落刀）')
        return 0
    shutil.copyfile(SRC, BAK)
    txt = u'\n'.join(out)
    io.open(SRC, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    new = io.open(SRC, encoding=u'utf-8').read()
    print(u'落刀｜備份 %s｜新 %d 行・%d B・sha256 %s' % (
        BAK, new.count(u'\n') + 1, len(new.encode(u'utf-8')),
        hashlib.sha256(new.encode(u'utf-8')).hexdigest()[:12]))
    return 0 if new.replace(u'\r\n', u'\n') == txt else 2


if __name__ == u'__main__':
    sys.exit(main())
