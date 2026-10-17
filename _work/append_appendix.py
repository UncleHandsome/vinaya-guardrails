# -*- coding: utf-8 -*-
"""附錄入書：把 _work/appendix_jieben.md 接於全書之末（尾聲之後）。
   紙本目錄不列附錄之目次：目錄清單多一行，build38 之大綱定位器即以目錄頁誤中同名條。
   --refresh：先於記憶體削舊附錄（自「# 附錄」H1 至檔尾）再接新稿，一次寫檔——
              分兩步（先 --undo 再 --go）時若中途失手，書中便無附錄，故立此一鍵換版。
   斷言：非 refresh 時附錄標題原不存於書中（免重覆插入）、行數增量相符、CRLF 不變。
用法：python -X utf8 _work/append_appendix.py [--go|--undo|--refresh]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = HP.SRC
APX = os.path.join(ROOT, u"_work", u"appendix_jieben.md")
GO = u"--go" in sys.argv
UNDO = u"--undo" in sys.argv
REFRESH = u"--refresh" in sys.argv

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
if UNDO or REFRESH:
    """撤除附錄：自「# 附錄」H1 至檔尾一併削去，並削其在目錄中所佔之兩行。
       --refresh 不寫檔，只把削舊之後之檔留在記憶體中接新稿（一鍵換版，中途不失附錄）。"""
    h = [i for i, l in enumerate(L) if l.startswith(u"# 附錄")]
    assert len(h) == 1, u"附錄標題存 %d 處，不撤" % len(h)
    a = h[0]
    while a > 0 and not L[a - 1].strip():
        a -= 1
    toc = [i for i, l in enumerate(L[:a]) if l.lstrip().startswith(u"* **附錄　全戒本歷條總表")]
    assert len(toc) <= 1, u"目錄之附錄項存 %d 處" % len(toc)     # 紙本目錄今不列附錄，零處乃常
    out = [l for i, l in enumerate(L[:a]) if i not in set(toc)]
    while out and not out[-1].strip():
        out.pop()
    if UNDO:
        new = u"\r\n".join(out) + u"\r\n"
        print(u"撤除：%d 行 → %d 行（-%d）｜CRLF %d" % (len(L), len(out), len(L) - len(out), new.count(u"\r\n")))
        io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new)
        print(u"已撤除附錄")
        sys.exit(0)
    L, raw = out, u"\r\n".join(out) + u"\r\n"
    print(u"換版：先削舊附錄，正文 %d 行" % len(L))
if REFRESH:
    # 「--refresh」之名易誤：舊版只換版不重算——凡例或指針之修訂若未另跑產生器，便悄悄留在舊 md 裡。
    # 第卅五輪之實害：通數算式與拆分後之新指針（尼單提第120條）俱未入書，而回報已稱落地。
    # 今令 --refresh 先重跑 gen_appendix --go，使「換版」必含「重算」，不留手工隨動之隙。
    import subprocess
    rr = subprocess.run([sys.executable, u"-X", u"utf8", os.path.join(ROOT, u"_work", u"gen_appendix.py"), u"--go"],
                        capture_output=True, text=True, encoding=u"utf-8", errors=u"replace")
    assert rr.returncode == 0, u"重算附錄失敗：%s" % ((rr.stderr or u"")[-400:] or (rr.stdout or u"")[-400:])
    tail = [x for x in (rr.stdout or u"").split(u"\n") if x.strip()][-1:]
    print(u"refresh 先重算產生器｜%s" % (tail[0] if tail else u"（無輸出）"))
apx = io.open(APX, encoding="utf-8", newline=u"").read().replace(u"\r\n", u"\n").rstrip(u"\n").split(u"\n")
head = apx[0]
assert not any(l == head for l in L), u"附錄標題已在書中，勿重覆插入"
while apx and not apx[-1].strip():
    apx.pop()
n_rule = sum(1 for x in apx if re.match(u"\\d+(?:～\\d+)?\\.\\s", x))
print(u"附錄歷號行 %d 行（自附錄行數實算，非手打；『1～69.』之合列行作一行計）" % n_rule)
out = list(L)
# 紙本目錄不列附錄：目錄清單一多一行，大綱定位器即以目錄頁誤中同名條（第一章副題落到 p4 之病）。
# 附錄之書籤仍由書檔 H1 取得；如必欲列於目錄，須先修 build38 使定位器跳過目錄之頁。
out += [u""] + apx                                      # 空行隔開，免 pandoc 把『# 附錄』吸入前段
tail = u"\r\n" if raw.endswith(u"\r\n") else u""        # 檔尾之空行須一仍其舊（原檔以 CRLF 收）
new = u"\r\n".join(out) + tail
print(u"附錄 %d 行｜全檔行數 %d → %d（+%d）｜檔尾%s" % (
    len(apx), len(L), len(out), len(out) - len(L), u"帶 CRLF" if tail else u"無 CRLF"))
assert len(out) == len(L) + 1 + len(apx), u"行數增量不合"
assert new.count(u"\r\n") == len(out) - 1 + (1 if tail else 0), u"CRLF 變形"
print(u"附錄首兩行：%s ｜ %s" % (apx[0][:40], apx[6][:52]))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new)
    print(u"已入書")
else:
    print(u"（覆核模式，未寫檔）")
