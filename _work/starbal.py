# -*- coding: utf-8 -*-
"""星號平衡尺：粗體記號 `**` 須成對；落單者會以字面星號洩入印面（verify_hulan 戊2 之『*』族）。
   口徑取「段」不取「行」：跨行之粗體（如連續 `>` 引文行）屬合法，行級數之則多假陽性。
   圍欄 ``` 內不計（那裏是圖，星號屬內容）。
用法：python -X utf8 _work/starbal.py <檔1> [<檔2> …]（預設為書檔）
     他尺可 `from starbal import para_odd` 共用同一定義。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DEFAULT = HP.SRC
FENCE = u"```"
BOLD = re.compile(u"\\*\\*")


def para_odd(lines):
    """回傳 [(起始行號 1 起, 段首 38 字)]：粗體記號數為奇數者。"""
    paras, cur = [], []
    for k, l in enumerate(lines):
        if l.strip() == u"" or l.startswith(FENCE):
            if cur:
                paras.append((k - len(cur) + 1, u"".join(cur)))
                cur = []
            continue
        if l.startswith(u">") and cur and cur[-1].startswith(u">"):
            cur.append(l)
        else:
            if cur:
                paras.append((k - len(cur) + 1, u"".join(cur)))
            cur = [l]
    if cur:
        paras.append((len(lines) - len(cur) + 1, u"".join(cur)))
    return [(a, t[:38]) for a, t in paras if len(BOLD.findall(t)) % 2]


def line_odd(lines):
    bad = []
    for i, l in enumerate(lines, 1):
        if l.startswith(FENCE):
            continue
        if len(BOLD.findall(l)) % 2 or re.sub(u"\\*\\*", u"", re.sub(u"^\\s*[*-]\\s+", u"", l)).count(u"*"):
            bad.append((i, l.strip()[:34], l.strip()[-34:]))
    return bad


for f in ((sys.argv[1:] or [DEFAULT]) if __name__ == "__main__" else []):
    # 本檔亦供 gate_draft 旁入（取 para_odd／line_odd 之同端口徑），故非主檔時絕不碰 argv
    raw = io.open(f, encoding="utf-8", newline="").read()
    L = raw.split(u"\r\n") if u"\r\n" in raw else raw.split(u"\n")
    po, lo = para_odd(L), line_odd(L)
    print(u"%s｜行 %d｜段級不平衡 %d｜行級 %d（行級含跨行粗體之假陽性）" % (
        os.path.basename(f)[:34], len(L), len(po), len(lo)))
    for a, h in po[:10]:
        print(u"  ✗段 L%-5d｜%s" % (a, h))
    for i, h, t in lo[:10]:
        print(u"  ·行 L%-5d｜%s … %s" % (i, h, t))
