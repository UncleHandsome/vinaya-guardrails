# -*- coding: utf-8 -*-
"""第三波『去延伸名相』·子刀：剝西方法政・心理・企管之外來語括號（巴利／梵之 apparatus 保留）。

立法之本：本書之『小界（Khuddikā-sīmā）』『客比丘（Āgantuka-bhikkhu）』『四種僧（Caturvarga…）』
        乃漢譯律學之正當標音，非『外掛』；而『正當程序（Due Process）』『不成就（Void Ab Initio）』
        『越權（Ultra Vires）』『疑罪唯輕（In Dubio Pro Reo）』之流，是西方法學院之名相——後者一刀剥之。

判式（機械可复核，非逐條手抄）：括號以 ASCII 起頭者，查其中**每一**拉丁詞——
  ① 帶變音符（ā ī ū ṃ ṇ ṭ ś ñ…）＝巴利／梵轉寫，留；
  ② 落巴利白名單（PALI 詞幹）者，留；
  ③ 一～二字母之變數（N、A、B）者，留；
  ④ 有一詞不落上述者，即西方法政心理企管之語 → 剥。
剥之法：『（English·漢字釋）』只剥前段留漢字釋；『（English）』整括剥除。圍欄內之剥須補格保欄。

用法：python -X utf8 _work/pairpurge.py           # 試跑（逐條印前后）
      python -X utf8 _work/pairpurge.py --write   # 落盤
"""
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
FILES = [F2, F1]

IAST_MARKS = {0x0304, 0x0307, 0x0323, 0x0331, 0x0303, 0x030D, 0x0332}
#  長音(̄) 上點(̇) 下點(̣) 下長音(̱) 鼻化(̃) 軟音(̭) 下短音(̒)——唯巴利／梵轉寫（IAST）用之。


def has_diacritic(s):
    """是否巴利／梵之轉寫字母。判式取『碼位』而非 NFD 分解：
       Unicode 裡 ś（U+015B）一类『無正規分解』之預合字母，NFD 查其結合符會漏（親踩：Daśavarga 誤剥）；
       而 ä ö é ß（U+00C0–U+00FF 之 Latin-1 區）乃歐語符，正該讓德文『Mittelbare Täterschaft』照剥。
       故：拉丁字母而碼位逾 Latin-1 者＝IAST 轉寫；ñ 雖在 Latin-1 而亦巴利用字，特許。
       （不立字面名單——名單經顯示層易失其形：本專案『碼位與歸簡之防』舊戒。）"""
    for c in unicodedata.normalize("NFD", s):
        if ord(c) in IAST_MARKS:
            return True
    return any(unicodedata.category(c) in ("Lu", "Ll") and (ord(c) > 0xFF or c in "ñÑ") for c in s)
PALI = {
    "sanga", "sangha", "saṅgha", "kamma", "karma", "karman", "dhamma", "dharma", "sutra", "vinaya",
    "sima", "sīmā", "nimitta", "uposatha", "pavara", "pavāra", "vassa", "katina", "kathina",
    "bhikkhu", "bhikkhuni", "pandaka", "panḍaka", "ubhatobyan", "ubhatobyañjanaka", "amanussa",
    "tiracch", "tiracchāna", "gabbha", "caturvarga", "pañcavarga", "pancavarga", "dasavarga",
    "daśavarga", "vimsativarga", "vimśativarga", "samagga", "khuddika", "khuddikā", "nivāsika",
    "nivānika", "agantuka", "chanda", "parisuddhi", "pārisuddhi", "upasampada", "upasampadā",
    "abbhana", "abhāna", "pabbajaniya", "pabbājanīya", "nasana", "nāsana", "antarayika",
    "antarāyikā", "nivarana", "nīvaraṇa", "sikkhamana", "sikkhamānā", "mulasana", "mulāyapa",
    "samavadhana", "samava", "suddhanta", "parivasa", "adhikarana", "adhikaraṇa", "samatha",
    "sampaja", "sampajañña", "sati", "metta", "karuna", "mudita", "upekkha", "citta", "cetaka",
    "cetanā", "cetasika", "manas", "manasikāra", "phassa", "vedana", "sañña", "sanna", "vipatti",
    "vipatti", "auddhatya", "audhatya", "krodha", "kauktya", "kaukṛtya", "kaukuktya", "abhiddha",
    "abhidhamma", "vinnatti", "vijñapti", "māna", "lobha", "dosa", "dveṣa", "moha", "kalyana",
    "devadatta", "parileyyaka", "lecca", "lecchha", "ananda", "ānanda", "sariputta", "moggallana",
    "upali", "upananda", "radha", "rahula", "rāhula", "kasyapa", "kāśyapa", "sakyamuni",
    "tathāgata", "tathagata", "buddha", "bodhisattva", "pratyekabuddha", "sarva", "vina",
    "pāli", "sanskrit", "prakrit", "prākrit", "āgama", "agama", "nikāya", "nikaya",
    "prātimokṣa", "pratimoksha", "pātimokkha", "bhikṣu", "śūra", "arya", "ārya", "māra", "brahma",
    "kharosthi", "brahmi", "devanagari", "siddham", "codaka", "coddaka", "kundaka", "kaccayana",
    "abhidharma", "kosa", "kośa", "nyaya", "vaibhashika", "sautrāntika", "cittamātra",
    "adarsana", "ādarsa", "smrti", "smṛti", "prabha", "prabhā", "simsong", "gunaprabha",
}
ASCII_PAREN = re.compile(r"[（(]([A-Za-z][^（()）]*)[）)]")
ASCII_WORD = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
CJK = re.compile(r"[一-鿿]")


def is_native(seg):
    """括號內之 ASCII 段是否巴利／梵之標音或變數（是→留）。
       判式取『首段』：漢譯律學之標音慣以巴利詞領頭（Samagga-saṅgha、Caturvarga·…），
       而西方法政之語慣以英文領頭（Declaratory Decree、Void Ab Initio）——
       非 ASCII 之變音符會把巴利詞腰截，故不可逐片段判，只認首段。"""
    if has_diacritic(seg):
        return True
    words = ASCII_WORD.findall(seg)
    if not words:
        return True
    head = words[0].lower().strip("-'’")
    if len(head) == 1 or head in {"id", "imei", "n"}:      # 單字母變數（A、B、N）
        return True
    if head in PALI:
        return True
    if len(head) >= 5 and any(head.startswith(p) for p in PALI if len(p) >= 5):
        return True                                        # 巴利長詞之首段（Samagga-saṅgha 之腰截）
    if len(head) >= 5 and any(p.startswith(head) for p in PALI if len(p) >= 5):
        return True
    return False


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


GUTTER = re.compile(r"\s {3,}")


def strip_parens(line, in_fence):
    """回 (新行, 剥除之清單)。先剥『Eng·漢』之前段，再剥整括之純外文。
       圍欄內之剥：唯『此行之後尚有欄間空白（≥3 格）』者才以同寬空格占位——
       單欄之圖（如『2. 【名相（English）】：』）剥後即合攏，不留難看之大洞。"""
    gone = []

    def mixed(mm):
        seg = mm.group(1)
        parts = re.split(r"[·・，,、]", seg, maxsplit=1)
        if len(parts) == 2 and re.search(r"[一-鿿]", parts[1]):
            if is_native(parts[0]):
                return mm.group(0)
            gone.append(parts[0].strip())
            keep = "（" + parts[1].strip() + "）"
            tail = line[min(len(line), mm.end()):]
            pad = " " * max(0, dwidth(mm.group(0)) - dwidth(keep)) \
                if (in_fence and GUTTER.search(tail)) else ""
            return keep + pad
        return mm.group(0)

    out = ASCII_PAREN.sub(mixed, line)

    def whole(mm):
        seg = mm.group(1)
        if is_native(seg):
            return mm.group(0)
        gone.append(seg.strip())
        tail = line[min(len(line), mm.end()):]
        return " " * dwidth(mm.group(0)) if (in_fence and GUTTER.search(tail)) else ""

    out = ASCII_PAREN.sub(whole, out)
    if not gone:
        return line, gone                     # 一字未剥即原樣交回：行尾之兩空格乃 markdown 之硬換行，動不得
    if not in_fence:
        # 剥後所遺之空斜體（`<br>*(Civility)*` → `<br>*`）須併除，否則印面出星號
        out = re.sub(r"<br>\*+(?=\s*(?:\||$))", "", out)
        out = re.sub(r"[ \t]+$", "", out)
    return out, gone


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - set("几")
    errs, ledger, plans = [], [], []
    for f in FILES:
        raw = (ROOT / f).read_bytes()
        lines = raw.decode("utf-8").split("\r\n")
        fence = m.fence_mask(lines)
        rows = []
        for i, l in enumerate(lines):
            if not re.search(r"[（(]\s*[A-Za-z]", l):
                continue
            new, gone = strip_parens(l, fence[i])
            if not gone:
                continue
            for c in set(new) & SIMPLE:
                errs.append(f"{f[:6]}・簡形：{c}｜L{i + 1}")
            rows.append((i + 1, l, new, gone))
            ledger.append(f"{f}\tL{i + 1}\t子・外文括號\t[{ '・'.join(gone)[:40] }] {l.strip()[:44]} → {new.strip()[:44]}")
        print("=" * 76)
        print(f"  子刀剥外文括號 {sum(len(r[3]) for r in rows)} 枚・動行 {len(rows)}"
              f"（零中者唯在『本冊已淨』時出現，如實報而不以為誤）")
        for i, o, w, g in rows:
            print(f"  L{i:<6}剥【{'・'.join(g)[:56]}】")
            print(f"         故 {o.strip()[:74]}")
            print(f"         新 {w.strip()[:74]}")
            lines[i - 1] = w
        plans.append((f, raw, lines))
    if errs:
        for e in errs:
            print("  ✗", e)
        print("★有誤 → 俱不落盤")
        return
    print("=" * 76)
    for f, raw, lines in plans:
        out = "\r\n".join(lines).encode("utf-8")
        if write:
            bak = ROOT / "_archive" / "備份" / "AI清理前" / (f + ".pre_purge")
            bak.write_bytes(raw)
            (ROOT / f).write_bytes(out)
            print(f"  落盤 {f[:12]}…：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(out).hexdigest()[:12]}"
                  f"・行 {len(raw.decode('utf-8').split(chr(13)+chr(10)))} → {len(lines)}（不動）")
        else:
            print(f"  {f[:12]}…・試跑未落盤（行 {len(lines)}）")
    (ROOT / "_work" / "pairpurge_zi_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"刀口清冊 {len(ledger)} 行 → _work/pairpurge_zi_cuts.txt")


if __name__ == "__main__":
    main()
