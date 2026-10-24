# AUDIT 1
- source_data/ (別リポジトリの gitlink)の 1〜7.txt と 00_README.md を調査。1行=1段落、空行あり、1行目が題名 `【　第一話:…　】` / `〔第二話：…〕`。
- 当初は使い捨て python で変換する想定だったが、ユーザから「Makefile と python は可」との追記があり、`tools/gen.py` + `Makefile` としてリポジトリに残す方針に変更。
- branch feat/style-index: `site/style.css`(白地・細罫線・青リンク・MS Pゴシック・表組み目次)→ main へ --no-ff merge。
- branch feat/generator: gen.py(標準ライブラリのみ、HTML エスケープ、題名の括弧除去、前/次/目次ナビ)。`make site` で 7話+目次を生成 → merge。
- 確認: 全章の `<p>` 数、ナビリンク、目次の字数表示を目視確認。ブラウザでの実表示確認は未実施。
- branch docs/iteration-1: README / OVERVIEW / REPORT。
- feat/mincho: 本文(#novel)を明朝体スタック(ヒラギノ明朝→游明朝→MS P明朝→Noto Serif JP→serif)に変更、行間2・字間0.04em。目次・UI はゴシックのまま。
- feat/unify-design(デザインレビュー): 目次/本文で h1 の体裁が不一致(ゴシック左寄せ罫線 vs 明朝中央罫線なし)、あらすじ・話タイトルがゴシック、灰色が無彩色で背景の暖色と不統一、色の直書き、を指摘。
  対応: CSS 変数で配色・書体を一元化。読ませる文は明朝、操作部品はゴシックに統一。h1 を両ページで同一(中央・明朝・罫線)にし、本文ページの題名を枠外へ移動(gen.py 修正)。灰色を暖色寄りに統一。480px 以下用の余白調整を追加。
  確認: headless Chrome のスクリーンショットで目次・本文を目視。スマホ幅(480px以下)は headless の最小幅制約で未確認。
- feat/title-synopsis: 「連載中」表示は根拠なく書いた誤りだった。7.txt 末尾が（完）、1〜6 は（続く）なので、gen.py が末尾の（完）を検出して「完結」と表示するよう変更。
  サイト題名を付け、あらすじを meta/synopsis.txt に追加。「作者のことば」として 00_README.md の一文を原文のまま掲載。source_data(原稿)は無変更。
- feat/apple-style: ユーザ指摘「Apple 的な美しさがない」「前書きがくどい/ネタバレが激しい」。
  前書き: 第2〜7話の人物・展開(軍手・烏丸・憲法)まで書いていたのが誤り。第一話の前提だけの一文に短縮。「あらすじ/作者のことば」の枠・見出しも廃止し、本文を中央寄せのリードに。
  デザイン: 当初依頼の「古いなろう風」から、余白・文字組み主体の静かなデザインへ方針変更(ユーザ指示)。枠線・二重線・青帯を廃止し、半透明 sticky ヘッダ、40px 明朝見出し、680px の読み幅、ヘアライン区切りの目次、SF/ヒラギノ系ゴシック、ダークモード対応。gen.py のマークアップも整理(header/main/article/nav)。
  確認: headless Chrome で目次・本文(ライト)を目視。ダークモード・スマホ幅は未確認。
- feat/retitle-font: ユーザ指示で題名を『あの頃にやり直したかったこと』に変更し、旧英題・旧題名をリポジトリから除去(副題表示も廃止。目次ページの上部は「完結」表示に)。入力ログ USERINPUT.txt はユーザ発言の原文記録なのでそのまま残す。
  フォントが細すぎるとの指摘: ヒラギノ明朝 W3 が細い原因。游明朝(Mac では Medium が使える)を先頭にして font-weight:500、文字色をより濃く(#111)、本文 18px へ。
  確認: 見出しの孤立した「ー」折り返しを 36px + text-wrap:balance で解消。headless Chrome で目次・本文を目視。
- fix/body-font: 「本文が細すぎる/日本の適正サイズを調べろ」。数値を根拠なく決めていたのが誤り。ウェブ調査(国内メディア調査・可読性解説記事)の結果: 本文 16〜18px(16px が最多)、行間 1.8 が最多(日本語は 1.7〜1.9)、字間 0〜0.02em、1行 35〜45字、画面では明朝の細線が潰れやすくゴシックが標準的。旧設定は字間 0.05em・行間 2.1・細い明朝でいずれも外れていた。
  対応: 游明朝/ヒラギノ明朝(W6)/ヒラギノ角ゴ W4 を同一文で並べて比較し、本文・リード・目次はヒラギノ角ゴ系(Windows は Yu Gothic Medium)に変更。17px / 行間 1.9 / 字間 0.02em / 読み幅 680px(約35字)、スマホ 16px。大見出しのみ明朝太字を維持。
  確認: headless Chrome で目次・本文を目視(Mac のみ。Windows の見え方は未確認)。
- feat/build-and-ink: 文字色を黒強調(ライト #000 / ダーク #fff、補助色も濃く)。誤字脱字修正に備え、`make build` を追加(`site` は別名)。gen.py に lint(括弧 「」『』（）() の対応・題名形式・タブ・行末空白を警告のみで通知)と、原稿が無くなった古い N.html の削除を追加。
  Makefile の依存関係による増分ビルドは、macOS の make 3.81 が秒単位の時刻判定のため直後の編集を取りこぼし、検証用の誤字が site/ に残る事故が起きたので廃止し、毎回全再生成に変更(再検証済み: 生成物に検証文字は残らず、source_data は無変更)。
  現状の lint 警告: 1.txt 96行目 / 7.txt 93行目の行末空白(表示には影響しないため原稿は未変更)。source_data は別リポジトリのため原稿の整形はしていない(題名括弧の【】/〔〕混在は gen.py が両対応)。
- feat/meta-into-source: 題名(gen.py 定数)とあらすじ(meta/synopsis.txt)が成果物側にしか無いのは不整合、とのユーザ指摘。原稿リポジトリ(source_data)に 00_TITLE.md / 00_SYNOPSIS.md を追加(ブランチ add-title-synopsis → main へローカル merge。source_data の origin は公開 gist のため push はしていない)。gen.py はそれらを読み、meta/ を削除。生成物は無変更(site に差分なし)。
  注意: 親リポジトリの gitlink は source_data のローカル commit を指すため、gist へ push するまで他環境では解決できない。
- fix/mobile-ellipsis-header: 自己レビューで見つけた欠陥の修正+ユーザ指示「ヘッダ UI は不要」。
  (1) スマホ幅で題名・本文が単語途中で折れる → `word-break: auto-phrase`(文節改行、Chrome/Edge)+`line-break: strict`、480px 以下の h1 を 24px に。Safari は auto-phrase 未対応のため通常禁則に退化(未確認)。
  (2) 三点リーダ「……」が行下端の点に見える → 原因は font-family 先頭の -apple-system(SF)の字形が使われること。日本語フォント(ヒラギノ角ゴ/Yu Gothic)を先頭に、-apple-system は後ろへ。
  (3) favicon 404 → インライン SVG(黒地に「あ」)を追加。
  (4) sticky ヘッダ(題名バー)を削除。各話からの目次導線は末尾の「前の話/目次/次の話」のみ。
  確認: headless Chrome で 390px 幅(iframe)の目次・第1話、デスクトップの第2話、ダーク配色(media ブロックを展開した検証用 CSS でシミュレーション)を目視。実機の prefers-color-scheme・Windows・Safari は未確認。
- GitHub: `gh repo create` で private 作成・push → `novel-now-there-is-tomorrow` に rename。Pages は無料プランの private では不可(HTTP 422)のため、ユーザ選択により repo を public 化(事前に履歴の秘密情報・メールを確認、問題なし)。`.github/workflows/pages.yml` で生成済み site/ をそのまま配信(Actions 上ではビルドしない)。
- docs/reader-first-readme: README を読者向けに全面書き直し(題名・一文あらすじ・「第1話から読む」リンク・公開サイトへの目次リンク・作者のことば)。保守手順は折りたたみ(details)に移動。
- test/e2e: `tools/e2e.py` + `make e2e` を追加。公開サイトの目次→全リンク、各話の見出し/本文/前後ナビ/CSS、GitHub 上で描画された README の公開サイトリンクを実際に HTTP で辿って検証(全項目 PASS)。目視: GitHub のリポジトリページ、公開サイトの目次と最終話末尾(390px 幅)。
  目視で見つけた導線の穴を修正: リポジトリ About 欄が空 → description と homepage(公開 URL)を設定。README 目次表の空の列見出しを「話」に。
- docs/all-rights-reserved: LICENSE(日英、All rights reserved)を追加。全ページのフッター・README に「Copyright © 2026 ririumu. All rights reserved.」。e2e に著作権表記と LICENSE の存在チェックを追加。
