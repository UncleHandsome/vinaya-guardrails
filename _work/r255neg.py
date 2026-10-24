# -*- coding: utf-8 -*-
"""第 255 輪・負測：造七處假病入副本，驗 v39chk 七把尺俱能逮（空轉之尺即無尺）。"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
NEG = os.path.join(ROOT, u'_work', u'_neg39.md')

t = io.open(SRC, encoding=u'utf-8').read()
lines = t.split(u'\n')
ORIG = list(lines)

# 甲・抽掉一枚卡題（連貫尺）
i = next(k for k, l in enumerate(lines) if l.startswith(u'### 〔案例 50〕'))
lines[i] = u'<<<NEG: 卡題已抽>>>'
# 乙・死指針
lines[i + 2] += u'　另參〔案例 130〕、〔補遺 99〕。'
# 丙・孤括號
j = next(k for k, l in enumerate(lines) if l.startswith(u'# 第一章'))
lines[j + 2] += u'（此處故意不閉'
# 丁・簡形入印面（以 chr() 構造，避傳遞層歸簡／鏡射之扰）
k = next(q for q, l in enumerate(lines) if l.startswith(u'# 第二章'))
lines[k + 2] += u'　' + chr(0x603B) + u'部' + chr(0x8BAE) + u'事須' + chr(0x603B) + u'共議。'
# 戊・自報之數謊稱
m = re.search(u'102 個判例單元', u'\n'.join(lines))
assert m
lines = [l.replace(u'102 個判例單元', u'105 個判例單元') for l in lines]
# 己・分批提示殘留
lines[k + 3] += u'　下回預告：三、四軸俱校。'
# 庚・分隔線前無空行
p = next(q for q, l in enumerate(lines) if l.strip() == u'---' and q > j)
lines[p - 1] = lines[p - 1] + u'（貼線之句）'
# 辛・舊帳案號
lines[k + 4] += u'　舊帳〔遮12〕之指針未改。'
# 壬・星號不pairs / 癸・空殼括號
lines[k + 5] += u'　此處**粗體未閉。'
lines[k + 6] += u'　引證空殼（）在此。'
# 子・圍欄內之 markdown 記號
fa = next(q for q, l in enumerate(lines)
          if l.strip().startswith(u'```') and q > j)
lines[fa + 1] += u'　圍欄內 **粗體** 記號。'
# 丑・行末一枚空格
lines[k + 7] = lines[k + 7].rstrip() + u' '
# 寅・標題行末帶句讀
h = next(q for q, l in enumerate(lines) if l.startswith(u'#### ') and q > k)
lines[h] += u'。'
# 卯・目錄指空
tc = next(q for q, l in enumerate(lines) if re.match(u'^\\s+\\* ', l) and q < j)
lines[tc] += u'〇〇決無此題〇〇'
# 辰・標題懸空
lines.insert(h + 1, u'#### 空頭之四級題')
# 巳・節級死指針
lines[k + 8] += u'　說詳第三章第九節。'
# 午・補遺缺枚（並帶篇題之數失相符）
bw = next(q for q, l in enumerate(lines) if l.startswith(u'### 〔補遺 41〕'))
lines[bw] = u'<<<NEG: 補遺 41 之題已抽>>>'
# 戌・檔名式引卷　亥・律意與掛引號相雜
lines[k + 11] += u'　引卷作' + u'01-10' + u'\u5377\u6bb5\u3002'
lines[k + 12] += u'　' + chr(0x5F8B) + chr(0x610F) + chr(0xFF1A) + chr(0x300C) + chr(0x67d0) + chr(0x53e5) + chr(0x300D) + u'\u3002'
# 申・組字碼入印面（以 chr 構造方括號，避 shell 之患）
lines[k + 9] += u'　' + chr(0x5F7C) + u'名作' + chr(0x5B) + chr(0x6728) + chr(0x2A) + chr(0x5948) + chr(0x5D) + u'字。'
# 酉・落單之 『
lines[k + 10] += u'　此處落單' + chr(0x300E) + u'之引。'

# 附・附錄四缺行（驗『一卡一行』）　戒・附錄四掛假引號（驗 v39apx4chk 之逐字面）
row4 = next(q for q, l in enumerate(lines) if l.startswith(u'|') and u'〔案例' in l)
del lines[row4]
row4b = next(q for q, l in enumerate(lines)
             if l.startswith(u'|') and u'〔案例' in l and u'\u300c' in l)
lines[row4b] = lines[row4b].replace(
    u'\u300c', u'\u300c' + chr(0x67d0) + chr(0x53e5) + chr(0x5fc5) + chr(0x4e0d) + chr(0x898b) +
    chr(0x65bc) + chr(0x539f) + chr(0x5178) + chr(0xff02), 1)

io.open(NEG, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
env = dict(os.environ, PYTHONIOENCODING=u'utf-8', TKSRC=NEG)
r = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_work', u'v39chk.py'), NEG],
                   capture_output=True, text=True, encoding=u'utf-8', env=env)
print(r.stdout)
print(r.stderr.strip()[:300])
print(u'———— v39chk 負測退碼 rc=%d（須為 1）' % r.returncode)
fails = [ln for ln in r.stdout.split(u'\n') if u'FAIL' in ln]
print(u'———— 逮得 %d 把尺：%s' % (len(fails), u'・'.join(f.split()[0] for f in fails)))
r2 = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_work', u'v39apx4chk.py')],
                    capture_output=True, text=True, encoding=u'utf-8', env=env)
print(u'———— v39apx4chk 負測退碼 rc=%d（須為 1）' % r2.returncode)
print(u'\n'.join([ln for ln in (r2.stdout or u'').split(u'\n')
                  if u'✘' in ln or u'⚠' in ln or u'————' in ln][:6]))
os.remove(NEG)
# ── 第 263 輪・獨立負測：一枚『舊窄名單之外』之簡形（让＝U+8BA9），驗廣名單確能逮
l2 = list(ORIG)
q2 = next(x for x, s in enumerate(l2) if s.startswith(u'# 第二章'))
l2[q2 + 2] = l2[q2 + 2].rstrip() + u'　退' + chr(0x8BA9) + u'一步之例。'
NEG2 = os.path.join(ROOT, u'_work', u'_neg39b.md')
io.open(NEG2, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(l2))
env2 = dict(os.environ, PYTHONIOENCODING=u'utf-8', TKSRC=NEG2)
r3 = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_work', u'v39chk.py'), NEG2],
                    capture_output=True, text=True, encoding=u'utf-8', env=env2)
f3 = [ln for ln in r3.stdout.split(u'\n') if u'FAIL' in ln]
print(u'———— 廣名單獨立負測（只植一枚「让」）：rc=%d（須 1）・逮得：%s' % (
    r3.returncode, u'・'.join(x.split()[0] for x in f3) or u'（無！尺空轉）'))
os.remove(NEG2)
sys.exit(0 if (r.returncode == 1 and r2.returncode == 1 and len(fails) >= 24
               and r3.returncode == 1 and len(f3) == 1) else 1)
