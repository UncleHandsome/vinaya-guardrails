# -*- coding: utf-8 -*-
"""hulan_path - 《佛陀的護欄》正文檔之唯一法源。

全書工具（_work/*.py 尺、_print/管線）一律 `import hulan_path as HP` 取 HP.SRC，
不得再各別硬編路徑；搬檔只改本檔（或搬後放根目錄即可自動偵測）。

解析順序：
  1. 環境變數 HULAN_SRC（暫時指別檔用）
  2. 工作資料夾根目錄中唯一一支「佛陀的護欄*.txt」
  3. 根目錄無此檔時，退至 `_archive/舊本/`（2026-10-18 奉令：兩本舊本移入 `_archive/舊本/`，
     不再列為正本，唯作合編之素材與逐字校據——故舊尺仍須跑得到它們）
前綴以 chr() 構造，避免中文經傳遞層被歸簡。
"""
import os
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
PREFIX = "".join(chr(c) for c in (0x4F5B, 0x9640, 0x7684, 0x8B77, 0x6B04))
GLOB_PAT = PREFIX + "*.txt"
ARCHIVE = os.path.join(ROOT, "_archive", u"舊本")     # 舊 = U+820A（勿誤寫 U+8208「興」）
# 備份之位址（2026-10-27 奉令「備份檔案另外找地方放」）：正本同層自此不留一支 .bak，
# 俱入 `_archive/備份/護欄/`。『備份』之名就 `_archive` 現目錄中取（首字 U+5099），
# 子庫之名則取本檔前綴之末二字（護欄 = U+8B77 U+6B04）——兩處皆不另立字面，免歸簡之災。


def _bkroot():
    arc = os.path.join(ROOT, "_archive")
    for d in os.listdir(arc):
        if os.path.isdir(os.path.join(arc, d)) and d[:1] == chr(0x5099):
            return os.path.join(arc, d)
    return os.path.join(arc, "".join(chr(c) for c in (0x5099, 0x4EFD)))


BACKUP = os.path.join(_bkroot(), PREFIX[-2:])


def bakpath(tag, src=None):
    """本輪改前之備份檔路徑：`HP.bakpath("71b")` ➔ _archive/備份/護欄/〈正本名〉.txt.bak71b。
    寫檔之器一律取此，不得再作 `BOOK + ".bakNN"`（那會把根目錄當垃圾場）。"""
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    return os.path.join(BACKUP, os.path.basename(src or SRC) + ".bak" + tag)


def detect():
    for base in (ROOT, ARCHIVE):
        hits = sorted(glob.glob(os.path.join(base, GLOB_PAT)))
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            raise RuntimeError("hulan_path: %s 應恰有一支 %s，實得 %d 支：%s"
                               % (base, GLOB_PAT, len(hits), [os.path.basename(x) for x in hits]))
    cand = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.txt")))
    raise RuntimeError("hulan_path: 根目錄與 %s 俱無 護欄*.txt；根目錄 *.txt 候選：%s" % (ARCHIVE, cand))


SRC = os.environ.get("HULAN_SRC") or detect()


def text():
    with open(SRC, "rb") as f:
        return f.read().decode("utf-8")


if __name__ == "__main__":
    print(SRC)
    print("exists=%s" % os.path.isfile(SRC))
