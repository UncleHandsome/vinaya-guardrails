# -*- coding: utf-8 -*-
"""第十五波・F2 之刀（乙1・乙2・甲3 之邊界收尾）。

乙1：第四篇（及卷首・五篇之引）之企業專名，依裁決算名替換：
      董事會／監事會／IIA 三線模型／非營利組織／SOP／KPI／穿透審計／實質受益人；
      准留之系統通喻（安全閥・防火牆・護網・落日原則・減量原則・避風港）不動。
乙2：款級（H4）標題依同一尺度同步。
形制：遷卡所遺之章界（「***」乃章盡之標）歸位——移於第十六章之前。

三道閘：唯一錨・簡形・式樣不增（改行內「…」之數不得多於改前）。
圍欄內之行須**保格寬**（缺寬之補償入本行最長之空白段），故改字必等寬或以 pad 補齊。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp                                       # noqa: E402

BOOK = next(os.path.join(ROOT, x) for x in os.listdir(ROOT)
            if x.startswith(u"如法推尋") and x.endswith(u".txt"))
BK = os.path.join(ROOT, "_archive", u"備份", u"AI清理前", os.path.basename(BOOK) + ".pre_a15c")
LF, CRLF = chr(10), chr(13) + chr(10)
BOX = (chr(0x2502), chr(0x2500), chr(0x250c), chr(0x2510), chr(0x251c), chr(0x2514),
       chr(0x2518), chr(0x2524), chr(0x252c), chr(0x2534))          # │─┌┐├└┘┤┬┴
SP = chr(0x25cf)


def dw(s):
    return sum(2 if ord(c) > 0x2000 else 1 for c in s)


def raw():
    return io.open(BOOK, "rb").read().decode("utf-8-sig")


def fence_flags(L):
    st, out = False, []
    for l in L:
        if re.match(r"^\s*(```|~~~)", l):
            st = not st
        out.append(st)
    return out


def keep_width(old, new):
    """改後須與改前同格寬：差數補入最長之空白段（格內之齊，分毫不可移）。"""
    d = dw(old) - dw(new)
    if d == 0:
        return new
    runs = [(m.start(), len(m.group(0))) for m in re.finditer(r" +", new)]
    if not runs:
        raise SystemExit(u"保格寬失敗（行內無空白可補）：%s" % new[:44])
    s0, ln = max(runs, key=lambda x: x[1])
    if ln + d < 1:
        raise SystemExit(u"保格寬失敗（可補之空白不足 %d 格）：%s" % (d, new[:44]))
    return new[:s0] + u" " * (ln + d) + new[s0 + ln:]


EDITS = [
    # (tag, old_substring, new_substring, 是否圍欄內保寬)
    (u"乙1·非營利(卷首結界)", u"異地會議已為非營利組織與跨國機構之常態",
     u"異地會議已為今世會眾團體與跨國機構之常態", False),
    (u"乙1·三線(第四篇提撕)", u"我們引進現代組織之三線模型",
     u"我們引進今世組織三級分權之說", False),
    (u"乙1·免設之目", u"（董事會、監事會、專職稽核、專職人資皆免設）",
     u"（執事會、監察長老眾、專職稽核、專職庶務皆免設）", False),
    (u"乙1·同構之宣",
     u"這套源自佛陀親制的「三重護念」，與國際內部稽核師協會發布的全球組織風控標準——**「三線模型」**，在系統控制論上呈現出完美的同構對位。",
     u"這套源自佛陀親制的「三重護念」，與今世組織風控所立之三級分權之說，"
     u"在系統控制論上呈現出完美的同構對位。", False),
    (u"乙1·柵左欄題", u"【現代三線模型", u"【世俗三級分權", True),
    (u"乙1·柵三線目", u"│ 第三線：獨立保證與治理（獨立審計）",
     u"│ 第三級：獨立保證與治理（獨立覆審）", True),
    (u"乙1·柵一線目", u"│ 第一線：操作層控制（業務自律）",
     u"│ 第一級：操作層控制（業務自律）", True),
    (u"乙1·柵二線目", u"│ 第二線：管理層監督（合規風控）",
     u"│ 第二級：執事眾監督（護念風控）", True),
    (u"乙1·柵董事行", u"│ 董事會、監事會、外部獨立審計、覆議",
     u"│ 執事會、監察長老、外部覆審、覆議", True),
    (u"乙2·款一題", u"#### 一、三線治理同構對位深度解剖",
     u"#### 一、三重護念同構對位深度解剖", False),
    (u"乙1·表頭", u"| 治理層級 | 現代 IIA 三線模型 |", u"| 治理層級 | 世俗三級分權之說 |", False),
    (u"乙1·表一線", u"| **第一線**<br>（操作自律） | **業務單位第一線控制**<br>",
     u"| **第一級**<br>（操作自律） | **業務單位初級控制**<br>", False),
    (u"乙1·表二線", u"| **第二線**<br>（管理監督） | **風險管理與法規遵循**<br>",
     u"| **第二級**<br>（管理監督） | **風險管理與規諫遵循**<br>", False),
    (u"乙1·表三線", u"| **第三線**<br>（獨立保證） | **獨立內部稽核與治理體**<br>",
     u"| **第三級**<br>（獨立保證） | **外部客僧覆審之體**<br>", False),
    (u"乙1·表三線乙", u"| **第三線**<br>（獨立保證）", u"| **第三級**<br>（獨立保證）", False),
    (u"乙1·表病相", u"**病相**：強人獨裁、董事會淪為橡皮圖章、派系暗箱。",
     u"**病相**：強人獨裁、執事會淪為備樣之章、派系暗箱。", False),
    (u"乙1·表對策", u"建立外部獨立仲裁通道。", u"建立客僧專案覆審之通道。", False),
    (u"乙1·引进之旨", u"引進三線模型，旨在建立", u"引進三級分權之說，旨在建立", False),
    (u"乙1·嚴禁之文", u"絕對嚴禁任何執事僧利用三線模型，", u"絕對嚴禁任何執事僧利用三級分權之說，", False),
    (u"乙1·根本之宣", u"第一線的自律永遠是根本，第二線、第三線的監督",
     u"第一級的自律永遠是根本，第二級、第三級的監督", False),
    (u"乙1·覆審院", u"由內部所差舉罪之眾（初審院）負責第一線查證與提出報告；但涉及解任董事、除名成員或終止重大合約之處分，**必須由獨立於管理層之外的獨立監察理事會（覆審院）召開獨立會議表決**",
     u"由內部所差舉罪之眾（初審院）負責初級查證與提出報告；但涉及解任執事、除名成員或終止重大合約之處分，**必須由超然於執事眾之外的監察長老眾（覆審院）召開獨立會議表決**", False),
    (u"乙1·分立原則", u"現代道場治理最大的法律雷區，在於管理層將「出家戒律的倫理位階」與「世俗法人的表決權限」混為一談。本框架確立**「戒法覆審與法人董事會分立原則」**",
     u"現代道場治理最大的法律雷區，在於執事眾將「出家戒律的倫理位階」與「世俗法人的表決權限」混為一談。本框架確立**『戒法覆審與世俗法人執事會分立原則』**", False),
    (u"乙1·柵二題", u"【戒法覆審 vs 法人董事會之管轄分立】", u"【戒法覆審 vs 法人執事會之管轄分立】", True),
    (u"乙1·柵二右", u"【世俗法人董事會（實定法管轄）】", u"【世俗法人執事會（實定法管轄）】", True),
    (u"乙1·女眾投票", u"嚴禁以八敬法剝奪女董事投票權", u"嚴禁以八敬法剝奪女眾投票權", True),
    (u"乙1·平等之一票", u"**全體董事（不論性別、出家或在家）依法行使完全平等之一人一票表決權**",
     u"**全體執事（不論性別、出家或在家）依法行使完全平等之一人一票表決權**", False),
    (u"乙1·挪用八敬", u"**絕對禁止挪用「八敬法」剝奪女性董事投票權**",
     u"**絕對禁止挪用『八敬法』剝奪女眾投票權**", False),
    (u"乙1·強令女眾", u"在世俗法人會議上，**絕對禁止任何男性董事或長老以出家「八敬法（如女眾應敬男眾）」為藉口，強令女性董事放棄發言、服從男眾決議或放棄投票權！**",
     u"在世俗法人會議上，**絕對禁止任何男性執事或長老以出家『八敬法（如女眾應敬男眾）』為藉口，強令女眾放棄發言、服從男眾決議或放棄投票權！**", False),
    (u"乙1·腐敗執事", u"極易被涉案的少數腐敗董事惡意利用——涉案董事只要在會議上高喊反對，便能讓反貪腐與追償議案永遠無法通過，導致法人治理陷入徹底癱瘓",
     u"極易被涉案的少數腐敗執事惡意利用——涉案執事只要在會議上高喊反對，便能讓反貪腐與追償議案永遠無法通過，導致常住治理陷入徹底癱瘓", False),
    (u"乙1·安全閥題", u"【董事會表決防癱瘓三大安全閥】", u"【執事會表決防癱瘓三大安全閥】", True),
    (u"乙1·追責之目", u"· 涉及董事個人追責、解任、", u"· 涉及執事個人追責、解任、", True),
    (u"乙1·回避之條", u"凡董事會審議事項涉及董事個人之損害賠償、職務解任、背信調查，或涉及該董事之直系親屬、實質關聯企業之重大採購合約者",
     u"凡執事會審議事項涉及執事個人之損害賠償、職務解任、背信調查，或涉及該執事之直系親屬、實質關聯之企業重大採購合約者", False),
    (u"乙1·回避之效", u"**該董事依法享有迴避義務，其表決權數自法定出席與表決母數中完全扣除，不得行使表決權，亦不得代理其他董事行使。**",
     u"**該執事依法享有迴避義務，其表決權數自法定出席與表決母數中完全扣除，不得行使表決權，亦不得代理其他執事行使。**", False),
    (u"乙1·異議之格", u"少數董事若在審議懲戒或財務追償案時提出異議", u"少數執事若在審議懲戒或財務追償案時提出異議", False),
    (u"乙1·主席裁定", u"主席得依法裁定該異議不適格", u"座元得依法裁定該異議不適格", False),
    (u"乙1·特別決議", u"章程授權董事會**終止一致決，自動轉軌為世俗法人法之「特別決議門檻」——由全體無利益衝突董事三分之二以上出席、出席董事三分之二以上同意通過**",
     u"章程授權執事會**終止一致決，自動轉軌為世俗法人法之『特別決議門檻』——由全體無利益衝突執事三分之二以上出席、出席執事三分之二以上同意通過**", False),
    (u"乙1·受用人", u"在現代反洗錢與非營利組織治理中，最核心的穿透審計工具是**「實質受益人審查」**",
     u"在現代反洗錢與修道共同體之治理中，最核心的穿透審查工具是**『實質受用人審查』**", False),
    (u"乙1·柵受用人", u"【實質受益人審查與穿透審計】", u"【實質受用人審查與穿透審查】", True),
    (u"乙1·鐵律", u"**穿透審計鐵律**：", u"**穿透審查鐵律**：", False),
    (u"乙1·穿透傳媒", u"僧團依實質受益人審查穿透紙上傳媒公司", u"僧團依實質受用人審查穿透紙上傳媒公司", False),
    (u"乙1·作持儀軌", u"【機構長照耗竭防禦 SOP 四大支柱】", u"【長照耗竭防禦作持儀軌四大支柱】", True),
    (u"乙1·結社", u"在非營利組織與社會運動中", u"在修道共同體與世俗結社中", False),
    (u"乙1·耶舍燈塔", u"耶舍案是現代非營利組織與公司治理的千古燈塔：",
     u"耶舍案是出世修道共同體治理的千古燈塔：", False),
]


def apply_edits(L, fs):
    done, skipped = 0, 0
    for tag, old, new, lock in EDITS:
        idx = [i for i, l in enumerate(L) if old in l]
        if not idx:
            if any(new in l or (lock and keep_probe(new) in l) for l in L):
                print(u"  %-18s 已在帳" % tag)
                skipped += 1
                continue
            raise SystemExit(u"錨未中（不敢假稱已治）：%s" % tag)
        if len(idx) > 1:
            raise SystemExit(u"錨非唯一：%s（%d 見 L%s）" % (tag, len(idx),
                                     "、".join(str(x + 1) for x in idx[:5])))
        i = idx[0]
        orig = old_line_backup[i]
        cand = L[i].replace(old, new)
        if lock:
            if not fs[i]:
                raise SystemExit(u"%s 標了保寬，其行卻不在圍欄內（L%d）" % (tag, i + 1))
            L[i] = keep_width(orig, cand)
            if dw(L[i]) != dw(orig):
                raise SystemExit(u"%s 保寬後格數仍畲 ➔ L%d" % (tag, i + 1))
        else:
            L[i] = cand
        print(u"  %-18s L%-5d %s" % (tag, i + 1, u"格寬已鎖" if lock else u"散文・表"))
        done += 1
    return L, done, skipped


def keep_probe(s):
    return s[:18]


def k_boundary(L):
    """甲3 收尾：章界「***」自十五章之中間移回第十六章之前。"""
    i = next((k for k, l in enumerate(L) if l.startswith(u"### 第四節　出坡作務")), None)
    if i is None:
        print(u"  界·無第四節（未遷？）")
        return L, 0
    star = [k for k in range(i - 6, i) if L[k].strip() == "***"]
    moved = 0
    if star:
        k = star[0]
        del L[k]
        while k > 0 and not L[k - 1].strip() and not L[k].strip():
            del L[k]
            break
        print(u"  界·除十五章內之章盡標『***』一枚（第四節之前非章界）")
        moved += 1
    j = next((k for k, l in enumerate(L) if l.startswith(u"### 第十六章")), None)
    back = u"\n".join(x.strip() for x in L[max(0, j - 6):j])
    if u"***" not in back:
        L[j - 1:j - 1] = [u"***", u""]
        print(u"  界·第十六章之前補章盡標『***』一枚（如章前之成例）")
        moved += 1
    else:
        print(u"  界·十六章前已有章界，不補")
    return L, moved


def main():
    go = "--write" in sys.argv
    before = raw()
    sha = hashlib.sha256(before.encode("utf-8")).hexdigest()[:12]
    L = before.replace(CRLF, LF).split(LF)
    global old_line_backup
    old_line_backup = list(L)
    fs = fence_flags(L)
    print(u"F2 %s・%d 行・SHA %s" % (os.path.basename(BOOK)[:14], len(L), sha))
    L, moved = k_boundary(L)                          # 先遷章界：行數之變在諸刀之前定穩
    old_line_backup = list(L)
    fs = fence_flags(L)
    L, done, skipped = apply_edits(L, fs)
    fs2 = fence_flags(L)
    if len(fs) != len(fs2) or [x for x, y in zip(fs, fs2) if x != y]:
        raise SystemExit(u"圍欄之界變了（柵開合失配）——須查")
    for i, l in enumerate(L, 1):
        h = pairsimp.hits(l)
        if h:
            raise SystemExit(u"簡形之閘未過 L%d「%s」" % (i, h))
    # 式樣不增：改過之行的「…」之數不得多於改前
    grew = []
    for tag, old, new, lock in EDITS:
        for i, l in enumerate(L):
            if new in l or (lock and keep_probe(new) in l):
                a = len(re.findall(u"「[^」]{4,}」", old_line_backup[i]))
                b = len(re.findall(u"「[^」]{4,}」", l))
                if b > a:
                    grew.append(u"L%d %d➔%d" % (i + 1, a, b))
    if grew:
        raise SystemExit(u"式樣增多（新掛逐字之框）：%s" u"、".join(grew[:5]))
    print(u"  合計 %d 刀・章界 %d 目・行 %d ➔ %d" % (done, moved, len(old_line_backup), len(L)))
    if not go:
        print(u"（試跑・加 --write 始落盤）")
        return 0
    if not os.path.isdir(os.path.dirname(BK)):
        os.makedirs(os.path.dirname(BK))
    io.open(BK, "wb").write(before.encode("utf-8"))
    nl = CRLF if CRLF in before else LF
    out = nl.join(L).encode("utf-8")
    io.open(BOOK, "wb").write(out)
    chk = io.open(BOOK, "rb").read().decode("utf-8")
    if chk.count(chr(13)) != chk.count(chr(10)):
        raise SystemExit(u"行尾混雜（CR %d ≠ LF %d）" % (chk.count(chr(13)), chk.count(chr(10))))
    print(u"  落盤：%d 行・%d B・SHA %s ➔ %s・備 %s"
          % (len(L), len(out), sha, hashlib.sha256(out).hexdigest()[:12],
             os.path.relpath(BK, ROOT)))
    return 0


old_line_backup = []
if __name__ == "__main__":
    sys.exit(main())
