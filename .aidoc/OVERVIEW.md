# OVERVIEW (HEAD)
- `source_data/` : 原稿(別 git リポジトリ。1〜7.txt、題名 00_TITLE.md、あらすじ 00_SYNOPSIS.md、作者のことば 00_README.md)。成果物にしかない文書データは置かない。
- `tools/gen.py` : 原稿 → `site/` を生成する標準ライブラリのみの python スクリプト。
- `Makefile` : `make build`(= `make site`) / `make serve` / `make clean`。
- `site/` : 生成済み static HTML 一式(コミット対象)。`style.css` のみ手書き(Apple 風の静かなデザイン。配色・書体は :root の CSS 変数、ダークモード対応。ヘッダ UI なし)。
- `.aidoc/` : AGENTS.md 規約の計画・監査・報告・入力ログ。
- `LICENSE` : Copyright (c) 2026 ririumu. All rights reserved.(全ページのフッターと README にも表記)。
- `tools/e2e.py` : 公開サイトと README の動線検証(`make e2e`)。`.github/workflows/pages.yml` で site/ を GitHub Pages 配信。
- 公開: https://ririumu.github.io/novel-now-there-is-tomorrow/ (repo: ririumu/novel-now-there-is-tomorrow, public)。全 commit は ririumu 名義。
