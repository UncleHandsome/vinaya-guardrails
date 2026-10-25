# -*- coding: utf-8 -*-
"""285・批三之器改靶：六支器同輪自『補遺』改指『調部深描』（名單勿兩抄之反版：此即其帳）。
以 chr() 構反斜線，免 heredoc 與 JSON 之雙重轉義歧義。"""
import io
import os

BS = chr(92)          # 一個反斜線
D2 = BS + BS          # 檔內實字之兩個反斜線
SM = u'調部深描'
BY = u'補遺'
APPLY = u'--apply' in __import__(u'sys').argv
EDITS = []


def sub(fn, old, new, n=1):
    EDITS.append((fn, old, new, n))


# ── v39chk：六處
V = u'_work/v39chk.py'
sub(V, u"re.finditer(u'\u3014" + BY + u" ?(" + D2 + u"d+)\u3015', F)",
    u"re.finditer(u'\u3014" + SM + u" ?(" + D2 + u"d+)\u3015', F)")
sub(V, u"chk(u'" + BY + u"指針可達'", u"chk(u'深描指針可達'")
sub(V, u"(u'" + BY + u"則數', len(buyi), 15)", u"(u'深描則數', len(buyi), 15)")
sub(V, u"u'^### \u3014(\u6848\u4f8b|" + BY + u") ([0-9]+)\u3015(.*)$'",
    u"u'^### \u3014(\u6848\u4f8b|" + SM + u") ([0-9]+)\u3015(.*)$'")
sub(V, u"u'\u3014(\u6848\u4f8b|" + BY + u") ?([0-9]+)\u3015([\u4e00-\u9fff]{3,14})'",
    u"u'\u3014(\u6848\u4f8b|" + SM + u") ?([0-9]+)\u3015([\u4e00-\u9fff]{3,14})'")
sub(V, u"\u3014(?:\u6848\u4f8b|" + BY + u")", u"\u3014(?:\u6848\u4f8b|" + SM + u")", 3)

# ── v39linchk・v39volchk：各一處
for f in (u'_work/v39linchk.py', u'_work/v39volchk.py'):
    sub(f, u"CARD = re.compile(u'^### \u3014(\u6848\u4f8b|" + BY + u") (" + D2 + u"d+)\u3015')",
        u"CARD = re.compile(u'^### \u3014(\u6848\u4f8b|" + SM + u") (" + D2 + u"d+)\u3015')")

# ── _casedef 之註
sub(u'_work/_casedef.py', BY + u"十五則", SM + u"十五則")

# ── r272teeth：三針
R = u'_work/r272teeth.py'
sub(R, u"u'### \u3014" + BY + u" 44\u3015'", u"u'### \u3014" + SM + u" 15\u3015'")
sub(R, u"repl(L, i, u'44\u3015', u'45\u3015'), u'" + BY + u" 44\u219245（越序）'",
    u"repl(L, i, u'15\u3015', u'16\u3015'), u'深描 15\u219216（越序）'")
sub(R, u"L[i] += u'\u3014" + BY + u"45\u3015'", u"L[i] += u'\u3014" + SM + u"16\u3015'")
sub(R, u"u'加無卡之號指針\u3014" + BY + u"45\u3015'", u"u'加無號之指針\u3014" + SM + u"16\u3015'")
sub(R, u"u'### \u3014" + BY + u" 40\u3015'", u"u'### \u3014" + SM + u" 11\u3015'")
sub(R, u"u'降一則" + BY + u"為四級題（篇內少一則）'", u"u'降一則深描為四級題（篇內少一則）'")

# ── build39：封面之數・號欄不折
B = u'_print/build39.py'
sub(B, u"buyi = len(re.findall(u\"(?m)^### \u3014" + BY + u" " + D2 + u"d+\u3015\", t))",
    u"buyi = len(re.findall(u\"(?m)^### \u3014" + SM + u" " + D2 + u"d+\u3015\", t))")
sub(B, u"(u\"" + BY + u"\", buyi)", u"(u\"深描\", buyi)")
sub(B, u"%d 則" + BY, u"%d 則深描")
sub(B, u"u\"[\u3014](\u906e|\u958b|\u50e7|\u907a|" + BY + u")([0-9]{1,3})[\u3015]\"",
    u"u\"[\u3014](\u906e|\u958b|\u50e7|\u907a|" + BY + u"|\u8abf\u90e8\u6df1\u63cf ?)([0-9]{1,3})[\u3015]\"")

CACHE = {}
ok = True
for fn, old, new, n in EDITS:
    if fn not in CACHE:
        CACHE[fn] = io.open(fn, encoding=u'utf-8').read()
    c = CACHE[fn].count(old)
    flag = u'OK' if c == n else u'!!'
    print(u'%s %-24s 命中 %d（期 %d）｜%s' % (flag, os.path.basename(fn), c, n, old[:44]))
    if c != n:
        ok = False
        continue
    CACHE[fn] = CACHE[fn].replace(old, new, n)
print(u'—— %d 支改錨・%d 檔' % (len(EDITS), len(CACHE)))
if ok and APPLY:
    for fn, txt in CACHE.items():
        io.open(fn, 'w', encoding=u'utf-8', newline=u'\n').write(txt)
    print(u'已寫入')
elif not ok:
    print(u'（有錨非一・未寫檔）')
elif not APPLY:
    print(u'（試跑・未寫檔）')
