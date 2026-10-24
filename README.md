<div align="center">

# あの頃にやり直したかったこと

西暦二〇五〇年。AI の炎に焼かれた世界で、<br>
弁護士・反橋聡太（四十）は、人生をやり直すために過去へ飛ぶ。

**[▶ 第1話から読む](https://ririumu.github.io/novel-now-there-is-tomorrow/1.html)**

完結 ・ 全7話 ・ 約1万1千字（一話あたり数分）

</div>

---

## 目次

| 話 | 題名 |
|---|---|
| 第1話 | [知識だ！チートだ！無双だ！](https://ririumu.github.io/novel-now-there-is-tomorrow/1.html) |
| 第2話 | [いざ、ババア幼女化計画！](https://ririumu.github.io/novel-now-there-is-tomorrow/2.html) |
| 第3話 | [弁護士、無職、タイムトラベラー](https://ririumu.github.io/novel-now-there-is-tomorrow/3.html) |
| 第4話 | [未来の常識は過去の非常識](https://ririumu.github.io/novel-now-there-is-tomorrow/4.html) |
| 第5話 | [知識チート、敗北の予感](https://ririumu.github.io/novel-now-there-is-tomorrow/5.html) |
| 第6話 | [おっさん、文明の壁にぶつかる](https://ririumu.github.io/novel-now-there-is-tomorrow/6.html) |
| 第7話 | [AIなし、己なし、されど](https://ririumu.github.io/novel-now-there-is-tomorrow/7.html) |

スマートフォンでもそのまま読めます。各話の末尾から次の話へ進めます。

> AI がない頃に憧れてみました。　―― 作者

<p align="center"><sub>Copyright &copy; 2026 ririumu. All rights reserved. 無断転載・複製・改変・再配布を禁じます（<a href="LICENSE">LICENSE</a>）。</sub></p>

<br>

<details>
<summary>このリポジトリについて（書き手・編集者向け）</summary>

公開サイトは、このリポジトリの `site/` をそのまま GitHub Pages で配信しています。

```
source_data/   原稿（各話 N.txt、題名 00_TITLE.md、あらすじ 00_SYNOPSIS.md、作者のことば 00_README.md）
tools/gen.py   原稿 → site/*.html（python3 標準ライブラリのみ）
site/          公開されるサイト（生成物もコミットする）
```

誤字脱字を直すとき:

```
$EDITOR source_data/3.txt   # 原稿を直す
make build                  # site/ を再生成（括弧の対応などの崩れは警告が出る）
make serve                  # http://localhost:8000 で確認
git push                    # main への push で公開サイトに反映
```

ビルドツールは使いません。`source_data/` は別リポジトリです。

</details>
