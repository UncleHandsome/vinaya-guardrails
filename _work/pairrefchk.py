# -*- coding: utf-8 -*-
"""指針對合之尺（雙子星兩冊）：書中凡『第N章』之指，須落得有章；跨冊之指須冠以冊名。
   管轄：全冊圍欄外之每一行。口徑：
     ・『第N章』左側十二字內見《起心動念》或《如法推尋》或『姊妹篇』『他冊』者，作跨冊之指，核他冊之章數；
     ・否則核本冊之章數；
     ・章數之外者即紅，點名其行。
   又『附錄N』之指須本冊實有其附錄。
用法：python -X utf8 _work/pairrefchk.py
"""
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import paircase_lib as CL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BOOKS = [("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt", "《起心動念》"),
         ("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt", "《如法推尋》")]
XCROSS = re.compile(r"《起心動念》|《如法推尋》|姊妹篇|他冊")
REZH = re.compile(r"第([一二三四五六七八九十百]+)章")
REAPX = re.compile(r"附錄([一二三四五六七八九十]+)")
RECARD_H = re.compile(r"^#{1,6}\s*【(?:制度)?案卷\s*[0-9]{2}")   # 案卷卡之題（封面・目錄・此尺同一形）
HAN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
       "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15, "十六": 16, "十七": 17,
       "十八": 18, "十九": 19, "二十": 20, "廿一": 21, "廿二": 22}


def cn2int(s):
    return HAN.get(s)


def fence_mask(lines):
    out, inside = [], False
    for l in lines:
        if l.strip().startswith("```"):
            out.append(inside)
            inside = not inside
        else:
            out.append(inside)
    return out


def cardset(lines):
    out = set()
    for l in lines:
        for m in re.finditer(r"【案卷\s*([0-9]+)(?:\s*&\s*([0-9]+))?[^】]*】", l):
            out.add(int(m.group(1)))
            if m.group(2):
                out.add(int(m.group(2)))
    return out


def main():
    data = {}
    for tag, fn, selfname in BOOKS:
        lines = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
        fm = fence_mask(lines)
        zhang = max((cn2int(m.group(1)) for l in lines if re.match(r"^#{1,3}\s*第[一二三四五六七八九十]+章", l)
                     for m in [REZH.search(l)] if m and cn2int(m.group(1))), default=0)
        apx = sorted({cn2int(m.group(1)) for l in lines if l.startswith("## 附錄")
                      for m in [REAPX.search(l)] if m and cn2int(m.group(1))})
        nhead = sum(1 for l in lines if re.match(r"^#{1,3}\s*第[一二三四五六七八九十]+章", l))
        data[tag] = dict(lines=lines, fm=fm, zhang=zhang, nhead=nhead, apx=apx, selfname=selfname,
                         cards=CL.findable(lines), subs=CL.subs(lines),
                         ncard=sum(1 for l in lines if RECARD_H.match(l)))
        print(f"■ {tag}・章之實數 {zhang}（題 {nhead} 枚）・附錄之實 {apx}・"
              f"案卷之卡 {data[tag]['ncard']}（子案 {len(data[tag]['subs'])}）・可檢案號 {len(data[tag]['cards'])}")
    bad = 0
    CITED = [0]
    for tag, fn, selfname in BOOKS:
        d = data[tag]
        other = data["F2" if tag == "F1" else "F1"]
        for i, l in enumerate(d["lines"]):
            if d["fm"][i]:
                continue
            for m in REZH.finditer(l):
                n = cn2int(m.group(1))
                if n is None:
                    continue
                pre = l[max(0, m.start() - 12):m.start()]
                cross = bool(XCROSS.search(pre)) or d["selfname"] not in l or other["selfname"] in pre
                lim = other["zhang"] if cross else d["zhang"]
                # 跨冊之判：指之數若本冊無而彼冊有，即歸跨冊（如十一之於 F2 二十章則必為本冊）
                if n > lim:
                    alt = d["zhang"] if cross else other["zhang"]
                    if n <= alt:
                        continue
                    bad += 1
                    print(f"  ✗ {tag} L{i + 1}・第{m.group(1)}章 越於兩冊之外（本冊 {d['zhang']}・彼冊 {other['zhang']}）")
                    print(f"      {l.strip()[:76]}")
            for m in REAPX.finditer(l):
                n = cn2int(m.group(1))
                if n and n not in d["apx"] and n not in other["apx"]:
                    bad += 1
                    print(f"  ✗ {tag} L{i + 1}・附錄{m.group(1)} 兩冊俱無其篇")
                    print(f"      {l.strip()[:76]}")
        dcl = CL.declared(d["lines"])
        print(f"  跨冊案號之約：{'立' if dcl else '未立'}")
        for i, k, pre in CL.cites(d["lines"]):
            CITED[0] += 1
            if k in d["cards"] or dcl:
                continue
            l = d["lines"][i]
            if "《起心動念》" in pre or "《如法推尋》" in pre or "姊妹" in pre:
                continue
            bad += 1
            print(f"  ✗ {tag} L{i + 1}・〔案 {k}〕本冊無其卡且不冠冊名（失指）")
            print(f"      {l.strip()[:76]}")
    print("=" * 60)
    print(f"指針對合：失指 {bad} 處・案號之引管轄 {CITED[0]} 條" + ("　✓ 全綠" if not bad else ""))
    return 0 if not bad else 1


raise SystemExit(main())
