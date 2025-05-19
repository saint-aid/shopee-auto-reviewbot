# Shopee 리뷰 자동 응답 MVP
*shopee-reviewbot*

✅ 목적
Shopee 셀러를 위한 리뷰 자동 응답 시스템입니다.

GPT가 생성한 자동 응답을 Shopee 판매자 관리자 페이지에 자동으로 입력하여, 운영자 개입 없이 리뷰 응답을 완료하는 자동화 단계입니다.


🧩 구성 요소
 - selenium: 브라우저 자동 제어

 - 이미 로그인된 cookies.pkl 재사용

 - data/reviews_with_replies.csv: GPT 응답이 포함된 파일로부터 응답할 리뷰들을 로딩


## 설치 방법
1. 저장소 클론
2. 필요한 패키지 설치: `pip install -r requirements.txt`

## 사용 방법
1. .env 파일을 만들고 OPENAI_API_KEY = [API key 입력]
2. `streamlit run app.py`
3. Shop ID 입력
4. 로그인 진행
5. 리뷰 수집 및 응답 생성
6. 리뷰 자동 등록


## 자동 응답 흐름
1. 로그인 세션 복원
   - cookies.pkl로 로그인 상태 복구

4. 리뷰 리스트 페이지 이동
   - 리뷰 관리 URL로 이동 (예: https://seller.shopee.sg/portal/product/rating)

3. 리뷰 식별 (review ID or reviewer info 등)
   - csv의 리뷰 content를 기준으로 DOM 내 리뷰와 매칭

5. 답변 입력창 클릭 후 응답 입력
   - GPT 응답을 textarea에 입력

5. [제출/등록] 버튼 클릭


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

