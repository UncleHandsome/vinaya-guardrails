# -*- coding: utf-8 -*-
"""第五波・案號兩刀合一：
   甲・立約——兩冊卷首凡例第一節各增『第七律・跨冊案號之索』（文在 `paircase_lib.NOTE_ITEM`，一刀一尺一產生器同取），
        標題遂由『引文承諾六律』改『七律』；
   乙・歸形——案號之引用形制各從本冊成例（心法卷〔案NN〕・法制卷〔案例 NN〕帶空格），唯本冊有載體者才歸形；
   丙・一處 ver39 舊章次『詳見第六章〔案例 76〕』→『詳見第五篇』。
用法：python -X utf8 _work/paircite_note.py [--write]"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import paircase_lib as CL  # noqa: E402

F1, F2 = CL.F1, CL.F2
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv
HEAD6 = "### 一、文獻底冊與引文承諾"
SIXTH = "6. **羯磨白文敬語統一**"
ZH6 = {"6. **羯磨白文敬語統一**"}


def run():
    tot = {}
    for fn in (F1, F2):
        lines = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
        find = CL.findable(lines)
        n = 0
        for i, l in enumerate(lines):
            if "【文獻底冊與引文承諾六律】" in l:          # 改標題則內引須同時歸位，勿留舊稱
                lines[i] = l.replace("【文獻底冊與引文承諾六律】", "【文獻底冊與引文承諾七律】")
                n += 1
                print(f"  ・{fn[:6]} L{i + 1}・內引『六律』→『七律』")
        if not CL.declared(lines):
            k = next(i for i, l in enumerate(lines) if l.startswith(HEAD6))
            lines[k] = lines[k].replace("六律", "七律")
            j = next(i for i, l in enumerate(lines) if l.startswith(SIXTH))
            lines[j + 1:j + 1] = ["", CL.NOTE_ITEM[fn]]
            n += 1
            print(f"  ・{fn[:6]} L{k + 1}・六律→七律；第七律立於 L{j + 3}")
        else:
            print(f"  · {fn[:6]}・約已立（不動）")
        # 乙・歸形
        for i, l in enumerate(lines):
            if l.strip().startswith("```"):
                continue
            if fn == F1:
                for m in re.finditer(r"〔案例\s*([0-9]{1,3})〕", l):
                    k = int(m.group(1))
                    if k in find:
                        lines[i] = lines[i].replace(m.group(0), f"〔案{k}〕", 1)
                        n += 1
            else:
                for m in re.finditer(r"〔案例([0-9]{1,3})〕", l):
                    if int(m.group(1)) in find:
                        lines[i] = lines[i].replace(m.group(0), f"〔案例 {m.group(1)}〕", 1)
                        n += 1
        for i, l in enumerate(lines):
            if "詳見第六章〔案例 76〕" in l:
                lines[i] = l.replace("詳見第六章〔案例 76〕", "詳見第五篇〔案例 76〕")
                n += 1
                print(f"  ・{fn[:6]} L{i + 1}・第六章→第五篇")
        tot[fn] = (lines, n)
        print(f"■ {fn[:6]}・治 {n} 處・管轄：案號之引 {len(CL.cites(lines))} 條・可檢 {len(find)} 號")
    if not W:
        print("（試跑：未落盤）")
        return
    for fn, (lines, n) in tot.items():
        p = ROOT / fn
        raw = p.read_bytes()
        new = "\r\n".join(lines).encode("utf-8")
        if new == raw:
            print(f"  · {fn[:6]}・一字未動")
            continue
        (BAK / (fn + ".pre_cases")).write_bytes(raw)
        p.write_bytes(new)
        print(f"  ● {fn[:6]}・{len(new)} B・SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(new).hexdigest()[:12]}")


run()
