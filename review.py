import requests
from bs4 import BeautifulSoup


def req_review(product_url):
    # URL을 읽어서 HTML를 Data에 받아옴(나중에 URL은 검색결과에서 받아옴)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(product_url, headers=headers)


    #data를 검색할수있도록 변경(beautifulsoup 활용)
    soup= BeautifulSoup(data.text,'html.parser' )

    # select를 이용해서, li들을 불러오기
    reviews = soup.select('#tabContent > div > ul.list_review > li')

    # print(reviews)  #정상 확인

    reviews_list=[]
    for review in reviews:
        # title 크롤링
        strong_tag = review.select_one('div > a > strong')
        if strong_tag is not None:
            review_title = strong_tag.text

        # 내용 크롤링
        review_tag = review.select_one('div > p')
        if review_tag is not None:  
            review_contents = review_tag.text

        # 출처
        origin_tag = review.select_one('div > div > span.txt_cate')
        if origin_tag is not None:  
            review_location = origin_tag.text
        # 글쓴이
        reviewer_tag = review.select_one('div > div > span > a')
        if reviewer_tag is not None:  
            reviewer = reviewer_tag.text
        #날짜
        date_tag = review.select_one('div > div > span.txt_info')
        if date_tag is not None:  
            review_date = date_tag.text


        reviews_list.append({
            'title':review_title,
            'contents':review_contents, 
            'location':review_location,
            'reviewer':reviewer,
            'date':review_date
        })
  
    return reviews_list

# print (reviews_list)










