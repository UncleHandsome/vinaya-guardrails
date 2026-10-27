# -*- coding: utf-8 -*-
"""第六波・心法卷總目錄之案序歸真（目錄須從正文，不可正文從目錄）。

今病（外路第八報告・第二項，量得俱真）：目錄所列案序與正文出現之序四章皆錯，
  且雙聯卡之次號（案20）在目錄漏列。治法：以正文卡序為法源重列，單號案仍用curated短注，
  雙聯卡合為一目（『〔案19&20〕卡題首語』），俾次號不漏。重建後即自覆核（序合＝綠）。
用法：python -X utf8 _work/pairf1toc.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv
CARD = re.compile(r"^####\s*【案卷\s*([0-9]{2}[A-Z]?)(?:\s*&\s*([0-9]{2})[^】]*)?】([^：]*)")
ZH = re.compile(r"^#\s*(第[一二三四五六七八九十]+章)[　 ](.*)$")
ITEM = re.compile(r"〔案\s*([0-9]{2}[A-Z]?)〕([^、）]*)")
TOCZH = re.compile(r"\*\*\s*(第[一二三四五六七八九十]+章)")


def body_order(L):
    """回 {章號: [ (案形, 雙聯次號或 None, 卡題首語) ]}——正文之實序（案形可帶子案之字母）。"""
    out, cur = {}, None
    for l in L:
        m = ZH.match(l.strip())
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        c = CARD.match(l.strip())
        if c and cur:
            out[cur].append((c.group(1), c.group(2), c.group(3).strip()))
    return out


def curated(L):
    """自今目錄取單號案之短注（curated 之詞乃作者所定，保留）。"""
    m = {}
    for l in L:
        if l.strip().startswith("（〔案"):
            for n, g in ITEM.findall(l):
                m[n] = g.strip()
    return m


def main():
    raise SystemExit(
        u"退役（第十四波）：目錄今由 _print/build_pair.py 之點線目錄生成器印出並載頁碼，"
        u"正本之 markdown 目錄塊已由 _work/pair14.py 除盡；再跑本器會生出不印之幽靈目錄。"
        u"覆核改走 _work/pairtocnum.py（逐條驗目錄號＝印面頁）。")
    p = ROOT / F1
    raw = p.read_bytes()
    L = raw.decode("utf-8").split("\r\n")
    order, gloss = body_order(L), curated(L)
    n = 0
    for i, l in enumerate(L):
        if not l.strip().startswith("（〔案"):
            continue
        z = next(k for k in range(i, 0, -1) if ZH.match(L[k].strip()) or TOCZH.search(L[k]))
        cur = (ZH.match(L[z].strip()) or TOCZH.search(L[z])).group(1)
        items = []
        for a, b, head in order.get(cur, []):
            if b:
                items.append(f"〔案{a}&{b}〕{head}")
            else:
                items.append(f"〔案{a}〕{gloss.get(a, head)}")
        new = "（" + "、".join(items) + "）"
        if new != l.strip():
            lead = l[:len(l) - len(l.lstrip())]
            trail = "  " if l.endswith("  ") else ""
            print(f"  L{i + 1}・{cur} 目錄案序歸真")
            print(f"     故 {l.strip()[:86]}")
            print(f"     新 {new[:86]}")
            L[i] = lead + new + trail
            n += 1
    # 自覆核：目錄序須等於正文序
    bad = 0
    order2 = body_order(L)
    for i, l in enumerate(L):
        if not l.strip().startswith("（〔案"):
            continue
        z = next(k for k in range(i, 0, -1) if ZH.match(L[k].strip()) or TOCZH.search(L[k]))
        cur = (ZH.match(L[z].strip()) or TOCZH.search(L[z])).group(1)
        toc = [(a, b or None) for a, b in re.findall(r"〔案([0-9]{2}[A-Z]?)(?:&([0-9]{2}))?〕", l)]
        bod = [(a, b or None) for a, b, _ in order2.get(cur, [])]
        if toc != bod:
            bad += 1
            print(f"  ✗ 覆核不合：{cur}・目錄 {toc} ≠ 正文 {bod}")
    bad2 = sorted({c for l in L for c in PS.hits(l)})
    print(f"歸真 {n} 行・覆核序之不合 {bad}・簡形 {bad2}")
    if bad or bad2:
        raise SystemExit("不合，不落盤")
    if not W:
        print("（試跑：未落盤）")
        return
    (BAK / (F1 + ".pre_toc")).write_bytes(raw)
    data = "\r\n".join(L).encode("utf-8")
    p.write_bytes(data)
    print(f"  ● {F1[:6]}・SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")


main()
