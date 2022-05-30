from main import *

beverage = [Beverage("아메리카노 Hot", [1, 5, 3, 2, 1], [True, False,True, True, True]), # 샷 추출 버튼 클릭(사람) -> 샷 추출(머신) -> 컵에 뜨거운 물(사람) -> 컵에 샷 붓기(사람) -> 손님에게 제공
Beverage("아메리카노 Ice", [1, 5, 2, 3, 2, 1], [True, False,True, True, True, True]) # 샷 추출 버튼 클릭(사람) -> 샷 추출(머신) -> 컵에 차가운 물 및 아이스(사람) -> 컵에 샷 붓기 -> 손님에게 제공
]

son = [[1, 0], [1], [0]] # 손님이 주문한 메뉴
son_left = []
for s in son:
  temp = []
  for i in s:
    temp.append(beverage[i].lenRecipe())
  son_left.append(temp)

print("손님이 주문한 음식", son)
print("주문한 음식이 만들어질때까지 남은 과정 수", son_left)