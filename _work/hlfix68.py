# -*- coding: utf-8 -*-
"""第 68 輪・甲：新第十一章草稿之預修刀（【律制】歸真・十三難之數・指針之正・交付殘跡）＋入冊。
法：草稿先行（逐條命中數斷言）→ 自證兩閘（粗體「」與【律制】須連寫・簡形須零）→ 行錨入冊 →
    CRLF 等式・行數等式・備份・SHA・回讀块體相等。乾跑為預設，--go 始寫檔。
用法：python -X utf8 _work/hlfix68.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import _tk
from _simpdict import MAP as SIMP

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\e3a2d791-db2e-4a47-9101-86925b60e4a3.txt"
BOOK = HP.SRC
BAK = BOOK + ".bak68a"
GO = "--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")

dr_raw = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert dr_raw.count(u"\r") == dr_raw.count(u"\n") == dr_raw.count(u"\r\n"), u"草稿 CRLF 異常"
D = dr_raw.split(u"\r\n")
if D and not D[-1].strip():
    D = D[:-1]
N0 = len(D)
print(u"草稿 %d 行" % N0)


def do(tag, ln, old, new, want=1):
    i = ln - 1
    c = D[i].count(old)
    assert c == want, u"%s｜稿L%d 命中 %d（欲 %d）：%s" % (tag, ln, c, want, old[:26])
    assert old != new, u"%s｜舊新同形" % tag
    D[i] = D[i].replace(old, new)
    print(u"  %s 稿L%-4d ✓×%d" % (tag, ln, want))


def ins_after(anchor, block, tag):
    hits = [i for i, l in enumerate(D) if anchor in l]
    assert len(hits) == 1, u"%s｜錨命中 %d（欲 1）：%s" % (tag, len(hits), anchor[:24])
    D[hits[0] + 1:hits[0] + 1] = block
    print(u"  %s 插 %d 行（錨 L%d 後）" % (tag, len(block), hits[0] + 1))


print(u"\n―― 壹・【律制】與律語之歸真（俱已預驗連寫）――")
do(u"甲1", 235,
   u"「汝不犯邊罪耶？不污比丘尼耶？不賊住耶？……父母聽汝不？不負債不？汝非奴不？年滿二十未？……」",
   u"「自今已去，聽問十三難事然後授具足戒。……汝不犯邊罪？汝不犯比丘尼？汝非賊心入道？汝非壞二道？"
   u"汝非黃門？汝非殺父殺母？汝非殺阿羅漢？汝非破僧？汝不惡心出佛身血？汝非是非人？汝非畜生？汝非有二形耶？」")
do(u"甲3", 366, u"若比丘有病、護身故，聽著一重革屣。", u"聽為護身、護衣、護臥具故，僧伽藍內，聽著一重革屣。")
do(u"甲4", 434, u"若供養我者，應當供養病僧。", u"若有欲供養我者，當供養病人。")
do(u"甲5", 437, u"「若供養我者，應當供養病僧！」", u"「若有欲供養我者，當供養病人！」")
do(u"甲6", 30, u"便已確立了「**處分愈重，正當法律程序愈嚴格**」的法治鐵律",
   u"便已確立了『處分愈重，正當法律程序愈嚴格』的法治鐵律")

print(u"\n―― 貳・數之對合與目次之歸屬――")
do(u"乙1", 15, u"佛陀在律中自列其目，完備之數整整二十：",
   u"佛陀在律中自列其目，律家相傳完備之數整整二十（本地現存律文標名可記者，"
   u"唯受戒、布薩、安居、自恣、皮革、衣、藥、迦絺那衣、房舍、比丘尼諸犍度）：")
do(u"乙2", 40, u"### 二、 深度案例解碼（上篇）",
   u"### 二、 深度案例解碼：四大樞紐與二十八場制度現場")
do(u"乙3", 240,
   u"包含重大倫理重罪（弒父、弒母、弒阿羅漢、破僧、出佛身血）、嚴重破壞僧制者（曾犯根本波羅夷、曾污比丘尼、"
   u"賊住冒充僧人、外道臥底）、非人與生理人格嚴重扭曲者（黃門、二形、畜生變形）。",
   u"律中列問十三事：犯邊罪（犯根本重罪）、犯比丘尼、賊心入道、壞二道、黃門、殺父、殺母、殺阿羅漢、破僧、"
   u"惡心出佛身血、非人、畜生、二形——重大倫理重罪、破壞僧制者、非人與生理人格嚴重扭曲者俱在內。")
do(u"乙4", 241, u"以及重度傳染病與殘障（癩、癰疽、白癬、癲狂）。",
   u"以及重度傳染病與殘障（癩、癰疽、白癩、乾痟、顛狂）。"
   u"（『十六遮』乃律家總目；本地律文但於受戒前逐條列問而不標其數，即上引第二條【律制】。）")

print(u"\n―― 參・指針之正（第107條屬尼部・三十捨墮第6條乃索衣戒）――")
do(u"丙1", 469,
   u"比丘們恪於「沙門衣物不得隨意施與在家人（三十捨墮第6條、單提第107條持沙門衣與白衣戒）」的死板清規",
   u"比丘們恪於「沙門衣物不得隨意施與在家人」的死板清規（尼部有明文：**「若比丘尼持沙門衣施與外道白衣者，"
   u"波逸提。」**——第十四章案例二十；比丘部律文則但制一「借」字）")
do(u"丙2", 471, u"【衝突戒相：捨墮第6條、單提第107條】",
   u"【衝突戒相：尼單提第107條（持沙門衣施與外道白衣）】")

print(u"\n―― 肆・補條（插行一律放在全部原位刀之後，免行號漂移）――")
ins_after(u"聽問十三難事然後授具足戒",
          [u"> **【律制】：** 「年滿二十不？衣鉢具足不？父母聽汝不？汝非負債人不？汝非奴不？汝非官人不？"
           u"汝是丈夫不？丈夫有如是病：癩、癰疽、白癩、乾痟、顛狂。」"], u"丁1")

print(u"\n―― 伍・自證兩閘（寫檔前必過）――")
txt = u"\r\n".join(D)
bad = []
for i, l in enumerate(D):
    cands = [m.group(1) or m.group(2) for m in PAT1.finditer(l)]
    if l.startswith(u"> 【") or (l.startswith(u">") and u"律制" in l[:16]):
        cands += [m.group(1) for m in re.finditer(u"「([^「」]+?)」", l)]
    for s in cands:
        s = s.strip()
        for frag in re.split(u"……|…", s):
            nb = _tk.norm(PUNC.sub(u"", frag))
            if len(nb) >= 4 and nb not in _tk.VINAYA:
                bad.append((i + 1, frag[:46]))
print(u"  款①＋【律制】之連寫：無據 %d 枚" % len(bad))
for i, f in bad:
    print(u"    × 稿L%-4d %s" % (i, f))
assert not bad, u"逐字閘未過"
CORPF = set(_tk.VINAYA)
spans = [m.span() for m in re.finditer(u"「[^」]*」", txt)]
inq = lambda x: any(a <= x < b for a, b in spans)
simp = []
for ch, tr in SIMP.items():
    for m in re.finditer(re.escape(ch), txt):
        if ch in CORPF and inq(m.start()):
            continue
        simp.append((ch, txt[:m.start()].count(u"\r\n") + 1))
print(u"  簡形（緊口徑・引號內豁免）：%d 枚" % len(simp))
assert not simp, u"簡形殘留：%s" % simp[:6]
assert u"・" not in txt, u"稿內有 U+30FB『・』"
NCASE = sum(1 for l in D if l.startswith(u"#### 案例"))
NLAY = sum(1 for l in D if re.match(u"^### 【第", l))
NFEN = sum(1 for l in D if l.startswith(u"```"))
assert NCASE == 28 and NLAY == 4 and NFEN == 0, u"案例 %d・中間層 %d・圍欄 %d" % (NCASE, NLAY, NFEN)
print(u"  形制：案例 %d 則・中間層 %d・圍欄 %d 段・行數 %d→%d" % (NCASE, NLAY, NFEN // 2, N0, len(D)))
print(u"  歸真之新形（目視覆讀）：")
for anchor in [u"聽問十三難事", u"年滿二十不？衣鉢具足不", u"聽為護身、護衣、護臥具故",
               u"若有欲供養我者", u"第十四章案例二十", u"二十八場制度現場", u"律家相傳完備之數"]:
    for i, l in enumerate(D):
        if anchor in l:
            print(u"    稿L%-4d %s" % (i + 1, l[:168]))

if not GO:
    print(u"\n（乾跑：加 --go 始入冊）")
    sys.exit(0)

print(u"\n―― 伍・入冊（取代舊第十一章）――")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"正本入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
i11 = next(i for i, l in enumerate(L) if l == u"# 第十一章 犍度精要")
i12 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十二章"))
assert L[i11 - 1] == u"" and L[i11 - 2] == u"---", u"上章界非『---＋空行』"
assert L[i12 - 1] == u"" and L[i12 - 2] == u"---", u"下章界非『---＋空行』"
blk = D[2:] + [u"", u"---"]
NEWL = L[:i11] + blk + L[i12 - 1:]
print(u"  舊章 %d 行 → 新章 %d 行｜全書 %d → %d 行" % (i12 - 1 - i11, len(blk), len(L), len(NEWL)))
out = u"\r\n".join(NEWL)
assert out.count(u"\r") == out.count(u"\n") == len(NEWL) - 1, u"CRLF 變形"
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(out.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == out, u"回讀不符"
back = chk.split(u"\r\n")
j = next(i for i, l in enumerate(back) if l == u"# 第十一章 犍度精要")
assert back[j:j + len(blk)] == blk, u"回讀块體不等"
print(u"  已寫檔｜sha %s→%s｜備份 %s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                                        os.path.basename(BAK)))
print(u"  全書 %d 行｜案例 %d 則｜圍欄 %d 段" % (
    len(back), sum(1 for l in back if re.match(u"^#### (?:★ )?案例", l)),
    sum(1 for l in back if l == u"```") // 2))
