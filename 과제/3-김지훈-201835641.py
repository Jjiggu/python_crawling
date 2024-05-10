import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def get_top100(top100_url, top100_name):
    url = 'https://finance.naver.com/sise/sise_quant.nhn'
    result = requests.get(url)
    html = BeautifulSoup(result.content.decode('euc-kr', 'replace'), 'html.parser')
    top_100 = html.find_all('a', {'class': 'tltle'})

    for i in range(100):
        url = 'http://finance.naver.com' + top_100[i]['href']
        # print(url)
        top100_url.append(url)
        company_name = top_100[i].string
        print(company_name)
        top100_name.append(company_name)
    return (top100_url, top100_name)


def main():
    top100_url = []
    top100_name = []
    print(f'\n---------{datetime.datetime.now()} 기준 네이버 금융 거래 상위 100 기업 목록 정보 수집을 시작합니다. --------- \n')
    top100_url, top100_name = get_top100(top100_url, top100_name)

    top100_tbl = pd.DataFrame(top100_name, columns=['회사명'])
    top100_tbl.to_csv('/Users/hoon/Desktop/빅데이터분석개론실습/실습/docs/finance/3-김지훈-201835641.csv', index=True,
                      encoding='cp949')
    print(f'\n--------- {datetime.datetime.now()} 기준 네이버 금융 거래 상위 100 기업 목록 정보 수집 완료 ---------\n')

if __name__ == '__main__':
    main()