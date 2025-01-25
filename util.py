from config import *
import math

import json


def get_name(chobj):
    base_name = chobj["display_name"][LANG]

    if "variant" in chobj:
        var_name = chobj["variant"][LANG]
        return f"{base_name} ({var_name})"
    return base_name


def parse_me(path):
    with open(path, "rt") as f:
        data = json.load(f)
        chobjs = data["value"]["character_stats"]
        online_bonus = int(data["value"]["subscription_multiplier"])

    chara_dict = {}
    for chobj in chobjs:
        name = get_name(chobj)
        step = chobj["prog"]
        chara_id = chobj["character_id"]
        if chara_id in SKIP_IDS:
            print(f"Skipping {name}")
            continue

        is_hard = False
        if "skill_id_text" in chobj:
            skill_text = chobj["skill_id_text"][LANG]
            if skill_text.startswith("HARD"):
                is_hard = True

        chara_dict[name] = {"hard": is_hard, "step": step}

    print("계정 정보 로드 완료 (https://webapi.lowiro.com/webapi/user/me)")
    print(f"  Arcaea online 월드 진행 보너스: {online_bonus-100}%")
    if OUTPUT_PARTNERS:
        print(f"  파트너 정보를 출력했습니다: ({OUTPUT_PARTNERS})")
        with open(OUTPUT_PARTNERS, "wt") as f:
            json.dump(chara_dict, f, ensure_ascii=False, indent=2)

    return chara_dict, online_bonus / 100.0


def sort_partners(chara_dict, prioritize_hard):
    hard_list = []
    easy_list = []
    for partner, spec in chara_dict.items():
        step = spec["step"]
        if spec["hard"]:
            hard_list.append((step, partner))
        else:
            easy_list.append((step, partner))

    if prioritize_hard:
        hard_list.sort(key=lambda x: x[0], reverse=True)
        easy_list.sort(key=lambda x: x[0], reverse=True)
        return hard_list + easy_list
    else:
        all_list = hard_list + easy_list
        all_list.sort(key=lambda x: x[0], reverse=True)
        return all_list


def get_play_potential(score, base_potential):
    result = base_potential
    if score == 10_000_000:
        result += 2
    elif 9_800_000 <= score:
        result += 1
        result += (score - 9_800_000) / 200_000
    else:
        result += (score - 9_500_000) / 300_000
    return 0 if result < 0 else result


def get_step(play_potential, chara_step, online_bonus):
    step = 2.5
    step += 2.45 * math.sqrt(play_potential)
    step *= chara_step / 50
    step *= online_bonus
    return step
