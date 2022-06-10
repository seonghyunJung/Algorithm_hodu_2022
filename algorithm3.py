# 알고리즘 3: 음료의 대기열 순서를 고려하며, 특정 개수의 음료 만을 동시에 제작하나, 
# 그 개수를 고정하지 않고, 공식 등을 통해 유동적으로 변경하는 알고리즘

import numpy as np
from main_2 import *
import copy # 깊은 복사에 사용
from utility import read_data_to_2d_array # 파일 읽기에 사용

 # 객체 생성
machineController = MachineController([Machine("에스프레소 머신1", 24), Machine("에스프레소 머신2", 24)],
                                          [Machine("블렌더1", 30), Machine("블렌더2", 30)],
                                          [Machine("티 우리기1", 300), Machine("티 우리기2", 300), Machine("티 우리기3", 300), Machine("티 우리기4", 300), Machine("티 우리기5", 300)])
person = Person(machineController)


file_path = "Testing_data(정상 주문)/testing_data(1만(정상)).txt"
team, case = read_data_to_2d_array(file_path)
i = 0
order = [copy.deepcopy(bevList[j]) for j in case[i]]

# order = [] #주문 (음료 큐)
# order = [BevAmericanoIce(), BevEarlGreyTeaIce(), BevCaffeMochaHot(), BevMochaFrappuccino(), BevAmericanoHot(), BevCaramelMacchiatoHot(), BevSignatureChocoHot(), BevColdBrew()]

#  [BevAmericanoIce(), BevEarlGreyTeaIce(), BevEarlGreyTeaIce(), BevMochaFrappuccino(), BevAmericanoHot(), BevMochaFrappuccino(), BevAmericanoIce(), BevAmericanoHot()]

# [BevAmericanoIce(), BevAmericanoIce(), BevAmericanoHot()]  # 주문 (음료 큐)


##--------------------우리가 짜야하는 알고리즘---------------------##



current_idx = 0 # 실행중 인덱스 초기화
doing = 1 # 진행중인 작업 개수 초기화
check = -1 # 무한반복 방지 기계 꽉참 표시 변수
temp = []

done = 0 # 완료한 음료 수

waited_time = 0 # 기계를 기다린 시간
complete_time = [0]*len(order)

while order: # 주문이 있는 동안 반복
    print()
    print("[진행중인 음료 수]", doing)
    print("[완료한 음료 수]", done)
    print("[남은 손님 수]", len(order))
    print("[현재 음료 정보]", order[current_idx].name)
    print("[현재 시간]", person.usedTime)
    res = person.do(order[current_idx]) # 위치의 인덱스 실행
    if res == 2: # 완료한 경우
        print("[제작 완료]", order[current_idx].name)
        order.pop(current_idx) # 해당 인덱스의 값 pop
        complete_time[current_idx+done] = person.usedTime # 끝난 시간 저장
        done += 1
        if doing !=1: # 모든 작업을 끝냈거나, 1개 초과로 실행중일 때
            doing -= 1 # 작업이 끝났으므로, 진행중인 작업 개수 -1
        if current_idx != 0:
            current_idx -= 1 # 처음 작업이 끝난게 아니라면 바로 이전 작업으로 돌아가기(먼저 들어온 음료 먼저 처리하는게 손님이 음료 빨리 받아서 이득)
            print("[음료 변경]", order[current_idx].name)
        
        check = -1 # 기계 꽉참 해제
        continue
    
    elif res == 1: # 작업이 진행되었을 때
        # print("[제작 진행]", end=" ")
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

        continue

    elif res == 0: # 해당 작업을 실행할 수 없는 경우
        print("[제작 실패]", end = " ")

        if check == current_idx: # 다른 작업을 진행해봤으나, 더 진행이 안되는 경우
            if doing<len(order):# 진행중인 작업 개수 늘릴 수 있을 때
                doing+=1 # 진행중인 작업 개수 +1
                print("작업수를 ", doing,"로 증가")

            else:
                f = min(machineController.getEarlistEnd(i+1) for i in range(len(machineController.machines))) # 가장 빨리 끝나는 기계 시간 # 가장 짧은 시간 계산
                waited_time += f # 기다린 시간 추가
                check = -1 # 기계 꽉참 해제
                print("모든 작업이 실행 불가능, 가장 빨리 끝나는 기계가 끝날 때까지",f,"초 기다림")
                person.timeFlow(f) # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
                continue

        elif check == -1: # 작업을 더이상 늘릴 수 없고, 다른 작업을 진행해볼 여지가 있을 때
            print("다른 작업이 실행 가능한지 탐색")
            check = current_idx # 할 일 : 사람이 할 수 있는 일 있는지 보고, 없으면 기계 기다리기...?

        # 실행 중 인덱스 업데이트
    current_idx = (current_idx + 1) % doing # 진행중 음료 개수로 나눈 나머지 값으로 업데이트 하여 동시에 제작하는 음료 수 제한
    print("[음료 변경]", order[current_idx].name)

print()
print("=========================== 실행 결과 ==========================")
print("총 걸린 시간:",person.usedTime)
print("모든 기계 실행중인 동안 기다린 시간:", waited_time)
print("음료가 나오기까지 걸린 시간:",complete_time)
print("================================================================")



# =========================== 실행 결과 ==========================
# 총 걸린 시간: 572
# 모든 기계 실행중인 동안 기다린 시간: 272
# 음료가 나오기까지 걸린 시간: [42, 325, 351, 401, 409, 494, 557, 572]
# ================================================================