import requests
res = requests.get("http://google.com")
print("응답코드 :", res.status_code)
 # 200이면 정상, 403이면 접근 권한 없음

# if res.status_code == requests.codes.ok:
#     print("normal")
# else:
#     print("error.[errorcode : ", res.status_code, "]")

res.raise_for_status()
#calls an error for values other than 200 normal and ends 
#the code atm

print(len(res.text))

with open("mygoogle.html", "w", encoding="utf8") as f:
    f.write(res.text)
