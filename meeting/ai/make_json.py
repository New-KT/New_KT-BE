import re 

def mkjs(post):
# 뉴스의 제목과 링크를 저장할 리스트
    titles = []
    links = []

    # 뉴스의 제목과 링크를 추출하여 리스트에 저장
    title = post['title']
    title = re.sub("<.*?>", "", title)
    titles.append(title)

    org_link = post['link']
    links.append(org_link)

    
    return titles, links
