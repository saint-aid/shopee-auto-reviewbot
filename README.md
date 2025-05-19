# Shopee 리뷰 자동 응답 MVP
*shopee-review-autobot*


Shopee 셀러를 위한 리뷰 자동 응답 시스템입니다.

## 설치 방법
1. 저장소 클론
2. 필요한 패키지 설치: `pip install -r requirements.txt`

## 사용 방법
1. `streamlit run app.py`
2. Shop ID 입력
3. 로그인 진행
4. 리뷰 수집 및 응답 생성
5. 리뷰 자동 등록


## 파이프라인 구조 및 흐름

🔍 1단계: 리뷰 및 셀러 응답 크롤링
Shopee 관리자 페이지에서 리뷰(content)와 판매자 응답(seller_response)을 가져옵니다.

결과는 reviews.csv로 저장됩니다.

사용 도구: app/crawler.py



🧠 2단계: GPT로 리뷰 분석 및 응답 생성
GPT API를 통해 리뷰 내용을 분석하고, 자동 응답 문장을 생성합니다.

기존에 응답이 있는 경우는 제외하거나, 덮어쓸 수 있습니다.

결과는 reviews_with_replies.csv에 저장됩니다.

사용 도구: app/gpt_service.py



🤖 3단계: RPA로 Shopee 관리자 페이지에 자동 응답 등록
GPT가 만든 응답을 Shopee 관리자 페이지에 자동으로 입력하고 제출합니다.

자동 로그인은 이미 저장된 cookies.pkl을 통해 처리합니다.

사용 도구: app/rpa.py





🔁 전체 흐름 요약
| 단계 | 작업 내용          | 결과 파일                      | 사용 코드            |
| -- | -------------- | -------------------------- | ---------------- |
| 1  | 리뷰 + 응답 수집     | `reviews.csv`              | `crawler.py`     |
| 2  | GPT 자동 응답 생성   | `reviews_with_replies.csv` | `gpt_service.py` |
| 3  | 리뷰 자동 등록 (RPA) | Shopee 관리자 페이지에 등록         | `rpa.py`         |




## Streamlit 예시화면
![shopee 자동응답기 mvp](https://github.com/user-attachments/assets/1b297702-e0b9-4839-9f92-96a8385b113c)

