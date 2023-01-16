# 概要
Google Mapsの過去のタイムライン情報から特定のデータのみを取得するスクリプト

# 使い方
1. Google Mapsの過去のタイムライン情報(zipファイル)を取得する。
1. 「1.」で取得したファイルパスをソースコード中の以下の変数に格納する。
    - zipfile_path
1. 実行する。
1. 以下フォーマットのjsonファイルが出力される。
```json
[
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longitude': zzzzzz,
    },
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longnitude': zzzzzz,
    },
    ...(省略)
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longnitude': zzzzzz,
    },
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longnitude': zzzzzz,
    }
]
```