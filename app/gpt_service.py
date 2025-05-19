import openai 
import os
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")
    
def generate_reply(review_text, previous_reply=None):
    prompt = f"""
당신은 리뷰에 대해 쇼피 판매자 입장에서 정중하고 친절하게 응답해주세요. 다음 리뷰를 분석하고 친절하고 도움이 되는 답변을 작성해주세요.
리뷰 내용에 맞춰 공감하고, 문제가 있다면 해결방안을 제시하며, 긍정적인 리뷰라면 감사를 표현해주세요.

고객 리뷰:
"{review_text}"

이전 답변:
"{previous_reply or 'N/A'}"

판매자 응답:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

def bulk_generate(input_csv="data/reviews.csv", output_csv="data/reviews_with_replies.csv"):
    df = pd.read_csv(input_csv)
    df["reply"] = df.apply(lambda row: generate_reply(
        review_text=row["content"],
        previous_reply=row.get("seller_response", None)
    ), axis=1)
    df.to_csv(output_csv, index=False)
    print(f"Generated replies for {len(df)} reviews")
    return df
