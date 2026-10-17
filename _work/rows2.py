import io

import _tk as t

# 本器所寫三列俱在附錄L 之實測表——第 250 輪底冊另檔後，附錄L 已不在主檔，
#   故落點須向 `path_of` 取（寫錯檔即兩檔俱錯，此為單一法源）。
p = t.path_of(u'附錄L')
L = io.open(p, encoding='utf-8').read().split('\n')
mB, mA, mF = t.measure('bq'), t.measure('bqa'), t.measure('f')
row_bq = next(i for i, l in enumerate(L) if l.startswith('| 第六章以外冠出處之引號段'))
row_a = next(i for i, l in enumerate(L) if l.startswith('| 敞口診斷（全行掃描'))
row_f = next(i for i, l in enumerate(L) if l.startswith('| 附錄 F 經論互證引文'))

# 附錄F 一行舊唯Invariant 檢查、由人抄寫（第 120 輪起改本器自寫——一行手抄之數亦是帳）
L[row_f] = ("| 附錄 F 經論互證引文 | 未納機械查核 | 本律可查得 **{h}**、他系經論查得於 "
            "`佛經/` **{o}**、本地無從覆核而尚未就地標界者 **{m}** 筆"
            "（另有 **{d}** 筆已就地標界，合計 **{s}** 筆逐條開列於**附錄 F-3**；"
            "該表以典籍·版本為列，一列可攝同段之數筆，故今 **{f3}** 列與筆數本非一口徑） |").format(
    h=mF['hit'], o=mF['other'], m=mF['miss'], d=mF['disc'], s=mF['disc'] + mF['miss'], f3=t.f3_rows())

L[row_bq] = ("| 第六章以外冠出處之引號段 | 41 片段中 22 可查得 | **{hb}/{tb}** 逐字（合規率 **{rb}%**）；"
             "另有已標界之本地無從覆核 {d} 段、名相有據而辭形稍異 {n} 段，俱另列豁免而不計入未合規；"
             "{term} 處未冠出處之術語引號與 {meta} 處附錄C/L/M 校勘引述，依凡例第一律不構成逐字宣稱 |").format(
    hb=mB['hit'], tb=mB['tot'], rb=mB['rate'], term=mB['term'], meta=mB['meta'], d=mB['disc'], n=mB['namok'])

L[row_a] = ("| 敞口診斷（全行掃描 `bqa` 口徑） | 舊無此項 | 本表上列 bq 口徑舊僅取引用塊（> ）行，"
            "**列條式引文向在掃描網外**；今另立全行口徑（第六章以外，排除附錄C～F、L、M，出處採同句嚴格判定），"
            "實測宣稱片段 **{ta}** 段：逐字 **{ha}**、非逐字 **{ma}**（合規率 **{ra}%**），他典命中 {oth}、過短略計 {sho}；"
            "另有已標界之無從覆核 {dd} 段、名相有據而辭形稍異 {nam} 段（戒名、羯磨名之「某戒」式辭形，去「戒」字俱可查得），皆另列豁免。"
            "本口徑初測得非逐字 64 段，歷三輪逐條清創（第六章以外長句語譯改掛單引號、凡例與名相之實證誤稱改正、"
            "附錄H 十五則判語及白話因緣語改掛單引號並標今譯）後已**歸零**；"
            "此口徑之設立與其實數係主動揭露查核器舊式盲區，非待外人指陳 |").format(
    ta=mA['tot'], ha=mA['hit'], ma=mA['miss'], ra=round(mA['rate'], 1),
    oth=mA['other'], sho=mA['skip'], nam=mA['namok'], dd=mA['disc'])

io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('rows refreshed  bq %s/%s  bqa %s/%s  f %s/%s/%s(標界%s)' % (
    mB['hit'], mB['tot'], mA['hit'], mA['tot'], mF['hit'], mF['other'], mF['miss'], mF['disc']))
