from meeting.ai.extract import *
from meeting.ai.crawling_main import *
import re

def keyword(output_file_path,keywords_list):
    load_dotenv()
    file_path = read_concatenate_news(output_file_path)
    
    result = extract_keywords_from_meeting(file_path,keywords_list)
   
    # 문자열 변수에 결과 추가
    result_string = f"{result}"
   

    lines = result_string.split(',')
    for line in lines:
        keywords_list.append(line)
    print(keywords_list)
    # keywords_list = re.findall(r'"([^"]*)"', str(keywords_list))
    # 결과 출력
    print(keywords_list)
    return keywords_list

def keyword2(text,keywords_list):
    load_dotenv()
    text = token_check(text)
    result = extract_keywords_from_meeting(text,keywords_list)
   
    # 문자열 변수에 결과 추가
    result_string = f"{result}"

    lines = result_string.split(',')
    for line in lines:
        keywords_list.append(line)
    print(keywords_list)
    # keywords_list = re.findall(r'"([^"]*)"', str(keywords_list))
    # 결과 출력
    print(keywords_list)
    return keywords_list