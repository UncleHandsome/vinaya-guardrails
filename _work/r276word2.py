# -*- coding: utf-8 -*-
"""276 續・刀二：外路四報所陳之實病（先逐條量今檔，量得方落刀）。

復量之判（今檔 sha 8b71e8c86498）：
  實病・落刀：單銀之世俗金融詞；數位四分無桥句；〔案例09〕誤掛『洗瘡雙判』（其名實為侵害者自欺，
             且 07 已列於同行之首＝重出）；『迎回與新立之案（重整後補入）』交付殘跡 5 枚；
             『。；』相撞 14 枚；『二、人際互動領域（20 案）』實列 19；『第四節第十六款』之死指針；
             附錄四與矩陣之『卷欠』四枚。
  非病・不刀：『極刑 18・言諍 8・覓諍 11・犯諍 23・事諍 15』逐一點名對合，與自報全合；
             『內臟』之喻三見各位在結語§三・結語§五印卡・終卷§一，乃刻意迴環（凡例已無『只存首尾』之約）；
             『0. 公訴排除』今檔 0 見（舊版之病）。
卷欄之據：案例 51 用本書集群矩陣自報之『卷十七·波逸提法第六十七條』；案例 102 用同表之
         『卷三十七·安居犍度』；案例 60 全書無卷可引，故如實標『卷次未細核』並附本地可證之卷段。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276word2.py [apply]
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
    (u'②志工報酬・去世俗金融詞',
     u'發給志工之單銀或道糧', u'發給志工之生活津貼或道糧', 1),
    (u'⑥照護領域・〔案例09〕誤掛洗瘡（其實名乃侵害者自欺，且 07 已列同行＝重出）',
     u'  〔案例07〕、〔案例43〕、〔案例55〕、〔案例56〕。；〔案例95〕親洗病僧；〔案例09〕洗瘡雙判。',
     u'  〔案例07〕洗瘡雙判、〔案例43〕、〔案例55〕、〔案例56〕；〔案例95〕親洗病僧。', 1),
    (u'⑥照護領域・宣稱 6 案實為 5 案',
     u'六、照護與護生專業領域（6 案）', u'六、照護與護生專業領域（5 案）', 1),
    (u'⑧人際互動領域・宣稱 20 案實列 19',
     u'二、人際互動領域（20 案）', u'二、人際互動領域（19 案）', 1),
    (u'⑨死指針・『第四節第十六款』歸第四節之『尼眾算法』（今冊 L3251 實有此條）',
     u'依第四節第十六款尼眾法相統一原則', u'依本章第四節『尼眾算法』之原則', 1),
    (u'⑤附錄四・案例 51 之卷欄（據本書集群矩陣自報之卷十七·第六十七條）',
     u'| **〔案例 51〕私度關逃稅** | 卷欠 |',
     u'| **〔案例 51〕私度關逃稅** | 卷十七·波逸提法第六十七條 |', 1),
    (u'⑤附錄四・案例 60 之卷欄（全書無卷可引，如實標未細核＋本地可證之卷段）',
     u'| **〔案例 60〕藏他衣鉢坐具針筒** | 卷欠 |',
     u'| **〔案例 60〕藏他衣鉢坐具針筒** | 卷次未細核・文在本地十一至二十一卷分段檔 |', 1),
    (u'⑤附錄四・案例 102 之卷欄（據本書集群矩陣自報之卷三十七·安居犍度）',
     u'| **〔案例 102〕受請安居聞利背約** | 卷欠 |',
     u'| **〔案例 102〕受請安居聞利背約** | 卷三十七·安居犍度 |', 1),
    (u'⑤集群矩陣・案例 60 之卷欄（同附錄四之如實標）',
     u'《四分律》卷欠',
     u'《四分律》卷次未細核・文在本地十一至二十一卷分段檔', 1),
]

DELS = [(u'⑦交付殘跡・『迎回與新立之案（重整後補入）』之標籤行',
         u'* **迎回與新立之案（重整後補入）**：')]

INSERTS = [(u'③數位四分・補連綴句（只舉二分，須告白其餘二分不列之故）',
            u'##### 3. 數位資產物權法相錨定',
            [u'', u'*〔按〕律制僧物有四分，此唯舉與數位資產直接相涉之第一分・第四分；'
                   u'餘二分各依其制，不預此列。*'])]


def main():
    apply = u'apply' in sys.argv
    raw = io.open(SRC, encoding=u'utf-8-sig').read()
    L = raw.replace(u'\r\n', u'\n').split(u'\n')
    print(u'正本｜%d 行・sha256 %s' % (len(L), hashlib.sha256(raw.encode(u'utf-8')).hexdigest()[:12]))
    out = list(L)
    for tag, old, new, want in REPS:
        n = sum(x.count(old) for x in out)
        if n != want:
            raise AssertionError(u'%s｜錨見 %d 次（須 %d）：%s' % (tag, n, want, old[:28]))
        out = [x.replace(old, new) for x in out]
        print(u'  ✓ %s（%d 處）' % (tag, n))
    for tag, anchor, newlines in INSERTS:
        idx = [i for i, l in enumerate(out) if l.strip() == anchor]
        if len(idx) != 1:
            raise AssertionError(u'%s｜題行得 %d 枚（須 1）：%s' % (tag, len(idx), anchor[:24]))
        i = idx[0]
        if out[i + 1:i + 1 + len(newlines)] == newlines:
            raise AssertionError(u'%s｜連綴句已在冊，勿重插' % tag)
        out[i + 1:i + 1] = newlines
        print(u'  ✓ %s（插 L%d 後 %d 行）' % (tag, i + 1, len(newlines)))
    for tag, line in DELS:
        idx = [i for i, l in enumerate(out) if l.strip() == line]
        if len(idx) != 5:
            raise AssertionError(u'%s｜標籤行得 %d 枚（須 5）' % (tag, len(idx)))
        out = [l for i, l in enumerate(out) if i not in set(idx)]
        print(u'  ✓ %s（刪 %d 行）' % (tag, len(idx)))
    n = sum(x.count(u'。；') for x in out)
    if n != 14 - 1:                       # ⑥ 那枚已隨整行改寫而去
        raise AssertionError(u'⑦『。；』殘存 %d 枚（須 13）' % n)
    out = [x.replace(u'。；', u'；') for x in out]
    print(u'  ✓ ⑦標點相撞・『。；』改『；』（%d 處）' % n)
    n2 = sum(x.count(u'；。') for x in out)
    print(u'  量｜『；。』残存 %d 枚' % n2)
    # 覆核：全書不得再有『卷欠』・『。；』・『迎回與新立』・單銀
    for pat in (u'卷欠', u'。；', u'迎回與新立', u'單銀', u'第十六款'):
        c = sum(x.count(pat) for x in out)
        print(u'  覆核｜『%s』今餘 %d%s' % (pat, c, u'' if c == 0 else u'　✗ 未淨'))
        if c:
            return 1
    # 六領域與心所軸之自報數須再合一次（改數之後）
    def lv(s):
        m = re.match(u'^(#+) ', s)
        return len(m.group(1)) if m else 99
    heads = [(i, lv(out[i])) for i in range(len(out)) if re.match(u'^#{3,6} ', out[i])]
    bad = []
    for k, (i, l) in enumerate(heads):
        m = re.search(r'共 (\d+) 案|（(\d+) 案）', out[i])
        if not m:
            continue
        nxt = next((q for (q, ql) in heads[k + 1:] if ql <= l), min(i + 400, len(out)))
        body = u'\n'.join(out[i + 1:nxt])
        u = {int(x) for x in re.findall(r'〔案例\s*0*(\d+)', body)}
        claim = int(m.group(1) or m.group(2))
        if u and claim != len(u):
            bad.append((i + 1, claim, len(u)))
    print(u'覆核｜自報案數對合：%d 項不合%s' % (len(bad), u'' if not bad else u'：%s' % bad[:8]))
    txt = u'\n'.join(out)
    if not apply:
        print(u'———— 乾跑畢（加 apply 方落刀）・行數 %+d・字數 %+d'
              % (len(out) - len(L), len(txt) - len(raw)))
        return 1 if bad else 0
    if bad:
        print(u'———— 自報數未合，擲刀不寫')
        return 1
    bak = os.path.join(WORK, u'r276word2.bak')
    shutil.copyfile(SRC, bak)
    io.open(SRC, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    new = io.open(SRC, encoding=u'utf-8').read()
    print(u'落刀｜備份 %s｜新 %d 行・%d B・sha256 %s' % (
        bak, new.count(u'\n') + 1, len(new.encode(u'utf-8')),
        hashlib.sha256(new.encode(u'utf-8')).hexdigest()[:12]))
    return 0 if new == txt else 2


if __name__ == u'__main__':
    sys.exit(main())
