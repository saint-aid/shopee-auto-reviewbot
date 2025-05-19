from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, pickle

LOGIN_URL = "https://seller.shopee.kr/"

def save_login_cookies():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(LOGIN_URL)
    input("🔐 로그인 후 Enter 창 유지...")
    cookies = driver.get_cookies()
    with open("data/cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)
    print("✅ 쿠키 저장 완료!")
    driver.quit()

if __name__ == "__main__":
    save_login_cookies()