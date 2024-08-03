
import requests
from bs4 import BeautifulSoup
import pandas as pd


# 참고: https://dalseobi.tistory.com/159 [달에 앉아있는 서비:티스토리]

"""

로또 결과에 대한 JSON 타입
{
"returnValue": "success",
"drwNo": 1,
"drwNoDate": "2002-12-07",
"firstAccumamnt": 863604600,
"firstPrzwnerCo": 0,
"firstWinamnt": 0,
"totSellamnt": 3681782000,
"drwtNo1": 10,
"drwtNo2": 23,
"drwtNo3": 29,
"drwtNo4": 33,
"drwtNo5": 37,
"drwtNo6": 40,
"bnusNo": 16
}
"""

## 로또 특정 회차 번호 받기
def getLottoNumber(draw_no):
    api_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={draw_no}"

    try:
        print(f"{draw_no}회차 로또 번호 받는중.. ")
        
        res = requests.get(api_url)
        res.raise_for_status()

        data = res.json()
        return {
            'drwNo' : data['drwNo'],
            'date': data['drwNoDate'], 
            'lottoNumb': [data[f"drwtNo{i}"] for i in range(1, 7)], 
            'bonusNumb': data['bnusNo']
        }

        
    except requests.exceptions.RequestException as e:
        print(f"오류가 발생했습니다: {e}")
        
## get most recent 
def getMaxRound():
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    max_numb = soup.find(name="strong", attrs={"id": "lottoDrwNo"}).text
    return int(max_numb)

## csv file update 
def updateCSV(csv_path) :
    print("로또 번호 최신 회차까지 업데이트...")
    maxRound = getMaxRound()
    
    ## check csv
    try :
        nums = pd.read_csv(csv_path)

        # csv 에 저장된 가장 최근 회차 +1 부터 번호 받기
        startInd = nums['round'].iloc[-1]+1
        new = False
        
        if startInd > maxRound :
            print("이미 최신임.") 
        else : 
            print(f"{startInd}회차부터 다운..")
        
            
    except :
        print('csv 파일이 없음. 첫회차부터 다운로드...')
        startInd = 1
        new = True

    updateDic = {
        'round':[],
        'date':[],
        'num1':[],
        'num2':[],
        'num3':[],
        'num4':[],
        'num5':[],
        'num6':[],
        'bonus':[],
    }
    
    for round in range(startInd, maxRound+1) :
        res = getLottoNumber(round)
        
        updateDic['round'].append(res.get('drwNo'))
        updateDic['date'].append(res.get('date'))
        updateDic['num1'].append(res.get('lottoNumb')[0])
        updateDic['num2'].append(res.get('lottoNumb')[1])
        updateDic['num3'].append(res.get('lottoNumb')[2])
        updateDic['num4'].append(res.get('lottoNumb')[3])
        updateDic['num5'].append(res.get('lottoNumb')[4])
        updateDic['num6'].append(res.get('lottoNumb')[5])
        updateDic['bonus'].append(res.get('bonusNumb'))
        
    updated = pd.DataFrame(updateDic)
        
    
    if updated.empty :
        print("업데이트 안함.")
    elif not new:
        ## update existing csv
        nums = pd.concat([nums, updated], ignore_index=True)
        nums.to_csv(csv_path, index=False )
    else :
        # new csv
        updated.to_csv(csv_path, index=False)
        
    return nums
        