# REPORT 1

依頼: source_data の小説を static HTML 一式にする(ビルドツール禁止、のちに Makefile と python は許可)。以後の指示で、デザイン・題名・公開・権利表記まで拡張。

## 成果
- 公開サイト: https://ririumu.github.io/novel-now-there-is-tomorrow/ (main への push で `site/` を GitHub Pages 配信)
- リポジトリ: https://github.com/ririumu/novel-now-there-is-tomorrow (public)。README は読者向け(「第1話から読む」+目次リンク)。
- 題名『あの頃にやり直したかったこと』、完結・全7話。題名・あらすじ・作者のことばは原稿(source_data、gist のサブモジュール)に置く。
- デザイン: 余白と文字組み主体。本文はヒラギノ角ゴ系 17px/行間1.9/字間0.02em(国内の目安に基づく)、見出しは明朝太字。黒強調、ダークモード、スマホ幅は文節改行、ヘッダ UI なし。
- 生成: `tools/gen.py`(python3 標準ライブラリのみ)+`make build`。原稿の体裁崩れは警告。検証: `make e2e`。

## 途中の誤りと是正
- 「連載中」を根拠なく表示 → 原稿の（完）から自動判定に。
- あらすじで第2話以降をネタバレ → 第一話の前提のみに。
- 本文のサイズ・行間・書体を根拠なく決定 → 調査に基づき修正。
- スマホ幅を未検証のまま報告 → 実測して折り返し・三点リーダを修正。
- make 3.81 の秒単位判定で更新を取りこぼし → 毎回全再生成に。

## 未確認・残課題
- Windows / Android / Safari 実機での表示(Safari は文節改行非対応で通常禁則になる)。
- 書き換え前の commit は SHA 直指定で GitHub 上にまだ残る(完全削除は GitHub サポートへの依頼が必要)。
- 原稿の行末空白 2 箇所(1.txt 96行目 / 7.txt 93行目)は表示に影響しないため未修正。
