import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib.request
import re
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

#발급받은 api 입력
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

# 요청형식 만들기
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# 네이버 검색 API를 통해 뉴스 검색
def getNaverSearch(node, srcText, start, display, sort):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s&sort=%s" % (urllib.parse.quote(srcText), start, display, sort)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if responseDecode == None:
        print(f"Error: No response received for URL: {url}")
        return None
    else:
        # print(f"Response received: {responseDecode}")
        return json.loads(responseDecode)

# 뉴스 기사에서 텍스트 추출
def get_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        article_text = soup.find('article').get_text(separator='\n', strip=True)
        return article_text

    except Exception as e:
        print(f"Error while fetching article from {url}: {e}")
        return None

# 결과 저장
def getPostData(post, jsonResult, cnt):
    title = post['title']
    title = re.sub("<.*?>", "", title)

    description = post['description']
    description = re.sub("<.*?>", "", description)

    org_link = post['link']
    
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900') 
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, 
                       'link': org_link, 'pDate': pDate})
    return None

def preprocess_text(text):
    # HTML 태그 제거
    text = re.sub(r'<.*?>', '', text)
    # 특수문자 및 숫자 제거
    text = re.sub(r'[^a-zA-Z가-힣\s]', '', text)
    # 여러 공백을 단일 공백으로 변환
    text = re.sub(r'\s+', ' ', text).strip()
    return text
