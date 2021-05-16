import re

# re -> regular expression 즉 정규식 library를 뜻함
# 정규표현식이란 파이썬만이 아니라 다른 언어에서도 문자열을 정규로써
# 표현할때 쓰는 기호들을 뜻한다. 이 기호들을 메타 문자라고 한다.
# . ^ $ * + ? { } [ ] \ | ( )

# . : 하나의 미지의 문자를 의미, ca.e -> care
# ^ : 문자열의 시작 ^de -> desk, destination
# $ : 문자열의 끝 se$ -> case, base
# * : 바로 앞 문자의 반복 ca*t -> caaat, cat (O), ct(O) -> 0번 반복
# + : 1번 이상 반복 ca+t -> caaat, cat (O), ct(X)
# | : or
# {m,n} : m 이상 n 이하 횟수 반복
# ? : 바로 앞 문자의 or, 있어도 되고 없어도 되고
# [] : 괄호 사이의 문자들과 매치 [abc] -> before(O), dude(X)
#      단, - 를 사용하여 범위 표현 가능 -> [abc]=[a-c], [0123]=[0-3]
#          eg : [a-zA-Z] = 모든 알파벳
#          또한 [] 속에 ^를 쓸 경우 not으로 풀이하며 다른 메타 문자들을 그
#           정의를 동일하게 사용한다. 
#           [^0-9] : 숫자가 아닌 문자만 선택
# () : 그루핑, ()안의 것을 하나로 간주, 즉 (abc)+ 일 경우 abc의 1회 이상 반복

# p는 pattern, 즉 compile 이라는 함수를 통해 조건으로 입력한 약어를
# 데이터에 적용가능한 pattern으로 변환시킨다.
p = re.compile("ca.e") 
# m = p.match("cafe")
# print(m.group())
def print_group(m):
    if m :
        print(m)
    else :
        print("no match")

print_group(p.findall("the long road to the cafe in the cave"))



# def print_match(m) :
#     if m : 
#         print(m.group())
#     else :
#         print("매칭되지 않음")

# m = p.match("cafe")
# print_match(m)
