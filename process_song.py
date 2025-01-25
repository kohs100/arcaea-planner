import json
import csv
from config import *

LEVELS = set(["[PST]", "[PRS]", "[FTR]", "[BYD]", "[ETR]"])


def get_bp_dict():
    with open(SONG_LIST_PATH, "rt") as f:
        songs = json.load(f)
    found = {song: False for song in songs}

    bp_dict = {}
    with open(BP_DB_PATH, "rt") as f:
        rdr = csv.reader(f)
        _ = next(rdr)
        head_row = next(rdr)

        assert head_row[4] == "LV"
        assert head_row[5] == "BP"
        assert head_row[6] == "곡명"

        for row in rdr:
            [lv, bp, fullname] = row[4:7]
            name = fullname[:-6]
            name_lvl = fullname[-5:]
            assert name_lvl in LEVELS, fullname

            [major, minor] = bp.split(".")
            major, minor = int(major), int(minor)
            assert minor < 10
            int_bp = major * 10 + minor

            if int_bp not in bp_dict:
                bp_dict[int_bp] = []
            if name in songs:
                assert name in found
                found[name] = True
                bp_dict[int_bp].append((name, name_lvl))
    print("BP 데이터베이스 로드 완료 (https://x.com/arcaea_sheet_kr)")
    for song in found:
        if not found[song]:
            raise KeyError(f"Song {song} not found in DB!")

    bp_dict = dict(sorted(bp_dict.items(), key=lambda item: item[0]))
    if OUTPUT_BP_DICT:
        with open(OUTPUT_BP_DICT, "wt") as f:
            # Print sorted dictionary as-is
            print(f"  선호곡 BP 정보를 출력했습니다: ({OUTPUT_BP_DICT})")
            json.dump(bp_dict, f, sort_keys=False, indent=2, ensure_ascii=False)

    return bp_dict


if __name__ == "__main__":
    get_bp_dict()
