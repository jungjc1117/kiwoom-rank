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

# 프로그램순매수상위50요청
def fn_ka90003(token, data, cont_yn='N', next_key=''):
	# 1. 요청할 API URL
	host = 'https://mockapi.kiwoom.com' # 모의투자
	# host = 'https://api.kiwoom.com' # 실전투자
	endpoint = '/api/dostk/stkinfo'
	url =  host + endpoint

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {token}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'ka90003', # TR명
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	print('Code:', response.status_code)
	print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

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
		'trde_upper_tp': '2', # 매매상위구분 1:순매도상위, 2:순매수상위
		'amt_qty_tp': '1', # 금액수량구분 1:금액, 2:수량
		'mrkt_tp': 'P00000', # 시장구분 P00101:코스피, P10102:코스닥
		'stex_tp': '1', # 거래소구분 1:KRX, 2:NXT 3.통합
	}

	# 3. API 실행
	fn_ka90003(token=MY_ACCESS_TOKEN, data=params)
    
	# next-key, cont-yn 값이 있을 경우
	# fn_ka90003(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')	
'''
{
	"prm_trde_trnsn":
		[
			{
				"cntr_tm":"170500",
				"dfrt_trde_sel":"0",
				"dfrt_trde_buy":"0",
				"dfrt_trde_netprps":"0",
				"ndiffpro_trde_sel":"1",
				"ndiffpro_trde_buy":"17",
				"ndiffpro_trde_netprps":"+17",
				"dfrt_trde_sell_qty":"0",
				"dfrt_trde_buy_qty":"0",
				"dfrt_trde_netprps_qty":"0",
				"ndiffpro_trde_sell_qty":"0",
				"ndiffpro_trde_buy_qty":"0",
				"ndiffpro_trde_netprps_qty":"+0",
				"all_sel":"1",
				"all_buy":"17",
				"all_netprps":"+17",
				"kospi200":"+47839",
				"basis":"-146.59"
			},
			{
				"cntr_tm":"170400",
				"dfrt_trde_sel":"0",
				"dfrt_trde_buy":"0",
				"dfrt_trde_netprps":"0",
				"ndiffpro_trde_sel":"1",
				"ndiffpro_trde_buy":"17",
				"ndiffpro_trde_netprps":"+17",
				"dfrt_trde_sell_qty":"0",
				"dfrt_trde_buy_qty":"0",
				"dfrt_trde_netprps_qty":"0",
				"ndiffpro_trde_sell_qty":"0",
				"ndiffpro_trde_buy_qty":"0",
				"ndiffpro_trde_netprps_qty":"+0",
				"all_sel":"1",
				"all_buy":"17",
				"all_netprps":"+17",
				"kospi200":"+47839",
				"basis":"-146.59"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
'''