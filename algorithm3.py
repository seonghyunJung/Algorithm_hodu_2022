# 알고리즘 3: 음료의 대기열 순서를 고려하며, 특정 개수의 음료 만을 동시에 제작하나, 
# 그 개수를 고정하지 않고, 공식 등을 통해 유동적으로 변경하는 알고리즘

import numpy as np
from main_2 import *

 # 객체 생성
machineController = MachineController([Machine("에스프레소 머신1", 10), Machine("에스프레소 머신2", 10)],
                                        [Machine("블렌더1", 30), Machine("블렌더2", 30)])
person = Person(machineController)

# order = [] #주문 (음료 큐)
order = [BevAmericanoIce(), BevAmericanoIce(), BevAmericanoHot()]

#  [BevAmericanoIce(), BevEarlGreyTeaIce(), BevEarlGreyTeaIce(), BevMochaFrappuccino(), BevAmericanoHot(), BevMochaFrappuccino(), BevAmericanoIce(), BevAmericanoHot()]

# [BevAmericanoIce(), BevAmericanoIce(), BevAmericanoHot()]  # 주문 (음료 큐)


##--------------------우리가 짜야하는 알고리즘---------------------##

current_idx = 0 # 실행중 인덱스 초기화
doing = 1 # 진행중인 작업 개수 초기화
check = -1 # 무한반복 방지 기계 꽉참 표시 변수
temp = []

while order: # 주문이 있는 동안 반복
    res = person.do(order[current_idx]) # 위치의 인덱스 실행

    if res == 2: # 완료한 경우
        order.pop(current_idx) # 해당 인덱스의 값 pop
        doing -= 1 # 작업이 끝났으므로, 진행중인 작업 개수 -1
        if current_idx != 0:
            current_idx -= 1 # 처음 작업이 끝난게 아니라면 바로 이전 작업으로 돌아가기(먼저 들어온 음료 먼저 처리하는게 손님이 음료 빨리 받아서 이득)
        
        check = -1 # 기계 꽉참 해제
        continue
    
    elif res == 1: # 작업이 진행되었을 때
        # # 선택지3: 사람이 진행하는 일이 있다면, 해당 작업을 저장, 없다면, 모든 진행중 저장
        # temp = [] # 초기화
        # temp = [i for i in range(doing) if order[i].getCurrentStep().actType == 0]
        # if not temp:
        #     temp = order[:doing]
        # 선택지1 : 진행중인 작업 중 제일 빨리 끝나는 작업 실행
        temp = order[:doing]
        current_idx = np.argmin(do.getCurrentStep().usingTime for do in temp)

        # 선택지2: 맨 처음 작업 실행
        # current_idx = 0

        # 선택지4: 바로 다음 작업 실행
        # pass

        


    elif res == 0: # 해당 작업을 실행할 수 없는 경우
        if doing<len(order):# 진행중인 작업 개수 늘릴 수 있을 때 
            doing+=1 # 진행중인 작업 개수 +1
        elif check == current_idx: # 작업을 더이상 늘릴 수 없는 경우, 다른 작업을 진행해봤으나, 더 진행이 안되는 경우
            # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
            f1 = machineController.getEarlistEnd(1)
            f2 = machineController.getEarlistEnd(2)
            f = min(f1, f2)
            person.timeFlow(f)
            check = -1
            continue
        elif check == -1: # 작업을 더이상 늘릴 수 없고, 다른 작업을 진행해볼 여지가 있을 때
            check = current_idx # 할 일 : 사람이 할 수 있는 일 있는지 보고, 없으면 기계 기다리기...?

    # 실행 중 인덱스 업데이트
    current_idx = (current_idx + 1) % doing # 진행중 음료 개수로 나눈 나머지 값으로 업데이트 하여 동시에 제작하는 음료 수 제한

print(person.usedTime)