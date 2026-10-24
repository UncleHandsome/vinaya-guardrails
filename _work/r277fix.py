# -*- coding: utf-8 -*-
"""277 輪・刀：附錄審查報告之實病（先逐條量今檔 sha 9a11c38f5322，量得方落刀）。

治七項：
  甲・附錄四表列之逆序（51・60 兩行被擱在 62 之後）➔ 歸位（51 繼 50、60 繼 59）。
  乙・附錄四與集群矩陣之佔位符（案例 60『卷次未細核』・案例 69『—』）➔ 60 補『卷十六·第五十八條』
      （據本書自報之條次↔卷序列：51〜52〜53〜61〜62 皆卷十六，58 在其間；外部報告同主此說）；
      69 如實標『卷次未細核・文在本地三十八至四十九卷分段檔』（其引文已證在 38-49 檔，細卷無據）。
  丙・附錄二錯指「第六章〔案例 18〕加判重增無知罪」——案例 18 實為『前妻示根』，全書無此案之卡；
      『重增無知』之論述實在第三章閘門二『怠學加重律』➔ 指針歸實（『詐言不知戒』之案另列候裁）。
  丁・附錄三末段之裸檔名「50-60」➔「卷五十至六十」（印面形制，尺之目 22 同輪放寬網眼）。
  戊・附錄一第五節 野狐公案之敘事腰斬（四鐵律忽云『火化死狐』而前文無死狐）➔ 補終幕一句
      （不掛引號：宗門敘事，不作逐字宣稱）。
  己・附錄六〔補遺 30〕事相含糊而原典特定（『行了不淨行』對『以男根著彼女人口中含』）➔ 事相補『以口道』。
  庚・凡例【原典層】既已如實記『十四欄』，本輪不再動。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r277fix.py [apply]
"""
import hashlib
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)

REPS = [
    (u'乙・案例 60 之卷欄（附錄四）',
     u'| **〔案例 60〕藏他衣鉢坐具針筒** | 卷次未細核・文在本地十一至二十一卷分段檔 |',
     u'| **〔案例 60〕藏他衣鉢坐具針筒** | 卷十六·波逸提法第五十八條 |', 1),
    (u'乙・案例 60 之卷欄（集群矩陣）',
     u'《四分律》卷次未細核・文在本地十一至二十一卷分段檔',
     u'《四分律》卷十六', 1),
    (u'乙・案例 69 之卷欄（附錄四）',
     u'| **〔案例 69〕誤入眠婦室看門相** | — |',
     u'| **〔案例 69〕誤入眠婦室看門相** | 卷次未細核・文在本地三十八至四十九卷分段檔 |', 1),
    (u'乙・案例 69 之卷欄（集群矩陣）',
     u'| 《四分律》— |',
     u'| 《四分律》卷次未細核・文在本地三十八至四十九卷分段檔 |', 1),
    (u'丙・附錄二錯指歸實',
     u'第六章〔案例 18〕加判重增無知罪',
     u'第三章閘門二『怠學加重律』（犯後抗辯『我今始知』者，本罪照罰，更加判重增無知波逸提）', 1),
    (u'丁・附錄三裸檔名歸卷段',
     u'推扇、除鳥巢、給果蒜亦資其勞（50-60、卷二十二至三十）',
     u'推扇、除鳥巢、給果蒜亦資其勞（卷五十至六十・卷二十二至三十）', 1),
    (u'戊・野狐公案補終幕（不掛引號，不作逐字宣稱）',
     u'後得百丈代下一轉語「**不昧因果**」，言下大悟，脫免狐身。',
     u'後得百丈代下一轉語「**不昧因果**」，言下大悟，脫免狐身。'
     u'老人自陳脱身之後，遺骸猶在後山岩下；百丈翌日領眾至岩下，以杖挑出死狐，依亡僧事例闍維送之。', 1),
    (u'己・補遺 30 事相扣合原典',
     u'與前來探病之婦女行了不淨行',
     u'與前來探病之婦女以口道行不淨行', 1),
]

ROW = re.compile(u'^\\| \\*\\*〔案例 ?0*(\\d+)〕')


def reorder(out):
    """甲・附錄四之表列歸序：51 繼 50、60 繼 59。以行首之案號為錨，移動整行。"""
    a4 = next(i for i, l in enumerate(out) if l.startswith(u'# 附錄四'))
    a5 = next(i for i, l in enumerate(out) if l.startswith(u'# 附錄五'))
    idx = {}
    for i in range(a4, a5):
        m = ROW.match(out[i])
        if m:
            idx[int(m.group(1))] = i
    moved = []
    for num, after in ((51, 50), (60, 59)):
        src = idx[num]
        row = out.pop(src)
        tgt = next(i for i, l in enumerate(out)
                   if (m := ROW.match(l)) and int(m.group(1)) == after
                   and i >= next(k for k, l in enumerate(out) if l.startswith(u'# 附錄四')))
        out.insert(tgt + 1, row)
        moved.append(u'%d 繼 %d' % (num, after))
    return out, moved


def audit(out):
    """改畢之覆核：序淨・佔位淨・行列數仍 102。"""
    a4 = next(i for i, l in enumerate(out) if l.startswith(u'# 附錄四'))
    a5 = next(i for i, l in enumerate(out) if l.startswith(u'# 附錄五'))
    nums = [int(m.group(1)) for l in out[a4:a5] if (m := ROW.match(l))]
    inv = [(nums[k], nums[k + 1]) for k in range(len(nums) - 1) if nums[k] > nums[k + 1]]
    occ = {p: sum(l.count(p) for l in out) for p in (u'卷欠', u'— |', u'| — |', u'（50-60', u'50-60、')}
    return len(nums), inv, occ


def main():
    apply = u'apply' in sys.argv
    raw = io.open(SRC, encoding=u'utf-8-sig').read()
    L = raw.replace(u'\r\n', u'\n').split(u'\n')
    print(u'正本｜%d 行・sha256 %s' % (len(L), hashlib.sha256(raw.encode(u'utf-8')).hexdigest()[:12]))
    out = list(L)
    for tag, old, new, want in REPS:
        n = sum(x.count(old) for x in out)
        if n != want:
            raise AssertionError(u'%s｜錨見 %d 次（須 %d）：%s' % (tag, n, want, old[:26]))
        out = [x.replace(old, new) for x in out]
        print(u'  ✓ %s' % tag)
    out, moved = reorder(out)
    print(u'  ✓ 甲・歸序：%s' % u'、'.join(moved))
    n, inv, occ = audit(out)
    print(u'覆核｜附錄四行列 %d・逆序 %d・佔位餘 %s' % (n, len(inv), occ))
    if n != 102 or inv or occ[u'卷欠'] or occ[u'| — |']:
        print(u'———— 覆核未淨，擲刀不寫')
        return 1
    txt = u'\n'.join(out)
    if not apply:
        print(u'———— 乾跑畢（加 apply 方落刀）・字數 %+d' % (len(txt) - len(raw)))
        return 0
    bak = os.path.join(WORK, u'r277fix.bak')
    shutil.copyfile(SRC, bak)
    io.open(SRC, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    new = io.open(SRC, encoding=u'utf-8').read()
    print(u'落刀｜備份 %s｜新 %d 行・%d B・sha256 %s' % (
        bak, new.count(u'\n') + 1, len(new.encode(u'utf-8')),
        hashlib.sha256(new.encode(u'utf-8')).hexdigest()[:12]))
    return 0 if new == txt else 2


if __name__ == u'__main__':
    sys.exit(main())
