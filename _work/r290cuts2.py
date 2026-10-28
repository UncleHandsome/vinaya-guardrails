# -*- coding: utf-8 -*-
r"""290・補刀：附錄四導言立『篇聚序可推卷次』之約（含本地實證與用法）。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')

OLD = (u'故唯記其分段檔所在，不作俱合之論；其有外來校語指某案當在某卷者，凡與本地檔段相容則存其說於案下，'
       u'不相容則仍標未細核，一不據以改判。')
NEW = (u'故唯記其分段檔所在，不作俱合之論；其有外來校語指某案當在某卷者，凡與本地檔段相容則存其說於案下，'
       u'不相容則仍標未細核，一不據以改判。又一：**本地檔中偶存之篇聚序得為推卷之據**——如二十二至三十卷分段檔內，'
       u'『一百七十八單提法』自『之一』至『之七』歷歷可數，而檔中恰存一行題『四分律卷第二十七・二分之六・明尼戒法』'
       u'正在『單提法之四』之上，故之四⇔卷二十七、之五⇔卷二十八、之六⇔卷二十九、之七⇔卷三十；'
       u'凡引文落在某『之N』段內者，其卷即隨段定，此屬**本地可推**，與外來校語之『存其說』有別，故〔案例 86〕定作卷二十九。')
assert T.count(OLD) == 1, T.count(OLD)
T = T.replace(OLD, NEW)
B = T.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'補刀畢：%d 行・%dB｜sha %s ➔ %s' % (len(T.split(u'\n')), len(B), SHA0,
      hashlib.sha256(T.encode('utf-8')).hexdigest()[:12]))
