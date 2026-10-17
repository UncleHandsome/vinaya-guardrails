# -*- coding: utf-8 -*-
"""一鍵複核（本書附錄 L 所稱「查核器」之總入口）。

    python verify_audit.py            # 不變量 + 引文逐字稽核（第六章／附錄E／附錄F／第六章以外・引用塊／全行）＋章序
    python verify_audit.py check      # 只跑結構不變量
    python verify_audit.py verify     # 只跑引文稽核
    python verify_audit.py order      # 章序（第五章前移）一致性

實作全在 _tk.py（含語料載入、異體字摺疊、刪節號切段、連續子字串比對）；
本檔僅作總入口與彙總統計，輸出寫入 _work/。
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _tk  # noqa: E402

MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'
out = []

if MODE in ('all', 'check'):
    _tk.do_check()
    out.append(open(os.path.join(_tk.WORK, 'check.txt'), encoding='utf-8').read())
if MODE in ('all', 'verify'):
    for scope in ('c6', 'e', 'f', 'bq', 'bqa'):
        try:
            _tk.do_verify(scope)
        except KeyError:
            out.append('（查核器尚無 %s 範圍）' % scope)
        p = os.path.join(_tk.WORK, 'verify_%s.txt' % scope)
        if os.path.exists(p):
            txt = open(p, encoding='utf-8').read().splitlines()
            out.append('\n'.join(l for l in txt if l.startswith(('scope=', '含非逐字', '全逐字'))))
if MODE in ('all', 'order'):
    _tk.do_order()
    out.append(open(os.path.join(_tk.WORK, 'order.txt'), encoding='utf-8').read())

report = '\n'.join(out)
open(os.path.join(_tk.WORK, 'summary.txt'), 'w', encoding='utf-8').write(report)
print(report)
