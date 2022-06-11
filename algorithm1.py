import numpy as np
from main_2 import *
import copy
from utility import read_data_to_2d_array

# 객체 생성
machineController = MachineController([Machine("에스프레소 머신1", 24), Machine("에스프레소 머신2", 24)],
                                          [Machine("블렌더1", 30),
                                           Machine("블렌더2", 30)],
                                          [Machine("티 우리기1", 300), Machine("티 우리기2", 300), Machine("티 우리기3", 300), Machine("티 우리기4", 300), Machine("티 우리기5", 300)])
person = Person(machineController)


file_path = "test_case_10.txt"
team, case = read_data_to_2d_array(file_path)

timeAll = []
waitAll = []
bevAll = []
bevCompAll = []

caseNo = 0
for t, c in zip(team, case):
    person.usedTime = 0
    waitingTime = 0
    bevStartTime = [0 for i in range(len(c))]
    bevCompTime = []
    bevTime = [0 for i in range(len(c))]

    caseNo += 1

    print()
    print("[ 테스트 케이스 ", caseNo, "]")

    order = [copy.deepcopy(bevList[j]) for j in c]
    print("[제작할 음료]", end=" ")
    for beverage in order:
        print(beverage.name, end=", ")
    print("\n")

    orderLen = len(order)
    while len(order) > 0:
        flag1 = False    # 기계 동작이 존재
        flag2 = False    # 사람 동작이 존재
        flag3 = False    # 기계 동작 실행 성공
        count = -1      
        currentOrder = []
        machineOrder = []
        personOrder = []

        # 음료별 현재 처리해야 할 act 기록
        for b in order:
            currentOrder.append(b.getCurrentStep())

        # act를 기계와 사람의 일로 분리
        for c in currentOrder:
            count += 1
            if c.actType > 0:
                machineOrder.append(count)
            if c.actType == 0:
                personOrder.append(count)

        # 기계동작이 존재하면 flag1을 True로 변경
        if len(machineOrder) > 0:
            flag1 = True
        if len(personOrder) > 0:
            flag2 = True

        # 기계동작이 존재하는 경우: 모든 기계 동작을 확인
        # 대기 중이면 다음 동작을 확인, 대기 중이지 않으면 실행함
        if flag1:
            for m in machineOrder:
                b = order[m]
                res = person.do(b)
                if res != 0:
                    if order[m].step <= 1 and bevStartTime[m] == 0:
                        bevStartTime[m] = person.usedTime
                    flag3 = True
                    break
                if res == 0:
                    continue
        
        # 기계동작이 존재하지 않거나 모든 기계가 대기중인 경우:
        # 기계가 필요없는 일을 한 바퀴 실행하면서 대기를 빼기
        # 기계가 필요없는 일이 존재하지 않는 경우에는 대기하기
        # 완료된 음료가 존재하면 오류 방지를 위해 break하기
        if not flag3:
            if not flag2:
                f1 = machineController.getEarlistEnd(1)
                f2 = machineController.getEarlistEnd(2)
                f3 = machineController.getEarlistEnd(3)
                f = min(f1, f2, f3)
                waitingTime += f
                person.timeFlow(f)
                print(str(f) + "초 대기")
            for p in personOrder:
                b = order[p]
                res = person.do(b)
                if res != 0:
                    if order[p].step <= 1 and bevStartTime[p] == 0:
                        bevStartTime[p] = person.usedTime
                    if res == 2:
                        bevCompTime.append(person.usedTime)
                        order.remove(b)
                        break
                if res == 0:
                    continue
    for t in range(orderLen):
        bevTime[t] = bevCompTime[t] - bevStartTime[t]

    bevAvg = sum(bevTime) / orderLen
    bevCompAvg = sum(bevCompTime) / orderLen

    print()
    print("=========================== 실행 결과 ==========================")
    print("총 걸린 시간: ", person.usedTime)
    print("모든 기계 실행중인 동안 기다린 시간: ", waitingTime)
    print("음료 별 제작에 걸린 시간: ", bevTime)
    print("음료 별 제작에 걸린 시간의 평균: ", bevAvg)
    print("음료 별 제작이 끝나는 시간: ", bevCompTime)
    print("음료 별 제작이 끝나는 시간의 평균: ", bevCompAvg)
    print("================================================================")
    print()

    timeAll.append(person.usedTime)
    waitAll.append(waitingTime)
    bevAll.append(bevAvg)
    bevCompAll.append(bevCompAvg)

timeAllAvg = sum(timeAll) / len(case)
waitAllAvg = sum(waitAll) / len(case)
bevAllAvg = sum(bevAll) / len(case)
bevCompAllAvg = sum(bevCompAll) / len(case)

print()
print("=========================== 전체 실행 결과 ==========================")
print("총 걸린 시간의 평균: ", timeAllAvg)
#print("모든 기계 실행중인 시간 동안 기다린 시간: ", waitAll)
print("모든 기계 실행중인 동안 기다린 시간의 평균: ", waitAllAvg)
#print("음료 별 제작에 걸린 시간: ", bevAll)
print("음료 별 제작에 걸린 시간의 전체 평균: ", bevAllAvg)
#print("음료 별 제작이 끝나는 시간: ", bevCompAll)
print("음료 별 제작이 끝나는 시간의 전체 평균: ", bevCompAllAvg)
print("====================================================================")
print()
