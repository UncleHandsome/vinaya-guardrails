# -*- coding: utf-8 -*-
import io, os, re
from collections import Counter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n")
for k in [u"八大正理",u"正理一",u"正理二",u"正理三",u"正理四",u"正理五",u"正理六",u"正理七",u"正理八",
          u"六閘門",u"六重心智閘門",u"閘門一",u"閘門二",u"閘門三",u"閘門四",u"閘門五",u"閘門六",
          u"十六觀心問",u"十六問",u"夜半四問",u"隨身三鏡",u"三鏡",u"隨身三印",u"四大金剛",u"夜半四照",
          u"八大正理法定定文",u"判準天平"]:
    print(u"%-14s %d" % (k, t.count(k)))
print(u"--- 第八章正理定文首四行 ---")
i=t.index(u"八大正理法定定文")
print(t[i-40:i+700])
