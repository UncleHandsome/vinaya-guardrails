# -*- coding: utf-8 -*-
r"""anchpre　印面字面一改即預檢 `pdfspot` 之長駐錨（第 243 輪立，源層工具）。

   所以立之：第 241 輪以 `r165shot` 之外另搭探針搜『（1）被出罪者本人』，報假病；又預檢錨時
   以源檔原文比對，未剝 `**` 粗體記號，遂使『治理方針（斯諍之處遇）』一條假性『未見』。
   今定名長用：**凡改印面字面，先跑本器**（源層即可知錨舊與否，不必等重建）。
   口徑：唯剔底冊四篇；比對前兩邊同剝空白與 markdown 標記（`**` `__` 反引號）——
   因 `pdfspot` 之錨取冊上純字面，而源檔帶記號。NOT 黑名單不在本器之列（彼屬產物層之檢）。
"""
import ast, io, re, sys
sys.path.insert(0, '_work'); sys.path.insert(0, '.')
import _tk as t

tree = ast.parse(io.open(u'_work/pdfspot.py', encoding='utf-8').read())
HAVE = next(ast.literal_eval(nd.value) for nd in tree.body
            if isinstance(nd, ast.Assign) and getattr(nd.targets[0], 'id', '') == u'HAVE')
NL = re.compile(r'\s+')
STRIP = re.compile(r'\*\*|`|__')


def norm(x):
    return STRIP.sub(u'', NL.sub(u'', x))


L = t.LINES
BOT = t.bottom_lines()
TXT = norm(u'\n'.join(L[i] for i in range(len(L)) if i not in BOT))
miss = [(a, sc) for a, sc in HAVE if norm(a) not in TXT]
print(u'HAVE %d 條｜今檔印面查無 %d 條' % (len(HAVE), len(miss)))
for a, sc in miss:
    print(u'   * 未見（scope=%s）：%s' % (sc, a[:56]))
sys.exit(0 if not miss else 1)
