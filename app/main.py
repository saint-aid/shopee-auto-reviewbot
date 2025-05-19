import streamlit as st
import crawler, gpt_service, rpa
from auth import ShopeeAuth

st.title("Shopee 리뷰 자동 응답 MVP")

# Shop ID 입력
shop_id = st.text_input("🏪 Shop ID를 입력하세요", 
    help="Shopee 셀러 센터의 상점 ID를 입력하세요.")

# Step 1: 로그인 및 쿠키 저장
if st.button("🔑 로그인 시작"):
    auth = ShopeeAuth()
    st.info("브라우저 창이 열리면 로그인을 진행해주세요.")
    
    if auth.save_login_cookies():
        st.success("쿠키가 성공적으로 저장되었습니다!")
    else:
        st.warning("로그인을 완료하고 '로그인 완료' 버튼을 클릭해주세요.")

# Step 2: 리뷰 수집
if st.button("📃 리뷰 가져오기"):
    if not shop_id:
        st.error("Shop ID를 입력해주세요!")
    else:
        with st.spinner("리뷰를 수집하고 있습니다..."):
            df = crawler.get_reviews(shop_id)  # shop_id 전달
            if df is not None:
                st.success("리뷰 수집 완료!")
                st.dataframe(df)
            else:
                st.error("리뷰 수집에 실패했습니다.")

# Step 3: GPT 응답 생성
if st.button("💬 GPT 응답 생성"):
    with st.spinner("GPT가 응답을 생성하고 있습니다..."):
        df = gpt_service.bulk_generate()
        st.success("응답 생성 완료!")
        st.dataframe(df)

# Step 4: 리뷰 응답 등록
if st.button("🤖 리뷰 응답 등록"):
    with st.spinner("리뷰 응답을 등록 중입니다..."):
        rpa.post_replies(shop_id)
    st.success("리뷰 응답 등록 완료!")
