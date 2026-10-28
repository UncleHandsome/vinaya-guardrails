# -*- coding: utf-8 -*-
"""『去現代法令』大掃除之範圍盤點（只讀，先印名不落刀）。

分三級：
  甲・行內實定法引用（法名／制度名／法院訴訟稅務等）
  乙・整節整款專講世俗法（標題即屬之）
  丙・章題與篇題含世俗法概念（改名之範圍）
用法：python -X utf8 _work/pairlaw.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt"),
         ("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt")]

LAW_NAME = ["勞基法", "勞動基準法", "民法", "刑法", "憲法", "信託法", "財團法人法", "公司法",
            "洗錢防制", "宗教事務條例", "受託人條例", "個人資料", "個資法", "GDPR", "勞資",
            "勞動契約", "僱傭契約", "委任契約", "受僱", "傭", "勞工", "雇主", "資遣費",
            "勞動法", "強制法", "強行法", "實定法"]
LAW_INST = ["除斥期間", "特留分", "假扣押", "假處分", "搜索票", "檢察官", "法院", "訴訟", "起訴",
            "判處", "律師", "會計師", "董事會", "監察人", "稅務", "土地增值稅", "所得稅", "保險",
            "司法審查", "侵權", "名譽權", "隱私權", "人格權", "停職", "解僱", "開除", "考勤", "打卡",
            "劳动", "合約", "契約"]
MGMT = ["IIA", "三線", "內部控制", "合規", "風控", "稽核", "吹哨", "創傷知情", "職能", "標準作業",
        "SOP", "管理學", "組織行為"]
XDOMAIN = ["世俗法", "世間法", "國法", "王法", "人間國法", "世俗實定", "世俗司法", "世俗民法",
           "世俗刑事", "世俗勞動", "世俗法院", "現代法學", "法學"]

CH = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+章[　 ].*)$")
PIAN = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+篇[:：].*)$")
SEC = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+節[　 ].*)$")
SUB = re.compile(r"^#{4,6}\s*(.+)$")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def cnt(lines, ws):
    return {w: sum(l.count(w) for l in lines) for w in ws if sum(l.count(w) for l in lines)}


for tag, fn in FILES:
    L = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
    n = cjk("\n".join(L))
    print("=" * 76)
    print(f"■ {tag}｜{len(L)} 行・{n:,} 字")
    for lbl, ws in (("法名", LAW_NAME), ("制度名", LAW_INST), ("管理學", MGMT), ("跨域語", XDOMAIN)):
        c = cnt(L, ws)
        tot = sum(c.values())
        print(f"   {lbl}：共 {tot} 見・每千字 {tot / n * 1000:.2f}｜" +
              "・".join(f"{k}{v}" for k, v in sorted(c.items(), key=lambda x: -x[1])[:12]))
    # 逐章歸戶
    chs = [(i, CH.match(l.strip()).group(1)) for i, l in enumerate(L) if CH.match(l.strip())]
    chs.append((len(L), "END"))
    print("   逐章之『法名＋制度名』密度（每千字）與行數：")
    for k in range(len(chs) - 1):
        a, b = chs[k][0], chs[k + 1][0]
        seg = L[a:b]
        m = cjk("\n".join(seg)) or 1
        t = sum(cnt(seg, LAW_NAME + LAW_INST).values())
        if t:
            print(f"      {chs[k][1][:30]:32} {t / m * 1000:5.1f}／千字・{t:>3} 見・{b - a:>4} 行")
    print("   乙級・節與款之標題含世俗法者：")
    for i, l in enumerate(L):
        s = l.strip()
        if not s.startswith("#"):
            continue
        t = re.sub(r"^#+\s*", "", s)
        if re.search(r"勞|勞動|僱|法人|董事|信託|稅|訴訟|法院|合規|契約|財產|醫療|長照|數位|自媒體|勞基", t):
            print(f"      L{i+1}: {t[:70]}")
    print("   丙級・篇題與章題：")
    for i, l in enumerate(L):
        s = l.strip()
        if CH.match(s) or PIAN.match(s):
            t = re.sub(r"^#+\s*", "", s)
            if re.search(r"現代|法人|治理|勞動|勞僱|財產|信託|合規|IIA|模型|防線|審計|數位", t):
                print(f"      L{i+1}: {t[:70]}")
