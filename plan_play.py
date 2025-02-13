import sys

from config import *
from util import parse_me, sort_partners, get_play_potential, get_step


INT_LO_LEVEL = int(LO_LEVEL)
INT_HI_LEVEL = int(HI_LEVEL)


def find_play_plan(range_start, range_end, step_list, online_bonus):
    plans = []
    for sobj in step_list:
        chara_step, name = sobj
        for display_lv in range(INT_LO_LEVEL, INT_HI_LEVEL + 1):
            lower = get_step(
                get_play_potential(LO_SCORE, display_lv), chara_step, online_bonus
            )
            upper = get_step(
                get_play_potential(HI_SCORE, display_lv + 1), chara_step, online_bonus
            )
            plan = (name, chara_step, display_lv, lower, upper)

            if range_start < lower and upper < range_end:
                plans.append(plan)
    return plans


def main():
    multiplier = float(sys.argv[1])
    range_start = float(sys.argv[2])
    range_size = float(sys.argv[3])

    range_end = range_start + range_size

    chara_dict, online_bonus = parse_me(USER_JSON_PATH)

    online_bonus *= multiplier

    print("--- 일반 플랜 ---")
    print(f"필요 진행도 범위: {range_start} ~ {range_end}")
    print(f"가정 점수 범위대: {LO_SCORE} ~ {HI_SCORE}")
    print(f"탐색 대상 레벨대: Lv.{INT_LO_LEVEL} ~ Lv.{INT_HI_LEVEL} (표기레벨)")
    step_list = sort_partners(chara_dict, False)
    plans = find_play_plan(range_start, range_end, step_list, online_bonus)
    if len(plans) == 0:
        print("정확히 매칭할 수 없습니다. 가정 점수 범위를 구체화해주세요.")

    for plan in plans:
        (name, chara_step, display_lv, lower, upper) = plan
        print(
            f"Lv.{display_lv} {lower:.2f} ~ {upper:.2f} | STEP {chara_step:.01f} [{name}]"
        )


if __name__ == "__main__":
    main()
