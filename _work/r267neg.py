# -*- coding: utf-8 -*-
"""267 輪・負測：三道植病，分證第 28 目（無號形制）與第 27 目之兩處新網眼（卷首・帶空格）。

判式（各道須同時滿足）：退碼 1・該目行現 FAIL・明细行（✗）點名被植之處・stderr 空。
還原之道須退 0（本檔另以正本為第四道對照，證『非因崩而紅』亦『非因植而盲』）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r267neg.py
"""
import io
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_neg267.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')

# 三道：(名, 錨, 植入, 須點名之關鍵, 該目名之前綴)
CASES = [
    (u'植無號形制（第 28 目）',
     u'〔案例98〕泉水停供反被舉、〔案例38〕', u'〔案例·泉水停供〕、〔案例38〕', u'〔案例·', u'案例指針必帶號'),
    (u'植卷首無空格之誤號（第 27 目・卷首已入網）',
     u'〔案例66〕觀聽伎樂反被看、〔案例87〕', u'〔案例01〕觀聽伎樂反被看、〔案例87〕', u'觀聽伎樂', u'案號與案名對合'),
    (u'植卷首帶空格之誤號（第 27 目・空格已入網）',
     u'〔案例95〕親洗病僧屎尿、〔案例06〕', u'〔案例 07〕親洗病僧屎尿、〔案例06〕', u'親洗病僧', u'案號與案名對合'),
]

base = io.open(SRC, encoding=u'utf-8').read()


def run(path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, path],
                       capture_output=True, text=True, encoding=u'utf-8')
    lines = (r.stdout or u'').split(u'\n')
    return (r.returncode,
            [x for x in lines if u'FAIL' in x],
            [x for x in lines if x.strip().startswith(u'\u2717')],
            (r.stderr or u'').strip(),
            [x for x in lines if u'不變量' in x])


allok = True
for tag, old, new, key, item in CASES:
    assert base.count(old) == 1, u'%s：錨命中 %d（須恰 1，不得空跑）' % (tag, base.count(old))
    assert base.count(new) == 0, u'%s：植入形已存在，錨選錯' % tag
    shutil.copyfile(SRC, TMP)
    try:
        txt = io.open(TMP, encoding=u'utf-8').read()          # 先讀入再寫：開檔即截檔之坑（266 補）
        planted = txt.replace(old, new, 1)
        assert planted.count(new) == 1 and planted.count(old) == 0, u'%s：植入未生效' % tag
        io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(planted)
        rc, fails, det, err, tally = run(TMP)
        named = [x for x in det if key in x]
        hit = [x for x in fails if item in x]
        ok = rc == 1 and hit and named and not err
        allok = allok and ok
        print(u'%-34s rc=%d・該目 FAIL=%d・點名=%d・stderr=%r  ➔ %s'
              % (tag, rc, len(hit), len(named), err[:40], u'逮' if ok else u'不逮'))
        for x in (hit + named)[:2]:
            print(u'      ', x.strip()[:108])
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

rc, fails, det, err, tally = run(SRC)
ok0 = rc == 0 and not fails and not err
allok = allok and ok0
print(u'正本對照：rc=%d・FAIL=%d・stderr=%r｜%s' % (rc, len(fails), err[:40],
      (tally[-1].strip()[:46] if tally else u'')))
print(u'———— 總判：%s（四道俱須如式，缺一即視該軸未證）' % (u'全逮' if allok else u'有未逮'))
sys.exit(0 if allok else 1)
