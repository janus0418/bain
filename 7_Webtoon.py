import requests
from bs4 import BeautifulSoup as BS


url = "https://comic.naver.com/webtoon/list.nhn?titleId=662774&weekday=wed"
res = requests.get(url)
res.raise_for_status()

soup = BS(res.text, "lxml")
# print(soup.title)
# print(soup.title.get_text())

# 페이지에 대한 구조 이해가 높을 떄 :
# print(soup.a) # soup객체에서 처음 발견괴는 a element
# print(soup.a.attrs) # a element의 속성 정보
# print(soup.a["href"]) # a element의 href 속성 값

# 페이지에 대한 구조 이해가 낮을 때 : find의 이용
cartoons = soup.find_all("td", attrs = {"class":"title"})
# title = cartoons[0].a.get_text()
# print(title) # testing title print
link = "https://comic.naver.com" + cartoons[0].a["href"]
# print(link)

# 만화 제목 및 링크 구하기

# ---제목이랑 링크 따와서 dictionary로 정리후 출력
# res_title_link = {}
# for x in cartoons:
#     title = x.a.get_text()
#     link = "https://comic.naver.com" + x.a["href"]
#     res_title_link[title] = link
# # print("133화 링크 : ", res_title_link["2부 133화"])

# ---정리된 dictionary 값 차례대로 출력 및 dictionary 총 길이 첨부
# for n in res_title_link:
#     print(n, " : ", res_title_link[n])
# print("총 개수 : ", res_title_link.__len__())

# 평점 및 평점 평균 구하기
cartoon_rate = soup.find_all("div", attrs={"class":"rating_type"})

# list로 정리
res_rates = []
for rate in cartoon_rate:
    res_rates.append(rate.find("strong").get_text())

total = 0
for n in res_rates:
    total += float(n) #받은 txt를 숫자로 변환
print(res_rates)
print("avg : ", total/len(res_rates))



