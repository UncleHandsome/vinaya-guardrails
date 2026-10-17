# -*- coding: utf-8 -*-
r"""條號對勘器（第 247 輪立・長用）：外路/附件所舉「第 N 條·X 戒」之宣稱 vs 書中之制。

用法：python -X utf8 _work/numcheck.py [宣稱檔]      （檔缺則讀 stdin 之全文）
法：① 由主檔印面抽「（尼薩耆／僧殘／提舍尼／）波逸提法第 N 條（X 戒）」之自引，
      建 (篇,序)→戒名 之書中-map；
   ② 由宣稱檔抽「#### N. X戒」式之逐條清單，或「· 第N條：X戒」式之表列；
   ③ 逐條判：合（書中同序之戒名與宣稱共有 ≥2 字之片段）／缺（書中未引此序）。
      同名之「異」在本器不單列——合之外即缺，缺者須另核語料（比丘篇九十波逸提在本地六檔不附序號，
      說在第 246 輪之掘）。
第 247 輪之教：片段窗口初設 3–5 字，遂使「飲酒戒」一類兩字戒名虛報為異——**窗口必含二字**。
只讀不寫，exit 0。
"""
import io
import os
import re
import sys

sys.path.insert(0, "_work")
sys.path.insert(0, ".")
import _tk as t

CN = {u"零": 0, u"〇": 0, u"一": 1, u"二": 2, u"三": 3, u"四": 4, u"五": 5, u"六": 6,
      u"七": 7, u"八": 8, u"九": 9, u"十": 10, u"百": 100}
NUM = re.compile(u"(尼薩耆|僧殘|提舍尼|波逸提)[^。\\n]{0,8}?第([一二三四五六七八九十百〇零\\d]{1,3})條")
NAME = re.compile(u"[（(·、，]?([一-鿿]{2,12}?)戒")
HEAD = re.compile(u"^#+\\s*(\\d+)\\.[^一-鿿]*([一-鿿][^\\n]{1,44}?)\\s*$")
INL = re.compile(u"第([一二三四五六七八九十百〇零\\d]{1,3})條[：:]?\\s*[禁不]?([^\\n（）()]{2,26}?)戒")


def c2i(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    tot, cur = 0, 0
    for ch in s:
        v = CN.get(ch)
        if v is None:
            return None
        if v >= 10:
            tot += (cur or 1) * v
            cur = 0
        else:
            cur = v
    return tot + cur


def sigs(name):
    s = re.sub(u"[：:禁不得與於]", u"", name).rstrip(u"戒")
    if len(s) <= 2:
        return [s] if s else []
    return [s[j:j + k] for k in (5, 4, 3) for j in range(0, len(s) - k + 1)]


def book_map():
    L = t.LINES
    BOT = t.bottom_lines()
    m = {}
    for i in range(len(L)):
        if i in BOT:
            continue
        line = L[i]
        for mo in NUM.finditer(line):
            n = c2i(mo.group(2))
            if not n or n > 120:
                continue
            tail = line[mo.end():mo.end() + 26]
            nm = NAME.search(tail)
            if nm:
                m.setdefault((mo.group(1), n), set()).add(nm.group(1))
    return m


def bare(name):
    return re.sub(u"[：:禁不得與於]", u"", name).rstrip(u"戒")


def main(argv):
    inline = "--inline" in argv
    argv = [a for a in argv if not a.startswith("--")]
    src = io.open(argv[0], encoding="utf-8", errors="replace").read() if argv else sys.stdin.read()
    bmap = book_map()
    claims = []
    for line in src.split("\n"):
        h = HEAD.match(line.strip())
        if h:
            claims.append((int(h.group(1)), h.group(2)))
            continue
        if not inline:
            continue
        for mi in INL.finditer(line):
            n = c2i(mi.group(1))
            if n:
                claims.append((n, mi.group(2)))
    ok = miss = 0
    print(u"宣稱 %d 條｜書中-map %d 組 (篇,序)" % (len(claims), len(bmap)))
    print(u"序｜宣稱名｜判定｜書中同序之戒名")
    seen = set()
    for n, name in claims:
        if (n, name) in seen:
            continue
        seen.add((n, name))
        got = []
        for pin in (u"波逸提", u"尼薩耆", u"僧殘", u"提舍尼"):
            got.extend(bmap.get((pin, n), set()))
        sg = sigs(name)
        nb = bare(name)
        hit = [g for g in got if any(s in g for s in sg) or g in nb]
        if hit:
            ok += 1
            v = u"合"
        else:
            miss += 1
            v = u"缺"
        print(u"%3d｜%-30s｜%s｜%s" % (n, name[:28], v, u"、".join(sorted(got))[:46] if got else u"—"))
    print(u"\n合計：合 %d｜缺 %d（缺＝書中未引此序，須另核語料；本地比丘篇九十波逸提不附序號）"
          % (ok, miss))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
