# -*- coding: utf-8 -*-
"""合編本驗尺（量產物，不量口號）。

用法：python -X utf8 _merge/merge_check.py
退出碼：有硬病則 1。
"""
import io, os, re, sys, glob, hashlib
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refnum as RN
import chapmap as CM
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = os.path.join(ROOT, "_archive", u"舊本")
BOOK = glob.glob(os.path.join(ROOT, u"合編本_*.md"))
fails, soft = [], []

if not BOOK:
    print("查無合編本（先跑 _merge/merge_build.py）")
    sys.exit(1)
BP = BOOK[0]
b = io.open(BP, encoding="utf-8").read()
L = b.split("\n")
v = io.open(glob.glob(os.path.join(OLD, "ver38*.md"))[0], encoding="utf-8").read()
h = io.open(glob.glob(os.path.join(OLD, u"佛陀的護欄*.txt"))[0], encoding="utf-8").read()


def p(k, x=""):
    print("%-46s %s" % (k, x))


print("=== 1 骨架 ===")
CH = re.findall(r"^# (第[一二三四五六七八九十]+章)　", b, re.M)
p("本冊章題（須 28）", "%d %s" % (len(CH), "" if len(CH) == 28 else "★非 28"))
if len(CH) != 28:
    fails.append("章題 %d≠28" % len(CH))
p("部題（須 7）", len(re.findall(r"^# 【第[一二三四五六七]部", b, re.M)))
if len(re.findall(r"^# 【第[一二三四五六七]部", b, re.M)) != 7:
    fails.append("部題≠7")
p("殘留他冊 H1（須 0）", len(re.findall(r"^# (?:附錄|結語|終卷|第[一二三四五六七八九十]+章 )", b, re.M)))
p("跳級（H1→H4／H1→H5）", sum(1 for i in range(1, len(L)) if re.match(r"^#{4,5} ", L[i]) and re.match(r"^# ", L[i - 1])))

print("\n=== 2 案例：不漏・不兩出 ===")
vc = re.findall(r"^#### (〔(?:遮|開|僧)\d+〕)", b, re.M)
vb = re.findall(r"^#### (〔補遺\d+〕)", b, re.M)
src_v = set(re.findall(r"^#### (〔(?:遮|開|僧|補遺)\d+〕)", v, re.M))
p("框架碼出現（百則／補遺）", "%d／%d（源冊共 %d）" % (len(set(vc)), len(set(vb)), len(src_v)))
lost = src_v - set(vc) - set(vb)
if lost:
    fails.append("佚失框架卡 %d：%s" % (len(lost), "、".join(sorted(lost))[:120]))
p("佚失（須 0）", "、".join(sorted(lost)) or "無")
dup = [c for c in set(vc + vb) if (vc + vb).count(c) > 1]
p("同一碼兩出（須 0）", "、".join(dup) or "無")
if dup:
    fails.append("兩出 %d 碼" % len(dup))
hc = re.findall(r"^#### 〔素材・護欄 (第[一二三四五六七八九十]+章) (案例[一二三四五六七八九十]+)〕", b, re.M)
src_h = []
cur = None
for l in h.split("\n"):
    m = re.match(r"^# (第[一二三四五六七八九十]+章)", l)
    if m:
        cur = m.group(1)
    m2 = re.match(r"^#### (案例[一二三四五六七八九十]+)", l)
    if m2 and cur:
        src_h.append((cur, m2.group(1)))
p("護欄升格卡", "%d／源冊 %d" % (len(set(hc)), len(src_h)))
lostH = [x for x in src_h if tuple(x) not in set(hc)]
p("護欄未升格而佚失（須 0）", "%d %s" % (len(lostH), "、".join("%s%s" % x for x in lostH[:6])))
if lostH:
    fails.append("護欄佚失 %d 案" % len(lostH))

print("\n=== 3 六段式之完缺（護欄升格卡）===")
blocks = re.split(r"^#### ", b, flags=re.M)[1:]
need = [u"##### 事相經過", u"##### 心相照鏡", u"##### 佛陀處斷", u"##### 人間智慧", u"◎原典"]
cnt = {k: 0 for k in need}
n_h = 0
for x in blocks:
    if not x.startswith(u"〔素材・護欄"):
        continue
    n_h += 1
    for k in need:
        if k in x:
            cnt[k] += 1
for k in need:
    p("  有「%s」" % k, "%d／%d" % (cnt[k], n_h))
p("  帶定位行者", "%d／%d" % (sum(1 for x in blocks if x.startswith(u"〔素材・護欄") and u"定位｜根本心" in x), n_h))

print("\n=== 4 未竟之帳（如實計數，不藏）===")
for k, pat in [(u"〔待寫", u"〔待寫"), (u"〔待校", u"〔待校"), (u"〔指針已重算・待復核〕", u"〔指針已重算・待復核〕"),
               (u"〔歸章待裁", u"歸章待裁"), (u"〔未裁", u"〔未裁")]:
    p("  " + k, b.count(pat))

print("\n=== 5 文獻衛生 ===")


def prose(t):
    """只留散文：剝圍欄、引號內之文（逐字引文如實登載舊形，舊尺通例不較）、括注。
    `> ` 行同剝——此即 relink『逐字引文不動』之同一域，兩尺須同一邊界。"""
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = "\n".join(l for l in t.split("\n") if not l.startswith(u"> "))
    for a, c in ((u"「", u"」"), (u"『", u"』"), (u"〔", u"〕"), (u"“", u"”")):
        t = re.sub(re.escape(a) + r"[^" + re.escape(c) + r"]*" + re.escape(c), "", t)
    return t


PR = prose(b)
p("機器絕對路徑（須 0）", len(re.findall(r"[A-Za-z]:[\\/]+Users", b)))
p("本機使用者名（須 0）", len(re.findall(r"lionc", b)))
p("工具字面（_tk|syncchk|bqa|PASS）", len(re.findall(r"_tk|syncchk|bqa|\bPASS\b|回歸測試", b)))
half = re.findall(r"[一-鿿][,.;:!?][一-鿿]", PR)
p("散文內半形標點（須 0；引號內從寬）", len(half))
try:
    sys.path.insert(0, os.path.join(ROOT, "_work"))
    import _simpmap as SM
    bad = re.findall(u"[" + u"".join(sorted(set(SM.MAP))) + u"]", PR)
    p("散文內簡形字（須 0；引號內如實舊形不較）", "%d %s" % (len(bad), "".join(sorted(set(bad)))[:20]))
    if bad:
        fails.append("簡形 %d 枚（%s）" % (len(bad), "".join(sorted(set(bad)))[:12]))
except Exception as e:
    p("簡形尺", "跳過（%s）" % e)
p("旧冊檔名洩入（ver38／佛陀的護欄）", b.count("ver38") + b.count(u"佛陀的護欄"))

print("\n=== 8 死鏈檢（章級・節級・戒本表）===")
sec = RN.chapter_blocks(b)
p("本冊章界切得（應 28）", "%d（最大章號 %d）" % (len(sec), max(sec) if sec else 0))
badref = [m.group(0) for m in RN.REF.finditer(b) if RN.cnum(m.group(2)) not in sec]
untagged = []
dead_list = list(RN.dead_refs(b))
for m, tagged in dead_list:
    if not tagged:
        untagged.append(m.group(0))
        print("   未掛標樣本：%s ｜其後：%s" % (m.group(0), b[m.end():m.end() + 12].replace("\n", "⏎")))
dead, stale = len(dead_list), b.count(RN.TAG) - len(dead_list)
p("章級死鏈（指向不存在之章）", "%d 種 %s" % (len(set(badref)), "、".join(sorted(set(badref)))[:64]))
p("節級死鏈（章在而節無）", "%d 條／%d 種｜其中未掛標 %d（須 0）" % (dead, len({m.group(0) for m, _ in dead_list}), len(untagged)))
p("〔指針待判〕之數（跨冊兩義・候裁）", "%d／殭標 %d（須 0）" % (b.count(RN.TAG), stale))
_kinds = Counter(m.group(0) for m, _ in dead_list)
p("死鏈逐種清單（候裁，×次）", "、".join("%s×%d" % (k, v) for k, v in _kinds.most_common()))
p("戒本表舊指針（書中：第X章案例Y）", len(re.findall(u"書中：第[一二三四五六七八九十]+章案例", b)))
p("素材卡標（應 164）", len(re.findall(u"^#### 〔素材・護欄", b, re.M)))
p("指針已重算待復核之標", b.count(u"〔指針已重算・待復核〕"))
if badref:
    fails.append("章級死鏈 %d 種" % len(set(badref)))
if untagged:
    fails.append("節級死鏈未掛標 %d 條" % len(untagged))
if stale:
    fails.append("〔指針待判〕殭標 %d 枚" % stale)

print("\n=== 6 舊本未動之證 ===")
EXP = {"ver38": "118a5961c090abf2", u"護欄": "a6a289211af5715e"}
for f, k in ((os.path.join(OLD, "ver38四分律_起心動念心智分析框架_修正版.md"), "ver38"),
             (glob.glob(os.path.join(OLD, u"佛陀的護欄*.txt"))[0], u"護欄")):
    s = hashlib.sha256(io.open(f, "rb").read()).hexdigest()[:16]
    ok = s == EXP[k]
    p("  %s" % k, "%s %s" % (s, "同（未動）" if ok else "★異★"))
    if not ok:
        fails.append("%s 舊本被動" % k)

print("\n=== 7 体量 ===")
p("行／漢字", "%d／%d" % (len(L), len(re.findall(r"[一-鿿]", b))))
p("兩本舊本漢字之和", len(re.findall(r"[一-鿿]", v)) + len(re.findall(r"[一-鿿]", h)))
print("\n=== 9 落地・重出（量產物之身，不量卡號有無）===")
# 比對一律先過 `chapmap.skeleton`：指針隨改（舊章號→新章名）不算佚文，改寫值亦不殘形
BSK = {CM.skeleton(l) for l in L if len(l.strip()) >= 12 and len(CM.skeleton(l)) >= 8}
BHEAD = {CM.skeleton(re.sub(r"^#{1,6} ", "", l)) for l in L if re.match(r"^#{1,6} ", l)}
BWIDE = [CM.skeleton(l) for l in L if l.startswith("# ")]
lost = []
for tag, src in ((u"框架", v), (u"護欄", h)):
    for l in src.split("\n"):
        m2 = re.match(r"^#{2,3} (.+)$", l)
        if not m2:
            continue
        k = CM.skeleton(m2.group(1))
        if len(k) < 4 or set(k) <= set("=─│ "):
            continue
        if k not in BHEAD and not any(k in x for x in BWIDE):
            lost.append((tag, m2.group(1).strip()[:26]))
p("源冊 H2～H3 標題未落地（須 0）", "%d %s" % (len(lost), u"｜".join("%s:%s" % z for z in lost[:4])[:76]))
if lost:
    fails.append("標題未落地 %d 目" % len(lost))

miss = 0
PTR = re.compile(u"第[一二三四五六七八九十]+章|第[一二三四五六七八九十]+節|附錄|書中：|案例|卷末|定位行")
for tag, src in ((u"框架", v), (u"護欄", h)):
    ls = src.split("\n")
    br = [i for i, l in enumerate(ls, 1) if re.match(r"^# (?:第[一二三四五六七八九十]+章|結語|終卷|【?第[一二三四五六七八九十]+部|附錄|尾聲)", l)] + [len(ls) + 1]
    for q in range(len(br) - 1):
        paras = [l.strip() for l in ls[br[q] - 1:br[q + 1] - 1] if len(l.strip()) >= 18]
        if len(paras) < 30:
            continue
        gone = [x for x in paras if len(CM.skeleton(x)) >= 8 and CM.skeleton(x) not in BSK]
        bare = [x for x in gone if not PTR.search(x)]
        hit = len([x for x in paras if len(CM.skeleton(x)) >= 8]) - len(gone)
        tot = len([x for x in paras if len(CM.skeleton(x)) >= 8])
        if tot < 20:
            continue
        if hit * 100 < tot * 85:
            print("   料文落地 %2d%%（%d／%d）於【%s・%s】，其缺皆含指針字樣：%s" % (
                hit * 100 // tot, hit, tot, tag, ls[br[q] - 1][2:14],
                "是（隨改，非佚）" if not bare else "★否！有 %d 行無指針而佚" % len(bare)))
            for x in bare[:3]:
                print("      佚｜%s" % x[:64])
        if bare:
            miss += 1
p("無指針而佚之章（須 0）", miss)
if miss:
    fails.append("料文真佚之章 %d 篇" % miss)
rows_old = len([l for l in h.split("\n") if u"書中：" in l])
rows_new = len([l for l in L if u"書中：" in l])
p("戒本歷條總表之指針行（舊 %d／新 %d，須等）" % (rows_old, rows_new), "等・足" if rows_old == rows_new else "★缺 %d 行" % (rows_old - rows_new))
if rows_old != rows_new:
    fails.append("戒本表指針行數不等（舊 %d／新 %d）" % (rows_old, rows_new))

W = 24
seen = {}
for i in range(len(L) - W):
    body = [CM.skeleton(x) for x in L[i:i + W]]
    if sum(1 for x in body if len(x) >= 12) < 6:
        continue
    k = "\n".join(body)
    if k in seen and i - seen[k] > W:
        print("   ★整塊重出：行 %d 與 %d｜%s" % (seen[k] + 1, i + 1, body[1][:40]))
        fails.append("整塊重出 @%d/@%d" % (seen[k] + 1, i + 1))
    seen.setdefault(k, i)
p("整塊重出（24 行窗・相距逾一窗）", "0（未報即無）" if not any("整塊" in f for f in fails) else "見上")

print("\n=== 10 目錄・附錄（目次須由册身生，不可另抄一份）===")
ti = next((i for i, l in enumerate(L) if l.startswith(u"## 【本冊總目錄】")), None)
if ti is None:
    fails.append("缺【本冊總目錄】")
    p("本冊總目錄", "★無")
else:
    t_end = next((i for i in range(ti + 1, len(L)) if L[i].strip() == u"---"), len(L))
    raw = [l for l in L[ti + 1:t_end] if l.lstrip().startswith((u"-", u"**"))]
    tc = [l[2:].strip() for l in raw if l.startswith(u"- ")]
    td = [l.strip().strip(u"*").strip() for l in raw if l.startswith(u"**")]
    ta = [l.strip()[2:].strip() for l in raw if l.startswith(u"  - ")]
    tc = [x for x in tc if not x.startswith(u"附錄")]
    ac = [re.sub(r"^# ", "", l) for l in L if re.match(r"^# 第[一二三四五六七八九十]+章　", l)]
    ad = [re.sub(r"^# ", "", l) for l in L if re.match(r"^# 【第[一二三四五六七八九十]+部：", l)] + \
         [re.sub(r"^# ", "", l) for l in L if l.startswith(u"# 【卷末")]
    aa = [re.sub(r"^## ", "", l) for l in L if re.match(r"^## 附錄[一二三四五六七八九十]+　", l)]
    bare = [l for l in L if re.match(r"^## 附錄[一二三四五六七八九十]+[^　]", l)]
    p("章・目次／册身", "%d／%d　%s" % (len(tc), len(ac),
      "全合" if tc == ac else "★不合：%s" % (set(tc) ^ set(ac))))
    p("部・目次／册身", "%d／%d　%s" % (len(td), len(ad), "全合" if sorted(td) == sorted(ad) else "★不合"))
    p("附錄・目次／册身（須帶題名）", "%d／%d　%s" % (len(ta), len(aa),
      "全合" if sorted(ta) == sorted(aa) else "★不合"))
    p("光板附錄題（只有編號無題名，須 0）", len(bare))
    if tc != ac or sorted(td) != sorted(ad) or sorted(ta) != sorted(aa):
        fails.append("目錄與册身不合")
    if bare:
        fails.append("附錄無題名 %d 篇" % len(bare))
    old = [i for i, l in enumerate(L) if re.match(r"^#{3,4} [^\n]*目錄】$", l) and u"本冊總目錄" not in l]
    unl = [i for i in old if not any(u"〔存檔" in L[j] for j in range(i + 1, min(i + 5, len(L))))]
    p("舊冊自錄之存檔按（應 2／未標須 0）", "%d／%d" % (len(old), len(unl)))
    if unl:
        fails.append("舊冊目錄未標存檔 %d 處" % len(unl))

print("\n判定：%s" % ("合格（硬病 0）" if not fails else "不合格 %d 項：\n  - %s" % (len(fails), "\n  - ".join(fails))))
sys.exit(1 if fails else 0)
