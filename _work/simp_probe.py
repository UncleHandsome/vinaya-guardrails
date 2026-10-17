# -*- coding: utf-8 -*-
"""簡形漏洞探針：以一份「繁體正書絕不會出現」之常見簡形候選表掃全檔（或新稿段落），
   語料自有之形一律擲除（免把混形當病灶），只報『書中有、語料無、而 `_simpdict` 未收』者——
   即字典之盲區。`simp_sweep` 報 0 只是『字典之 0』，此尺報的才是『書之 0』。
用法：python -X utf8 _work/simp_probe.py [檔] [--only=起,迄]（行範圍，1 起算）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from _simpdict import MAP  # noqa: E402

BOOK = HP.SRC

# 候選：常見簡體專用形→繁體正字。只作『探針』不作『歸形』——命中一律人工判讀後方改，
# 因个别形（后・干・云・厉・适・折・征）於古典自有其合法用法，不可由表直斷。
CAND = (
    u"关员边办为书买传众优会的伟伦侧侦债倾储尽显术机权条来杨极枪柜标栏树样检楼欢欧歼毕"
    u"汇汉沟没济测涛湿满滤炉灾独狮猎献环现电画疗疯盘确碍礼祸种称积竞笔简类粮紧纠红级纪"
    u"纯纳纸线练组细织终经绑结绕绘给络绝统继绩续维绵综绿缓编缘缩职联聪肠肤脑脸临举艰艺"
    u"节苏范荣药获营悬区医华单卖卫厂厅历压厌双变恋复忧态壮声壳处对导尔尘层当专义习乡亏"
    u"产亲亿从仓仪宠审宪宫悦战护抛扰拟拥择挂摄数敌无晓乱块夸迟额饱蚀败验种属余闭闻阶陆"
    u"陈险隐难须饭饮饰馆马驱驶骗鱼鲜鸟鸡麦黄龄笼签国图圆坏坛场坝执扩抚执"
    u"与乐几论测较则张离着户办沉后台干伙围绕镜轻账轮胆价师饮别个谁为体毁"
)
TPAIR = {}
for k, v in MAP.items():
    TPAIR[k] = v

f = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else BOOK
t = io.open(f, encoding="utf-8", errors="ignore").read()
only = [x for x in sys.argv if x.startswith("--only=")]
if only:
    a, b = only[0][7:].split(",")
    L = t.split("\n")
    t = u"\n".join(L[int(a) - 1:int(b)])
corp = u"".join(io.open(p, encoding="utf-8", errors="ignore").read() for p in glob.glob(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"原文", u"*.txt")))

bad = []
for c in sorted(set(CAND)):
    if c in TPAIR or corp.count(c):
        continue
    n = t.count(c)
    if n:
        bad.append((c, n, t.find(c)))
print(u"%s｜候選 %d 字（已剔字典所收 %d 與語料自有者）｜書中見而字典未收：%d 種 %d 處"
      % (os.path.basename(f), len(set(CAND)), len(TPAIR), len(bad), sum(x[1] for x in bad)))
for c, n, i in bad:
    seg = t[max(0, i - 20):i + 20].replace(u"\r\n", u"").replace(u"\n", u"/")
    # 碼位必附：終端／渲染層會把若干繁體字顯示成簡體形（關→关、辦→办），只憑肉眼判形必誤。
    print(u"  %s U+%04X ×%d｜…%s…" % (c, ord(c), n, seg))
