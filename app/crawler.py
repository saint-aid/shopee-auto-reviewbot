import pickle, time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def load_cookies(driver):
    with open("data/cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


def get_reviews(shop_id):  # shop_id 파라미터 추가
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=UseDnsHttpsSvcbAlpn")
    driver = webdriver.Chrome(options=options)

    try:
        # 초기 페이지 로드 및 쿠키 설정
        driver.get("https://seller.shopee.kr/")
        time.sleep(2)
        load_cookies(driver)
        driver.refresh()
        time.sleep(3)

        # 리뷰 페이지로 이동 (shop_id 사용)
        review_url = f"https://seller.shopee.kr/portal/settings/shop/rating?cnsc_shop_id={shop_id}"
        driver.get(review_url)
        time.sleep(5)

        reviews = []
        page = 1

        while True:  # 무한 루프로 변경
            #print(f"Processing page {page}")
            
            # 리뷰 목록 가져오기
            rows = driver.find_elements(By.CSS_SELECTOR, "[class*='border-solid']")
            if not rows:
                print("No reviews found")
                break

            # 각 리뷰 처리
            for row in rows:
                try:
                    content = row.find_element(By.CSS_SELECTOR, "div[class*='whitespace-pre-wrap']").text
                    if not content.strip():
                        print("Skipping review with empty content")
                        continue

                     # 더보기 버튼이 있는지 확인하고 클릭
                    try:
                        more_button = row.find_element(By.CSS_SELECTOR, "span[class*='text-[#1f75d5]']")
                        driver.execute_script("arguments[0].click();", more_button)
                        time.sleep(1)  # 내용이 펼쳐질 때까지 대기
                    except NoSuchElementException:
                        pass  # 더보기 버튼이 없는 경우
                    
                    content = row.find_element(By.CSS_SELECTOR, "div[class*='whitespace-pre-wrap']").text
                    
                    review = {
                        "order_id": row.find_element(By.CSS_SELECTOR, "div.underline").text,
                        "product": row.find_element(By.CSS_SELECTOR, "div[class*='font-medium']").text,
                        "content": content,
                        "review_date": row.find_element(By.CSS_SELECTOR, "div[class*='text-xs']").text,
                        "seller_response": ""
                    }
                    
                    try:
                        review["seller_response"] = row.find_element(By.CSS_SELECTOR, "div[class*='leading-4']").text
                    except:
                        pass
                        
                    reviews.append(review)
                    
                except Exception as e:
                    print(f"Error processing review: {e}")
                    continue

            print(f"Collected {len(reviews)} reviews so far")

            # 다음 페이지 버튼이 비활성화되어 있는지 확인
            try:
                next_button = driver.find_element(By.CLASS_NAME, "eds-react-pagination-pager__button-next")
                # 비활성화된 버튼 확인
                if "disabled" in next_button.get_attribute("class"):
                    print("Reached last page")
                    break
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
                page += 1
            except Exception as e:
                print(f"Could not navigate to next page: {e}")
                break

    except Exception as e:
        print(f"Error during crawling: {e}")
    
    finally:
        driver.quit()
        
    # 결과 저장
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_csv("data/reviews.csv", index=False)
        print(f"Saved {len(reviews)} reviews to CSV")
        return df
    return None