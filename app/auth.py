from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import streamlit as st

class ShopeeAuth:
    def __init__(self):
        self.login_url = "https://seller.shopee.kr/"
        
    def save_login_cookies(self):
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        
        try:
            driver.get(self.login_url)
            st.info("브라우저에서 로그인을 완료한 후 아래 '로그인 완료' 버튼을 클릭해주세요.")
            
            if st.button("로그인 완료"):
                cookies = driver.get_cookies()
                with open("data/cookies.pkl", "wb") as f:
                    pickle.dump(cookies, f)
                return True
            return False
            
        except Exception as e:
            st.error(f"Error saving cookies: {e}")
            return False
        finally:
            driver.quit()