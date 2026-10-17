# -*- coding: utf-8 -*-
"""第 120 輪之軸：定稿前最後一批經證候選——逐條親量，不信代理之報。

每筆候選核三事：① 所稱語料檔內是否**真的逐字有這一句**（以查核器同一 `norm` 口徑，
needle 與 haystack 兩側同歸一）；② 該句於**全語料**（本律六檔＋佛經諸檔）見幾處，
可辨「唯此一見」之宣稱；③ 該關鍵詞於**本書主檔**見幾處，以定此乃『書中述其義而無經證』
之缺口，還是早已入檔（早入者列『已備』不重做）。
用法：PYTHONPATH=. python _work/r120chk.py
"""
import glob, io, os, sys
import importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('_tk', os.path.join(ROOT, '_tk.py'))
tk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tk)
norm = tk.norm

BOOK = os.path.join(ROOT, 'ver38四分律_起心動念心智分析框架_修正版.md')
book = io.open(BOOK, encoding='utf-8').read()
CORPUS = sorted(glob.glob(os.path.join(ROOT, u'原文', '*.txt'))) + \
    sorted(glob.glob(os.path.join(ROOT, u'佛經', '**', '*.txt'), recursive=True))
CACHE = [(os.path.basename(p) if not os.path.isdir(os.path.dirname(p))
          else os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p),
          io.open(p, encoding='utf-8-sig').read().split('\n')) for p in CORPUS]
ALLN = u'\x00'.join(norm(u'\n'.join(ls)) for _n, ls in CACHE)
BOOKN = norm(book)

# (號, 檔名, 稱行, 逐字句, 書中關鍵詞)
CAND = [
    (u'A1 法語眾', u'50-60 原文.txt', 1317, u'法語眾我讚歎為尊', u'法語眾'),
    (u'A1b 如法眾', u'50-60 原文.txt', 1317, u'是為如法眾', u'如法眾'),
    (u'A2 有主有主想', u'01-10原文.txt', 320, u'有主有主想，不與取，五錢、若過五錢，波羅夷', u'有主有主想'),
    (u'A3 展轉相諫', u'01-10原文.txt', 782, u'展轉相諫、展轉相教、展轉懺悔', u'展轉相諫'),
    (u'A4 乞不癡毘尼', u'38-49 原文.txt', 1462, u'我今不癡，從僧乞不癡毘尼', u'從僧乞不癡毘尼'),
    (u'A4b 聽與不癡毘尼', u'38-49 原文.txt', 1462, u'聽僧與難提比丘不癡毘尼白四羯磨', u'不癡毘尼'),
    (u'B1 解深密七相', u'5.txt', 43, u'四者、宣說有犯自性故', u'有犯自性'),
    (u'B1b 捨律儀', u'5.txt', 43, u'七者、宣說捨律儀故', u'捨律儀'),
    (u'B2 調伏定義', u'5.txt', 39, u'是名調伏', u'是名調伏'),
    (u'B3 微細誤犯', u'4.txt', 19, u'微細誤犯愚癡', u'誤犯'),
    (u'B4 三十頌心所', u'唯識三十頌.txt', 9, u'此心所遍行', u'遍行'),
    (u'B4b 善心所頌', u'唯識三十頌.txt', 11, u'善謂信慚愧', u'信慚'),
    (u'B5 入行論護心', u'入菩薩行論.txt', 211, u'欲護學處者，策勵當護心', u'欲護學處'),
    (u'B5b 何勞戒其餘', u'入菩薩行論.txt', 228, u'除此護心戒', u'除此護心戒'),
    (u'B6 菩提行經護心', u'菩提行經.txt', 37, u'持戒為護心', u'持戒為護心'),
    (u'B7 勝鬘折伏攝受', u'勝鬘經.txt', 59, u'應折伏者而折伏之', u'應折伏者'),
    (u'B7b 令法久住', u'勝鬘經.txt', 59, u'以折伏攝受故令法久住', u'折伏攝受'),
    (u'B8 煩惱不觸心', u'勝鬘經.txt', 121, u'煩惱不觸心，心不觸煩惱', u'煩惱不觸心'),
    (u'B9 梵網說四眾過', u'梵網經心地戒品下.txt', 60, u'而菩薩反更自說佛法中罪過者', u'說佛法中罪過'),
    (u'B10 梵網不教悔罪', u'梵網經心地戒品下.txt', 100, u'不教悔過者，犯輕垢罪', u'不教悔過'),
    (u'B11 梵網守三寶物', u'梵網經心地戒品下.txt', 186, u'善守三寶物，莫無度用', u'善守三寶物'),
    (u'B12 菩薩地疾疾還淨', u'2.txt', 77, u'設有違犯即應如法疾疾悔除令得還淨', u'疾疾悔除'),
    (u'B12b 應訶不訶', u'2.txt', 73, u'懷染污心而不訶責', u'而不訶責'),
    (u'B12c 犯已還淨', u'1.txt', 10, u'犯已還淨', u'犯已還淨'),
]

print(u'語料檔 %d 個（本律 6＋佛經 %d）' % (len(CACHE), len(CACHE) - 6))
bad = []
for lab, fn, ln, quote, term in CAND:
    files = [(n, ls) for n, ls in CACHE if n.endswith(fn)]
    qn = norm(quote)
    where = [u'%s:%d' % (n, i + 1) for n, ls in files for i, l in enumerate(ls) if qn in norm(l)]
    ncorpus = ALLN.count(qn)
    nbook = BOOKN.count(norm(term))
    tagfile = u'OK' if any(w.endswith(':%d' % ln) for w in where) else u'行號不符'
    ok = bool(where) and ncorpus >= 1
    if not ok:
        bad.append(lab)
    print(u'%-22s %-22s 命中 %-26s 全語料 %2d 見｜書中「%s」%3d 見 [%s]' % (
        lab, fn, (u';'.join(where[:2]) or u'查無'), ncorpus, term, nbook, tagfile))
print(u'==== 查無者：%s ====' % (bad if bad else u'無（悉數逐字有據）'))
