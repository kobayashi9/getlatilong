import zipfile
import glob
import shutil
import json
from datetime import datetime

"""
zipファイルをtmpフォルダに全て解凍する。

"Semantic Location"というフォルダを探し、
その下のフォルダのjsonファイルから情報を収集する。
例：年/月.json

"placeVisit"から情報を抽出し以下のjsonフォーマットに変換する。
[
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longitude': zzzzzz,
    },
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longitude': zzzzzz,
    },
    ...(省略)
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longitude': zzzzzz,
    },
    {
        'datetime': 'xxxxx',
        'latitude': yyyyy,
        'longitude': zzzzzz,
    }
]
"""

# 解凍するzipファイルパス
zipfile_path = "./xxxxx.zip"

# 解凍先
unzipfile_path = "./tmp/"


def unzip(file_path:str, output_path:str):
    zipfile.ZipFile(file_path).extractall(output_path)

def get_all_jsonfile_path(tgt_path:str):
    jsonfile_path_list = []
    
    root_path = glob.glob(tgt_path + "**/Semantic Location History", recursive=True)
    for path in glob.glob(str(*root_path) + "/**/*.json", recursive=True):
        jsonfile_path_list.append(path)
    jsonfile_path_list.sort()

    return jsonfile_path_list

def main():

    unzip(zipfile_path, unzipfile_path)

    archivefile_path_list = get_all_jsonfile_path(unzipfile_path)
    
    visitedplaces_list = list()

    # 全てのjsonファイルから位置情報抽出
    for archivefile_path in archivefile_path_list:
        archive_json = {}
        with open(archivefile_path, 'r') as jf:
            archive_json = json.load(jf)
        
        for timline_value in archive_json.get("timelineObjects"):
            if timline_value.get("placeVisit"):
                tmp_place = dict()
                tmp_place["datetime"] = timline_value.get("placeVisit").get("duration").get("startTimestamp")
                tmp_place["latitude"] = timline_value.get("placeVisit").get("location").get("latitudeE7") / 10000000
                tmp_place["longitude"] = timline_value.get("placeVisit").get("location").get("longitudeE7") / 10000000
                visitedplaces_list.append(tmp_place)

    with open(f"visited_place_{datetime.now():%Y%m%d%H%M%S}.json", "w") as output_file:
        json.dump(visitedplaces_list, output_file, indent=4, ensure_ascii=False)

    # 解凍したzipファイル削除
    #shutil.rmtree("./tmp/Takeout")

if __name__ == '__main__':
    main()