# -*- coding: utf-8 -*-
# r232lnk　校勘記所引行號之今量（刀後一律重指，勿沿刀前之數）
import io
import os

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
L = io.open(MD, encoding=u'utf-8').read().split(NL)


def cjk(s):
    return sum(1 for c in s if u'一' <= c <= u'鿿')


Q = [
    (u'捨別住定文（兩處）', u'我某甲比丘，今捨別住'),
    (u'三階欄之新指', u'**【第二節 軌道甲·公堂審計表】'),
    (u'內文分工二行', u'翻開【第三節 軌道乙·十六觀心問】'),
    (u'道岔六徽章', u'【道岔六：移轉管轄】'),
    (u'存檔卡提舍尼', u'[ ] 波羅提提舍尼（可呵法·向彼悔）'),
    (u'卡三圍欄首', u'【行動卡三：禁語防護自律卡（反靈性煤氣燈操縱）】'),
    (u'卡四勞法新行', u'· 受薪人員被移出者：移除群組與系統權限屬工作條件'),
    (u'導言兩問', u'不列入日用『夜半四問』之速檢'),
    (u'九章四節三款', u'終止契約之意思表示'),
    (u'九章四大禁言首', u'『你拿戒尺量人'),
    (u'本節卸下法條', u'本節卸下沉重的法條'),
    (u'提舍尼篇聚', u'法定唯得向一位清淨比丘對首悔過'),
    (u'突吉羅對首責心', u'突吉羅依輕重行對首發露或責心悔過'),
    (u'八問首行', u'我此心染淨何如'),
    (u'問九俗白', u'洗淨自己的嘴巴與心肝'),
    (u'三事標題', u'封存案卷，語業歸零'),
    (u'消磁標題二', u'撤除公堂，出坡洗心'),
]
for nm, s in Q:
    print(u'%-18s %s 見｜L%s' % (nm, sum(1 for x in L if s in x),
                                 [i + 1 for i, x in enumerate(L) if s in x][:5]))
nine = [i for i, x in enumerate(L) if u'『你拿戒尺量人' in x or u'『萬法皆空，這點金錢' in x
        or u'『法尚應捨，你咬住制度' in x or u'『我們要如草覆地' in x]
print(u'九章禁語四條：L%s' % [i + 1 for i in nine if i > 9900])
print(u'八問之十行今屬 L%s' % [i + 1 for i, x in enumerate(L)
                             if u'正理' in x and u'：' in x and u'「我' in x][:12])
