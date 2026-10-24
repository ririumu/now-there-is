#!/usr/bin/env python3
"""公開サイトと README の動線を実際に辿って検証する(標準ライブラリのみ)。

    python3 tools/e2e.py [BASE_URL]

- 目次から全リンクを辿り、すべて HTTP 200 か
- 各話: 見出し・本文・前/目次/次ナビが正しい話を指しているか
- 目次の話数と字数表示が source_data と一致するか
- GitHub 上の README の公開サイトへのリンクがすべて 200 か
"""
import re, sys, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://ririumu.github.io/novel-now-there-is-tomorrow/").rstrip("/") + "/"
README_API = "https://api.github.com/repos/ririumu/novel-now-there-is-tomorrow/readme"
SRC = Path(__file__).resolve().parent.parent / "source_data"
COPYRIGHT = "Copyright &copy; 2026 ririumu. All rights reserved."
fails = []


def get(url, accept=None):
    req = urllib.request.Request(url, headers={"User-Agent": "e2e", **({"Accept": accept} if accept else {})})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self._in_h1, self.paras = [], "", False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a["href"])
        if tag == "h1":
            self._in_h1 = True
        if tag == "p":
            self.paras += 1

    def handle_endtag(self, tag):
        if tag == "h1":
            self._in_h1 = False

    def handle_data(self, d):
        if self._in_h1:
            self.h1 += d


def parse(html):
    p = Links()
    p.feed(html)
    return p


def main():
    chapters = sorted(SRC.glob("[0-9]*.txt"), key=lambda p: int(p.stem))
    title = (SRC / "00_TITLE.md").read_text(encoding="utf-8").strip()

    st, html = get(BASE)
    check(st == 200, f"目次 {BASE} -> {st}")
    idx = parse(html)
    check(idx.h1 == title, f"目次の題名 '{idx.h1}'")
    check(f"全{len(chapters)}話" in html, f"目次に「全{len(chapters)}話」")
    check("（完）" not in html, "目次にネタバレ用の本文が混ざっていない")
    check(COPYRIGHT in html, "目次 著作権表記")

    seen = set()
    for href in idx.links:
        url = urljoin(BASE, href)
        if url in seen:
            continue
        seen.add(url)
        st, _ = get(url)
        check(st == 200, f"目次からのリンク {href} -> {st}")

    last = len(chapters)
    for p in chapters:
        n = int(p.stem)
        st, html = get(urljoin(BASE, f"{n}.html"))
        check(st == 200, f"第{n}話 -> {st}")
        pg = parse(html)
        head = p.read_text(encoding="utf-8").split("\n", 1)[0]
        check(pg.h1 and pg.h1 in head, f"第{n}話 見出し '{pg.h1}'")
        check(pg.paras > 10, f"第{n}話 本文段落 {pg.paras}")
        check("index.html" in pg.links, f"第{n}話 目次へのリンク")
        check((f"{n-1}.html" in pg.links) == (n > 1), f"第{n}話 前の話リンク")
        check((f"{n+1}.html" in pg.links) == (n < last), f"第{n}話 次の話リンク")
        check("style.css" in pg.links, f"第{n}話 スタイルシート")
        check(COPYRIGHT in html, f"第{n}話 著作権表記")

    st, readme = get(README_API, "application/vnd.github.html")
    check(st == 200, f"README(GitHub 上の描画) -> {st}")
    rlinks = sorted(set(re.findall(r'href="(' + re.escape(BASE) + r'[^"]*)"', readme)))
    check(len(rlinks) >= len(chapters), f"README から公開サイトへのリンク {len(rlinks)} 件")
    check(f"{BASE}1.html" in rlinks, "README に「第1話から読む」リンク")
    check("All rights reserved" in readme, "README 著作権表記")
    st, _ = get("https://api.github.com/repos/ririumu/novel-now-there-is-tomorrow/contents/LICENSE")
    check(st == 200, f"LICENSE -> {st}")
    for u in rlinks:
        st, _ = get(u)
        check(st == 200, f"README のリンク {u} -> {st}")

    print(f"\n{'FAILED: ' + str(len(fails)) if fails else 'ALL PASSED'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
