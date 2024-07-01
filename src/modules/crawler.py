from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import urllib.parse



class address_crawler():
    def __init__(self) -> None:
        chrome_options = Options()

        # chrome_options.add_argument("--headless")
    
        # 브라우저 설정 최적화
        chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화
        chrome_options.add_argument("--disable-gpu")  # GPU 사용 비활성화
        chrome_options.add_argument("--window-size=1280x1696")  # 창 크기 설정
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 로드 비활성화

        # 사용자 에이전트 설정 (크롤링 탐지 회피)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

        # Chrome 프로세스 최적화
        # chrome_options.add_argument("single-process")  # 단일 프로세스 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
        chrome_options.add_argument("--disable-dev-tools")  # 개발자 도구 비활성화
        chrome_options.add_argument("--no-zygote")  # Zygote 비활성

        # 로깅 비활성화 및 자동화 탐지 회피
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    


    def get_address(self, search)->None:
        encoded_search = urllib.parse.quote(search)  # 검색어 인코딩
        url: str = f"https://map.naver.com/p/search/{encoded_search}?c=13.00,0,0,0,dh"
        self.driver.get(url=url)


        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#searchIframe")))

            search_result_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='_pcmap_list_scroll_container']"))
            )

            last_height = self.driver.execute_script("return arguments[0].scrollHeight", search_result_div)
            while True:
                # 스크롤을 아래로
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", search_result_div)
                time.sleep(2)  # 스크롤 후 로딩 대기

                # 스크롤 후 높이 계산
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", search_result_div)
                if new_height == last_height:  # 더 이상 스크롤할 내용이 없으면 중단
                    break
                last_height = new_height

            search_result = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='_pcmap_list_scroll_container']/ul"))
            )


            search_results = search_result.find_elements(By.CSS_SELECTOR, "li.VLTHu.OW9LQ")
            
            for result in search_results:
                try:
                    name = result.find_element(By.CSS_SELECTOR, "span.YwYLL").text  # 장소 이름
                    print(f"Name: {name}")
                except Exception as e:
                    print(f"결과 처리 중 오류 발생: {str(e)}")

                try:
                    button = result.find_element(By.CSS_SELECTOR, " div.KgfA6.D7FgR> span.lWwyx > a")
                    button.click()
                    address = result.find_element(By.CSS_SELECTOR, "div.KgfA6.D7FgR div > div.AbTyi > div.zZfO1").text
                    print(f"address: {address}")
                except Exception as e:
                    print(f"결과 처리 중 오류 발생: {str(e)}")
        except Exception as e:
            print(f"실패: {str(e)}")

    


ad = address_crawler()
ad.get_address("농협은행 지점")
