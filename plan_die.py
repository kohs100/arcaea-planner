import sys
from config import *
from util import parse_me, sort_partners, get_step


def find_die_plan(range_start, range_end, step_list, online_bonus):
    assert range_start < range_end

    for sobj in step_list:
        chara_step, _ = sobj

        step = get_step(0, chara_step, online_bonus)
        if step < range_start:
            nxt = find_die_plan(range_start - step, range_end - step, step_list, online_bonus)
            if nxt is None:
                continue
            else:
                return [sobj] + nxt
        elif step > range_end:
            continue
        else:
            return [sobj]
    return None


def main():
    range_start = float(sys.argv[1])
    range_size = float(sys.argv[2])

    range_end = range_start + range_size

    chara_dict, online_bonus = parse_me(USER_JSON_PATH)

    print("--- 폭사 플랜 ---")
    print(f"필요 진행도 범위: {range_start} ~ {range_end}")
    step_list = sort_partners(chara_dict, True)
    plan = find_die_plan(range_start, range_end, step_list, online_bonus)
    for i, (chara_step, partner) in enumerate(plan):
        actual_step = get_step(0, chara_step, online_bonus)
        print(f"{i+1}. 폭사 {actual_step:.2f} | STEP {chara_step:.1f} [{partner}]")


if __name__ == "__main__":
    main()
