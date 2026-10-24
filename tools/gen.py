#!/usr/bin/env python3
"""manuscript/N.txt -> site/N.html, site/index.html (標準ライブラリのみ)"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manuscript"
OUT = ROOT / "site"

BOOK = (SRC / "00_TITLE.md").read_text(encoding="utf-8").strip()

PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23000'/%3E%3Ctext x='32' y='46' font-size='40' text-anchor='middle' fill='%23fff' font-family='serif'%3E%E3%81%82%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
{body}
</main>
<footer id="foot">Copyright &copy; 2026 ririumu. All rights reserved.</footer>
</body>
</html>
"""


def e(s):
    return html.escape(s, quote=False)


def split_title(first):
    """【　第一話:知識だ！…　】 -> (第一話, 知識だ！…)"""
    t = re.sub(r"^[【〔\[]\s*|\s*[】〕\]]$", "", first.strip("　 \t"))
    m = re.match(r"(第.+?話)\s*[:：]\s*(.*)", t)
    return (m.group(1), m.group(2).strip()) if m else ("", t)


def lint(path, text, title_ok):
    """誤字脱字の修正で入りやすい崩れを警告する(ビルドは止めない)。"""
    warns = []
    if not title_ok:
        warns.append("1行目が『〔第N話：題名〕』『【　第N話:題名　】』の形式でない")
    for o, c in (("「", "」"), ("『", "』"), ("（", "）"), ("(", ")")):
        if text.count(o) != text.count(c):
            warns.append(f"括弧の対応が合わない {o}{c}: {text.count(o)} / {text.count(c)}")
    if "\t" in text:
        warns.append("タブ文字がある")
    for i, l in enumerate(text.split("\n"), 1):
        if l != l.rstrip():
            warns.append(f"{i}行目: 行末に空白")
    for w in warns:
        print(f"warning: {path.name}: {w}", file=sys.stderr)


def chapters():
    files = sorted(SRC.glob("[0-9]*.txt"), key=lambda p: int(p.stem))
    out = []
    for p in files:
        text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        lines = text.split("\n")
        num, sub = split_title(lines[0])
        lint(p, text, bool(num))
        body = lines[1:]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        out.append({"n": int(p.stem), "sub": sub, "body": body,
                    "chars": sum(len(l) for l in body)})
    return out


def nav(n, last):
    prev = f'<a href="{n-1}.html">‹ 前の話</a>' if n > 1 else '<span class="off">‹ 前の話</span>'
    nxt = f'<a href="{n+1}.html">次の話 ›</a>' if n < last else '<span class="off">次の話 ›</span>'
    return f'<nav class="nav">{prev}<a href="index.html">目次</a>{nxt}</nav>'


def chapter_page(c, last):
    paras = "\n".join(f"<p>{e(l)}</p>" if l.strip() else "<p><br></p>" for l in c["body"])
    body = (f'<p class="eyebrow">第{c["n"]}話</p>\n<h1>{e(c["sub"])}</h1>\n'
            f'<article id="novel">\n{paras}\n</article>\n{nav(c["n"], last)}')
    return PAGE.format(title=e(f"第{c['n']}話 {c['sub']} - {BOOK}"), book=BOOK, body=body)


def index_page(cs):
    total = sum(c["chars"] for c in cs)
    rows = "\n".join(
        f'<tr><td class="no">第{c["n"]}話</td><td class="title"><a href="{c["n"]}.html">{e(c["sub"])}</a></td>'
        f'<td class="size">{c["chars"]:,}字</td></tr>' for c in cs)
    synopsis = "<br>\n".join(e(l) for l in (SRC / "00_SYNOPSIS.md").read_text(encoding="utf-8").strip().split("\n"))
    words = (SRC / "00_README.md").read_text(encoding="utf-8").strip()
    status = "完結" if "（完）" in cs[-1]["body"][-1] else "連載中"
    body = f"""<p class="eyebrow">{status}</p>
<h1>{BOOK}</h1>
<p class="sub">全{len(cs)}話 ・ {total:,}字</p>
<p class="lead">{synopsis}</p>
<p class="words">{e(words)}</p>
<table class="toc">
{rows}
</table>"""
    return PAGE.format(title=BOOK, book=BOOK, body=body)


def main():
    cs = chapters()
    OUT.mkdir(exist_ok=True)
    keep = {f"{c['n']}.html" for c in cs}
    for old in OUT.glob("[0-9]*.html"):
        if old.name not in keep:
            old.unlink()
    for c in cs:
        (OUT / f"{c['n']}.html").write_text(chapter_page(c, len(cs)), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(cs), encoding="utf-8")
    print(f"generated {len(cs)} chapters + index", file=sys.stderr)


if __name__ == "__main__":
    main()
