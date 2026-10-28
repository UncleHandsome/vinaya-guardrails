# -*- coding: utf-8 -*-
"""外文括號之全數清點：凡含 ASCII 之括號，逐一列・自動分『巴利／梵（留）』與『西方法政心理（除）』。

分判之法：① 帶變音符（ā ī ū ṃ ṇ ṭ ś ñ 等）者即巴利／梵之轉寫，留；
          ② 落白名單（Buddhist 術語）者留；③ 其餘為西方法政・心理・企管之外來語，除。
除之法：括號內若以『·』或『/』分兩段且後段為漢字者，只剝前段（漢字之釋留在書中）。
用法：python -X utf8 _work/pairpurge_parens.py
"""
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {"F2": ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "F1": ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt"}
DIAC = set("āīūṃṇṭśṣñḍḷĀĪŪÉéòōṅýčšž")
PALI = re.compile(r"^(Sa[ṃn]?gha|Kamma|Dhamma|P[āa]li|Vinaya|S[īi]m[āa]|Bhikkhu|Bhikkhun[īi]|"
                  r"Sikkhaman|Pav[āa]ra[ṇn]|Uposatha|Pariv[āa]ra|Kathina|P[āa]risuddhi|Chanda|"
                  r"Abbh[āa]na|Pabb[āa]jan[īi]ya|N[āa]sana|Antar[āa]y[īi]ka|N[īi]vara[ṇn]|"
                  r"Pandaka|Ubhatobyan|Amanussa|Tiracch|Gabbha|Cāturvarga|Pa[^ ]*varga|Da[^ ]*varga|"
                  r"Vim[^ ]*atirvarga|Samagga|Khuddik|Nimitta|Nivāsika|Āgantuka|Uparikamma|"
                  r"Adhikarana|Samatha|Vipassan|Sati|Appam|Kalyā[aṇ]|Mett|Karu[ṇn]|"
                  r"Muc|Parivra|Bhikkhu|Śūra|Ārya|Dharma|Sūtra|Kārik|Abhidh|Vijñapti|"
                  r"Māna|Lobha|Dveṣ|Dveṣa|Moha|Īrhyā|Kauk|Aśraddh|Styāna|Kuy|F|Coddaka)", re.I)
PAREN = re.compile(r"[（(]([^）)]*[A-Za-z][^）)]*)[）)]")

for tag, p in BOOKS.items():
    ls = p.read_bytes().decode("utf-8").split("\r\n")
    keep, drop = [], []
    for i, l in enumerate(ls, 1):
        for mm in PAREN.finditer(l):
            s = mm.group(1)
            if any(c in DIAC for c in s):
                keep.append((i, s))
                continue
            head = re.split(r"[·/／、，,]", s)[0].strip()
            if PALI.match(head):
                keep.append((i, s))
            else:
                drop.append((i, s, bool(re.search("[\u4e00-\u9fff]", re.sub(r"^[^(·/／、，,]*", "", s)))))
    print("=" * 74)
    print(f"■ {tag}・外文括號：留（巴利／梵）{len(keep)} 枚・除（西方法政心理企管）{len(drop)} 枚")
    print("  【除】逐條：")
    for i, s, has_zh in drop:
        print(f"    L{i:<6}{'留漢字釋' if has_zh else '整括剝除'}｜{s[:64]}")
