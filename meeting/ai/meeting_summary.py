import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import json
from meeting.ai.gpt_api import *

def summary_meeting(file_path):
    # Set up OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Define system and user messages
    GPT_MODEL = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are the best summarizer for meetings. Summarize the entire content of the meeting efficiently. All responses should be in Korean."},
        {"role": "user", "content": f"회의 전체 내용 텍스트파일이야. 회의 내용을 요약해줘. 회의 제목, 주요 이슈 및 진행상황, 새로운 상황 및 공지사항, 추가 안건 등이 무조건 포함된 회의록 작성해줘 . {file_path}"}
    ]

    # Make API request using the content from the text file
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    # Extract and return the generated response
    response_message = response.choices[0].message.content
    return response_message
 

def mts(summary_text): 
    load_dotenv()
    if summary_text is None:
        return {
            "회의 제목": "",
            "주요 이슈 및 진행상황": "",
            "새로운 상황 및 공지사항": "",
            "추가 안건":"" 
        }
    text = token_check(summary_text)
    # Call the function and print the result
    result = summary_meeting(text)
       
    if result is not None:
        return parse_meeting_result(result)
    else:
        return {
            "회의 제목": "",
            "주요 이슈 및 진행상황": "",
            "새로운 상황 및 공지사항": "",
            "추가 안건":"" 
        }
            

def parse_meeting_result(result_text):
    result_dict = {
        "회의 제목": "",
        "주요 이슈 및 진행상황": "",
        "새로운 상황 및 공지사항": "",
        "추가 안건":"" 
    }
    current_key = None

    # Split the result text into sections based on newlines
    lines = result_text.strip().split('\n')

    for line in lines:
        # Check if the line contains a colon, indicating a key-value pair
        if ':' in line:
            # Split the line into key and value
            key, value = map(str.strip, line.split(':', 1))
            current_key = key
            if key in result_dict:
                result_dict[key] = value
        elif current_key:
            # If there is a current key, append the line to its value
            result_dict[current_key] += ' ' + line

    return result_dict

