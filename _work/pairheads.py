# -*- coding: utf-8 -*-
import re
import sys

p = sys.argv[1]
a, b = int(sys.argv[2]), int(sys.argv[3])
ls = open(p, encoding="utf-8").read().split("\n")
for i in range(a, b + 1):
    s = ls[i - 1].rstrip()
    if re.match(r"^#{1,6}\s", s) or s.lstrip().startswith("```") or s.startswith("**【"):
        print(i, s[:80])
