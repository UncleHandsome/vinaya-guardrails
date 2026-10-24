# -*- coding: utf-8 -*-
"""275 輪・通道之兩邊負測：證『試跑通道』真能改讀他檔，且不作偽紅。

三道一器（每尺各跑三遍）：① 不帶參跑正本 → rc=0（基線，歷輪之綠不假）；
                          ② 帶參跑**同一正本** → rc=0（通道不誤傷，讀檔＝讀冊）；
                          ③ 帶參跑**該尺専屬之植病假冊** → rc≠0（通道確讀假冊）。
兩處加嚴（前車：五尺共用一盆病，紅得不知因誰；且『報錯』不等於『點名』）：
  （一）**病各歸尺**——每尺只植它管得著之一枚，紅即此尺之功；
  （二）**點名真答案**——判式不止 rc，須在該尺輸出裡看見其點名之病灶（指針錯靶須報出其真家）。
植病皆以『改一處』為度：核卷尺改卡身引卷之卷次（逐candidates 試至其文實落不合），餘尺各植其句式。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r275chneg.py [-v]
"""
import io
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
if WORK not in sys.path:
    sys.path.insert(0, WORK)                                  # 278・共器 _casedef 之徑
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
NUM = u'(?:[0-9]+|[一二三四五六七八九十]{1,4})'
VOLTok = re.compile(u'卷\\s*\\[?' + NUM + u'\\]?(?:\\s*(?:至|～|-|―)\\s*' + NUM + u')?')
NUM2 = u'[一二三四五六七八九十百0-9]{1,6}'
RNG = re.compile(u'卷\\s*(' + NUM2 + u')\\s*至\\s*(' + NUM2 + u')')
HEADRE = re.compile(u'^>\\s*(?:《[^》]{1,16}》\\s*)?(?:又|兼)?卷')


def run(tool, path=None):
    args = [sys.executable, u'-X', u'utf8', os.path.join(WORK, tool)] + ([path] if path else [])
    q = subprocess.run(args, capture_output=True, text=True, encoding=u'utf-8', env=env, cwd=ROOT)
    return q.returncode, (q.stdout or u''), (q.stderr or u'').strip()[:80]


def card_blocks(L):
    """原典欄之區間（起於該欄下一行，訖於任何標題／分隔線）——278・改走共器 `_casedef.verb_blocks`。
       本器舊抄『#### 【律典原典】』一形，第六章改製後該形存 0 而新形存 14，遂空植而誤報『通道未證』：
       形制一改，負測器自身之錨亦須歸共器（尺之尺亦不免此病）。"""
    import _casedef as CD
    return [(i + 1, j) for i, j, _lab in CD.verb_blocks(L)]


def plant_volchk(base):
    """取前數卡，將其原典欄之引卷一律改成『卷999』（本律僅六十卷，必落在實落之外）；
       以核卷尺點名其不合者為得——紅即此尺之通道已證。"""
    L = base.split(u'\n')
    for a, b in card_blocks(L)[:6]:
        blk = [VOLTok.sub(u'卷999', l) if u'卷' in l else l for l in L[a:b]]
        if blk == L[a:b]:
            continue
        bad = u'\n'.join(L[:a] + blk + L[b:])
        rc, out, err = run(u'v39volchk.py', write_tmp(bad))
        if rc != 0 and u'✗ ' in out:
            return bad, u'✗ '
    raise AssertionError(u'核卷尺之植病不可令紅（通道未證）')



def plant_volrange(base):
    """取書中一根真實之『卷X至Y』宣稱行，改其卷區為他段，試至引卷尺點名『不合』。
       278・錨歸實形：舊只認『^> 《…》卷A至B』＋其下『#### 【律典原典】』之式（卡制），第六章改製後
       該式存 0 而書中另有 16 處作『「文」（卷A至B）』與表列之『卷A至B·篇聚』——空錨即空植，
       報『通道未證』而非『通道已壞』，故此器之錨亦須隨形制而改（負測器同受『諸尺各抄舊形』之戒）。"""
    L = base.split(u'\n')
    idx = [i for i, l in enumerate(L) if RNG.search(l) and (HEADRE.match(l) or u'「' in l)]
    for i in idx[:8]:
        for v in (u'卷五十八至五十九', u'卷三至卷四', u'卷三十一至卷三十二', u'卷五十至卷五十一'):
            bad = u'\n'.join(L[:i] + [RNG.sub(v, L[i], count=1)] + L[i + 1:])
            rc, out, err = run(u'v39volrange.py', write_tmp(bad))
            if rc != 0 and u'不合' in out and u'不合 0' not in out:
                return bad, u'不合'
    raise AssertionError(u'引卷尺之植病不可令紅（通道未證）・候選 %d 行' % len(idx))


TMP = tempfile.mkdtemp(prefix=u'r275chneg_')
_cnt = [0]


def write_tmp(text):
    _cnt[0] += 1
    p = os.path.join(TMP, u'planted_%d.md' % _cnt[0])
    io.open(p, 'w', encoding=u'utf-8').write(text)
    return p


try:
    base = io.open(SRC, encoding=u'utf-8-sig').read()
    plants = [
        (u'v39chk.py', base + u'\n### 〔案例 99〕通道植病之虛卡\n', u'FAIL'),
        (u'v39quote2.py',
         base + u'\n《四分律》卷二十一：「此語必定不存在於語料之中之偽逐字引文」\n', u'✗'),
        (u'v39secref.py',
         base + u'\n又見第五章第四節（受害者修復與極限更生微光），如前所說。\n', u'錯靶'),
    ]
    rows = ([(u'v39volchk.py',) + plant_volchk(base)]
            + [(u'v39volrange.py',) + plant_volrange(base)]
            + [(t, b, w) for t, b, w in plants])
    passed = []
    for tool, badtext, want in rows:
        bad = write_tmp(badtext)
        st = [run(tool), run(tool, SRC)]
        rc3, out3, err3 = run(tool, bad)
        st.append((rc3, out3, err3))
        ok = (st[0][0] == 0 and st[1][0] == 0 and st[2][0] != 0
              and not st[0][2] and not st[1][2] and want in out3)
        passed.append(ok)
        named = [x for x in out3.split(u'\n') if want in x]
        print(u'%-16s %s｜無參 rc=%d・帶參正本 rc=%d・帶參植病 rc=%d｜點名『%s』%s' % (
            tool, u'✓' if ok else u'✗', st[0][0], st[1][0], rc3, want,
            (named[0].strip()[:76] if named else u'（無此行）')))
        if not ok or u'-v' in sys.argv:
            for tag, s in zip((u'無參', u'正本', u'植病'), st):
                tail = s[1].rstrip().split(u'\n')[-1][:80] if s[1] else u''
                print(u'      %s rc=%d｜%s｜err %s' % (tag, s[0], tail, s[2]))
finally:
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)

print(u'———— 通道兩邊負測（逐尺専屬病・並點名）：%d/%d 如所期' % (sum(passed), len(rows)))
sys.exit(0 if all(passed) else 1)

