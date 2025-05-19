from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time, pickle
import os

def post_replies(shop_id):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=UseDnsHttpsSvcbAlpn")
    driver = webdriver.Chrome(options=options)
    
    try:
        # CSV 파일 로드
        df = pd.read_csv("data/reviews_with_replies.csv")
        
        # 초기 페이지 로드 및 쿠키 설정
        driver.get("https://seller.shopee.kr/")
        time.sleep(2)
        load_cookies(driver)
        driver.refresh()
        time.sleep(3)

        # 리뷰 페이지로 이동
        driver.get("https://seller.shopee.kr/portal/settings/shop/rating?cnsc_shop_id={shop_id}")
        time.sleep(5)

        posted_count = 0
        
        # 각 리뷰에 대해 응답 등록
        for _, row in df.iterrows():
            try:
                if pd.isna(row['reply']) or pd.isna(row['order_id']):
                    continue
                    
                # 주문번호로 리뷰 찾기
                review_element = driver.find_element(By.XPATH, 
                    f"//div[contains(text(), '{row['order_id']}')]//ancestor::div[contains(@class, 'border-solid')]")
                
                # 응답 버튼 찾기 및 클릭
                reply_button = review_element.find_element(By.XPATH, 
                    ".//button[contains(@class, 'eds-react-button text-[#333]') or contains(text(), 'Reply')]")
                driver.execute_script("arguments[0].click();", reply_button)
                time.sleep(1)
                
                # 응답 입력
                textarea = driver.find_element(By.CSS_SELECTOR, "textarea[class*='eds-react-input__textarea']")
                textarea.clear()
                textarea.send_keys(row['reply'])
                time.sleep(1)
                
                # 등록 버튼 클릭
                submit_button = driver.find_element(By.XPATH, 
                    "//button[contains(@class, 'eds-react-button eds-react-button--primary eds-react-button--normal') or contains(text(), 'Submit')]")
                driver.execute_script("arguments[0].click();", submit_button)
                time.sleep(2)
                
                posted_count += 1
                print(f"Posted reply for order {row['order_id']}")
                
            except Exception as e:
                print(f"Error posting reply for order {row['order_id']}: {e}")
                continue
                
        print(f"Successfully posted {posted_count} replies")
            
    except Exception as e:
        print(f"Error during RPA process: {e}")
        
    finally:
        driver.quit()

def load_cookies(driver):
    with open("data/cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)