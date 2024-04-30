## 필요한 패키지 import
import urllib.request
import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sys import platform


## ServiceKey 정보 입력
serviceKey = "PrnCXubPpC7QR6yoJ3Fe2us5MIA%2Bcr8zHjEm0Er26tGnMHOFTv9lz47fAygM%2Fo4cTZZroZwtX9t2NjeEADvfgw%3D%3D"

"""크롤러에 필요한 함수 선언"""

#[Code 1]
def getRequestUrl(url):
    # 매개 변수로 받은 url에 대한 요청을 보낼 객체 생성
    req = urllib.request.Request(url)
    try:
        # 요청 객체를 보내서 받은 응답 데이터를 response 객체에 저장
        response = urllib.request.urlopen(req)
        # reponse 객체에 저장된 코드를 확인 만약 코드가 200이면 정상 처리한 것이므로 성공
        # 현재 시간과 Url Request Success 메시지를 출력 후 응답을 utf-8 형식으로 디코딩하여 저장
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            print(response.headers)
            return response.read().decode("utf-8")
   # 요청이 정상적으로 처리되지 않은 예외가 발생하면 에러메시지 출력
    except Exception as e:
            print(e)
            print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
            return None


# [CODE 2]
def getCovidStatsItem(status_dt):
    # 보건복지부_코로나19 감염현황 총괄 통계에서 제공하는 서비스 url 및 파라미터로 데이터 요청 url 구성
    service_url = "http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api"
    parameters = "?apiType=JSON&serviceKey=" + serviceKey
    parameters += "&status_dt=" + status_dt

    url = service_url + parameters

    # 위에서 구성한 url을 [CODE 1] 함수를 호출하여 받은 응답을 response_data에 저장
    response_data = getRequestUrl(url)

    if (response_data == None):
        return None
    else:
        return json.loads(response_data)


# [CODE 3]
def getCovidstatsService(statusDt, endStatusDt):
    jsonResult = []
    result = []
    statusDt = dt.datetime.strptime(statusDt, '%Y%m%d')
    endStatusDt = dt.datetime.strptime(endStatusDt, '%Y%m%d')

    # 크롤링할 날짜 범위를 pd.period_range를 pr_test에 저장
    pr_test = pd.period_range(start=statusDt, end=endStatusDt, freq='D')
    dataEnd = "{0}{1:0>2}{2:0>2}".format(str(endStatusDt), str(12), str(31))
    isDataEnd = 0

    for i in pr_test:
        if (isDataEnd == 1): break
        startDate = i.strftime('%Y%m%d')
        jsonData = getCovidStatsItem(startDate)

        # 응답 데이터가 정상인지 확인
        if (jsonData['resultMsg'] == 'NORMAL SERVICE'):
            # 응답 데이터가 비어있으면 아직 데이터가 입력되지 않은 상태이기 때문에 날짜를 dataEnd에 저장 후 데이터 크롤링 중단
            if jsonData['items'] == '':
                isDataEnd = 1
                dataEnd = str(endStatusDt)
                print("데이터 없음.... \n 제공되는 통계 데이터는 %s년 %s월 %s일 까지입니다." % (
                str(startDate.year), str(startDate.month), str(startDate.day)))
                break
            # 크롤링 하는 JSON 데이터 출력
            print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))

            # 수집한 데이터를 저장
            accDefRate = jsonData['items'][0]['accDefRate']
            accExamCnt = jsonData['items'][0]['accExamCnt']
            accExamCompCnt = jsonData['items'][0]['accExamCompCnt']
            careCnt = jsonData['items'][0]['careCnt']
            dPntCnt = jsonData['items'][0]['dPntCnt']
            gPntCnt = jsonData['items'][0]['gPntCnt']
            hPntCnt = jsonData['items'][0]['hPntCnt']
            resutlNegCnt = jsonData['items'][0]['resutlNegCnt']
            statusDt = jsonData['items'][0]['statusDt']
            statusTime = jsonData['items'][0]['statusTime']
            uPntCnt = jsonData['items'][0]['uPntCnt']

            pageNo = jsonData['pageNo']
            resultCode = jsonData['resultCode']
            totalCount = jsonData['totalCount']

            numOfRows = jsonData['numOfRows']
            resultMsg = jsonData['resultMsg']

            print('----------------------------------------------------------------------')
            # 수집한 데이터를 딕셔너리 자료형으로 구성하여 jsonResult 리스트에 원소로 추가
            jsonResult.append({
                'accDefRate': accDefRate,
                'accExamCnt': accExamCnt,
                'accExamCompCnt': accExamCompCnt,
                'careCnt': careCnt,
                'dPntCnt': dPntCnt,
                'gPntCnt': gPntCnt,
                'hPntCnt': hPntCnt,
                'resultNegCnt': resutlNegCnt,
                'statusDt': statusDt,
                'statusTime': statusTime,
                'uPntCnt': uPntCnt,
                'pageNo': pageNo,
                'resultCode': resultCode,
                'totalCount': totalCount,
                'numOfRows': numOfRows,
                'resultMsg': resultMsg
            })
            result.append(jsonResult)
    # 수집한 데이터를 반환
    return (jsonResult, result, dataEnd, totalCount)

# [CODE 0]
def main():
    jsonResult = []
    result = []

    # 데이터 수집할 날짜를 입력받음
    print("보건복지부_코로나19 감염현황 총괄 통계 데이터를 수집합니다.")
    statusDt = input('데이터를 수집을 시작할 날짜를 입력해 주세요 ex)20201028 : ')
    endStatusDt = input('데이터를 수집을 마칠 날짜를 입력해 주세요 ex)20211028 : ')

    # [CODE 3] getCovidstatsService() 함수를 호출하여 반환된 결과를 변수에 저장
    jsonResult, result, dataEnd, totalCount = getCovidstatsService(statusDt, endStatusDt)

    # 수집된 데이터의 개수가 0개인 경우 에러 메시지 출력
    if (totalCount==0) : #URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        # 수집된 데이터를 딕셔너리 리스트로 저장한 후 jsonResult를 json.dumps()를 통해 json 객체로 변환 후 JSON 파일에 저장
        with open(f'./{statusDt}_{endStatusDt}.json','w', encoding="utf-8") as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=False, ensure_ascii=False)
            outfile.write(jsonFile)

        result_df = pd.read_json(f'./{statusDt}_{endStatusDt}.json')
        # 데이터프레임 컬럼을 한글로 변환
        result_df.rename(columns={'accDefRate' : '누적확진율',
                  'accExamCnt' : '누적검사수',
                  'accExamCompCnt' : '누적검사완료수',
                  'careCnt' : '치료중환자수',
                  'dPntCnt' : '격리해제수',
                  'gPntCnt' : '사망자수',
                  'hPntCnt' : '확진자수',
                  'numOfRows' : '한 페이지 결과 수',
                  'pageNo' : '페이지 번호',
                  'resultCode' : '결과코드',
                  'resultMsg' : '결과메시지',
                  'resultNegCnt' : '결과음성수',
                  'statusDt' : '기준일자',
                  'statusTime' : '기준시간',
                  'totalCount' : '전체 결과 수',
                  'uPntCnt' : '검사중수'}, inplace=True)
        # 데이터프레임 객체인 result_df를 CSV 파일로 저장
        result_df.to_csv(f'./{statusDt}_{endStatusDt}.csv', index=False, encoding="utf-8")


"""보건복지부_코로나19 감염현황 총괄 통계 크롤링 시작 """
if __name__ == '__main__':
    main()


"""월 별 변화 그래프"""

def plot_covid_stats(data_csv):
    # data_csv = './20201028_20210228.csv'
    # CSV 파일 읽기
    df = pd.read_csv(data_csv)

    # '기준일자'을 Datetime으로 변환
    if '기준일자' not in df.columns:
        raise ValueError("'기준일자 컬럼이 존재하지 않습니다. 컬럼명을 확인해주세요.")

    # 기준일자를 YYYYMMDD 형식으로 변환
    df['기준일자'] = pd.to_datetime(df['기준일자'], format='%Y%m%d', errors='coerce')

    # 월 단위로 변환
    df['기준월'] = df['기준일자'].dt.to_period('M')

    # 일 기준으로 되어있던 데이터를 월 단위 계산하여 변경
    monthly_data = df.groupby('기준월').agg({
        '누적확진율': 'mean',
        '누적검사수': 'sum',
        '누적검사완료수': 'sum',
        '치료중환자수': 'sum',
        '격리해제수': 'sum',
        '사망자수': 'sum',
        '확진자수': 'sum',
        '결과음성수': 'sum',
        '검사중수': 'sum',
    }).reset_index()

    # 한글 깨짐 문제 해결
    plt.rc('font', family='AppleGothic') # 맥

    # LinePlot 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['누적확진율'], marker='o', label='accDefRate')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['누적검사수'], marker='o', label='accExamCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['누적검사완료수'], marker='o', label='accExamCompCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['치료중환자수'], marker='o', label='careCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['격리해제수'], marker='o', label='dPntCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['사망자수'], marker='o', label='gPntCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['확진자수'], marker='o', label='hPntCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['결과음성수'], marker='o', label='resultNegCnt')
    plt.plot(monthly_data['기준월'].astype(str), monthly_data['검사중수'], marker='o', label='uPntCnt')

    # 그래프 설정
    plt.xlabel('기준 월')
    plt.ylabel('총 인원')
    plt.title('월별 코로나19 감염현황 총괄 통계')
    plt.legend()
    plt.grid(True)

    plt.show()  # 그래프 표시

def main():
    plot_covid_stats('./20201028_20210228.csv')

# 코드 실행
if __name__ == '__main__':
    main()