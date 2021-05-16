import requests
url = "http://nadocoding.tistory.com"
headers = {"Usser-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
res = requests.get(url, headers=headers)
print("응답코드 :", res.status_code)
#res.raise_for_status()
with open("mygoogle.html", "w", encoding="utf8") as f:
    f.write(res.text)

