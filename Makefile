# 標準ライブラリのみの python3 で manuscript から site/ を生成する。
# 原稿(manuscript/*.txt)や meta/synopsis.txt を直したら `make build` するだけ。
# 生成は一瞬なので更新判定はせず毎回全再生成する(macOS 付属 make 3.81 の秒単位の時刻判定による取りこぼしを避ける)。
# 古い N.html は原稿が無くなれば消え、原稿の体裁崩れ(括弧の対応など)は警告される。

.PHONY: build site serve clean e2e
build:
	python3 -I tools/gen.py

site: build

serve: build
	python3 -m http.server 8000 --directory site

clean:
	rm -f site/index.html $(wildcard site/[0-9]*.html)

# 公開サイトと GitHub 上の README の動線を実際に辿って検証する
e2e:
	python3 -I tools/e2e.py
