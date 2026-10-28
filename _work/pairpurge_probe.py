# -*- coding: utf-8 -*-
"""第三波『去延伸名相』之靶量：五類逐一查實數、落點、是否入標題（入標題者牽動書籤與指針）。

用法：python -X utf8 _work/pairpurge_probe.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")

GROUPS = {
    "甲・拉丁與西方法學": [
        r"Due Process", r"Res Judicata", r"Estoppel", r"Ultra Vires", r"In Dubio Pro Reo",
        r"Nulla poena", r"Self-Incrimination", r"Fruit of the Poisonous Tree", r"Garantenstellung",
        r"Stare Decisis", r"Cross-Examination", r"Privilege", r"Non bis in idem", r"Class Action",
        r"Beyond a Reasonable Doubt", r"Preponderance of Evidence", r"Void Ab Initio", r"Mobbing",
        r"Workplace Bullying", r"Dissenting Opinion", r"Sikkham", r"Enabling Governance",
        r"正當法律程序", r"正當程序", r"既判力", r"一事不再理", r"疑罪唯輕", r"疑罪從無",
        r"不自[證言].{0,4}罪", r"毒樹之果", r"保證人義務", r"不作為犯", r"先例拘束", r"自白任意性",
        r"預備{0,2}理", r"追訴", r"公訴", r"排除合理懷疑", r"優勢證據", r"證明標準", r"證據能力",
        r"管轄權", r"司法審查", r"救濟", r"上訴", r"終審",
    ],
    "乙・刑警偵訊與法院": [
        r"偵訊", r"偵查", r"檢調", r"檢察", r"搜索票", r"勘驗", r"指紋", r"血跡", r"監視器",
        r"監視影像", r"專案調查官", r"專案小組", r"專案組", r"調查官", r"反詰", r"詰問", r"质证|質證",
        r"傳喚", r"到庭", r"出庭", r"法警", r"法庭记录|法庭記錄", r"卷宗", r"開庭", r"庭審", r"休庭",
        r"隔室視訊", r"單次陳述", r"求聽",
    ],
    "丙・心理學與腦神經": [
        r"前額葉", r"神經脈衝", r"杏仁核", r"多巴胺", r"血清素", r"腦[神经神]|腦路|迴路", r"目標致盲",
        r"Goal[- ]?[A-Za-z]+ Blindness", r"自戀狂怒", r"Narcissistic", r"破罐破摔", r"What[- ]the[- ]Hell",
        r"獎賞迴路|reward", r"煤氣燈", r"Gaslighting", r"創傷知情", r"Trauma-Informed", r"脫敏",
        r"Desensitiz", r"強迫症", r"抑鬱", r"適應障礙", r"PTSD|創傷後壓力", r"心理", r"精神醫學",
        r"情緒", r"認知", r"行為經濟", r"鏡像神經", r"右腦|左腦",
    ],
    "丁・經濟學與政治學": [
        r"尋租", r"Rent[- ]?seeking", r"靈性資本主義", r"Spiritual Materialsm|Spiritual Materialism",
        r"部落主義", r"Tribalism", r"漏斗", r"Funnel", r"非營利組織", r"公共選擇", r"治理",
        r"資本", r"市場", r"經濟學", r"政治學", r"民主", r"獨裁", r"民粹", r"專制",
    ],
    "戊・工業與軍事比喻": [
        r"防空洞", r"消磁", r"Demagnet", r"雷達", r"Radar", r"手術刀", r"防彈", r"堡壘", r"城堡",
        r"重甲", r"鎧", r"武器", r"彈", r"火藥", r"核", r"工程", r"機械", r"工廠", r"生產線",
        r"急診", r"病房", r"醫院", r"免疫", r"疫苗", r"病毒", r"細菌", r"X光|X 光", r"顯微鏡",
        r"顯影", r"解剖", r"外科", r"藥", r"CT|磁振", r"衛星", r"鏡頭", r"螢幕", r"數位", r"電子",
        r"網路|網路|線上", r"雲端", r"晶片", r"AI",
    ],
}
BOOKS = [("F2", F2), ("F1", F1)]
for g, rxs in GROUPS.items():
    print("=" * 78)
    print("■", g)
    for rx in rxs:
        row = []
        for tag, ls in BOOKS:
            hits = [i + 1 for i, l in enumerate(ls) if re.search(rx, l)]
            heads = [i + 1 for i in hits if m.ANY_HEAD.match(ls[i].strip())]
            if hits:
                row.append(f"{tag} 見 {sum(len(re.findall(rx, l)) for l in ls if re.search(rx, l)):3d}"
                           f"・行 {len(hits):3d}" + (f"・標題 {len(heads)}" if heads else ""))
        if row:
            ex = next((l.strip()[:44] for tag, ls in BOOKS for l in ls if re.search(rx, l)), "")
            print(f"  {rx:26s}｜" + "｜".join(row) + f"　例：{ex}")
