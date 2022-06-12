# 알고리즘 3: 음료의 대기열 순서를 고려하며, 특정 개수의 음료 만을 동시에 제작하나, 
# 그 개수를 고정하지 않고, 공식 등을 통해 유동적으로 변경하는 알고리즘

import numpy as np
from main_2 import *
import copy # 깊은 복사에 사용
from utility import read_data_to_2d_array # 파일 읽기에 사용
import json
import time

class Recorder: # 알고리즘 평가 지표 기록 클래스
    def __init__(self):
        self.all_complete_time_list = [] # case 별 모든 작업이 끝날 때까지 걸린 시간 기록
        self.waited_time_list = [] # case 별 기다린 시간 기록
        self.beverage_average_making_time_list = [] # case 별 음료가 만들어지는 시간의 평균 기록
        self.beverage_average_complete_time_list = [] # case 별 음료가 완성된 시간의 평균 기록
        self.team_average_complete_time_list = [] # case 별 팀 음료가 모두 완성된 시간의 평균 기록
        self.average = []
        self.operation_time = []

    def record(self, all_complete_time:int, waited_time:int, beverage_start_time:list, beverage_complete_time:list, team_len:list, time:int):
        self.all_complete_time_list.append(all_complete_time)# case 별 모든 작업이 끝날 때까지 걸린 시간 기록
        self.waited_time_list.append(waited_time)# case 별 기다린 시간 기록

        maiking_time = np.array(beverage_complete_time) - np.array(beverage_start_time) # 만드는데 걸린 시간 np.array()
        self.beverage_average_making_time_list.append(np.mean(maiking_time))# case 별 음료가 만들어지는 시간의 평균 기록
        self.beverage_average_complete_time_list.append(np.mean(beverage_start_time)) # case 별 음료가 완성된 시간의 평균 기록
        
        team_idx = self.team_len_to_team_idx(team_len) # 팀 길이 -> 팀 인덱스 변환
        team_complete_time = [max(beverage_complete_time[i:j]) for i, j in zip([0]+team_idx,team_idx)] # 팀별 끝난 시간 계산
        self.team_average_complete_time_list.append(np.mean(team_complete_time)) # case 별 팀 음료가 모두 완성된 시간의 평균 기록

        self.operation_time.append(time)

    def team_len_to_team_idx(self, team_len) -> list:
        len = 0
        team_idx = []
        for l in team_len:
            len+=l
            team_idx.append(len)
        return team_idx

    def save_to_file(self):
        dic = {}
        dic["average of all_complete_time,waited_time,beverage_average_making_time,beverage_average_complete_time,team_average_complete_time, operation_time"]=self.average
        dic["all_complete_time_list"] = self.all_complete_time_list
        dic["waited_time_list"] = self.waited_time_list
        dic["beverage_average_making_time_list"] = self.beverage_average_making_time_list
        dic["beverage_average_complete_time_list"] = self.beverage_average_complete_time_list
        dic["team_average_complete_time_list"] = self.team_average_complete_time_list
        with open('./algorithm3_data.json','w') as f:
            json.dump(dic, f, indent=4) # 한글 포함된 경우, ensure_ascii=False 옵션 추가

    def print_average(self):
        self.average = [np.mean(self.all_complete_time_list), 
        np.mean(self.waited_time_list), 
        np.mean(self.beverage_average_making_time_list),
        np.mean(self.beverage_average_complete_time_list),
        np.mean(self.team_average_complete_time_list),
        np.mean(self.operation_time) ]

        print("all_complete_time", self.average[0])  
        print("waited_time", self.average[1])  
        print("beverage_average_making_time", self.average[2])
        print("beverage_average_complete_time", self.average[3])
        print("team_average_complete_time", self.average[4])
        print("operation_time", self.average[5])


 # 객체 생성
# machineController = machineController
# MachineController([Machine("에스프레소 머신1", 24), Machine("에스프레소 머신2", 24)],
#                                           [Machine("블렌더1", 30), Machine("블렌더2", 30)],
#                                           [Machine("티 우리기1", 300), Machine("티 우리기2", 300), Machine("티 우리기3", 300), Machine("티 우리기4", 300), Machine("티 우리기5", 300)])



file_path = "Testing_data(비정상 주문)/testing_data(10만(비정상)).txt"
# "Testing_data(비정상 주문)/testing_data(10만(비정상)).txt"
# "Testing_data(비정상 주문)/testing_data(1만(비정상)).txt"
# "Testing_data(정상 주문)/testing_data(1만(정상)).txt"
# "Testing_data(정상 주문)/testing_data(10만(정상)).txt"
team, case = read_data_to_2d_array(file_path)

# order = [] #주문 (음료 큐)
# order = [BevAmericanoIce(), BevEarlGreyTeaIce(), BevCaffeMochaHot(), BevMochaFrappuccino(), BevAmericanoHot(), BevCaramelMacchiatoHot(), BevSignatureChocoHot(), BevColdBrew()]

#  [BevAmericanoIce(), BevEarlGreyTeaIce(), BevEarlGreyTeaIce(), BevMochaFrappuccino(), BevAmericanoHot(), BevMochaFrappuccino(), BevAmericanoIce(), BevAmericanoHot()]

# [BevAmericanoIce(), BevAmericanoIce(), BevAmericanoHot()]  # 주문 (음료 큐)


##--------------------우리가 짜야하는 알고리즘---------------------##

record = Recorder()
temp = []

for t, c in zip(team, case):

    order = [copy.deepcopy(bevList[j]) for j in c]
    # print("[제작할 음료]", end=" ")
    # for beverage in order:
        # print(beverage.name, end=", ")
    # print()

    # 변수 초기화
    person = Person(machineController)
    current_idx = 0 # 실행중 인덱스 초기화
    check = -1 # 무한반복 방지 기계 꽉참 표시 변수

    # doing = 1 # 진행중인 작업 개수 초기화
    doing_idx = 0 # 진행중인 리스트에서 진행중인 작업의 인덱스
    doing_list = [0] # 진행중인 작업 인덱스 리스트

    done = 0 # 완료한 음료 수

    waited_time = 0 # 기계를 기다린 시간

    beverage_start_time = [-1]*(len(order)) # 음료 제작을 시작한 시간
    beverage_complete_time = [-1]*len(order) # 음료 제작을 완료한 시간

    start_time = time.time()

    while done != len(order): # 주문이 있는 동안 반복
        res = person.do(order[current_idx]) # 위치의 인덱스 실행
        if res == 2: # 완료한 경우           
            order[current_idx] = None
            done += 1
            doing_list.pop(doing_idx) # 실행중 리스트에서 현재 실행한 값 제외
            check = -1 # 기계 꽉참 해제
            if not doing_list:
                if len(doing_list)<(len(order)-done):# 진행중인 작업 개수 늘릴 수 있을 때
                    temp = 0
                    while order[temp] == None or temp in doing_list: # temp<len(order) and 
                        temp += 1
                    doing_list.append(temp) # 진행중인 리스트에 새로운 인덱스 추가

                else:
                    break
        
        elif res == 1: # 작업이 진행되었을 때
            temp = [order[i] for i in doing_list]
            doing_idx = np.argmin(do.getCurrentStep().usingTime for do in temp)
            current_idx = doing_list[doing_idx]
            continue

        elif res == 0: # 해당 작업을 실행할 수 없는 경우

            if check == current_idx: # 다른 작업을 진행해봤으나, 더 진행이 안되는 경우
                if len(doing_list)<(len(order)-done):# 진행중인 작업 개수 늘릴 수 있을 때
                    temp = 0
                    while order[temp] == None or temp in doing_list: # temp<len(order) and 
                        temp += 1
                    doing_list.append(temp) # 진행중인 리스트에 새로운 인덱스 추가

                else:
                    f = min(machineController.getEarlistEnd(i+1) for i in range(len(machineController.machines)))
                    check = -1 # 기계 꽉참 해제
                    person.timeFlow(f) # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
                    continue

            elif check == -1: # 작업을 더이상 늘릴 수 없고, 다른 작업을 진행해볼 여지가 있을 때
                check = current_idx 
                
        doing_idx = (doing_idx + 1) % len(doing_list) 
        current_idx = doing_list[doing_idx]
        

    record.record(person.usedTime, waited_time, beverage_start_time, beverage_complete_time, t, time.time()-start_time)

record.print_average()
record.save_to_file()

# =========================== 실행 결과 ==========================
# 총 걸린 시간: 572
# 모든 기계 실행중인 동안 기다린 시간: 272
# 음료가 나오기까지 걸린 시간: [42, 325, 351, 401, 409, 494, 557, 572]
# ================================================================
