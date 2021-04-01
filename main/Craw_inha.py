# -*- encoding: utf-8 -*-
# 셀리니움을 불러옵니다.
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pymysql  # pymysql 임포트
import bs4

class Craw_inha:
    def __init__(self, id, pw):
        self.id = id
        self.pw = pw
        self.options = webdriver.ChromeOptions()
        # headless 옵션 설정
        # self.options.add_argument('headless')
        # self.options.add_argument("no-sandbox")
        # 브라우저 윈도우 사이즈
        self.options.add_argument('--start-fullscreen')
        # 사람처럼 보이게 하는 옵션들
        self.options.add_argument("disable-gpu")  # 가속 사용 x
        self.options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
        # 드라이버 위치 경로 입력
        self.driver = webdriver.Chrome('C:\chrome_driver\80\chromedriver.exe', chrome_options=self.options)
        # 접속할 url
        self.url = "https://cyber.inhatc.ac.kr/Main.do?cmd=viewHome"
        # 접속 시도
        self.driver.get(self.url)
        # 10초까지 파싱 시간 기다리기
        self.driver.implicitly_wait(10)  # seconds

    def crawStart(self):

        # 접속 시도
        self.driver.get(self.url)
        # 10초까지 파싱 시간 기다리기
        self.driver.implicitly_wait(10)  # seconds
        self.popx()
        self.driver.find_element_by_id('id').send_keys(self.id)
        self.driver.find_element_by_id('pw').send_keys(self.pw)
        self.driver.find_element_by_class_name('loginBtn').click()
        # driver.find_element_by_id('pw').send_keys(Keys.RETURN)
        self.popx()
        try:
            if (self.driver.find_element_by_id('id')):
                return "로그인 실패"
        except:
            return "로그인 성공"

        
        


    def craw_sub(self,lName):
        try:

            # 학습활동클릭
            self.driver.find_element_by_xpath('//*[@id="3"]').click()

            # 10초까지 파싱 시간 기다리기
            self.driver.implicitly_wait(10)  # seconds

            # 과제클릭
            self.driver.find_element_by_xpath('//*[@id="3"]/ul/li[2]').click()
            # 현재 페이지 소스 가져오기
            html = self.driver.page_source
            # BeautifulSoup로 페이지 소스 파싱
            bs = bs4.BeautifulSoup(html, "html.parser", from_encoding='utf-8')
            # div 태그 중, class가 listContent pb20인 태그를 찾는다.
            table = bs.find('div', attrs={'class': 'listContent pb20'})
            # h4 태그 중, class가 f14인 태그를 찾고 text찾기. 제목
            title = table.find('h4', attrs={'class': 'f14'}).contents[2]
            # h4태그 중 class가 f14인 태그 안에 span태그 text. 진행중 마감
            degree = table.find('h4', attrs={'class': 'f14'}).find('span').text
            degree = (degree).replace('\t', '').replace('\n', '')
            # 불필요한 \t \n제거
            title = (title).replace('\t', '').replace('\n', '')
            title = str(title)
            title = title.replace('\\xa0', '').replace('xa0', '')

            # h4 태그 중, class가 f14인 태그를 찾고 text찾기. 제목
            aCheck = table.find('a', attrs={'class': 'btn small'}).contents[1].replace('\t', '').replace('\n', '')
            # 내용 가져오기
            con = table.find('div', attrs={'class': 'cont pb0'}).text
            con = (con).replace('\t', '').replace('\n', '')
            dt = table.find('td', attrs={'class': 'first'}).text
            dt = (dt).replace('\t', '').replace('\n', '')
            dtls = dt.split('~')
            list1 = [str(lName).strip(), title.strip(), degree.strip(), str(aCheck).strip(), con.strip(), dtls[0].strip(),
                     dtls[1].strip()]

            return list1

        except:
            return "err"


    def craw(self):
        try:
            list2 = []
            print("craw start")
            i = 0
            self.driver.implicitly_wait(10)  # seconds
            self.driver.find_element_by_xpath('//*[@id="mainContent"]/form/div[1]/div[2]/ul/li[1]/a').click()
            self.driver.implicitly_wait(10)  # seconds
            self.driver.find_element_by_xpath('//*[@id="listBox"]/table/tbody/tr[1]/td[7]/a').click()

            html = self.driver.page_source
            bs = bs4.BeautifulSoup(html, "html.parser", from_encoding='utf-8')

            for temp in bs.findAll("option"):
                i = i + 1
                if i == 1:
                    continue

                # 10초까지 파싱 시간 기다리기
                self.driver.implicitly_wait(10)  # seconds
                # 강의 목록 클릭
                self.driver.find_element_by_xpath('//*[@id="conArea"]/div[1]/fieldset/div').click()
                # xpath 문자형 변환 변수로 쓰기위해 str대신 변수써서 반복문 돌릴예정
                temp = '//*[@id="conArea"]/div[1]/fieldset/div/div/ul/li[' + str(i) + ']'
                # 10초까지 파싱 시간 기다리기
                self.driver.implicitly_wait(10)  # seconds

                # 강의사이트접속
                self.driver.find_element_by_xpath(temp).click()
                # 강의명가져오기
                lName = self.driver.find_element_by_xpath('//*[@id="headerContent"]/h1/a').text
                if lName[-1] == "L":
                    continue
                list1 = self.craw_sub(lName)

                if list1 == "err":
                    continue
                # 리스트로 저장

                list2.append(list1)
            return list2
        except:
            print("err")
            return "err"

    def popx(self):
        try:
            # 10초까지 파싱 시간 기다리기
            self.driver.implicitly_wait(3)  # seconds
            # 팝업창 닫기
            self.driver.switch_to_window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
            # dialog 닫기

        except:
            print("no popup")
        try:
            # 10초까지 파싱 시간 기다리기
            self.driver.implicitly_wait(3)  # seconds
            self.driver.find_element_by_class_name('ui-button').click()
        except:
            print("no popup")



