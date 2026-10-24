# -*- coding: utf-8 -*-
"""第 253 輪・刀二・刀三：案例事相之文獻精確度與附錄三詞目之補收。

刀二：〔案例 01〕「三度行不淨行」——律文唯云「與故二共行不淨行」，無次數之宣稱
      （語料『三度』0 見、『三道』0 見：外路所建議之「共行三道」亦屬偽託律據，不採）；
      〔案例 02〕補「作瓦屋—佛呵責—敕僧打破」之前置因緣（律有明文），並正「三度被
      樵夫拆薪」為律之「取薪人破其草屋」。
刀三：附錄三辭典補收 29 目——第三十八版 D-2 有而三十九版削去、全書卻數數用之者
      （五種罪名、故作誤作、三時心、淨人守園人、自恣明相、式叉摩那、離處……）。
      定義逕取 D-2 原文（歷輪已覆核），非本輪手撰，免再添無據之說。

用法：python -X utf8 _work/r253terms.py          # dry-run
      python -X utf8 _work/r253terms.py apply
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
V38 = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')

# ── 刀二：事相之文獻精確度 ────────────────────────────────────────
FIXES = [
    (u'遂於林中屏處與前妻三度行不淨行。',
     u'遂於林中屏處，與前妻共行不淨行。'),
    (u'陶師之子檀尼迦比丘於王舍城深山結草庵，三度被樵夫拆薪取去。檀尼迦無處止宿，轉向王室官庫。  ',
     u'陶師之子檀尼迦比丘於王舍城耆闍崛山旁獨處一草屋。入村乞食既返，草屋已為取薪人所破持去。'
     u'檀尼迦自恃本師子舊藝，和泥作全成瓦屋，聚積柴薪牛屎燒之，屋成色赤如火。'
     u'佛從山下遙見，知而故問，以無數方便呵責：「我常無數方便說慈愍眾生，云何癡人自作泥屋，'
     u'聚積柴薪牛屎而燒之？」遂制「自今已去，不得作赤色全成瓦屋，作者突吉羅」，'
     u'並勅諸比丘共往打破。檀尼迦屋破之後無處止宿，遂轉向王室官庫。  '),
]

# ── 刀三：附錄三補目（依類而列，定義取自 D-2）────────────────────
ORDER = [u'僧伽婆尸沙', u'偷蘭遮', u'波逸提', u'尼薩耆波逸提', u'波羅提提舍尼', u'突吉羅',
         u'故作', u'誤作', u'作持', u'止持', u'使作', u'三時心', u'境差／緣差／心差',
         u'境想六句', u'善逝推定', u'三重護念', u'四清淨', u'五如法', u'四瑕疵',
         u'三種舉羯磨', u'憶念毘尼', u'不癡毘尼', u'離處', u'明相', u'自恣',
         u'式叉摩那', u'淨人', u'守園人', u'白衣']


def d2_rows():
    txt = io.open(V38, encoding=u'utf-8').read()
    ms = list(re.finditer(u'(?m)^### (\\S+　.*)$', txt))
    seg = u''
    for i, m in enumerate(ms):
        if m.group(1).startswith(u'D-2'):
            seg = txt[m.start():ms[i + 1].start() if i + 1 < len(ms) else len(txt)]
            break
    out = {}
    for line in seg.split(u'\n'):
        mm = re.match(u'\\|\\s*\\*\\*([^*|]+?)\\*\\*\\s*\\|(.*)$', line.strip())
        if not mm:
            continue
        term = mm.group(1).strip()
        cells = [c.strip() for c in line.strip().strip(u'|').split(u'|')]
        body = cells[1] if len(cells) > 1 else u''
        head = term.split(u'（')[0]
        out[head] = body
    return out


def main():
    apply = u'apply' in sys.argv[1:]
    text = io.open(SRC, encoding=u'utf-8').read()
    lines = text.split(u'\n')
    for old, new in FIXES:
        n = text.count(old)
        if n != 1:
            raise SystemExit(u'刀二錨點命中 %d 次（須恰 1）：%s' % (n, old[:40]))
        text = text.replace(old, new)
    print(u'刀二：事相之改 2 處俱中')

    d2 = d2_rows()
    m3 = re.search(u'(?m)^# 附錄三.*$', text)
    m4 = re.search(u'(?m)^# 附錄四.*$', text)
    a3 = text[m3.start():m4.start()]
    have = [w for w in ORDER if w in a3]
    add = [w for w in ORDER if w not in a3]
    miss_src = [w for w in add if w not in d2]
    if miss_src:
        raise SystemExit(u'D-2 查無此詞目：%s' % miss_src)
    block = [u'*   **%s**：%s' % (w, d2[w]) for w in add]
    # 落點：附錄三「一、」之末條之後（即本篇首個『---』分隔之前）
    idx = None
    for i, l in enumerate(lines):
        if l.startswith(u'# 附錄三'):
            j = next(k for k in range(i, len(lines)) if lines[k].strip() == u'---')
            idx = j
            break
    if idx is None:
        raise SystemExit(u'附錄三落點失锚')
    if lines[idx - 1].strip() == u'':                    # 緊接末條項目之後，不成疏列表
        new_lines = lines[:idx - 1] + block + lines[idx - 1:]
    else:
        new_lines = lines[:idx] + block + [u''] + lines[idx:]
    print(u'刀三：附錄三今有 %d 目｜補入 %d 目｜已有而skip %d 目（%s）'
          % (len(have), len(add), 0, u'、'.join(have[:6])))
    print(u'補目：%s' % u'、'.join(add))
    for b in block[:3]:
        print(u'   %.110s' % b)
    if not apply:
        print(u'（dry-run，未落檔）')
        return
    io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(new_lines))
    print(u'已落檔｜行數 %d → %d' % (len(lines), len(new_lines)))


main()
