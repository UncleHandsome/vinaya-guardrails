# -*- coding: utf-8 -*-
"""第七十七輪盤點：工程語彙、卸甲套語、跨章重複、幽靈附錄引用之實分布（只列不改）。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, [f for f in os.listdir(ROOT) if f.startswith('ver38') and f.endswith('.md')][0])
LINES = open(MD, encoding='utf-8').read().split('\n')
sys.path.insert(0, ROOT)
import _tk  # noqa


def sec_rng(name):
    return _tk.sec(name)


RANGES = {}
for nm in [u'卷首'] + [u'第%s章' % c for c in u'一二三四五六七八九'] + [u'結語', u'附錄A', u'附錄K', u'附錄L', u'附錄M']:
    r = sec_rng(nm) if nm != u'卷首' else (0, sec_rng(u'第一章')[0])
    if r:
        RANGES[nm] = r


def where(pat, flags=0):
    out = []
    rx = re.compile(pat, flags)
    for i, l in enumerate(LINES):
        if rx.search(l):
            tag = next((k for k, (a, b) in RANGES.items() if a <= i < b), '?')
            out.append((i + 1, tag, l.strip()[:64]))
    return out


out = []
GROUPS = [
    (u'一、工程語彙（印面須洗）', r'FAIL|腳本|程式檢索|回歸測試|不變量|死鏈|第[六七]輪|隨動|CI|迴歸'),
    (u'二、卸甲套語', r'放下秤砣|手術刀入鞘|出堂洗心|樹下吹風|吃茶|感覺不到內臟|渡河之筏|病好出院|法架自捨|歸家無事|平常吃茶'),
    (u'三、四大禁語（八/九重覆）', r'法尚應捨，你咬住制度程序|你把事情鬧大就是破壞和合|這點金錢分別有何好計較|自己心裡早就沒有慈悲'),
    (u'四、三級心智標籤（凡例/二章重覆）', r'三級心智標籤|Root Engine|Statutory Pivot|Microscopic Texture'),
    (u'五、133 算術自證', r'133|71\s*[+＋]|41\s*單|51\s*[+＋]\s*27'),
    (u'六、調部字頻辨析', r'348|198|152|92|256'),
    (u'七、幽靈附錄引用（slim 落空）', r'見附錄\s*[CDEFHIJ]|附錄\s*[CDEFHIJ][-－0-9]*[　 ]'),
    (u'八、雙重編碼（出站口/閥門/道岔）', r'出站口|出院閥門|四大閥門|道岔'),
]
for title, pat in GROUPS:
    rows = where(pat)
    out.append(u'')
    out.append(u'══ %s：%d 行 ══' % (title, len(rows)))
    for ln, tag, txt in rows[:26]:
        out.append(u'  L%-6d %-6s %s' % (ln, tag, txt))
    if len(rows) > 26:
        out.append(u'  …另有 %d 行' % (len(rows) - 26))
open(os.path.join(HERE, 'survey77.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('survey written lines', len(out))
