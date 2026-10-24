# -*- coding: utf-8 -*-
"""282・帳：把『長段不可逐字構碼』補入 user 記憶 `feedback-tool-param-unicode-escapes.md`。"""
import hashlib
import io
import os

P = os.path.join(u'C:', u'\\', u'Users', u'lionc', u'.qoder', u'memory',
                 u'feedback-tool-param-unicode-escapes.md')
S = io.open(P, encoding=u'utf-8-sig').read()
ADD = u'''

**第十一度・一段文章不是一次碼位之集合（2026-10-25・戒律分析 ver39 第 282 輪）**：本輪要以廿五對新文重寫第六章矩陣。我先寫成 `\\uXXXX` 之長串（圖避開傳輸層之歸簡），結果 `r282glyph.py` 掃出**簡形七枚＋錯字十數**：『最上大賊』成『最上大贿』、『於大眾中』成『冼大眾中』、『所竊』成『所篡』、『追責』成『追賬』、『誰各』成『抖各』、『同崩』成『同葡』、『皆不成立』成『皆不可徒門』，又有括號失衡之『極刑既起】』。此非傳輸之禍，乃**憑記憶構碼必錯**之禍（第十度已記『夾』與『夺』兩例，本輪把範圍從單字推到整段）。定則：**長段新撰一律直接打字落檔（Write 工具不失形），落檔後以 `_simpdict`∪`_simpmap` 掃簡形、再把全段印出目視**；`chr()`／`\\uXXXX` 只用於『檔中已有此形、須以碼位點名』之單字場合，且須印 `U+%04X` 覆讀。**新建之文與修改既有之文，同須過同一支簡形之尺**——本輪之 `_work/r282sweep.py`（掃任何腳本之簡形，附上下文與枚數，非零即退 1）即為此設，一輪之內逮住自己新打的『经・当・处・书・则・该』六枚。
'''
assert u'第十一度' not in S, u'已記過'
io.open(P, 'a', encoding=u'utf-8').write(ADD)
back = io.open(P, encoding=u'utf-8-sig').read()
print(u'今 %d 行・sha %s・含十一度：%s' % (
    len(back.split(u'\n')), hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12], u'第十一度' in back))
