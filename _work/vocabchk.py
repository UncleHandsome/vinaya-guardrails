# -*- coding: utf-8 -*-
"""三級心智標籤層級合法性：定位行之『根本心』欄只許用第一級根心，
得複合（加）、對照（對比）、附二級節點、括號內三級深描——越級與未宣告者報出。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT = _tk.ROOT
L1 = {u'貪', u'瞋', u'癡', u'慢', u'清淨', u'無記', u'懈怠', u'判準態', u'總則', u'無'}
L2 = {u'覆', u'慳', u'掉舉', u'悔'}
L3 = {u'嫉', u'憍', u'諂', u'誑', u'恨', u'散亂', u'放逸', u'慈悲', u'無貪', u'明辨',
      u'行捨', u'不害', u'審慮簡擇', u'欲心', u'盜心', u'殺心', u'殺胎心', u'對治', u'戒法未內化',
      u'程序裁量', u'差誤阻卻', u'意志阻卻', u'表業未成', u'名利', u'名位', u'名聞', u'權力貪著',
      u'以群體為盾', u'身現相施壓', u'畏怖錯會', u'嫉', u'創傷出離', u'生理慈悲', u'定力', u'法喜',
      u'發露', u'護法', u'護念', u'嚴拒誘惑', u'欲牽殺機', u'未離欲', u'已離欲', u'信', u'智慧疏離',
      u'智慧明辨', u'利他', u'慈悲護念', u'無我知足', u'應變', u'感恩', u'明辨', u'放逸', u'散亂',
      u'度人未審', u'行持疑懼', u'制度處分', u'貫穿全篇之社會心理學基礎', u'資格不合', u'近癡',
      u'後段自毀犯淫', u'不信', u'無欲心', u'折辱', u'恨'}

L = _tk.LINES
out, bad, n = [], 0, 0
for i, l in enumerate(L):
    if not l.strip().startswith(u'**定位'):
        continue
    m = _tk.POS_RE.match(l.strip())
    if not m:
        continue
    n += 1
    g = m.group(1)
    head = re.split(u'對比', g)[0]
    toks = re.split(u'加', head)
    off = []
    for k, t in enumerate(toks):
        base = re.split(u'（', t)[0].strip()
        if base in L1:
            pass
        elif base in L2 and k > 0:
            pass
        else:
            off.append(base)
        for inner in re.findall(u'（([^）]*)）', t):
            for piece in re.split(u'[，、；/ \u3000]+', inner):
                piece = piece.strip()
                if not piece or len(piece) < 2:
                    continue
                if piece in L3 or re.match(u'^[^（）]*無犯', piece) or u'非' in piece or u'不涉' in piece:
                    continue
                if piece in L1 or piece in L2:
                    continue
                off.append(u'括:' + piece)
    if off:
        bad += 1
        out.append(u'L%d %s ｜未列舉：%s' % (i + 1, g[:44], u'、'.join(off)))
out.insert(0, u'定位行 %d 條；含未宣告標籤者 %d 條' % (n, bad))
io.open(os.path.join(ROOT, u'_work', u'vocab.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(n, bad)
