# -*- coding: utf-8 -*-
"""285・記憶（user 層）：第五十八度入 feedback-self-checkers…；索引行同條加尾標。"""
import io

F = u'C:/Users/lionc/.qoder/memory/feedback-self-checkers-must-measure-reality.md'
I = u'C:/Users/lionc/.qoder/memory/MEMORY.md'
ADD = (u'\n\n**第五十八度・折行與重排之器須自證總數；插入之文須自帶行尾；裁語亦須先量**'
       u'（2026-10-26・戒律分析 ver39 第 285 輪）：本輪奉作者親裁放行十六項，三課俱由器現形而非由眼獲。'
       u'① **折行即可能刪文**——以三次 `partition` 把一行圍欄折成三段時，我把中間段（『依第四章第一節』七字）'
       u'丟了：`a1, s1, r1 = ln.partition(m1)` 之後只取 `s1`、`s2` 而忘了第二次 partition 的 `a2`。'
       u'現形之道不是重讀，而是**計數降**：`v39secref` 之節級指針自 38 ➔ 37。'
       u'**通則：凡以文字換文字・折行・重排之器，寫檔前須先斷言『輸入之字元總數＝輸出之字元總數』'
       u'（或逐段保義清單對合，如今輪大圖之『舊圖 49 種【】〔〕（）名相逐一見於新圖，缺一即不寫』）；'
       u'否則折行＝刪文，而全書之尺可能照綠。**'
       u'② **插入之文須自帶分隔**——新 bullet 直接黏在舊 bullet 之後（未附 newline），遂併成一行，'
       u'粗體星號由偶變奇 ➔ v39chk 第 9 目當輪即紅。落刀後之第一件事不是讀 diff，而是**跑形制目**。'
       u'③ **一動形制，先數有幾支器抄其舊形**——本輪三處形制之改（一章一 H1・附錄六改號・原典欄 14➔19），'
       u'牽動六支器同改靶（v39chk 五處・v39linchk・v39volchk・_casedef 之註・r272teeth 三針・'
       u'`_print/build39.py` 之封面自算與號欄不折碼），另加兩處『今十四欄』之自稱載體。'
       u'**口徑：改形制前以 grep 立載體名單，改畢立即全批重跑；封面・凡例・目錄・尺之目名同屬一數之載體。**'
       u'④ **裁語亦須先量，無靶之裁要如實呈**——#37 令『撮述之欄改標律典攝要』，量得 19 欄之引段俱屬逐字宣稱'
       u'且覆核全中（尺二 67 區全中・尺三未標界 0），**無一欄是撮述**➔ 如實呈『無靶可改』，改於凡例立'
       u'『欄題之義』界說（他日純撮述之欄須降標）；#16 令『把臨濟四奪移出判準層級表』，量得表內該行今已作'
       u'『除偏鏡（不入判準層級）』且卷中已有辨正之句➔**判為偽病灶（已是今文），一字未動**。'
       u'外部清單要查證，**作者之裁語同樣要查證**：裁的是病，不是名目；名目已癒而強刀，即造新傷。\n')

S = io.open(F, encoding='utf-8').read()
assert S.count(u'第五十八度') == 0
S2 = S.rstrip(u'\n') + ADD
io.open(F, 'w', encoding='utf-8', newline=u'\n').write(S2)
print(u'第五十八度入檔（%d➔%d 字）' % (len(S), len(S2)))

DO = io.open(I, encoding='utf-8').read()
OLD = u'＋**importlib 直跑被 `sys.exit` 吞輸出＝器之啞非器之綠**'
NEW = (OLD + u'；**五十八度・折行與重排之器須自證總數（三次 partition 丟中間段，賴指針計數降現形）、'
             u'插入之文須自帶行尾（併行則星號成奇）、一動形制先數幾支器抄舊形、裁語亦須先量（無靶之裁如實呈）**')
print(u'索引錨命中 %d' % DO.count(OLD))
assert DO.count(OLD) == 1
io.open(I, 'w', encoding='utf-8', newline=u'\n').write(DO.replace(OLD, NEW, 1))
print(u'索引已加尾標')
