import zipfile
import glob
import shutil
import json
from datetime import datetime
import sys

"""
zipファイルをtmpフォルダに全て解凍する。

"Semantic Location"というフォルダを探し、
その下のフォルダのjsonファイルから情報を収集する。
例：年/月.json

"placeVisit"と"activitySegment"から情報を抽出し以下のjsonフォーマットに変換する。
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
"""

# 解凍先
UNZIPFILE_PATH_ = "./tmp/"
LATLON_E7_DECIMAL_SEPARATOR_ = 10000000

def unzip(file_path:str, output_path:str):
    zipfile.ZipFile(file_path).extractall(output_path)

def get_all_json_path(tgt_path:str):
    json_paths_list = []
    
    root_path = glob.glob(tgt_path + "**/Semantic Location History", recursive=True)
    for path in glob.glob(str(*root_path) + "/**/*.json", recursive=True):
        json_paths_list.append(path)
    json_paths_list.sort()

    return json_paths_list

def main():
    args = sys.argv
    if len(args) != 2:
        exit()

    # 解凍するzipファイルパス
    zipfile_path  = args[1]
    unzip(zipfile_path, UNZIPFILE_PATH_)

    archive_paths_list = get_all_json_path(UNZIPFILE_PATH_)
    
    visited_places_list = list()

    # 全てのjsonファイルから位置情報抽出
    for archive_path in archive_paths_list:
        archive_json = {}
        with open(archive_path, 'r') as jf:
            archive_json = json.load(jf)
        
        for timeline_value in archive_json.get("timelineObjects"):
            # 自分が訪れた位置データ収集
            if timeline_value.get("activitySegment"):
                activity_segment_value = timeline_value.get("activitySegment")
                # スタート地点情報
                start_place = dict()
                start_place["datetime"] = activity_segment_value.get("duration").get("startTimestamp")
                start_place["latitude"] = activity_segment_value.get("startLocation").get("latitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                start_place["longitude"] = activity_segment_value.get("startLocation").get("longitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                visited_places_list.append(start_place)

                # ゴール地点情報
                goal_place = dict()
                goal_place["datetime"] = activity_segment_value.get("duration").get("endTimestamp")
                goal_place["latitude"] = activity_segment_value.get("endLocation").get("latitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                goal_place["longitude"] = activity_segment_value.get("endLocation").get("longitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                visited_places_list.append(goal_place)

            # 訪れたランドマークデータ収集
            elif timeline_value.get("placeVisit"):
                landmark_place = dict()
                place_visit_value = timeline_value.get("placeVisit")
                landmark_place["datetime"] = place_visit_value.get("duration").get("startTimestamp")
                landmark_place["latitude"] = place_visit_value.get("location").get("latitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                landmark_place["longitude"] = place_visit_value.get("location").get("longitudeE7") / LATLON_E7_DECIMAL_SEPARATOR_
                visited_places_list.append(landmark_place)
            else:
                continue

    with open(f"visited_places_{datetime.now():%Y%m%d%H%M%S}.json", "w") as output_file:
        json.dump(visited_places_list, output_file, indent=4, ensure_ascii=False)

    # 解凍したzipファイル削除
    #shutil.rmtree("./tmp/Takeout")

if __name__ == '__main__':
    main()