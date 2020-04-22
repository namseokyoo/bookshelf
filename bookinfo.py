import requests
from bs4 import BeautifulSoup


def req_info(product_url):
    # URL을 읽어서 HTML를 Data에 받아옴
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(product_url, headers=headers)


    #data를 검색할수있도록 변경(beautifulsoup 활용)
    soup= BeautifulSoup(data.text,'html.parser' )

    # select를 이용
    # title 크롤링
    bookinfo = soup.select('#tabContent > div > div > div.wrap_cont > strong')
    title = bookinfo[0].getText().strip()

    # 저자명
    bookinfo = soup.select('#tabContent > div > div > div > dl > dd')
    author = bookinfo[0].getText().strip()

    # 출판사/출간일
    bookinfo = soup.select('#tabContent > div > div > div > dl > dd ')
    company_date = bookinfo[1].getText()
    c_d = company_date.split("|")
    company= c_d[0].strip()
    date = c_d[1].strip()

    #imag
    bookinfo = soup.select('#tabContent > div > div > div > span.thumb > img ')
    img = bookinfo[0].get('src')
    info=[]
    info=({
        'title':title,
        'author':author,
        'company':company,
        'date':date,  
        'img':img  
    })
    
    return info


# print (reviews_list)










