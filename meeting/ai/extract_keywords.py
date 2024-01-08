from meeting.ai.gpt_api import *
from openai import OpenAI
import re

def keyword(text,keywords_list):
    load_dotenv()
    text = token_check(text)
    result = extract_keywords_from_meeting(text,keywords_list)
   
    # 문자열 변수에 결과 추가
    result_string = f"{result}"

    lines = result_string.split(',')
    for line in lines:
        keywords_list.append(line)

    # keywords_list = re.findall(r'"([^"]*)"', str(keywords_list))
    # 결과 출력
    print(keywords_list)
    return keywords_list

def extract_keywords_from_meeting(file_path,keywords_list):
    # Set up OpenAI client
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    GPT_MODEL = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are the best keyword extractor. You need to extract keywords from the meeting content. All responses should be in Korean."},
        {"role": "user", "content": f"회의 내용이야. {file_path} 에서 회의의 핵심 키워드 2개만 추출해줘  list = {keywords_list}내에 있는 키워드는 제외하고! 다른 사담없이 오직 키워드 단어 2개 쉼표로 구분해서 추출해 "} #수정후
    ]

    # Make API request using the content from the text file
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0.3
    )

    # Extract and return the generated response
    response_message = response.choices[0].message.content
    return response_message

