# -*- coding: utf-8 -*-
# 第 213 輪·負測：第 43 軸 `r213case` 須有牙（⓪ 淨本不報・①② 植缺號即報・③ 圍欄從寬・④ 底冊從寬）
import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding=u'utf-8', errors=u'replace')

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
TRY = u'_work/_r213try.md'
src = io.open(MD, encoding=u'utf-8').read()
h0 = hashlib.sha256(src.encode(u'utf-8')).hexdigest()
res = []


def run(tag, text, want_rc):
    io.open(TRY, 'w', encoding=u'utf-8', newline=u'\n').write(text)
    p = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r213case.py', TRY],
                       capture_output=True, text=True, encoding=u'utf-8', errors=u'replace')
    out = (p.stdout or u'') + (p.stderr or u'')
    line = [l for l in out.split(u'\n') if l.startswith(u'==')]
    ok = (p.returncode == want_rc)
    res.append((tag, ok, p.returncode, want_rc, (line[-1] if line else u'')[:64]))
    return out


try:
    run(u'⓪ 淨本（自建基準，須退 0）', src, 0)
    a = src.replace(u'〔遮45〕', u'〔遮46〕')
    assert a != src, u'植①未中：印面無〔遮45〕'
    run(u'① 全族改號致空穴（須退 1）', a, 1)
    b = src.replace(u'〔遺19〕', u'〔遺21〕')
    assert b != src, u'植②未中：印面無〔遺19〕'
    run(u'② 他族空穴（須退 1）', b, 1)
    # ③ 圍欄內植同形超號：須不報（證其界）
    i = src.index(u'\n```text\n')
    c = src[:i + 9] + u'〔遮99〕欄內舉例一枚\n' + src[i + 9:]
    run(u'③ 同形落圍欄（須退 0）', c, 0)
    # ④ 底冊（附錄M 之後）植超號：須不報
    j = src.index(u'# 附錄M')
    d = src[:j] + u'〔開99〕底冊舉例一枚\n\n' + src[j:]
    run(u'④ 同形落底冊（須退 0）', d, 0)
finally:
    if os.path.exists(TRY):
        os.remove(TRY)

bad = 0
for tag, ok, got, want, last in res:
    print(u'  %-30s %s｜rc=%d（須 %d）%s' % (tag, u'中' if ok else u'不中', got, want, last))
    bad += 0 if ok else 1
h1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希 %s（%s）' % (u'如舊' if h0 == h1 else u'已臟！', h0[:12]))
ok = bad == 0 and h0 == h1 and len(res) == 5
print(u'結果斷：%s' % (u'軸有牙、圍欄與底冊從寬、主檔一字未損' if ok else u'負測不合'))
sys.exit(0 if ok else 1)
