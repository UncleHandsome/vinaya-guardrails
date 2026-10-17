# -*- coding: utf-8 -*-
"""台帳自算器（第九十二輪奉命解綁，第九十三輪並接管諸帳）。

唯一法源＝第六章定位行；其次為各帳自身之案例枚舉（帳之所由生，即帳之所由算）。
第一遍（定位行所出）：
  一、第七章速查表之「綁定數」欄與「完整案例清單」欄；二、「全書合計」列；
  三、篇別 ╳ 正理矩陣之格數、篇計、總計與單雙三分佈式；四、附錄I-3 八行之「全書 N 則」。
第二遍（枚舉所出）：
  五、第七章『四諍』各類之「共 N 案」；六、第七章『七階』各階案數與『合計 N 支』口徑行；
  七、第二章三十格矩陣『全表 N 處落點』之括注（落點、雙支對照案之名與數、單支案）；
  八、「N 則複統攝」與「（4 則三正理 ＋ 25 則雙正理）」（源出定位行，散見標題與散文五處）。
用法：`python _work/ledger.py` 只報差（試運行）；`--go` 就地重排。
往後改帳之儀：改定位行或清單 → 跑此器 → 跑 `verify_audit.py`。不復手工多處同步。

總表（第七章 100 列）之「根本心／正理對位」兩欄屬本案屬性，仍由人定，
`_tk.py` 以「定位行↔總表一致」一條守之——此非算術帳，故不解。
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

GO = "--go" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDNAME = "ver38四分律_起心動念心智分析框架_修正版.md"
CN = "一二三四五六七八"
ORDER = ["遮%d" % i for i in range(1, 46)] + ["開%d" % i for i in range(1, 26)] \
    + ["僧%d" % i for i in range(1, 31)]
CASE = re.compile(r"〔(遮|開|僧)(\d+)〕")

# ── 法源：第六章定位行 ───────────────────────────────────────────────
s6, e6 = _tk.sec("第六章")
truth, cur = {}, None
for i in range(s6, e6):
    m = _tk.CASE_RE.match(_tk.LINES[i])
    if m:
        cur = m.group(1) + m.group(2)
    p = _tk.POS_RE.match(_tk.LINES[i])
    if p and cur:
        truth[cur] = [CN.index(x) + 1 for x in re.findall(r"正理([一二三四五六七八])", p.group(3))]
assert len(truth) == 100, len(truth)

bind = {k: [] for k in range(1, 9)}
for cid in ORDER:
    for k in truth[cid]:
        bind[k].append(cid)
cnt = {k: len(v) for k, v in bind.items()}
tot = sum(cnt.values())
per_pian, dist = {}, {}
for g in "遮開僧":
    ids = [c for c in ORDER if c.startswith(g)]
    per_pian[g] = {k: sum(1 for c in ids if k in truth[c]) for k in range(1, 9)}
    n1 = sum(1 for c in ids if len(truth[c]) == 1)
    n2 = sum(1 for c in ids if len(truth[c]) == 2)
    n3 = sum(1 for c in ids if len(truth[c]) >= 3)
    dist[g] = (n1, n2, n3, n1 + 2 * n2 + 3 * n3)
single = sum(dist[g][0] for g in "遮開僧")
twon = sum(dist[g][1] for g in "遮開僧")
threen = sum(dist[g][2] for g in "遮開僧")
multi = twon + threen                       # 複統攝則數

# 本器把整串行寫回主檔，故須取 `MAIN_LINES`——`LINES` 今＝主檔＋底冊備檔（第 250 輪底冊另檔），
#   以 `LINES` 寫主檔即把備檔整份倒回書檔，前車之鑑。
lines = list(_tk.MAIN_LINES)
changes = []


def note(msg):
    changes.append(msg)


def cells(l):
    return [x.strip() for x in l.split("|")]


def render(cs):
    return "| " + " | ".join(cs[1:-1]) + " |"


def enum_tokens(i):
    """自第 i 行之下一行起，收集縮排接續行內之案號（含子群分行）。"""
    got, j = [], i + 1
    while j < len(lines):
        b = lines[j]
        if b.startswith("  ") and (CASE.search(b) or b.lstrip().startswith("* **")):
            got += CASE.findall(b)
            j += 1
            continue
        break
    return [g + d for g, d in got]


# ══ 第一遍：定位行所出之帳 ═══════════════════════════════════════════
for i, l in enumerate(lines):
    m = re.match(r"^\|\s*\*\*正理([一二三四五六七八])\*\*<br>", l)
    if m:                                             # 速查表
        k = CN.index(m.group(1)) + 1
        cs = cells(l)
        want_n, want_list = "**%d**" % cnt[k], "".join("〔%s〕" % c for c in bind[k])
        if cs[3] != want_n:
            note("L%d 速查表 正理%s 綁定數 %s→%s" % (i + 1, m.group(1), cs[3], want_n))
            cs[3] = want_n
        if cs[5] != want_list:
            note("L%d 速查表 正理%s 案例清單重算（%d 案）" % (i + 1, m.group(1), cnt[k]))
            cs[5] = want_list
        lines[i] = render(cs)
        continue
    if l.startswith("| **全書合計**"):                  # 合計列
        cs = cells(l)
        for idx, w in ((2, "**%d 判例單元（%d 單＋%d 雙＋%d 三正理）**" % (100, single, twon, threen)),
                       (3, "**%d**" % tot),
                       (4, "**橫、縱、篇別三向可覆核**（索引一致性之檢，非法理定數；"
                           "由定位行自算）")):
            if cs[idx] != w:
                note("L%d 合計列第%d格重算" % (i + 1, idx))
                cs[idx] = w
        lines[i] = render(cs)
        continue
    m = re.match(r"^\|\s*\*\*(遮止篇|開許篇|僧伽篇)（\d+ 案）\*\*\s*\|", l)
    if m:                                              # 篇別矩陣
        g = m.group(1)[0]
        n1, n2, n3, sm = dist[g]
        terms = " ＋ ".join(str(x) for x in (n1, 2 * n2, 3 * n3) if x)
        want = ["**%s（%d 案）**" % (m.group(1), n1 + n2 + n3)] \
            + [str(per_pian[g][k]) for k in range(1, 9)] \
            + ["**%d**" % sm, "%d單 ＋ %d雙 ＋ %d三（%s ＝ %d）" % (n1, n2, n3, terms, sm)]
        if cells(l)[1:-1] != want:
            note("L%d 篇別矩陣 %s 重算" % (i + 1, m.group(1)))
            lines[i] = render([""] + want + [""])
        continue
    if l.startswith("| **全書總計"):                    # 矩陣總計
        want = ["**全書總計（100 案）**"] + ["**%d**" % cnt[k] for k in range(1, 9)] \
            + ["**%d**" % tot, "**三向加總相符：共 %d 處綁定點（由定位行自算）**" % tot]
        if cells(l)[1:-1] != want:
            note("L%d 矩陣總計列重算" % (i + 1))
            lines[i] = render([""] + want + [""])
        continue
    m = re.match(r"^\|\s*\*\*\d+\*\*\s*\|\s*\*\*正理([一二三四五六七八])", l)
    if m:                                              # 附錄I-3
        k = CN.index(m.group(1)) + 1
        new = re.sub(r"全書 \d+ 則判例單元直接綁定", "全書 %d 則判例單元直接綁定" % cnt[k], l)
        if new != l:
            note("L%d 附錄I-3 正理%s 分計→%d" % (i + 1, m.group(1), cnt[k]))
            lines[i] = new
        continue

# ══ 第二遍：枚舉所出之帳 ═════════════════════════════════════════════
runs, floors = [], []          # 四諍之列、七階之列
matrix_cells = []              # 第二章三十格矩陣
for i, l in enumerate(lines):
    m = re.match(r"^\* \*\*([一二三四])、(言諍|覓諍|犯諍|事諍)（", l)
    if m:
        runs.append((i, m.group(1), len(enum_tokens(i))))   # 計「支」不計「案」：一案兩支者兩見
        continue
    m = re.match(r"^\* \*\*第([一二三四五六七])階：(.+?)，(\d+) 案）\*\*[:：]\s*$", l)
    if m:
        toks = enum_tokens(i)
        floors.append((i, m.group(1), len(toks), toks))
        continue
    if re.match(r"^\|\s*\*\*[一二三四五六]、", l) and "領域軸" not in l:
        for c in cells(l)[2:]:
            matrix_cells += [g + d for g, d in CASE.findall(c)]

# 五、四諍
for i, cn2, n in runs:
    new = re.sub(r"共 \d+ 案", "共 %d 案" % n, lines[i], count=1)
    if new != lines[i]:
        note("L%d 四諍 %s 案數→%d" % (i + 1, cn2, n))
        lines[i] = new

# 五之二、四諍子群（每群一行，案數即該行枚舉之支數）
for i, l in enumerate(lines):
    m = re.match(r"^  \* \*\*[^*（]*（[^（）]*?，(\d+) 案）\*\*[:：]", l)
    if not m:
        continue
    toks = [g + d for g, d in CASE.findall(l)]
    if not toks:
        continue
    new = re.sub(r"，\d+ 案）", u"，%d 案）" % len(toks), l, count=1)
    if new != l:
        note("L%d 四諍子群 %s→%d 案" % (i + 1, l[4:16], len(toks)))
        lines[i] = new

# 六、七階
flo_sum = sum(f[2] for f in floors)
allf = [c for f in floors for c in f[3]]
flo_uni = len(set(allf))
for i, cn2, n, _ in floors:
    new = re.sub(r"，\d+ 案）\*\*", "，%d 案）**" % n, lines[i], count=1)
    if new != lines[i]:
        note("L%d 七階 第%s階 案數→%d" % (i + 1, cn2, n))
        lines[i] = new
for i, l in enumerate(lines):
    if "七階計「支」不計「案」" in l and "合計" in l:
        new = re.sub(r"落階者 \d+ 案，加\s*\d*支之重複，七階合計 \d+ 支",
                     "落階者 %d 案，加 %d 支之重複，七階合計 %d 支" % (flo_uni, flo_sum - flo_uni, flo_sum), l)
        if new != l:
            note("L%d 七階口徑行重算（落階 %d／合計 %d）" % (i + 1, flo_uni, flo_sum))
            lines[i] = new

# 七、三十格矩陣落點（雙支案號就地列名，其名與數俱由表內實點自算，不入手寫之帳）
mt = len(matrix_cells)
mu = len(set(matrix_cells))
seen = []
for c in matrix_cells:
    if c not in seen:
        seen.append(c)
dupids = [c for c in seen if matrix_cells.count(c) > 1]
dupcase = len(dupids)
duptxt = "".join("〔%s〕" % c for c in dupids)
for i, l in enumerate(lines):
    if "全表" in l and "處落點" in l:
        new = re.sub(r"全表 \d+ 處落點", "全表 %d 處落點" % mt, l)
        new = re.sub(r"\d+ 則雙支對照案(?:〔[^〕]*〕)*各佔 2 格、餘 \d+ 案各佔 1 格",
                     "%d 則雙支對照案%s各佔 2 格、餘 %d 案各佔 1 格" % (dupcase, duptxt, mu - dupcase), new)
        if new != l:
            note("L%d 三十格矩陣落點重算（%d 處｜覆案 %d｜雙支 %d：%s）" % (i + 1, mt, mu, dupcase, duptxt))
            lines[i] = new
        continue
    if "雙支對照案各佔兩格" in l:          # 精簡本之括注同計，向未隨動（第 226 輪補）
        new = re.sub(r"（\d+ 處落點，雙支對照案各佔兩格）", "（%d 處落點，雙支對照案各佔兩格）" % mt, l)
        if new != l:
            note("L%d 精簡本矩陣落點重算→%d" % (i + 1, mt))
            lines[i] = new

# 八、複統攝則數（源出定位行）
for i, l in enumerate(lines):
    new = re.sub(r"(\d+) 則複統攝", "%d 則複統攝" % multi, l)
    new = re.sub(r"有 \d+ 則案例呈現", "有 %d 則案例呈現" % multi, new)
    new = re.sub(r"（\d+ 則三正理 ＋ \d+ 則雙正理）",
                 "（%d 則三正理 ＋ %d 則雙正理）" % (threen, twon), new)
    if new != l:
        note("L%d 複統攝則數重算→%d" % (i + 1, multi))
        lines[i] = new

def summary():
    return "法源：定位行 100 則｜綁定分計 %s｜總計 %d\n旁帳：四諍 %s｜七階合計 %d（覆案 %d）｜" \
           "矩陣落點 %d（覆案 %d）｜複統攝 %d" % (
               [cnt[k] for k in range(1, 9)], tot,
               [n for _, _, n in runs], flo_sum, flo_uni, mt, mu, multi)


if __name__ == "__main__":
    sys.stdout.write(summary() + "\n")
    sys.stdout.write("差異 %d 處\n" % len(changes))
    for c in changes[:24]:
        sys.stdout.write("  " + c + "\n")
    if GO:
        io.open(os.path.join(ROOT, MDNAME), "w", encoding="utf-8").write("\n".join(lines))
        sys.stdout.write("已寫入\n" if changes else "無差，不需寫入\n")
