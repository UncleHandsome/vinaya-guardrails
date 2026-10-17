# -*- coding: utf-8 -*-
"""無頭瀏覽器列印之參數 A/B 量測（交錯輪次取最小值，避機緣噪音）。

樣本：現成之 final38_精簡本_screen.html（293 頁）。每變體各跑 3 遍，遍次交錯
（A B C D | A B C D | A B C D），每變體取其最小 wall 秒；並記頁數與文字長度，
三者同者方為「版面無變」。另測共用 profile 與近空白頁之啟動底數。
"""
import importlib.util, os, shutil, subprocess, sys, tempfile, time
import pymupdf

PR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_print")
spec = importlib.util.spec_from_file_location("b38", os.path.join(PR, "build38.py"))
b38 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b38)
BROWSER = b38.find_browser()

HTML = os.path.join(PR, "final38_精簡本_screen.html")
URL = "file:///" + HTML.replace("\\", "/")
BLANK = os.path.join(PR, "_blank_probe.html")
open(BLANK, "w", encoding="utf-8").write("<html><body><p>x</p></body></html>")
BLANK_URL = "file:///" + BLANK.replace("\\", "/")

BASE = ["--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", "--disable-extensions", "--no-pdf-header-footer"]
EXTRA = ["--disable-background-networking", "--disable-background-timer-throttling",
         "--disable-backgrounding-occluded-windows", "--disable-breakpad",
         "--disable-component-update", "--disable-domain-reliability",
         "--disable-sync", "--metrics-recording-only", "--mute-audio"]
COMP = "--run-all-compositor-stages-before-draw"
VTB = "--virtual-time-budget=240000"

VARIANTS = [
    ("A 現行(compositor+VTB)", BASE + [COMP, VTB]),
    ("B 去compositor", BASE + [VTB]),
    ("C 去二者", BASE),
    ("D 去二者+disable群", BASE + EXTRA),
]
PDF = os.path.join(PR, "_probe.pdf")
res = {n: [] for n, _ in VARIANTS}
sig = {}


def run(flags, url, profile=None):
    own = profile is None
    tmp = profile or tempfile.mkdtemp(prefix="probe-")
    if os.path.exists(PDF):
        os.remove(PDF)
    cmd = [BROWSER] + flags + ["--user-data-dir=" + tmp, "--print-to-pdf=" + PDF, url]
    t = time.perf_counter()
    subprocess.run(cmd, check=False, cwd=PR, timeout=900)
    for _ in range(600):
        if os.path.exists(PDF) and os.path.getsize(PDF) > 0:
            break
        time.sleep(0.05)
    el = time.perf_counter() - t
    if own:
        shutil.rmtree(tmp, ignore_errors=True)
    return el


def stat():
    d = pymupdf.open(PDF)
    n = d.page_count
    ch = sum(len(p.get_text()) for p in d)
    d.close()
    return n, ch, os.path.getsize(PDF)


for rnd in range(3):
    for name, flags in VARIANTS:
        el = run(flags, URL)
        res[name].append(el)
        sig[name] = stat()
        print("round%d %-26s %5.1fs 頁%d 字%d" % (rnd + 1, name, el, sig[name][0], sig[name][1]))

out = ["##### 各變體三遍取最小（同一 293 頁樣本）#####"]
for name, _ in VARIANTS:
    ts = sorted(res[name])
    out.append("%-26s min %5.1fs｜中 %5.1fs｜max %5.1fs｜頁字檔 %s"
               % (name, ts[0], ts[1], ts[2], sig[name]))
base_min = min(res[VARIANTS[0][0]])
for name, _ in VARIANTS[1:]:
    out.append("   %s 較現行省 %5.1fs（%.0f%%）"
               % (name, base_min - min(res[name]),
                  100.0 * (base_min - min(res[name])) / base_min))

prof = tempfile.mkdtemp(prefix="probe-")
out.append("##### 共用 profile（連跑三遍，同一臨時目錄不刪）#####")
for i in range(3):
    el = run(BASE + [COMP, VTB], URL, profile=prof)
    st = stat()
    out.append("   第%d遍 %5.1fs｜頁%d 字%d 檔%dKB" % (i + 1, el, st[0], st[1], st[2] / 1024))
    print(out[-1])
shutil.rmtree(prof, ignore_errors=True)

el = run(BASE + [COMP, VTB], BLANK_URL)
out.append("##### 啟動底數（近空白頁，同旗標）：%5.1fs｜293 頁樣本 min %5.1fs → 排版占 %.0f%%"
           % (el, base_min, 100.0 * (base_min - el) / base_min))
io_dir = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(io_dir, "spd.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
for f in os.listdir(PR):
    if f.startswith("_probe") or f == "_blank_probe.html":
        os.remove(os.path.join(PR, f))
print("\n".join(out))
