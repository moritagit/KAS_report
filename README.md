# 知能獲得システム論課題


[livedoor news corpus](https://www.rondhuit.com/download/ldcc-20140209.tar.gz)を教師なし学習でどれだけ分類できそうかを調べる。

主な実行は`notebooks/notebook.ipynb`で行っており，`src`以下にいくつかクラス等を定義したPythonファイルがある。

`data/processed/livedoor_new_corpus`以下に，元々のテキストデータをjsonlinesとして保存し直し，train / dev / testに分けたデータを置く。
テキストデータが`text`キーで，数値化されたラベルが`label`でアクセスできるようにする。

