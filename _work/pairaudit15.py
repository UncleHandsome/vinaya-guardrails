# -*- coding: utf-8 -*-
"""第十五波・甲部取證：終審裁決十五案之『今檔實形』一律量出來，不據裁決文之記憶下手。

只讀不寫。逐案印：落點行號・現形・管轄計數。
用法：python -X utf8 _work/pairaudit15.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F1 = os.path.join(ROOT, u"起心動念：四分律的心智顯微鏡與唯識解剖.txt")
F2 = os.path.join(ROOT, u"如法推尋：僧伽憲政、法權審理與修復正義.txt")
V39 = os.path.join(ROOT, u"ver39四分律_起心動念心智分析框架_修正版.md")


def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")


def fence_state(L):
    st, out = False, []
    for l in L:
        if re.match(r"^\s*(```|~~~)", l):
            st = not st
        out.append(st)
    return out


def heads(L):
    return [(i + 1, len(m.group(1)), m.group(2).strip())
            for i, l in enumerate(L) for m in [re.match(r"^(#{1,6})\s+(\S.*)$", l)] if m]


def sect(L, want, upto=None):
    """印出含 want 之標題行及其下至次一同級或更高級標題之範圍。"""
    hs = heads(L)
    for k, (ln, lv, t) in enumerate(hs):
        if want in t:
            nxt = next((l for l, l2, _ in hs[k + 1:] if l2 <= lv), len(L) + 1)
            print("      H%d L%d–L%d（%d 行）・題：%s" % (lv, ln, nxt - 1, nxt - ln, t[:66]))
            if upto:
                return


def census(L, name, terms, fs=None):
    fs = fs or fence_state(L)
    print("   ■ %s（%d 行）" % (name, len(L)))
    for t in terms:
        locs = [(i + 1, fs[i]) for i, l in enumerate(L) if t in l]
        if not locs:
            print("      %-14s 0" % t)
            continue
        body = sum(1 for _, f in locs if not f)
        inf = sum(1 for _, f in locs if f)
        print("      %-14s %d 見（圍欄外 %d／圍欄內 %d）首三：%s"
              % (t, len(locs), body, inf,
                 "、".join("L%s%s" % (n, "〔柵〕" if f else "") for n, f in locs[:3])))


print("=" * 74)
print("壹・甲2① —— F1 第十一章第三節（移轉管轄→第一人稱自救）今形")
A = rd(F1)
hs = heads(A)
ch11 = [(ln, lv, t) for ln, lv, t in hs if t.startswith(u"第十一章")]
print("   章題：%s" % (ch11[0][2][:60] if ch11 else "未得！"))
if ch11:
    c0 = ch11[0][0]
    nxt = next((ln for ln, lv, t in hs if ln > c0 and lv <= (ch11[0][1] or 2)), len(A) + 1)
    sub = [(ln, lv, t) for ln, lv, t in hs if c0 <= ln < nxt and lv == 3]
    print("   章之範圍 L%d–L%d・其下 H3 共 %d 枚：" % (c0, nxt - 1, len(sub)))
    for ln, lv, t in sub:
        print("      L%d  %s" % (ln, t[:70]))
    third = [x for x in sub if x[2].startswith(u"###") or u"第三節" in x[2]]
    if third:
        ln = third[0][0]
        end = next((l for l, l2, _ in hs if l > ln and l2 <= 3), nxt)
        seg = A[ln:end - 1]
        print("   第三節之身 L%d–L%d（%d 行）・漢字 %d"
              % (ln, end - 1, end - ln, sum(len(re.findall(u"[\u4e00-\u9fff]", x)) for x in seg)))
        print("   節文首八行：")
        for x in seg[:8]:
            print("      | " + x[:78])

print("=" * 74)
print("貳・甲2② —— F1 第一章第三節（改題『問心之兩徑』）今形與稱名之抄")
c1 = [(ln, lv, t) for ln, lv, t in hs if t.startswith(u"第一章")]
print("   章題：%s" % c1[0][2][:60])
c0 = c1[0][0]
nxt = next((ln for ln, lv, t in hs if ln > c0 and lv <= 2), len(A) + 1)
for ln, lv, t in [(l, l2, l3) for l, l2, l3 in hs if c0 <= l < nxt and lv == 3]:
    print("      L%d  %s" % (ln, t[:70]))
for w in (u"言詞問", u"證據問", u"問心之兩徑", u"雙軌分流"):
    print("   全冊『%s』%d 見：%s" % (w, sum(1 for l in A if w in l),
                                     "、".join("L%d" % (i + 1) for i, l in enumerate(A) if w in l)[:78]))

print("=" * 74)
print("參・乙3 —— F1 三段式樣待查之落點")
for needle in (u"染污心共染污心男子身相觸", u"分惡房、生瞋恚", u"徇自名利"):
    for i, l in enumerate(A, 1):
        if needle in l:
            print("   L%-5d %s" % (i, l.strip()[:104]))
print("=" * 74)
print("肆・丁2 —— F1『解牛雙案』圍欄之形")
fs = fence_state(A)
op = [i for i, l in enumerate(A) if re.match(r"^\s*```", l)]
for k in range(0, len(op) - 1, 2):
    lo, hi = op[k], op[k + 1]
    body = A[lo + 1:hi]
    if any(u"解牛" in x for x in body) or any(u"發動鏈" in x for x in body):
        w = max((sum(2 if ord(c) > 0x2000 else 1 for c in x) for x in body), default=0)
        print("   柵 #%d｜源 L%d–L%d・行 %d・最大格寬 %d・首行：%s"
              % (k // 2 + 1, lo + 1, hi + 1, len(body), w, body[0][:46] if body else ""))
        for x in body[:6]:
            print("      |" + x[:70])
for i, l in enumerate(A, 1):
    if u"解牛" in l and not fs[i - 1]:
        print("   散文之『解牛』L%d：%s" % (i, l.strip()[:80]))

print("=" * 74)
print("伍・甲3・丁3・戊1 —— F2 今形")
B = rd(F2)
hsb = heads(B)
print("   冊首六行：")
for i, l in enumerate(B[:6], 1):
    print("      L%d|%s" % (i, l[:86]))
for ln, lv, t in hsb:
    if t.startswith(u"第十五章") or t.startswith(u"第十六章") or t.startswith(u"第二十章"):
        print("   H%d L%d  %s" % (lv, ln, t[:70]))
for nm in (u"第十五章", u"第十六章", u"第二十章"):
    hh = [(ln, lv, t) for ln, lv, t in hsb if t.startswith(nm) and lv <= 2]
    if not hh:
        continue
    c0, lv0, _ = hh[0]
    nxt = next((ln for ln, l2, _ in hsb if ln > c0 and l2 <= lv0), len(B) + 1)
    print("   %s 之範圍 L%d–L%d・其下 H3：" % (nm, c0, nxt - 1))
    for ln, l2, t in hsb:
        if c0 <= ln < nxt and l2 == 3:
            print("      L%d  %s" % (ln, t[:62]))
    print("   其下之案卷卡：")
    for ln, l2, t in hsb:
        if c0 <= ln < nxt and u"案卷" in t:
            print("      H%d L%d  %s" % (l2, ln, t[:58]))
for w in (u"制度案卷 104", u"【制度案卷 104】", u"畢陵伽婆蹉受五百守園人"):
    print("   F2『%s』%d 見：%s" % (w, sum(1 for l in B if w in l),
                                    "、".join("L%d" % (i + 1) for i, l in enumerate(B) if w in l)[:110]))
for w in (u"制度案卷 103", u"制度案卷 105"):
    print("   F2『%s』%d 見：%s" % (w, sum(1 for l in B if w in l),
                                   "、".join("L%d" % (i + 1) for i, l in enumerate(B) if w in l)[:110]))
print("   凡例第八律：")
for i, l in enumerate(B, 1):
    if u"八律" in l or u"第八律" in l:
        print("      L%d %s" % (i, l.strip()[:100]))
print("   F1 側對 104・103・105 之引：%s"
      % "、".join("L%d" % (i + 1) for i, l in enumerate(A)
                  if re.search(u"案卷 10[345]|案例 10[345]|案 10[345]", l))[:120])
print("   F2 章名之他抄（十五/十六章題名之前八字見於何處）：")
for probe in (u"分際之護", u"十方僧物不可分割", u"默擯之界", u"淨人作務", u"出坡作務"):
    print("      『%s』F2 %d 見 L%s｜F1 %d 見" % (probe, sum(1 for l in B if probe in l),
            "、".join(str(i + 1) for i, l in enumerate(B) if probe in l)[:60],
            sum(1 for l in A if probe in l)))

print("=" * 74)
print("陸・乙1・乙2 —— 企業專名之計數（兩冊）")
TERMS = [u"董事會", u"監事會", u"三線模型", u"三線", u"非營利組織", u"NPO", u"SOP", u"KPI",
         u"穿透審計", u"穿透名實", u"實質受益人", u"實質受用人", u"內部控制", u"合規",
         u"稽核", u"法人", u"機構化", u"重甲", u"安全閥", u"防火牆", u"護網", u"落日",
         u"減量原則", u"避風港", u"吹哨", u"大眾羯磨院", u"執事會", u"監察長老眾"]
census(A, u"起心動念 F1", TERMS)
census(B, u"如法推尋 F2", TERMS)

print("=" * 74)
print("柒・戊1 —— ver39 工具箱三段之資產實形")
V = rd(V39)
for w in (u"道場治理實操工具箱", u"九則引橋", u"隨身自律行動卡", u"合規自檢表", u"一票否決", u"四署"):
    ls = [i + 1 for i, l in enumerate(V) if w in l]
    print("   ver39『%s』%d 見：%s" % (w, len(ls), "、".join(str(x) for x in ls[:8])))
k = [i for i, l in enumerate(V) if u"道場治理實操工具箱" in l]
if k:
    lo = k[0]
    seg = V[lo:lo + 130]
    print("   自 L%d 起 130 行內之結構：標題 %d・列點 %d・勾選框 %d・漢字 %d"
          % (lo + 1, sum(1 for x in seg if re.match(r"^#{1,6}\s", x)),
             sum(1 for x in seg if re.match(r"^\s*[-*]\s", x)),
             sum(1 for x in seg if u"[ ]" in x or u"[x]" in x),
             sum(len(re.findall(u"[\u4e00-\u9fff]", x)) for x in seg)))
    for x in seg[:26]:
        print("      |" + x[:82])
