# -*- coding: utf-8 -*-
"""第 253 輪・刀四～刀六：第六章兩組缺題、卷首目錄之實題對齊、附錄五補一脈經證。

刀四：第六章 第一組・第二組 各只立『（上）』一題（案例 09～15、24～31 悬於『上』題之下，
      與 第三／四／五組之上下分題之制相左）→ 補立兩枚 H2。
刀五：卷首手寫目錄與實題之漂移，逐條依『實題為準』改正（目錄之括注屬描述，留）。
      又削一指空頭目（【篇聚五組導航指針】書中無此題），補兩指實有之目
      （【四大隨身自律行動卡】、第六章各組之上下分題）。
刀六：附錄五補《瑜伽師地論》一條（正文引其逐字而互證表無著），並正目錄对该篇之描述
      （今唯「大乘經論逐字對照」，舊稱「未收典籍如實揭露清單」乃第三十八版附錄F-3 之制，
      三十九版無其節，不可虛列）。

用法：python -X utf8 _work/r253align.py          # dry-run
      python -X utf8 _work/r253align.py apply
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
sys.path.insert(0, ROOT)
import _tk                                                  # noqa: E402  語料與 norm 之法源

V = _tk.norm(_tk.VINAYA)
OTH = _tk.norm(u''.join(_tk.read(f) for f in __import__('glob').glob(
    os.path.join(ROOT, u'佛經', u'**', u'*.txt'), recursive=True)))
for probe, pool, nm in [(u'由慚愧故，能善防護所受尸羅', OTH, u'佛經庫'),
                        (u'知慚愧者得安樂', V, u'本律')]:
    print(u'〔語料核〕『%s…』%s 可查：%s' % (probe[:10], nm, _tk.norm(probe) in pool))

HEAD_INSERT = [
    (u'### 〔案例 09〕洗瘡殺心支', u'## 第一組：根本性罪與不可逆底線（波羅夷法篇·下）\n\n'),
    (u'### 〔案例 24〕慈地無根謗沓婆', u'## 第二組：僧殘重傷與欲望改裝（僧殘法篇·下）\n\n'),
]
TOC_FIX = [
    (u'    * 導言　大樹隱喻體系解剖學定錨與心事背反律（藉事顯心公約）',
     u'    * 導言　大樹隱喻與心事非對稱背反律（解剖學定錨·藉事顯心公約）'),
    (u'    * 【篇聚五組導航指針】', u'    * 【卷首導言：急診室的照鏡法】'),
    (u'    * 第一組·根本性罪與不可逆底線（四大波羅夷及相關判例）',
     u'    * 第一組：根本性罪與不可逆底線（波羅夷法篇·上・下）'),
    (u'    * 第二組·僧殘重傷與欲望改裝（十三僧殘及相關判例）',
     u'    * 第二組：僧殘重傷與欲望改裝（僧殘法篇·上・下）'),
    (u'    * 第三組·資產極簡與物理沒收（三十捨墮及相關判例）',
     u'    * 第三組：資產極簡與物理沒收（捨墮法篇）'),
    (u'    * 第四組·微環境遮防與語言暴力（九十波逸提、提舍尼、眾學法及調部極限裁判）',
     u'    * 第四組：微環境遮防與語言暴力（波逸提法篇·上・中・下）'),
    (u'    * 第五組·僧伽憲政與集體運作（二十犍度相關判例）',
     u'    * 第四組：微環境遮防與威儀細行（提舍尼、眾學法與調部裁判）\n'
     u'    * 第五組：僧伽憲政與集體運作（二十犍度法篇·上・下）'),
    (u'    * 第二節　百則判例快速索引指南（心所／領域／四諍／處分）',
     u'    * 第二節　百則判例四維極速檢索矩陣（心所病相／生活場域／四諍衝突／處分階梯）'),
    (u'    * 第三節　行者夜半四照自省手冊（平心觀受 ➔ 剖思見心 ➔ 穿覆拔面 ➔ 解縛歸家）',
     u'    * 第三節　行者夜半四照自省手冊（軌道乙·觀心專用：平心觀受 ➔ 剖思見心 ➔ 穿覆拔面 ➔ 解縛歸家）'),
    (u'    * 第四節　僧團執事公堂審計表（開庭前置防錯檢核）',
     u'    * 第四節　僧團執事公堂審計表（軌道甲·開庭專用·前置防錯檢核）'),
    (u'    * 第五節　法庭淨空與消磁儀軌（出堂洗心三事）',
     u'    * 第五節　法庭淨空、消磁與歸家（出堂洗心三事·竹筏自捨協議）'),
    (u'    * 第二節　調查實務：舉罪五德面談指針、創傷知情調查、吹哨人反報復盾牌、反靈性煤氣燈操縱令（吸納〔J-1 靈性壓榨案〕）',
     u'    * 第二節　調查實務：舉罪五德、創傷知情調查與吹哨人防禦機制（反靈性煤氣燈操縱令·吸納〔J-1 靈性壓榨案〕）'),
    (u'    * 第三節　人事與勞動：出世僧籍與世俗勞僱雙軌解耦、默擯之勞動法防線、通訊群組正命治理（吸納〔J-3 群組冷暴力案〕）、常住志工防爆SOP',
     u'    * 第三節　人事與勞動：出世僧籍、世俗勞僱與數位正命（雙軌解耦模型·默擯勞動法防線·吸納〔J-3 群組冷暴力案〕）'),
    (u'    * 第四節　財產與數位：寺產借名代持與信託確權三軌、數位資產法相、穿透名義代持與假帳審計（吸納〔J-4 假帳案〕）、長照機構失靈防線（吸納〔J-2 長照耗竭案〕）',
     u'    * 第四節　財產、數位與醫療：信託防禦、穿透審計與長照防線（借名代持與實質受益人審查·吸納〔J-4 假帳案〕〔J-2 長照耗竭案〕）'),
    (u'    * 【道場現代治理合規自檢表】',
     u'    * 【四大隨身自律行動卡】\n    * 【道場現代治理合規自檢表】'),
    (u'  * 四、無事僧的三個日常功課：少事少業、但自觀行、常樂空閑',
     u'  * 四、無事僧的三個日常功課（少事少業、但自觀行、常樂空閑）'),
    (u'  * 附錄四　百則原典回查與基準檢索總表（百則判例大正藏卷段檢索、五大篇聚權威底冊字典）',
     u'  * 附錄四　百則判例原典逐條回查索引（五大篇聚之卷段定位與律典關鍵原句）'),
    (u'  * 附錄五　經論逐字互證表（經論逐字引文、未收典籍如實揭露清單）',
     u'  * 附錄五　經論逐字互證表（大乘經論逐字引文與框架法理對位）'),
]
ROW = (u'| **觀心·慚愧二善護盾** | 《瑜伽師地論》卷四十（玄奘譯） | '
       u'「由慚愧故，能善防護所受尸羅。」 | 與本律卷五十七親宣『知慚愧者得安樂』之法印相對位，'
       u'確立慚愧二善心所為持戒之心理前防。 |')


def main():
    apply = u'apply' in sys.argv[1:]
    lines = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
    text = u'\n'.join(lines)
    n_ins = 0
    for anchor, ins in HEAD_INSERT:
        idx = next((i for i, l in enumerate(lines) if l.startswith(anchor)), None)
        if idx is None:
            raise SystemExit(u'刀四錨點失中：%s' % anchor)
        if ins.strip() in text:
            print(u'刀四：%s 已立，略' % ins.strip()[:24])
            continue
        # 插入點：本卡標題之前（其上為『---』與空行）
        k = idx - 1
        while k > 0 and lines[k].strip() in (u'', u'---'):
            k -= 1
        lines[k + 1:k + 1] = [ins.rstrip(u'\n'), u'']
        n_ins += 1
    print(u'刀四：補立第六章組題 %d 枚' % n_ins)
    text = u'\n'.join(lines)
    n_toc = 0
    for old, new in TOC_FIX:
        c = text.count(old)
        if c == 0 and new.split(u'\n')[0] in text:
            print(u'刀五：已改，略過 ｜%s' % old[:34])
            continue
        if c != 1:
            raise SystemExit(u'刀五錨點命中 %d 次（須恰 1）：%s' % (c, old[:44]))
        text = text.replace(old, new)
        n_toc += 1
    print(u'刀五：目錄隨實題改正 %d 條（共 %d 條）' % (n_toc, len(TOC_FIX)))
    m35 = re.search(u'(?m)^# 附錄五.*$', text)
    m36 = re.search(u'(?m)^# 附錄六.*$', text)
    a5 = text[m35.start():m36.start()]
    if u'瑜伽師地論' in a5:
        print(u'刀六：附錄五已含《瑜伽師地論》，略')
    else:
        rows = [mm for mm in re.finditer(u'(?m)^\\|.*\\|$', a5)]
        last = rows[-1]
        text = text[:m35.start() + last.end()] + u'\n' + ROW + text[m35.start() + last.end():]
        print(u'刀六：附錄五補 1 條（今表行 %d → %d）' % (len(rows), len(rows) + 1))
    print(u'行數 %d → %d' % (len(lines), len(text.split(u'\n'))))
    if not apply:
        print(u'（dry-run，未落檔）')
        return
    io.open(SRC, 'w', encoding=u'utf-8').write(text)
    print(u'已落檔')


main()
