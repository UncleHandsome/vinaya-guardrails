# -*- coding: utf-8 -*-
"""第六十一輪前哨：以較廣之簡體字形集掃全書「」『』以外文字，逐條列出待人工分診。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()

# 已在 _tk.py 名單內者不重列；此處補一批常見簡形（多為「異體/古字同形」之高風險形，須人工判）
EXTRA = (u'屡志告回向众刃丰型' .replace(u'志', u'').replace(u'告', u'').replace(u'回', u'')
         .replace(u'向', u'').replace(u'众', u'').replace(u'刃', u'').replace(u'丰', u'')
         .replace(u'型', u''))
EXTRA = u'屡众缘远ynther' .replace('yntherr','').replace('ynth','')
CAND = [u'屡', u'众', u'缘', u'远', u'艺', u'节', u'报', u'类', u'严', u'欢', u'顾',
        u'礼', u'义', u'气', u'丝', u'乱', u'亏', u'于', u'云', u'亩', u'亲', u'仆',
        u'从', u'仓', u'仪', u'价', u'众', u'优', u'会', u'伞', u'体', u'余', u'佛'.replace(u'佛', u''),
        u'佣', u'佞', u'伪', u'怜', u'悯', u'罗', u'罚', u'罢', u'职', u'聪', u'肃', u'胀',
        u'脉', u'脑', u'舰', u'沧', u'没', u'为', u'丽', u'举', u'艺', u'艰', u'芦', u'苏']
CAND = sorted(set(CAND))
plain_spans = []
for m in re.finditer(u'「[^」]*」|『[^』]*』', DOC):
    plain_spans.append(m.span())

def in_quote(i):
    return any(a <= i < b for a, b in plain_spans)

hits = {}
for i, ch in enumerate(DOC):
    if ch in CAND and not in_quote(i):
        hits.setdefault(ch, []).append(DOC[:i].count('\n') + 1)

out = []
out.append(u'候補之簡形（引號外）')
for ch in CAND:
    if ch in hits:
        out.append(u'  %s U+%04X  %d 處  行:%s' % (ch, ord(ch), len(hits[ch]), hits[ch][:8]))
out.append(u'')
out.append(u'全書高頻漢字中、形而簡於繁體對應者之粗篩（前 40 由人工看）')
# 列出全書所有非引號字之中，屬於「簡化字專用」者：以一套 wide 名單
WIDE = (u'个們來這對經視見請許設讓還錢鐵傳遞記錄舉處聲復斷書馬鳥魚東風飛當應專長陽陰隊階陣陸隨難極樣類產無為說變關邊鐘電'
        u'场尽显汇词虚数量断准闭张线据写转头页顾悬闻术单号拥护报读摄点样构备审议识误剧别到制复梦奖将专业丛东丝两严丧个'
        u'临丽举义乐习书买亚产亲仅从仓仪们价众优伞传估余佛作物状猎现环生命单厂历双发变只台号同后员周和叹吗呢员则刚'
        u'别创利删剂劝势单卫厂双变恋恼悬惊惧惯愿慎成战户所担指据排掌插搜摄支收敌数文断新无旧时显晓暂术机权条来极构'
        u'枢枪标树样档检梦欢毁毕气汇汉沟没泽治准凉减凑凛凤凳刘击分历剧劝办务动协占卢卫叙厅发变口只台号叶各合向吗员'
        u'问间队阶际陆陈险隐难雏电须顶顾题颜风飞食饭馆马驶验骤欢欧殡歼殁残殒殓没沙泽净济浏浅涨渐温湿温满滤灯灵灾'
        u'炼热爱牵状犹狮独狱猎玛环现珑璃电画疗疯痈皱盘盖监盘真睁着矣矣知码砖研确碍礼祖视览觉誉计划让识译财类粮紧'
        u'纠红级纪纯纲纳纵纷线练织终经结给络统继绩维综绿缓缩网罗罚罢职联聪肃肤肿胀胆胁脉脑舰舱艰范荐荣药莱获营蓝'
        u'虑虚虫蚀蛮补袭衬见观规视览觉言罚罢职据划为灭炉悬门')
seen = {}
for i, ch in enumerate(DOC):
    if ch in WIDE and not in_quote(i):
        seen.setdefault(ch, []).append(DOC[:i].count('\n') + 1)
for ch in sorted(seen):
    out.append(u'  %s U+%04X %3d 處 %s' % (ch, ord(ch), len(seen[ch]), seen[ch][:6]))
txt = '\n'.join(out)
open(os.path.join(HERE, 'simp61.txt'), 'w', encoding='utf-8').write(txt)
print('written', len(seen))
