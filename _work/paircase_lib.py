# -*- coding: utf-8 -*-
"""案號之『可檢性』共器（雙子星兩冊）：何謂此冊能找到某案？三形俱是載體——
   ① 卡題 `【案卷 NN】`（可帶『 & M』『雙聯案』之尾巴）；② 表行首格 `| **【案例 NN】事名**`；
   ③ 附錄之索引／矩陣行（其首格即案號）。除此之外之『〔案NN〕』引用，須冠姊妹冊名方不失指。
   兩處用之（刀 `paircases`・尺 `pairrefchk`），單一定義在此，勿各抄。"""
import re

FENCE = "```"
CIT = re.compile(r"〔案例?\s*([0-9]{1,3})〕")
CARD = re.compile(r"【案卷\s*([0-9]+)((?:\s*&\s*[0-9]+)?)[^】]*】")
SUB = re.compile(r"【案卷\s*([0-9]{2}[A-Z])(?:】|[　 ])")     # 子案（心法卷 03A／19A／37A）：不入百二之帳
CELL = re.compile(r"^\|\s*\*\*〔案例?\s*([0-9]{1,3})〔?")
TOC = re.compile(r"^\s*\*\s+\*\*第[一二三四五六七八九十]+章.*〔案([0-9]{1,3})")


def subs(lines):
    """回本冊子案之號（含字母者）——其數字部分**不**得充當百二案之載體。
       管轄唯**卡題之行**（`^#{1,6} 【案卷…】`）：凡例・行文提及子案之名，不算是其卡。"""
    out, fence = set(), False
    for l in lines:
        if l.strip().startswith(FENCE):
            fence = not fence
            continue
        if fence or not re.match(r"^#{1,6}\s*【(?:制度)?案卷\s*[0-9]{2}", l.strip()):
            continue
        for m in SUB.finditer(l):
            out.add(m.group(1))
    return out


def findable(lines):
    """回本冊『有載體』之案號集合，與管轄之引數（尺須自印管轄）。
       子案（『案卷 03A』之屬）只算其卡，不使其數字變成可檢——免以『案 03』誤索於心法卷。"""
    out, fence = set(), False
    for l in lines:
        if l.strip().startswith(FENCE):
            fence = not fence
            continue
        if fence:
            continue
        for m in CARD.finditer(l):
            if l[m.end(1):m.end(1) + 1].isalpha():      # 帶字母者乃子案，其本數不入帳
                continue
            out.add(int(m.group(1)))
            for x in re.findall(r"[0-9]+", m.group(2)):
                out.add(int(x))
        m = CELL.match(l.strip())
        if m:
            out.add(int(m.group(1)))
        if l.strip().startswith("| **〔案例"):
            for x in CIT.finditer(l.split("|")[1]):
                out.add(int(x.group(1)))
    return out


def cites(lines):
    """回 [(行號, 案號, 前文)]——管轄：圍欄外之每一引用。"""
    out, fence = [], False
    for i, l in enumerate(lines):
        if l.strip().startswith(FENCE):
            fence = not fence
            continue
        if fence:
            continue
        for m in CIT.finditer(l):
            out.append((i, int(m.group(1)), l[max(0, m.start() - 14):m.start()]))
    return out


# ── 跨冊案號之約（一處立文，刀・尺・產生器三處同取，勿兩抄）──
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
NOTE_HEAD = "### 一、文獻底冊與引文承諾%s"
NOTE_ITEM = {
    F1: ("7. **跨冊案號之索**：兩冊共用同一百零二案之號。本冊行文引案而本冊無【案卷】卡者，"
         "其判例之全貌在姊妹篇《如法推尋》——以號索其附錄二《判例原典逐條回查索引》即可，"
         "故行文不逐處冠以冊名；本冊自有卡者不在此例。"),
    F2: ("7. **跨冊案號之索**：兩冊共用同一百零二案之號。本冊附錄二即其總帳；"
         "凡判例之心靈解剖（臨床深描）在姊妹篇《起心動念》之【案卷】卡，以號索之即可，行文不逐處冠以冊名。"),
}
DECL = re.compile(r"跨冊案號之索")

# ── 子案之約（第九波・心法卷補三案後立，兩冊各一句，一刀一尺同取）──
NOTE_SUB = {
    F1: ("8. **子案與新增案之號**：本冊另立三則子案——【案卷 03A】阿利吒起惡見不捨・【案卷 19A】偷羅難陀之嫉・"
         "【案卷 37A】畢陵伽婆蹉呼『小婢』，俱是新增之獨立案卷，**不在百零二案之帳內**；"
         "其號後之字母表其序次，不表同案之分支，故行文引『〔案03〕』之類仍當索百零二案之帳於姊妹篇附錄二，"
         "不得指此三卡為其原案。又三案之中，唯 03A 之事本在《四分律》，19A・37A 之情節出律藏相傳、"
         "本地無文，其卡首已各立〔文獻之界〕如實標明，不掛逐字之式樣。"
         "另：姊妹篇《如法推尋》今亦新立三案——【制度案卷 103】亡僧遺物分流・【104】畢陵伽婆蹉受五百守園人・"
         "【105】瞻病次第差，號過百二，同不入其附錄二之帳，檢索勿向彼冊索引求之。"),
    F2: ("8. **子案與新增案之號**：姊妹篇《起心動念》另立三則子案——【案卷 03A】阿利吒起惡見不捨・"
         "【案卷 19A】偷羅難陀之嫉・【案卷 37A】畢陵伽婆蹉呼『小婢』，俱是該冊新增之獨立案卷，"
         "**不入本冊百零二案之帳**，故本冊附錄二《判例原典逐條回查索引》不載其目。"
         "又本冊第十六章今新立三案——【制度案卷 103】亡僧遺物分流・【104】畢陵伽婆蹉受五百守園人・"
         "【105】瞻病次第差，號過百二，是本冊新增之憲政法權大案，**同不入百零二案之帳**，"
         "故附錄二亦不載其三；其律據一依各卡所標之本地卷段，行文引『〔案例 NN〕』之數仍一以百零二案為準。"),
}
SUB_DECL = re.compile(r"子案[與之]")          # 旧稱『子案之號』・新稱『子案與新增案之號』，兩者俱認


def sub_declared(lines):
    return any(SUB_DECL.search(l) for l in lines)


def declared(lines):
    return any(DECL.search(l) for l in lines)


def note_lines(fn):
    """回 (插入錨＝第六律之行首, 新行之全文)——錨唯心法卷作『6. 』，法制卷作『7. 』。"""
    return NOTE_ITEM[fn]
