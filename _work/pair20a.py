# -*- coding: utf-8 -*-
"""第二十波・第二本第三輪（六事）：條次之誤・索引漏案・巴利正名・章名之實・法條打架・名相打架。
每刀唯一錨・乾跑印前後・落畢自證（舊字盡去・新文無簡形・CRLF 不動・BOM 不動）。

用法：python -X utf8 _work/pair20a.py [--write]
"""
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp as PS                                          # noqa: E402

F2 = os.path.join(ROOT, "如法推尋：僧伽憲政、法權審理與修復正義.txt")
BAK = os.path.join(ROOT, "_archive", "備份", "AI清理前")
WRITE = "--write" in sys.argv

JOBS = [
    (u"案卷104・波逸提11之條次正誤",
     u"稿所稱『壞生草木戒第十一條』，本地無此目（本律波逸提第十一乃提婆達伴黨順從之戒），故不掛條次。",
     u"稿所稱『壞生草木戒第十一條』，本律作『壞鬼神村』（波逸提法第十一條，本地語料 11-21 檔段），"
     u"名異而制同；前稿誤指為伴黨戒者，係混淆僧殘第十一條助破僧戒之誤，今正之。"),
    (u"第十章・失宿之巴利名（Vipatti➔Ratticcheda）",
     u"「失宿（Vipatti）」", u"「失宿（Ratticcheda）」"),
    (u"第八章・象力之巴利名（Sāmaṇaka➔Hatthaka）",
     u"象力釋子（Sāmaṇaka）", u"象力釋子（Hatthaka Sakyaputta）"),
    (u"第五章・疑罪從無之但書",
     u"客觀損害雖已成辦，但嫌疑人堅決否認，且客觀證據鏈無法排除合理懷疑者，"
     u"聲聞律庭恪守司法自制",
     u"客觀損害雖已成辦，但嫌疑人堅決否認，且客觀證據鏈無法排除合理懷疑者"
     u"（**除第三節軌道 B 性罪既遂之客觀鐵證宣告外**），聲聞律庭恪守司法自制"),
    (u"十九章・章首明其兼採犍度二案",
     u"> 穿透這十五座險峰，出世法治的極致精密與深沉慈悲，方得以全息展現。",
     u"> 其中〔專題 03〕（卷四十四至四十五・呵責犍度）與〔專題 08〕（卷三十八・皮革犍度）"
     u"出自二十犍度，取其在代理越權與制度賦能之法理；餘十三則俱出調部。"
     u"故仍以『調部專題』為名，而實兼採犍度，讀者幸察。\n"
     u">\n"
     u"> 穿透這十五座險峰，出世法治的極致精密與深沉慈悲，方得以全息展現。"),
]
BAN = (u"波逸提第十一乃提婆達伴黨", u"（Vipatti）", u"（Sāmaṇaka）")

GRP1_OLD = (u"  〔案例 02〕、〔案例 03〕、〔案例 05〕、〔案例 12〕、〔案例 14〕、〔案例 15〕、"
            u"〔案例 17〕、〔案例 24〕、〔案例 27〕")
GRP1_NEW = (u"  〔案例 08〕、〔案例 03〕、〔案例 05〕、〔案例 12〕、〔案例 14〕、〔案例 15〕、"
            u"〔案例 17〕、〔案例 09〕、〔案例 27〕")


def run(path):
    raw = io.open(path, "rb").read()
    txt = raw.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in txt else "\n"
    for why, old, new in JOBS:
        n = txt.count(old)
        print(u"  · %-34s 命中 %d" % (why, n))
        if n != 1:
            raise SystemExit(u"錨不唯一／不見：%s" % why)
        i = txt.find(old)
        print(u"      ⟪%s⟫" % txt[max(0, i - 18):i + len(old) + 14].replace(nl, u"¶"))
        txt = txt.replace(old, new.replace("\n", nl))
    n = txt.count(GRP1_OLD)
    print(u"  · %-34s 命中 %d" % (u"附錄一・個人修煉組換案（02・24➔08・09）", n))
    if n != 1:
        raise SystemExit(u"生活場域第一組之錨不唯一")
    txt = txt.replace(GRP1_OLD, GRP1_NEW)
    for b in BAN:
        if b in txt:
            raise SystemExit(u"落刀後仍見禁字『%s』" % b)
    bad = [(x, PS.hits(l)) for x, l in enumerate(txt.split(nl), 1) if PS.hits(l)]
    if bad:
        raise SystemExit(u"簡形：%s" % bad[:4])
    if txt.count("\r") != txt.count("\r\n") or txt.count("\n") != txt.count("\r\n"):
        raise SystemExit(u"換行不齊")
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    out = bom + txt.encode("utf-8")
    print(u"  行數 %d・CRLF %d・BOM %s" % (txt.count(nl) + 1, txt.count(nl), u"有" if bom else u"無"))
    # 自證：生活場域六組之不重不漏
    import re
    lines = txt.split(nl)
    k0 = [k for k, l in enumerate(lines) if u"一、個人修煉領域" in l][0]
    groups = []
    for k in range(k0, k0 + 14):
        if re.match(u"^\\s*〔案例", lines[k]):
            groups.append([int(x) for x in re.findall(u"〔案例 (\\d+)〕", lines[k])])
    from collections import Counter
    c = Counter(n for g in groups for n in g)
    dup = sorted(k for k, v in c.items() if v > 1)
    miss = [x for x in range(1, 103) if x not in c]
    print(u"  自證：各組 %s・總 %d・去重 %d・重號 %s・缺號 %s"
          % ([len(g) for g in groups], sum(len(g) for g in groups), len(c), dup, miss))
    if dup or miss:
        raise SystemExit(u"生活場域軸仍有重號或缺號")
    if WRITE:
        os.makedirs(BAK, exist_ok=True)
        dst = os.path.join(BAK, os.path.basename(path) + ".pre_a20")
        if not os.path.isfile(dst):
            shutil.copy2(path, dst)
        with open(path, "wb") as f:
            f.write(out)
        print(u"  ✎ 已寫入（備份 %s）" % os.path.basename(dst))


print("=" * 74)
run(F2)
print("=" * 74)
print(u"%s" % (u"落盤完畢" if WRITE else u"乾跑（未寫）：python -X utf8 _work/pair20a.py --write"))
