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
