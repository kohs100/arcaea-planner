import sys

from config import *
from util import parse_me, sort_partners, get_play_potential, get_step

from process_song import get_bp_dict

PRINT_MAX = 5


def find_prefer_plan(range_start, range_end, step_list, bp_dict, online_bonus):
    plans = []

    bp_list = [(int_bp, songs) for int_bp, songs in bp_dict.items()]
    bp_list.sort(key=lambda x: x[0])

    for sobj in step_list:
        chara_step, name = sobj
        for int_bp, _ in bp_list:
            bp = int_bp / 10.0
            if bp < LO_LEVEL or HI_LEVEL < bp:
                continue
            lower = get_step(get_play_potential(LO_SCORE, bp), chara_step, online_bonus)
            upper = get_step(get_play_potential(HI_SCORE, bp), chara_step, online_bonus)
            plan = (name, chara_step, int_bp, lower, upper)

            if range_start < lower and upper < range_end:
                plans.append(plan)
    return plans


def main():
    range_start = float(sys.argv[1])
    range_size = float(sys.argv[2])

    range_end = range_start + range_size

    chara_dict, online_bonus = parse_me(USER_JSON_PATH)
    bp_dict = get_bp_dict()

    bp_dict_lo = min(int_bp for int_bp in bp_dict) / 10.0
    bp_dict_hi = max(int_bp for int_bp in bp_dict) / 10.0

    eff_bp_lo = LO_LEVEL if LO_LEVEL > bp_dict_lo else bp_dict_lo
    eff_bp_hi = HI_LEVEL if HI_LEVEL < bp_dict_hi else bp_dict_hi
    print("--- 선호곡 플랜 ---")
    print(f"필요 진행도 범위: {range_start} ~ {range_end}")
    print(f"가정 점수 범위대: {LO_SCORE} ~ {HI_SCORE}")
    print(f"탐색 대상 레벨대: BP {eff_bp_lo} ~ BP {eff_bp_hi}")

    step_list = sort_partners(chara_dict, False)
    plans = find_prefer_plan(range_start, range_end, step_list, bp_dict, online_bonus)
    if len(plans) == 0:
        print("정확히 매칭할 수 없습니다. 가정 점수 범위를 구체화해주세요.")

    printed_num = 0
    for plan in plans:
        (name, chara_step, int_bp, lower, upper) = plan
        bp = int_bp / 10.0
        print(
            f"BP {bp:.1f} {lower:.2f} ~ {upper:.2f} | STEP {chara_step:.01f} [{name}]"
        )
        if printed_num < PRINT_MAX:
            for song, song_lv in bp_dict[int_bp]:
                print(f"  {song_lv} {song}")
                printed_num += 1
                if printed_num == PRINT_MAX:
                    break


if __name__ == "__main__":
    main()
