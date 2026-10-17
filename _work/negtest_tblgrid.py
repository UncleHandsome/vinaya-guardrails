# -*- coding: utf-8 -*-
"""負測：把 \\x01 重新注入一份暫存 HTML，印成暫存 PDF，驗 _work/tblgrid.py 逮不逮到散架。
   逮不到即代表此軸是假綠；逮到則證其確有偵測力。暫存檔一律自刪。"""
import os, subprocess, sys, tempfile, time
import importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRINT = os.path.join(ROOT, '_print')

spec = importlib.util.spec_from_file_location('tblgrid', os.path.join(HERE, 'tblgrid.py'))
tg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tg)

src = os.path.join(PRINT, 'final38.html')
neg_html = os.path.join(HERE, '_neg38.html')
neg_pdf = os.path.join(HERE, '_neg38.pdf')
html = io_open = open(src, encoding='utf-8').read()
n = html.count('<table class="keep">')
html = html.replace('<table class="keep">', '<table' + chr(1) + ' class="keep">')
open(neg_html, 'w', encoding='utf-8').write(html)
print(u'注入 %d 處（模擬第 105 輪之病）' % n)

BR = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
      r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
      r'C:\Program Files\Google\Chrome\Application\chrome.exe']
browser = next((b for b in BR if os.path.isfile(b)), 'msedge')
prof = tempfile.mkdtemp(prefix='neg-profile-')
if os.path.exists(neg_pdf):
    os.remove(neg_pdf)
t0 = time.time()
subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-first-run',
                '--no-default-browser-check', '--disable-extensions',
                '--user-data-dir=' + prof, '--no-pdf-header-footer',
                '--print-to-pdf=' + neg_pdf,
                'file:///' + neg_html.replace('\\', '/')], cwd=PRINT, timeout=900)
# 落盤等待：窗須大於實測落盤時間（第 119 輪量得 33～51 秒，舊三十秒窗必誤判——
# 與 build38.render_pdf 同一病，兩處同改；此處不求省時，只求真等得到）
last, same = -1, 0
_dead = t0 + float(os.environ.get("RENDER_WAIT", "300"))
while time.time() < _dead:
    try:
        sz = os.path.getsize(neg_pdf)
    except OSError:
        time.sleep(0.25)
        continue
    if sz == last and sz > 0:
        same += 1
        if same >= 3:
            break
    else:
        same = 0
    last = sz
    time.sleep(0.25)
print(u'暫存列印完成：%d 秒、%d KB' % (time.time() - t0, os.path.getsize(neg_pdf) // 1024))

tot, bad, unk, ok, lost = tg.check(neg_html, neg_pdf)
print(u'負測結果：表 %d｜格線確認 %d｜散架 %d｜缺字 %d｜待考 %d' % (tot, ok, len(bad), len(lost), len(unk)))
for b in bad[:5]:
    print(u'   逮到 表%02d 頁 %d「%s」%s' % (b[0], b[2], b[3], b[4]))
for b in lost[:5]:
    print(u'   缺字 表%02d「%s」%d 格' % (b[0], b[2], b[3]))
os.remove(neg_html)
os.remove(neg_pdf)
import shutil as _sh
_sh.rmtree(prof, ignore_errors=True)
print(u'判定：%s' % (u'此軸有效（能逮散架）' if bad else u'此軸假綠——逮不到，須改驗法'))
sys.exit(0 if bad else 1)
