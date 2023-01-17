# 概要
Google Mapsの過去のタイムライン情報から以下のデータのみを取得する。
- 自分が訪れた位置データ
- 訪れたランドマークの位置データ

# 使い方
1. Google Mapsの過去のタイムライン情報(zipファイル)を取得する。
1. 「1.」で取得したファイルパスをソースコード中の以下の変数に格納する。
    - zipfile_path
3. 以下フォーマットのjsonファイルが出力される。
```json
[
    {
        "datetime": "xxxxx",
        "latitude": "yyyyy",
        "longitude": "zzzzzz",
    },
    {
        "datetime": "xxxxx",
        "latitude": "yyyyy",
        "longitude": "zzzzzz",
    },
    {
        "datetime": "xxxxx",
        "latitude": "yyyyy",
        "longitude": "zzzzzz",
    },
    {
        "datetime": "xxxxx",
        "latitude": "yyyyy",
        "longitude": "zzzzzz",
    }
]
```
