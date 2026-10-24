# -*- coding: utf-8 -*-
"""268 輪・帳五：使用者層回饋檔附一節（負測判式之升級・名冊須配實物・附加式 patch 之反形）。"""
import io
import os

P = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'memory',
                 u'feedback-self-checkers-must-measure-reality.md')
ADD = u"""
**第卅六度（2026-10-20，戒律分析第 268 輪：負測之判式要昇一級——『報錯』不等於『逮得』）**：新立一把『括號命題須落於所靶之節』的尺，做負測時發現：**只查『有 ✗ 行』會放過一張指錯家的尺**。三道植病各須點名**真正該去的那一節**才算逮（植回上輪那枚幽靈 ➔ 必須報『⟶ 第三章・閘門三』；移靶他章 ➔ 必須點名原家）。判式由此改定：**失敗要帶著『正確答案』出現，否則它只是叫了一聲**。同輪三則：
① **檢『編號存否』者，从不檢『編號之內容對否』**——第 10 目歷輪全綠，因為它只問『第二章第四節存不存在』；而書上的錯是把**屬於第三章的文字掛在第二章**，節號俱在，舊尺天生無感。**每讀一條『A 存在否』之檢，當場問它的孿生兄弟『A 裡住的是不是 A 的東西』由誰守**。
② **名冊（清單）本身要跑一次『每項配得著實物』**：記憶層的『尺群名冊』被我寫成 `r268simp.py`，而實檔是 `r267simp.py`——幽靈檔名與幽靈篇題同形（第十八度『以檔名為鍵之清單於改名時無聲失效』之**自我版**：这次失真的是我自己的工具清冊）。做法：把名冊與 `os.path.exists` 對一次，報缺失數（本輪：32 檔・缺失 0）。
③ **附加式 patch 的反向誤報**：我的寫後斷言寫成 `count(old)==0`，而 new 串把 old 含在內（附加式），於是**檔已寫對而斷言炸出 AssertionError**。此即檔上舊誡『new 含 old 會騙過已套偵測』之**鏡像形**：同一條子有兩面——偵測『已套』不可只看 old 不在，斷言『成功』亦不可要求 old 歸零。**正確判式：count(new)==期望數，且 count(old)==（new 內所含 old 的次數）× 套用次數**。凡斷言失败先回讀實態再判是病是器（本輪即靠回讀證明八項俱已落地，未把一次成功寫成失敗）。
④ 又犯二項舊誡，如實記：**在 shell 字串裡帶反引號**（含反引號的中文被命令替換掉，見 [[no-backticks-in-shell-command-strings]]）；**憑改後的記憶檔直接續跑而不回讀**（檔被我改過、old 已不在，乾跑報『錨不合 15』實為『已套用』之據——要讀實態，不能讀乾跑）。參 [[project-round31-state]]、[[prefer-self-healing-over-hand-rigor]]。
"""
t = io.open(P, encoding=u'utf-8').read()
if ADD[:40] in t:
    print(u'（本節已在檔內，未重複附入）')
    raise SystemExit(0)
io.open(P, 'a', encoding=u'utf-8', newline=u'').write(ADD)
chk = io.open(P, encoding=u'utf-8').read()
print(u'已附入・檔內行數 %d・命中 %d' % (len(chk.split(u'\n')), chk.count(u'第卅六度')))
