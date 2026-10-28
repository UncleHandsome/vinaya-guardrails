# -*- coding: utf-8 -*-
"""去現代法令·大掃除（作者親裁 2026-10-26：「現代法令的部分拿掉，讀者自己判斷就好」）。

對象：《如法推尋》（法制卷）為主；《起心動念》（心法卷）今冊實測法名僅 12 見，只在有命中時才動。

五刀（一律試跑印名，--write 方落盤；落盤前自動備份＋記 SHA）：
  甲・款塊刪：以世俗實定法為骨之節／款（標題命中法名或制度名者），連其下內文整塊削。
  乙・表欄刪：律制↔世俗法之對照表，刪其『世俗法欄』（保留律制欄），表結構重排。
  丙・行內刪：整行即屬法條引用者（依《X法》／向管轄法院／由當地律師／稅務…）。
  丁・標題與章篇題改名：去『法人治理／勞動／信託／合規』之世俗法字眼，改歸律語（層級不動）。
  戊・同級補號：甲級砍出斷號者（第N節／一、／N. 指標M），依存者之序補號；
        補前須自證『刀前本為連續 1..N』——刀前已亂者非本刀之責，不動。

甲級六護（目驗而後護，皆改判『待改寫』交筆，不交刀）：
  護一・骨架：章・篇之題永不刪（二十章之戶口不動）。
  護二・呼吸：章末指針・留白・終卷呈辭・致…：・迴向偈——全書呼吸口，只掛了世俗名。
  護三・律制：標題內含自制法語（默擯・草覆地・戒法・五德…）之塊，乃律制掛世俗名。
  護四・判例：塊內含【現代演繹判例】【制度案卷】【案卷 NN】【案例】者——
        若卡在其下款級，本塊只放行（砍其世俗之款，留其判例之骨肉）；卡即此塊者，護起。
        現01〜現04 乃作者明令保留之法相骨肉。
  護五・過半：一『節』之下擬砍之款已過其款數之半，即併其節護起（砍到過半＝節體皆碎，改由筆治）。
  護六・總綱：母塊為【…】式總綱（卷首凡例・四大動線・終卷…）者，其子不砍——
        刪一则其母自稱之『四大』即虛報，護起待筆改。

用法：python -X utf8 _work/pairdelaw.py            # 試跑
      python -X utf8 _work/pairdelaw.py --write    # 落盤
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "起心動念：四分律的心智顯微鏡與唯識解剖.txt"]

LAW = (r"勞基法|勞動基準法|勞動法|民法|刑法|憲法|信託法|公司法|財團法人法|洗錢防制|宗教事務條例|"
       r"受託人條例|個人資料|個資法|GDPR|勞動契約|僱傭契約|委任契約|資遣費|勞工|雇主|受僱|僱傭")
INST = (r"除斥期間|特留分|假扣押|假處分|搜索票|檢察官|法院|訴訟|起訴|判處|律師|會計師|土地增值稅|"
        r"所得稅|稅務|保險|侵權|名譽權|隱私權|人格權|解僱|考勤|打卡|司法審查|強制法|強行法|實定法")
# 甲級之靶：只認『實定法制度』之字眼；「憲法」「刑法」在本書多為自制之喻（憲法級法理、
# 調部『刑法總論』分類、『罪刑法定』乃未制不犯之律語），故不入甲級靶，只入待改寫報告。
LAW_HEAD = (r"勞基法|勞動基準法|勞動法|勞僱|勞動|僱傭|受僱|勞工|雇主|僱主|資遣費|信託|代持|特留分|"
            r"除斥期間|假扣押|假處分|訴訟|法院|司法審查|土地增值稅|稅務|保險|侵權|名譽權|隱私權|"
            r"法人|合規|合約|契約|董事會|監察人|個資|GDPR|律師|會計師|考勤|打卡|解僱")
SELF_WORD = re.compile(r"憲法級|活著的憲法|罪刑法定|未制戒|二不定法|草覆地|戒法|律制|毘尼|羯磨|"
                       r"波羅夷|僧殘|偷蘭遮|別住|摩那埵|出罪|滅擯|結界|與欲|自言治|布薩|五德|心所|"
                       r"默擯|捨置|僧物|瞻病|說戒|自恣|安居")
CARD = re.compile(r"【現代演繹判例|【制度案卷|【案卷\s|【案例|〔案例\s*[現〇一二三四五六七八九十0-9]")
BREATH_HEAD = re.compile(r"^#{1,6}\s*(【本章章末|【本章留白|【章末|【終卷|【終局|【結行|【出堂|致[^\n]{2,40}：\s*$)")
FRAME_HEAD = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+章[　 ]|第[一二三四五]篇[:：]|【第[一二三四五]篇)")
ZHONGGANG = re.compile(r"^#{1,6}\s*【[^】]+】")
HEAD_LAW = re.compile(r"^#{1,6}\s.*(" + LAW_HEAD + r")")
SEC_HEADING = re.compile(r"^#{3,6}\s")
ANY_HEAD = re.compile(r"^#{1,6}\s")
COL_LAWY = re.compile(r"世俗法|國法|法院|司法|勞動|勞基|法律|信託法|民法|刑法|稅|訴訟|侵權|除斥|特留分")
VINAYA_WORDS = (r"羯磨|毘尼|布薩|自恣|僧殘|波羅夷|偷蘭遮|舍彌|別住|摩那埵|出罪|滅擯|結界|與欲|"
                r"自言治|懺|戒體|律制|僧團|二部僧|舉罪|滅諍|呵責|擯出|依止|白衣|沙門|比丘|"
                r"草覆地|四諍|五德|三時心|心所|意喜|僧伽|如法|清淨|四種僧|七佛|略戒")
LINE_LAW = re.compile(
    r"(?:依|據|循|本於)[^。]{0,14}(?:" + LAW + r")"
    r"|向管轄法院|提起[^。]{0,8}訴訟|聲請[^。]{0,10}(?:假處分|假扣押)|移送[^。]{0,8}(?:檢調|司法)"
    r"|由當地律師|當地律師|會計師|土地增值稅|特留分|除斥期間|資遣費|保險給付|侵權行為|公訴重罪之?通報")
HAS_LAW = re.compile(LAW + r"|" + INST)
HAS_VINAYA = re.compile(VINAYA_WORDS)

_HANMAP = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
           11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七",
           18: "十八", 19: "十九", 20: "二十"}
_HANREV = {v: k for k, v in _HANMAP.items()}

# 丁・改名：只換題面之世俗法字眼，層級（篇=##、章=###）一律保留——印面之階梯歸列印層。
RENAME = [
    (re.compile(r"^#+\s*第四篇[:：]現代道場防禦重甲——法人治理與深水合規\s*$"),
     "第四篇：道場秩序與僧俗邊界——執事任事與常住物權之防線"),
    (re.compile(r"^#+\s*第十三章[　 ]現代三線治理模型（IIA）與雙院分立\s*$"),
     "第十三章　三道防線與二部僧雙院分立"),
    (re.compile(r"^#+\s*第十四章[　 ]調查實務、創傷知情與吹哨人防禦機制\s*$"),
     "第十四章　調查倫理、舉罪五德與告發人護念"),
    (re.compile(r"^#+\s*第十五章[　 ]人事與勞動：出世僧籍、世俗勞僱與數位正命\s*$"),
     "第十五章　分際之護：默擯之界與通訊群組之正命"),
    (re.compile(r"^#+\s*第十六章[　 ]財產、數位與醫療：信託防禦、穿透審計與長照防線\s*$"),
     "第十六章　常住物、數位與瞻病：僧物不可分割與照護防線"),
    (re.compile(r"^#+\s*第二節[　 ]寺產借名代持與信託確權「三軌架構」（深度演繹〔案例 現04〕）\s*$"),
     "第二節　名實之辨：十方僧物不隨世俗名相（深度演繹〔案例 現04〕）"),
]


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def fence_mask(lines):
    inside, mask = False, []
    for l in lines:
        if re.match(r"^\s*```", l):
            mask.append(inside)
            inside = not inside
        else:
            mask.append(inside)
    return mask


def level(s):
    return len(re.match(r"^(#+)", s.strip()).group(1))


def block_end(lines, i, lv):
    j, n = i + 1, len(lines)
    while j < n:
        s = lines[j].strip()
        if ANY_HEAD.match(s) and level(s) <= lv:
            break
        j += 1
    return j


def nearest_head_before(lines, i):
    for k in range(i - 1, -1, -1):
        if ANY_HEAD.match(lines[k].strip()):
            return k
    return None


def upper_level(lines, i, lv):
    """最近之上位標題（層級嚴格低於 lv）；本書 節＝章＝H3，故款級找父用此。"""
    for k in range(i - 1, -1, -1):
        s = lines[k].strip()
        if ANY_HEAD.match(s) and level(s) < lv:
            return k
    return None


RE_ZHANG = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+章[　 ]")


def chapter_of(lines, i):
    """『第N節』之父＝其上最近之『第N章』標題（無則退回最近上位層級）。"""
    for k in range(i - 1, -1, -1):
        s = lines[k].strip()
        if RE_ZHANG.match(s):
            return k
    return upper_level(lines, i, level(lines[i].strip()))


def plan(name, lines):
    n = len(lines)
    marks = [None] * n
    guarded = [False] * n          # 護起之塊（連其下款級）：丙・乙二刀亦不得入
    inm = fence_mask(lines)
    renames, mixed, cand = [], [], []
    blocks_extra = []

    heads = [i for i, l in enumerate(lines) if SEC_HEADING.match(l.strip()) and not inm[i]]
    for i in heads:
        if guarded[i] or marks[i]:
            continue
        l = lines[i].strip()
        if FRAME_HEAD.match(l):                     # 護一
            continue
        if not HEAD_LAW.match(l):
            continue
        lv = level(l)
        j = block_end(lines, i, lv)
        body = "\n".join(lines[i:j])
        par = upper_level(lines, i, lv)
        if BREATH_HEAD.match(l):                    # 護二
            mixed.append((i + 1, "護二・呼吸口→手改", l[:52]))
            for k in range(i, j):
                guarded[k] = True
            continue
        if SELF_WORD.search(l):                     # 護三
            mixed.append((i + 1, "護三・律制掛世俗名→手改", l[:52]))
            for k in range(i, j):
                guarded[k] = True
            continue
        if CARD.search(body):                       # 護四
            sons = [k for k in heads if i < k < j and level(lines[k]) > lv and CARD.search(
                "\n".join(lines[k:block_end(lines, k, level(lines[k]))]))]
            if sons:
                continue                            # 卡在其下款級 → 放行（只砍世俗之款）
            mixed.append((i + 1, "護四・判例卡→手改", l[:52]))
            for k in range(i, j):
                guarded[k] = True
            continue
        if par is not None and ZHONGGANG.match(lines[par].strip()):   # 護六
            mixed.append((i + 1, "護六・總綱之子→手改", l[:52]))
            for k in range(i, j):
                guarded[k] = True
            continue
        cand.append((i, j, lv, l[:44], par))

    # 塊之重出：父塊既已入刀，其下之款不再另記一刀（清冊不 Double count，砍亦只一次）
    outer = [(i, j) for i, j, lv, t, par in cand]
    cand = [c for c in cand if not any(a <= c[0] and c[1] <= b and (a, b) != (c[0], c[1]) for a, b in outer)]

    # 護五・節體之裁：一節之下擬砍之款已過其款數之半，即判此節之骨落在何處——
    #   節內無判例卡 → 世俗法即此節之骨，連其題整節砍（不留碎節）
    #   節內有判例卡 → 骨是判例、殼是世俗法，只砍其款、留其骨肉（現01〜現04 之護）
    RE_JIE = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+節")
    groups = {}
    for item in cand:
        par = item[4]
        if par is None or not RE_JIE.match(lines[par].strip()):
            continue
        groups.setdefault(par, []).append(item)
    whole, keep_sons = [], []
    for par, items in groups.items():
        lv0 = level(lines[par].strip())
        end = block_end(lines, par, lv0)
        total = len([k for k in heads if par < k < end and level(lines[k].strip()) == lv0 + 1])
        if not total or len(items) * 2 <= total:
            continue
        if CARD.search("\n".join(lines[par:end])):
            keep_sons.append((par, items, len(items), total))
        else:
            whole.append((par, end, len(items), total))
    for par, items, nc, total in keep_sons:
        for i0, j0, lv0, t0, _ in items:
            mixed.append((i0 + 1, f"護五・節有判例卡({nc}/{total})→只砍其款", t0))
    for par, end, nc, total in whole:
        blocks_extra.append((par + 1, end, f"節・砍款過半({nc}/{total})整節削｜{lines[par].strip()[:40]}"))
        cand = [c for c in cand if not (par <= c[0] < end)]
        for k in range(par, end):
            if not marks[k]:
                marks[k] = "甲-款塊刪"

    for i, j, lv, t, par in cand:
        for k in range(i, j):
            if not marks[k]:
                marks[k] = "甲-款塊刪"
    blocks = [(i + 1, j, t) for i, j, lv, t, par in cand] + blocks_extra
    blocks.sort()

    # 丙・純法條行之整行刪（圍欄內不動；護起之塊不動；與律制混行者不刪，改入『待改寫』）
    stray = []
    for i, l in enumerate(lines):
        if marks[i] or inm[i] or guarded[i] or not l.strip():
            continue
        if not LINE_LAW.search(l):
            continue
        if HAS_VINAYA.search(l) or SELF_WORD.search(l):
            mixed.append((i + 1, "行・律制與法條混行→待改寫", l.strip()[:52]))
            continue
        marks[i] = "丙-行內法條"
        stray.append((i + 1, l.strip()[:52]))

    # 丁・篇題章題改名（層級保留）
    for i, l in enumerate(lines):
        if marks[i] or inm[i]:
            continue
        s = l.strip()
        for rx, new in RENAME:
            if rx.match(s):
                hs = re.match(r"^(#+)\s*", l).group(1)
                lines[i] = f"{hs} {new}"
                renames.append((i + 1, s[:46], lines[i].strip()[:46]))
                break

    # 乙・對照表之世俗法欄刪除（護起塊內之表不動）
    tables = []
    i = 0
    while i < n:
        if lines[i].strip().startswith("|") and not inm[i] and not guarded[i] and not marks[i]:
            j = i
            while j < n and lines[j].strip().startswith("|") and not marks[j] and not guarded[j]:
                j += 1
            rows = lines[i:j]
            if len(rows) >= 3 and rows[1].strip().startswith("|"):
                head = [c.strip() for c in rows[0].strip().strip("|").split("|")]
                # 欄之判：表頭屬世俗法者除；表頭雖掛『法律』而實述律制算法者（如『具體算法與法律效果』）留。
                lawcols = [k for k, h in enumerate(head)
                           if COL_LAWY.search(h) and not re.search(r"算法|治法|羯磨|戒體|律制|養心", h)]
                keep = [k for k in range(len(head)) if k not in lawcols]
                if lawcols and keep and len(head) >= 3:
                    def cut(row):
                        cells = [c for c in row.strip().strip("|").split("|")]
                        return "| " + " | ".join(c.strip() for c in [cells[k] for k in keep if k < len(cells)]) + " |"
                    for k, r in enumerate(rows):
                        lines[i + k] = cut(r)
                    tables.append((i + 1, len(rows), [head[k] for k in lawcols], [head[k] for k in keep]))
            i = j if j > i else i + 1
        else:
            i += 1

    # 戊・同級補號：甲級砍出斷號者，依存者之序補號。
    #   父之求法因本書形制而異：『第N節』與『第N章』同為 H3，故節之父必得以『第N章』標；
    #   款級（一、／1.）之父取其最近之上位層級（即所屬之節）。
    STYLES = [
        (re.compile(r"^(#+)\s*第([〇一二三四五六七八九十]+)(節[　 ].*)$"), chapter_of),
        (re.compile(r"^(#+)\s*([〇一二三四五六七八九十]+)、(.*)$"),
         lambda ls, k: upper_level(ls, k, level(ls[k].strip()))),
        (re.compile(r"^(#+)\s*(\d+)\.\s*(指標([〇一二三四五六七八九十]+))?(.*)$"),
         lambda ls, k: upper_level(ls, k, level(ls[k].strip()))),
    ]
    relabels = []
    for t_st, (st, parent_fn) in enumerate(STYLES):
        groups, order = {}, []
        for k in range(n):
            s = lines[k].strip()
            if inm[k] or not ANY_HEAD.match(s):
                continue
            m = st.match(s)
            if not m:
                continue
            par = parent_fn(lines, k)
            key = (par, t_st)
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append((k, m, marks[k] is not None))
        for key in order:
            items = groups[key]
            nums = [int(m.group(2)) if m.group(2).isdigit() else _HANREV.get(m.group(2), 0)
                    for k, m, dead in items]
            if 0 in nums or len(set(nums)) != len(nums):
                continue                              # 號不明／重號：非本刀之責，不動
            if nums != list(range(1, len(nums) + 1)):
                continue                              # 刀前已亂：自證連續才補號
            alive = [t for t, (k, m, dead) in enumerate(items, 1) if not dead]
            if alive == list(range(1, len(alive) + 1)):
                continue                              # 刀後本連：無需補
            t = 0
            for k, m, dead in items:
                if dead:
                    continue
                t += 1
                if t_st == 0:
                    new = f"{m.group(1)} 第{_HANMAP[t]}{m.group(3)}"
                elif t_st == 1:
                    new = f"{m.group(1)} {_HANMAP[t]}、{m.group(3)}"
                else:
                    tag = f"指標{_HANMAP[t]}" if m.group(3) else ""
                    new = f"{m.group(1)} {t}. {tag}{m.group(4)}"
                if new != lines[k]:
                    relabels.append((k + 1, lines[k].strip()[:40], new.strip()[:40]))
                    lines[k] = new

    kept = [lines[k] for k in range(n) if not marks[k]]
    CH_ONLY = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+章[　 ]")
    pos = [k for k in range(n) if not marks[k] and CH_ONLY.match(lines[k].strip())]
    empties = []
    for t, start in enumerate(pos):
        end = pos[t + 1] if t + 1 < len(pos) else n
        body = [lines[k].strip() for k in range(start + 1, end)
                if not marks[k] and lines[k].strip()]
        if not any(not x.startswith("#") for x in body):
            empties.append(lines[start].strip()[:28])
    tally = {}
    for m in marks:
        if m:
            tally[m] = tally.get(m, 0) + 1
    return dict(name=name, n=n, marks=marks, blocks=blocks, stray=stray, renames=renames,
                relabels=relabels, tables=tables, tally=tally, kept=kept, mixed=mixed,
                empties=empties, guarded=sum(1 for g in guarded if g), src=lines)


def main():
    write = "--write" in sys.argv
    ledger = []
    for fn in FILES:
        p = ROOT / fn
        raw = p.read_bytes()
        lines = raw.decode("utf-8").split("\r\n")
        orig = list(lines)
        r = plan(fn, lines)
        print("=" * 76)
        print("■", fn)
        print(f"  甲・款塊 {len(r['blocks'])} 塊・{r['tally'].get('甲-款塊刪', 0)} 行")
        for a, b, t in r["blocks"]:
            print(f"      L{a}〜{b}（{b - a} 行）{t}")
        print(f"  乙・對照表去世俗法欄 {len(r['tables'])} 張")
        for a, nr, gone, keep in r["tables"]:
            print(f"      L{a}（{nr} 行）除欄：{gone}｜留：{keep}")
        print(f"  丙・行內法條 {len(r['stray'])} 行")
        for a, t in r["stray"][:14]:
            print(f"      L{a}: {t}")
        print(f"  丁・改名 {len(r['renames'])} 處")
        for a, o, w in r["renames"]:
            print(f"      L{a}: {o}\n            → {w}")
        print(f"  戊・同級補號 {len(r['relabels'])} 處")
        for a, o, w in r["relabels"]:
            print(f"      L{a}: {o} → {w}")
        print(f"  護起 {r['guarded']} 行・待改寫（刀不動，交筆）{len(r['mixed'])} 處")
        for a, w, t in r["mixed"]:
            print(f"      L{a} [{w}] {t}")
        print(f"  空殼之檢：刀後無一字之章 {len(r['empties'])} 個 {r['empties'][:5]}")
        write_this = write and not r["empties"]
        if not any([r["blocks"], r["stray"], r["tables"], r["renames"], r["relabels"]]):
            write_this = False
            print("  無刀（此冊本輪零砍零改）→ 不落盤，免無謂之 SHA 漂移")
        if r["empties"]:
            print("  ★有空殼章 → 本檔不落盤（先補『本章之律制骨』再刀）")
        before = cjk("\n".join(orig))
        after = cjk("\n".join(r["kept"]))
        print(f"  合計：{r['n']} 行 → {len(r['kept'])} 行・漢字 {before:,} → {after:,}（-{before - after:,}）")
        res = sum(len(HAS_LAW.findall(l)) for l in r["kept"])
        print(f"  殘留法名／制度名：{res} 見（刀前 {sum(len(HAS_LAW.findall(l)) for l in orig)} 見）")
        for a, b, t in r["blocks"]:
            ledger.append(f"{fn}\tL{a}-{b}\t甲-款塊\t{t}")
        for a, t in r["stray"]:
            ledger.append(f"{fn}\tL{a}\t丙-行內法條\t{t}")
        for a, nr, gone, keep in r["tables"]:
            ledger.append(f"{fn}\tL{a}\t乙-表欄({nr}行)\t除{gone}｜留{keep}")
        for a, o, w in r["renames"]:
            ledger.append(f"{fn}\tL{a}\t丁-改名\t{o} → {w}")
        for a, o, w in r["relabels"]:
            ledger.append(f"{fn}\tL{a}\t戊-補號\t{o} → {w}")
        for a, wd, t in r["mixed"]:
            ledger.append(f"{fn}\tL{a}\t待改寫\t{wd}｜{t}")
        if write_this:
            bak = ROOT / "_archive" / "備份" / "AI清理前" / (fn + ".pre_delaw")
            bak.write_bytes(raw)
            out = "\r\n".join(r["kept"]).encode("utf-8")
            p.write_bytes(out)
            print(f"  落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(out).hexdigest()[:12]}"
                  f"・{len(out)} B・備份 {bak.relative_to(ROOT)}")
        else:
            print("  （試跑：未落盤）")
    (ROOT / "_work" / "pairdelaw_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"\n刀口清冊 {len(ledger)} 行 → _work/pairdelaw_cuts.txt")


if __name__ == "__main__":
    main()
