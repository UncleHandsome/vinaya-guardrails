# -*- coding: utf-8 -*-
"""附錄三・乙部之补齐：比丘尼八悔過法・百眾學法・七滅諍法（合 115 號）。

法源：律藏原文 `原文/22-30 原文.txt` 尼犍度收束段（『一百七十八波逸提法竟』→『如乞酥無異』→
『下眾學戒與大僧戒無異，故不出耳』）。舊源冊謂此三組『律但云如前、不逐條別宣』——查其實：
眾學・滅諍二組確不別宣（律有明文），八悔過則**有制戒因緣與結戒文**，其第2～8號以一句列目。
故依律實況登號：有文者逐字引（自語料切片，不手打），無文者標其所依，不強造戒文。
"""
import io
import os
import re

A_END178 = u'一百七十八波逸提法竟'
A_JIE = u'若比丘尼，不病乞酥食者'
A_BIAN = u'彼比丘尼，無病而乞酥食'
A_MU = u'乞油'
A_MU_END = u'如乞酥無異'
A_ZHU = u'上四戒'


def ni_block(root):
    """自律藏原文取尼犍度收束段，回结戒文・辯相・七目句・律注。斷錨即停，不產空表。"""
    p = os.path.join(root, u'原文', u'22-30 原文.txt')
    L = io.open(p, encoding='utf-8', errors='ignore').read().replace(u'\r\n', u'\n').split(u'\n')
    i = next(k for k, l in enumerate(L) if A_END178 in l)
    seg = u'\n'.join(L[i:i + 24])
    jie = re.search(A_JIE + u'.*?是名悔過法。', seg)
    bian = re.search(A_BIAN + u'.*?波羅提提舍尼。', seg)
    mu = re.search(A_MU + u'[^。]*' + A_MU_END + u'。', seg)
    zhu = re.search(u'[（(]' + A_ZHU + u'[^）)]*[）)]', seg)
    if not (jie and mu and zhu):
        raise SystemExit(u'尼犍度收束段斷錨：結戒=%s 七目=%s 律注=%s'
                         % (bool(jie), bool(mu), bool(zhu)))
    body = mu.group(0)[:mu.group(0).index(A_MU_END)]
    items = [u'酥']
    for piece in re.split(u'[，、]', body):
        piece = piece.replace(u'若', u'').strip().rstrip(u'。')
        if not piece:
            continue
        items.append(piece[1:] if piece.startswith(u'乞') else piece)
    return {'jie': jie.group(0), 'bian': bian.group(0) if bian else u'',
            'mu': mu.group(0), 'zhu': zhu.group(0).strip(u'（）()'), 'items': items}


def _sec(raw, key):
    lines = raw.split(u'\n')
    i = next((k for k, l in enumerate(lines) if l.startswith(u'## ') and key in l), None)
    if i is None:
        raise SystemExit(u'源冊附錄無此組：%s' % key)
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith(u'## ')), len(lines))
    return lines[i + 1:j]


def _rows(raw, key):
    out = []
    for l in _sec(raw, key):
        m = re.match(r'^\s*(\d+)(?:[～~](\d+))?\.\s', l)
        if m:
            out.append((int(m.group(1)), int(m.group(2) or 0), l.rstrip()))
    if not out:
        raise SystemExit(u'源冊此組無歷條：%s' % key)
    return out


def _span(rows):
    """一組實幾號：『N～M.』之段計其長，單號計一。"""
    return sum(b - a + 1 if b else 1 for a, b, _ in rows)


def _ptr(line):
    m = re.search(u'｜書中：(.*)$', line.strip())
    return m.group(1).strip() if m else u'－'


def groups(raw, root):
    """乙部三組全文（指針仍用源冊口徑，交由 relink 落地）。"""
    nb = ni_block(root)
    o = []

    o.append(u'## 乙、比丘尼戒本：八悔過法（波羅提提舍尼）（戒本 8 條，律文別宣 1 條｜'
             u'其第2～8號律以一句列目，云『如乞酥無異』）')
    o.append(u'')
    o.append(u'律於尼犍度收束處先別結乞酥一戒，再以一句次及其餘七物：『%s』——'
             u'故八號之中唯第一號有別結之文，二至八號但依所列之物登號。' % nb['mu'])
    o.append(u'')
    o.append(u'1. 「%s」　｜書中：－' % nb['jie'])
    for n in range(2, 9):
        it = nb['items'][n - 1] if n - 1 < len(nb['items']) else u''
        o.append(u'%d. 乞%s（律以一句列目，云『如乞酥無異』——結戒文與悔過之式俱同第一號，不別宣）　｜書中：－'
                 % (n, it))
    o.append(u'')
    if nb['bian']:
        o.append(u'結罪之相：「%s」' % nb['bian'])
    o.append(u'律注：「%s」' % nb['zhu'])

    jia100 = _rows(raw, u'甲、比丘戒本：百眾學法')
    o.append(u'')
    o.append(u'## 乙、比丘尼戒本：百眾學法（式叉迦羅尼）（戒本 %d 條，律文別宣 0 條｜'
             u'律注明文『下眾學戒與大僧戒無異，故不出耳』，號位一一同甲部）' % _span(jia100))
    o.append(u'')
    o.append(u'此百條非尼眾另製，乃大僧學法之全數移用；律既不出其文，本表亦不強造，'
             u'但依號登位，『書中』一欄即甲部同號之解剖處——讀尼眾此號，即讀大僧同號。')
    o.append(u'')
    for a, b, line in jia100:
        head = u'%d～%d' % (a, b) if b else u'%d' % a
        o.append(u'%s. （與大僧同制，律不出——即甲部百眾學法第%s號）　｜書中：%s'
                 % (head, head, _ptr(line)))

    jia7 = _rows(raw, u'甲、比丘戒本：七滅諍法')
    o.append(u'')
    o.append(u'## 乙、比丘尼戒本：七滅諍法（戒本 %d 條｜七法乃滅諍之程序，二部同之，更無別宣）'
             % _span(jia7))
    o.append(u'')
    o.append(u'滅諍不以『若比丘尼…』之禁語立文，而以七種程序為法；律於尼眾別制『不為滅諍』之波逸提'
             u'（有比丘尼共諍，詣偷羅難陀求為滅諍而竟不為滅，遂致彼休道），其七法之名目與處斷一一如甲部。')
    o.append(u'')
    for a, b, line in jia7:
        head = u'%d～%d' % (a, b) if b else u'%d' % a
        m = re.match(r'^\s*\d+(?:[～~]\d+)?\.\s*(.*?)\s*｜', line)
        o.append(u'%s. %s（二部同此七法，更無別宣）　｜書中：%s'
                 % (head, m.group(1) if m else u'', _ptr(line)))
    return u'\n'.join(o)


def insert(raw, root):
    """三組插到『## 甲、比丘戒本：七滅諍法』之前，俾甲部末組仍收全表。"""
    anchor = u'## 甲、比丘戒本：七滅諍法'
    i = raw.index(anchor)
    return sum_claim(raw[:i] + groups(raw, root) + u'\n\n' + raw[i:])


def fix_claim(raw):
    """源冊『本表乙部列 233 號……本表不另立號』一句今須改實（乙部已列足 348）。"""
    m = re.search(u'至通數之別：[^\n]*', raw)
    if not m:
        return raw
    new = (u'至通數之別：比丘二百五十，本表甲部恰合（含二不定法）；比丘尼三百四十八，本表乙部今亦列足'
           u'——八波羅夷・十七僧殘・三十捨墮・一百七十八單提凡 233 號，律有別宣之文；'
           u'八悔過・百眾學法・七滅諍法凡 115 號（233＋115＝348）：悔過一組律有乞酥之別結，'
           u'餘七物以『如乞酥無異』一句列目；眾學一組律注明言『下眾學戒與大僧戒無異，故不出耳』；'
           u'滅諍一組乃程序之法，二部同之。舊本於此三者不另立號，今依號登位而各著其所依，'
           u'非以意造戒文，乃使通數可按圖而考。')
    return raw.replace(m.group(0), new)


def sum_claim(raw):
    """表凡例之算式由組頭自算：『比丘 4＋…＝250 條、比丘尼 …＝N 條，共 M 號』。
       組頭若改，此句即隨之——冊上不許有第二份通數。"""
    d = []
    for l in raw.split(u'\n'):
        m = re.match(u'^## ([甲乙])、.*?戒本 (\\d+) 條', l)
        if m:
            d.append((m.group(1), int(m.group(2))))
    jia = sum(n for b, n in d if b == u'甲')
    yi = sum(n for b, n in d if b == u'乙')
    if not (jia and yi):
        return raw
    old = re.search(u'（比丘 [^＝]*＝\\d+ 條、比丘尼 [^＝]*＝\\d+ 條，共 \\d+ 號', raw)
    if old:
        raw = raw.replace(old.group(0),
                          u'（比丘 4＋13＋2＋30＋90＋4＋100＋7＝%d 條、'
                          u'比丘尼 8＋17＋30＋178＋8＋100＋7＝%d 條，共 %d 號' % (jia, yi, jia + yi), 1)
    return raw


def counts(txt):
    """由表身實數甲・乙兩部之號（含『N～M.』之號段）。"""
    out = {u'甲': 0, u'乙': 0}
    cur = None
    for l in txt.split(u'\n'):
        m = re.match(r'^#{2,5}\s*([甲乙])、', l)
        if m:
            cur = m.group(1)
            continue
        if cur:
            r = re.match(r'^\s*(\d+)(?:[～~](\d+))?\.\s', l)
            if r:
                out[cur] += (int(r.group(2)) - int(r.group(1)) + 1) if r.group(2) else 1
    return out
