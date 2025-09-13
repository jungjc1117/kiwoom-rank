import requests
import json

# 접근토큰 발급
def fn_au10001(data):
    url = 'https://mockapi.kiwoom.com/oauth2/token'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('token')
        print("Access Token:", access_token)
        return access_token
    else:
        print("Token Error:", response.status_code, response.text)
        return None

# 실시간종목조회순위
def fn_ka00198(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    host = 'https://mockapi.kiwoom.com' # 모의투자
    #host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/stkinfo'
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'authorization': f'Bearer {token}',
        'cont-yn': cont_yn,
        'next-key': next_key,
        'api-id': 'ka00198',
    }

    # 3. API 요청 및 응답 처리
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
        
        # JSON 응답을 파싱
        response_data = response.json()
        print("\nAPI Response:")
        print(json.dumps(response_data, indent=4, ensure_ascii=False))

        # 'item_inq_rank' 데이터만 추출하여 출력 (API 응답 구조에 맞게)
        if 'item_inq_rank' in response_data:
            print("\nReal-time Stock Search Ranking:")
            for item in response_data['item_inq_rank']:
                print(f"Rank: {item['bigd_rank']}, Stock: {item['stk_nm']} ({item['stk_cd']}), Current Price: {item['past_curr_prc']}")
        else:
            print("\n'item_inq_rank' key not found in the response.")
            
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"\nAPI Request Error: {e}")
        return None

# 실행 구간
if __name__ == '__main__':
    access_params = {
        'grant_type': 'client_credentials',
        'appkey': 'qDyfxixyK38gUcyxhhiV8RKDD_LALkd-zBzDYcWJQP4',
        'secretkey': 'egNgDJdNQkg6b8t5UBfGu-pAr0UJwlzGapfVwc73vn0',
    }

    MY_ACCESS_TOKEN = fn_au10001(data=access_params)

    if MY_ACCESS_TOKEN:
        params = {
            "qry_tp": "5"
        }
        fn_ka00198(token=MY_ACCESS_TOKEN, data=params)
# next-key, cont-yn 값이 있을 경우
# fn_ka10001(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
	
'''

    "item_inq_rank": [
        {
            "stk_nm": "키움증권",
            "bigd_rank": "1",
            "rank_chg": "0",
            "rank_chg_sign": "N",
            "past_curr_prc": "+70700",
            "base_comp_sign": "2",
            "base_comp_chgr": "+0.57",
            "prev_base_sign": "3",
            "prev_base_chgr": "0.00",
            "dt": "20250827",
            "tm": "085900",
            "stk_cd": "005930"
        },
        {
            "stk_nm": "키움증권",
            "bigd_rank": "2",
            "rank_chg": "-1",
            "rank_chg_sign": "-",
            "past_curr_prc": "+206000",
            "base_comp_sign": "2",
            "base_comp_chgr": "+0.49",
            "prev_base_sign": "3",
            "prev_base_chgr": "0.00",
            "dt": "20250827",
            "tm": "085900",
            "stk_cd": "039490"
        },
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
'''