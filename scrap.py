import requests
from bs4 import BeautifulSoup
import csv

# 웹페이지 주소
url = "https://www.kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do"

# 웹페이지 내용 가져오기
response = requests.get(url)
html = response.text

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 원하는 데이터 추출
menu_elements = soup.select('.table_wrap scroll_table food_table')  # 예시로 클래스명이 'menuName'인 요소를 가져옴

# 추출한 데이터를 CSV 파일로 저장
csv_filename = 'menu_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Menu'])

    for menu_element in menu_elements:
        menu_name = menu_element.get_text(strip=True)
        csv_writer.writerow([menu_name])

print(f'Data saved to {csv_filename}')
