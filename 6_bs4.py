import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
# print(soup.title)
# print(soup.title.get_text())
# print(soup.a) # soup 객체에서 처음 발견되는 a element를 반환
# print(soup.a.attrs) # a element의 속성 정보를 반환
# print(soup.a["href"]) # a element의 href 속성 값을 반환


#print(soup.find("a", attrs = {"class" : "Nbtn_upload"}))
# soup개체 중에서 a 태그가 있는 첫번째 element에서 class가 조건 값을 만족하는 것 반환
# 즉, class = "Nbtn_upload" 인 a element를 찾아줘
# 이때 soup.find(attrs = {"class" : "Nbtn_upload"})라고 검색도 가능
# 이때는 해당 class 값이 유일하기 때문에 가능 
# 즉, class = "Nbtn_upload" 인 어떤 element를 찾아줘 

#print(soup.find("li", attrs = {"class" : "rank01"}))
rank1 = soup.find("li", attrs = {"class" : "rank01"})
#print(rank1.a)

print("rank 1 : " + rank1.a.get_text())

#부모로 가기
print(rank1.parent)

# 형제 갖고 오기
print("rank 2 1st :" + rank1.next_sibling) # 출력 안됨
print("rank 2 2nd :" + rank1.next_sibling.next_sibling.a.get_text()) # 출력 됨; 줄과 줄 사이 공백, 계행정보 때문인 경우
#http://www.dreamy.pe.kr/zbxe/CodeClip/163266
#따라서

# rank2 = rank1.next_sibling.next_sibling
# rank3 = rank2.next_sibling.next_sibling
# print(rank3.a.get_text())
# rank2 = rank3.previous_sibling.previous_sibling
# print(rank2.a.get_text())

# 그러나 위 처럼 next_sibling을 두번씩 사용하는 것 등이 분별하기
# 어렵거나 귀찮을 경우 find_next_sibling을 사용
# () 안에 조건을 입력
rank2ver2 = rank1.find_next_sibling("li")
print("rank2ver2 : " + rank2ver2.a.get_text())
rank3ver2 = rank2ver2.find_next_sibling("li")
print("rank3ver2 : " + rank3ver2.a.get_text())

#이를 대량으로 하고 싶을 때
rank1sibs = rank1.find_next_siblings("li")
print( rank1sibs)

# find의 다른 활용 방법
webtoon = soup.find("a", text="갓 오브 하이스쿨-507화")
# 전체중에서 해당 텍스트를 가진 a element를 반환 요구
print("webtoon : ")
print(webtoon)