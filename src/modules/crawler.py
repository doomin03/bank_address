from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time



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
        chrome_options.add_argument("single-process")  # 단일 프로세스 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
        chrome_options.add_argument("--disable-dev-tools")  # 개발자 도구 비활성화
        chrome_options.add_argument("--no-zygote")  # Zygote 비활성

        # 로깅 비활성화 및 자동화 탐지 회피
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    


    def get_address(self, search)->None:
        url:str = "https://map.naver.com/p/search/"+search+"?c=5.00,0,0,0,dh"
        self.driver.get(url=url)
        try:
            
            main_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='app-root'] //*[@id='_pcmap_list_scroll_container]/ul']"))
            )

            address = main_div.find_elements(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.qbGlu > div.ouxiq > div > div > span:nth-child(2) > a > span.Pb4bU")        
        except Exception as e:
            print("실패")

    


