# -*- coding: utf-8 -*-
"""依『新版終極修正指南』之分流台帳，實測兩冊今形之覆蓋與缺口（只讀不改）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = Path(r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments"
             r"\81d8a717-89a8-40b2-bce9-de0f4d4d91cc\3bf01ebf-ec20-47ec-b582-3b41be4447c3.txt")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
G = GUIDE.read_text(encoding="utf-8")

CH = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十百]+章[　 ]+\S.*)$")


def chapters(lines):
    return [m.group(1).strip() for l in lines if (m := CH.match(l.strip()))]


def cnt(lines, rx):
    return sum(1 for l in lines if re.search(rx, l))


print("■ 章題對合（指南所定 vs 今冊實有）")
g1 = re.findall(r"\*\*第([一二三四五六七八九十]+)章 ([^*]+)\*\*", G)
g2 = re.findall(r"\*\*第([一二三四五六七八九十]+)章 ([^*（]+)", G)
a1, a2 = chapters(F1), chapters(F2)
print(f"  指南第二篇列章 {len(g1)}・第三篇列章 {len(g2)}；今 F1 {len(a1)} 章・F2 {len(a2)} 章")
print("  F1 今章題：")
for t in a1:
    print("     ", t[:52])
print("  F2 今章題：")
for t in a2:
    print("     ", t[:52])

print("\n■ 副標與心印")
print("  指南宣稱副標：", set(re.findall(r"《起心動念：([^》]+)》", G)))
print("  今 F1 書名行：", next(l for l in F1 if l.startswith("# 《"))[:60])
print("  指南 F2 終局心印『和』今見：", cnt(F2, r"心印.*「 ?和 ?」|「 ?和 ?」"), "・『案結諍平』", cnt(F2, r"案結諍平"))
print("  F1 終局心印『歇』今見：", cnt(F1, r"「 ?歇 ?」"))

print("\n■ 分流資產之歸位實測（指南所派 vs 兩冊今見）")
probes = {
    "三十二字略戒心印": (r"三十二字略戒", r"三十二字略戒"),
    "五遍行": (r"五遍行", r"五遍行"),
    "三階思/三時心": (r"三階思|三時心", r"三階思|三時心"),
    "四根本煩惱換裝": (r"換裝", r"換裝"),
    "十一善心所": (r"十一善心所", r"十一善心所"),
    "夜半四照": (r"夜半四照", r"夜半四照"),
    "四大神聖邊界": (r"四大神聖邊界|四大.*邊界", r"四大神聖邊界"),
    "六重心智閘門": (r"六重心智閘門|閘門[一二三四五六]", r"六重心智閘門|閘門[一二三四五六]"),
    "自言治": (r"自言治", r"自言治"),
    "別住/意喜/摩那埵": (r"別住|摩那埵|意喜", r"別住|摩那埵|意喜"),
    "二十大僧出罪": (r"二十大僧|阿浮呵那", r"二十大僧|阿浮呵那"),
    "七滅諍/四諍": (r"七滅諍|四諍", r"七滅諍|四諍"),
    "三線模型IIA": (r"三線(治理)?模型|IIA", r"三線(治理)?模型|IIA"),
    "現01〜現04": (r"現0[1-4]", r"現0[1-4]"),
    "調部十五則": (r"調部疑難判例法理專題|調部專題|專題 ?1[0-5]|專題 ?0[1-9]", r"同左"),
    "執事公堂審計表": (r"執事公堂審計表|公堂審計表", r"公堂審計表"),
    "自然人心證四署": (r"四署", r"四署"),
    "草覆地": (r"草覆地", r"草覆地"),
    "提婆達多破僧": (r"提婆達多", r"提婆達多"),
    "耶舍七百結集": (r"耶舍", r"耶舍"),
    "拘睒彌大諍": (r"拘睒彌", r"拘睒彌"),
    "富羅那異議": (r"富羅那", r"富羅那"),
    "泉水停供(案98)": (r"泉水", r"泉水"),
    "高勝受託(案91)": (r"高勝", r"高勝"),
    "金布祇園(案97)": (r"金布", r"金布"),
    "結界大界標相": (r"大界標相", r"大界標相"),
    "與欲代理": (r"與欲", r"與欲"),
    "十三難": (r"十三難", r"十三難"),
    "胎月折算": (r"胎月", r"胎月"),
    "寺產代持/UBO": (r"代持|實質受益人|UBO", r"代持|實質受益人|UBO"),
    "長照防線": (r"長照", r"長照"),
    "創傷知情/吹哨人": (r"創傷知情|吹哨", r"創傷知情|吹哨"),
    "勞動雙軌": (r"勞僱|勞動法", r"勞僱|勞動法"),
    "凡例（文獻體例）": (r"凡例", r"凡例"),
    "五層顯微模型": (r"五層顯微模型", r"五層顯微模型"),
    "五層法理案卷": (r"五層法理|法理判例案卷", r"五層法理|法理判例案卷"),
}
print(f"  {'資產':22} F1 行見   F2 行見")
for k, (rx1, rx2) in probes.items():
    rx = rx1 if rx1 != "同左" else rx2
    print(f"  {k:22} {cnt(F1, rx):>5}      {cnt(F2, rx):>5}")

print("\n■ 案例主號戶口")
c1 = sorted({int(x) for x in re.findall(r"[〔\[]案(?:卷|例) ?(\d{1,3})", "\n".join(F1))})
c2 = sorted({int(x) for x in re.findall(r"[〔\[](?:制度)?案卷 ?(\d{1,3})", "\n".join(F2))})
print("  F1 案卷號：", c1, f"（共 {len(c1)} 主號）")
print("  F2 制度案卷號：", c2, f"（共 {len(c2)} 主號）")
print("  F1 斜線次碼形：", cnt(F1, r"/ ?[遮僧開]\d"), "・F2 斜線次碼形：", cnt(F2, r"/ ?[遮僧開]\d"))

print("\n■ 內部實驗室殘跡（公開書不宜之自指）")
lab = {
    "ver3x 版次字樣": r"ver\s*3[0-9]|Ver3[0-9]|第 ?3[0-9] ?版|三十九版",
    "大正藏/冊號": r"大正藏|T\d{2,3}n\d{3,4}|CBETA",
    "附錄四/附錄六（框架冊附錄名）": r"附錄[一二三四五六七八九]",
    "台帳/定位行/指針（工程語）": r"台帳|定位行|矩陣之靶|尺目|負測",
    "本地卷段/本地實測（校勘語）": r"本地卷段|本地實測|本地無文|本律無文",
    "書中自制之凡例宣稱": r"書中自制|本冊不立|本書自制|讀者切勿混同",
}
for k, rx in lab.items():
    h1, h2 = cnt(F1, rx), cnt(F2, rx)
    print(f"  {k:30} F1 {h1:>4}・F2 {h2:>4}")
    for nm, L in (("F1", F1), ("F2", F2)):
        hits = [(i + 1, l.strip()) for i, l in enumerate(L) if re.search(rx, l)][:3]
        for i, l in hits:
            print(f"        {nm} L{i}: {l[:62]}")

print("\n■ 紀律三・每章呼吸口（林下留白／道場消磁）")
for nm, L, chs in (("F1", F1, a1), ("F2", F2, a2)):
    br = cnt(L, r"林下留白|急診室】|消磁|出堂|走齬|留白：")
    per = {}
    cur = None
    for l in L:
        if (m := CH.match(l.strip())):
            cur = m.group(1)[:14]
            per.setdefault(cur, 0)
        elif cur and re.search(r"林下留白|消磁|出堂|留白：", l):
            per[cur] += 1
    zero = [k for k, v in per.items() if v == 0]
    print(f"  {nm}：呼吸口行見 {br}・章數 {len(per)}・無呼吸口之章 {len(zero)} 個 {zero}")

print("\n■ 指南自身之脚手（背景檔亦係 AI 產物，未據為正文）")
print("  指南內『下一次對話預告/遵命/請隨時發出指令』行見：",
      len(re.findall(r"下一次對話預告|遵命|請隨時發出指令|我們即刻進入", G)))
