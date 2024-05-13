# 필요한 라이브러리 import
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

title_list = []
author_list = []
company_list = []
date_list = []


# [CODE 0]
def kyobo_crwal(result):
    for page in range(1, 50):  # 2024.05.09일 기준, 온라인 베스트셀러 전체 항목 49페이지까지 존재
        try:
            kyobo_url = 'https://product.kyobobook.co.kr/bestseller/online?period=001&dsplDvsnCode=000&page=%d' % (page)
            # 셀레니움을 사용하기 위한 크롬 웹드라이버
            wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            wd.get(kyobo_url)
            # 웹페이지 연결할 동안 5초 대기
            time.sleep(5)

            html = wd.page_source
            soupKY = bs(html, 'html.parser')

            # 책 제목
            book_title = soupKY.select(
                'div.wrapper > main > section.contents_wrap.aside > div > section > div.tab_wrap.type_line.justify.ui-tabs.ui-corner-all.ui-widget.ui-widget-content > div.tab_wrap.type_tag.type_fold > div.tab_content > div.view_type_list.switch_prod_wrap > ol > li > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a')
            # 책 저자
            book_author = soupKY.select(
                'div.wrapper > main > section.contents_wrap.aside > div > section > div.tab_wrap.type_line.justify.ui-tabs.ui-corner-all.ui-widget.ui-widget-content > div.tab_wrap.type_tag.type_fold > div.tab_content > div.view_type_list.switch_prod_wrap > ol > li > div.prod_area.horizontal > div.prod_info_box > span.prod_author')

            for title, author in zip(book_title, book_author):
                # \n 및 공백 제거 후 데이터 저장
                title_list.append(title.get_text().replace("//n", " ").strip())

                # 저자, 출판사, 출판 일자 값이 null인 경우가 존재하기 때문에 예외 처리를 통해 값을 저장한다.
                try:
                    author_list.append(author.get_text().split("·")[0])  # 저자
                    company_list.append(author.get_text().split("·")[1])  # 출판사
                    date_list.append(author.get_text().split("·")[2])  # 출판 일자

                # 비어있는 경우(IndexError 발생 시) 출판사와 출판 일자도 null값 저장
                except IndexError:
                    company_list.append(author.get_text().split("·")[0])
                    date_list.append(author.get_text().split("·")[0])
                    pass
        except:
            pass

    # 항목별 저장한 값을 result에 병합
    for title_result, author_result, company_result, date_result in zip(title_list, author_list, company_list,
                                                                        date_list):
        result.append([title_result] + [author_result] + [company_result] + [date_result])
        print(title_result)


def main():
    result = []

    print("------------------ 교보문고 온라인 베스트셀러 정보를 수집합니다. ------------------ \n")

    kyobo_crwal(result)  # [CODE 0]

    # DataFrame으로 전환 후 columns값 지정
    kyobo_tbl = pd.DataFrame(result, columns=('제목', '저자', '출판사', '출판일자'))
    # csv 파일로 저장(인코딩 확인)
    kyobo_tbl.to_csv('/Users/hoon/Desktop/빅데이터분석개론실습/실습/docs/kyobo/2-김지훈-201835641.csv', encoding='cp949', mode='w',
                     index=True)

    print("\n------------------ 베스트셀러 정보 수집이 완료되었습니다. ------------------")

if __name__ == '__main__':
  main()