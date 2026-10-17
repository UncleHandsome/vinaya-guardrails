# -*- coding: utf-8 -*-
"""擬補入簡形閘口之字表，先驗其於書中（引號外）是否零見。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
doc = io.open(MD, encoding="utf-8").read()
plain = re.sub(r"「[^」]*」|『[^』]*』", "", doc)
ADD = ("对观击强层纲摄织纪则称显报轮结册没员确级统义习违连续归场众审计时业丛"
       "压历参双发怀态总悬愿战据觉绝艺节镜竞净迈独类变让关门开圆图书产经网络"
       "极叠听启职位? ".replace("?", "").replace(" ", ""))
ADD = "".join(dict.fromkeys(ADD))
bad = [c for c in ADD if c in plain]
print("擬補 %d 字；引號外實見者：%s" % (len(ADD), "".join(bad) or "無"))
for c in bad:
    i = plain.find(c)
    print("  %s → …%s…" % (c, plain[max(0, i - 16):i + 14].replace("\n", " ")))
