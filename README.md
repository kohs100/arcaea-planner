# arcaea-planner

Arcaea world mode progress fine tuning calculator.

## Configuration

### 계정 정보 입력

Arcaea 온라인에 로그인된 상태에서 아래 링크에 접속

- https://webapi.lowiro.com/webapi/user/me

json 데이터를 복사하여 `input/me.json` 에 저장

#### 예시 (input/me.json)

```
{
  "success": true,
  "value": {
    "subscription_multiplier": 120,
    "is_aprilfools": false,
    "locked_char_ids": [],
    "user_missions": [
      {
        "status": "claimed",
        "mission_id": "mission_1_1_tutorial",
        "_id": "677e7c694fc895025f1e6f78"
      },
...
```

### config.py

```
LANG = "ko"

# Skip insight(72) and fatalis(55)
SKIP_IDS = [72, 55]

# 일반 플레이시 점수 범위 가정
HI_SCORE = 10_000_000
LO_SCORE = 9_700_000

# 일반 플레이시 BP 범위 가정
HI_LEVEL = 9.5
LO_LEVEL = 4
```

필요에 맞게 설정하기

## Examples

### 선호곡 플래너

```
$ python plan_prefer.py 17.7 1
Skipping 히카리 (Fatalis)
Skipping 혜안 (초월자 - 여덟번째 추적자)
계정 정보 로드 완료 (https://webapi.lowiro.com/webapi/user/me)
  Arcaea online 월드 진행 보너스: 20%
  파트너 정보를 출력했습니다: (./output/partners.json)
BP 데이터베이스 로드 완료 (https://x.com/arcaea_sheet_kr)
  선호곡 BP 정보를 출력했습니다: (./output/bp_dict.json)
--- 선호곡 플랜 ---
필요 진행도 범위: 17.7 ~ 18.7
가정 점수 범위대: 9700000 ~ 10000000
탐색 대상 레벨대: BP 4 ~ BP 9.5
BP 8.0 17.72 ~ 18.69 | STEP 76.0 [코우]
  [FTR] world.execute(me);
BP 9.4 17.75 ~ 18.61 | STEP 72.0 [고독 (초월자 - 여섯 번째 추적자)]
  [PRS] Testify
  [FTR] Equilibrium
  [FTR] Raven's Pride
BP 9.5 17.82 ~ 18.68 | STEP 72.0 [고독 (초월자 - 여섯 번째 추적자)]
  [PRS] Fracture Ray
```

### 난이도 플래너

```
$ python plan_play.py 17.7 4
Skipping 히카리 (Fatalis)
Skipping 혜안 (초월자 - 여덟번째 추적자)
계정 정보 로드 완료 (https://webapi.lowiro.com/webapi/user/me)
  Arcaea online 월드 진행 보너스: 20%
  파트너 정보를 출력했습니다: (./output/partners.json)
--- 일반 플랜 ---
필요 진행도 범위: 17.7 ~ 21.7
가정 점수 범위대: 9700000 ~ 10000000
탐색 대상 레벨대: Lv.4 ~ Lv.9 (표기레벨)
Lv.7 18.02 ~ 19.89 | STEP 80.9 [히카리 (Fracture)]
Lv.8 18.86 ~ 20.63 | STEP 80.9 [히카리 (Fracture)]
Lv.9 19.64 ~ 21.33 | STEP 80.9 [히카리 (Fracture)]
Lv.7 17.82 ~ 19.68 | STEP 80.0 [타이리츠]
Lv.8 18.65 ~ 20.40 | STEP 80.0 [타이리츠]
Lv.9 19.43 ~ 21.10 | STEP 80.0 [타이리츠]
Lv.8 17.72 ~ 19.38 | STEP 76.0 [코우]
Lv.9 18.45 ~ 20.04 | STEP 76.0 [코우]
```

### 폭사 플래너

```
$ python plan_die.py 4.5 1
Skipping 히카리 (Fatalis)
Skipping 혜안 (초월자 - 여덟번째 추적자)
계정 정보 로드 완료 (https://webapi.lowiro.com/webapi/user/me)
  Arcaea online 월드 진행 보너스: 20%
  파트너 정보를 출력했습니다: (./output/partners.json)
--- 폭사 플랜 ---
필요 진행도 범위: 4.5 ~ 5.5
1. 폭사 1.44 | STEP 24.0 [애시드]
2. 폭사 1.44 | STEP 24.0 [애시드]
3. 폭사 2.55 | STEP 42.5 [루나]
```
