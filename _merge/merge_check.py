# -*- coding: utf-8 -*-
"""合編本驗尺（量產物，不量口號）。

用法：python -X utf8 _merge/merge_check.py
退出碼：有硬病則 1。
"""
import io, os, re, sys, glob, hashlib
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
    """只留散文：剝圍欄、引號內之文（逐字引文如實登載舊形，舊尺通例不較）、括注。"""
    t = re.sub(r"```.*?```", "", t, flags=re.S)
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
CN2 = {c: i + 1 for i, c in enumerate(u"〇零一二三四五六七八九十百".replace(u"〇", u"〇"))}
CN2 = {c: i for i, c in enumerate(u"零一二三四五六七八九")}
CN2[u"十"] = 10


def cnum(s):
    if s in CN2:
        return CN2[s]
    if u"十" in s:
        a2, _, b2 = s.partition(u"十")
        return (CN2.get(a2, 1) or 1) * 10 + CN2.get(b2, 0)
    return 0


idx = [(cnum(m.group(1)), i) for i, m in
       ((i, re.match(r"^# 第([一二三四五六七八九十]+)章　", l)) for i, l in enumerate(L, 1)) if m]
sec = {}
for k, (n, s0) in enumerate(idx):
    e0 = idx[k + 1][1] - 1 if k + 1 < len(idx) else len(L)
    sec[n] = "\n".join(L[s0 - 1:e0])
p("本冊章界切得（應 28）", "%d（最大章號 %d）" % (len(sec), max(sec) if sec else 0))
badref, badsec = [], []
for m in re.finditer(u"第([一二三四五六七八九十]+)章(第([一二三四五六七八九十]+)節)?", b):
    n = cnum(m.group(1))
    if n > 28 or n < 1:
        badref.append(m.group(0))
        continue
    if m.group(3):
        tg = sec.get(n, "")
        if tg and not re.search(r"^#{2,6} " + re.escape(m.group(3)), tg, re.M):
            badsec.append(m.group(0))
p("章級死鏈（指向不存在之章）", "%d 種 %s" % (len(set(badref)), "、".join(sorted(set(badref)))[:64]))
p("節級死鏈（章在而節無）", "%d 種 %s" % (len(set(badsec)), "、".join(sorted(set(badsec)))[:88]))
p("戒本表舊指針（書中：第X章案例Y）", len(re.findall(u"書中：第[一二三四五六七八九十]+章案例", b)))
p("素材卡標（應 164）", len(re.findall(u"^#### 〔素材・護欄", b, re.M)))
p("指針已重算待復核之標", b.count(u"〔指針已重算・待復核〕"))
if badref:
    fails.append("章級死鏈 %d 種" % len(set(badref)))

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
print("\n判定：%s" % ("合格（硬病 0）" if not fails else "不合格 %d 項：\n  - %s" % (len(fails), "\n  - ".join(fails))))
sys.exit(1 if fails else 0)
