from main_2 import *
import copy
import time
import numpy as np
INF = 10000

def algor2_1(order):
    person = Person(machineController)

    bevStartTime = {}
    bevEndTime = []
    bevWaitTime = []
    teamWaitTime = []
    doNothingTime = 0
    # 팀 단위로 끊는 알고리즘 - 대기 시간이 있으면 기다리기만 함
    while len(order) > 0:
        for oneTeam in order:
            while len(oneTeam) > 0:
                b = None
                minLeft = INF
                minInd = INF

                listMState = [True, machineController.find(0) is not None,machineController.find(1) is not None,machineController.find(2) is not None]
                for _b in oneTeam:
                    if _b.waiting:
                        continue
                    i = 0
                    leftRecipe = _b.recipe[_b.step:0]
                    for _a in leftRecipe:
                        if minInd > i:
                            break
                        if _a.actType > 0 and listMState[_a.actType]:
                            minInd = i
                            b = _b
                        i += 1

                    if minInd == INF:
                        l = len(leftRecipe)
                        if l < minLeft:
                            minLeft = l
                            b = _b

                if b is None:
                    b = oneTeam[0]

                if b.step == 0:
                    bevStartTime[b] = person.usedTime

                res = person.do(b)
                if res != 0:
                    if res == 2:
                        # bevEndTime[b] = person.usedTime
                        bevEndTime.append(person.usedTime)
                        bevWaitTime.append(person.usedTime - bevStartTime.get(b))

                        oneTeam.remove(b)
                        if len(oneTeam) == 0:
                            teamWaitTime.append(person.usedTime)

                            order.remove(oneTeam)
                            print("팀 하나 끝")
                            break
                # 할 수 있는게 없는 경우
                if res == 0:
                    # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
                    f1 = machineController.getEarlistEnd(1)
                    f2 = machineController.getEarlistEnd(2)
                    f3 = machineController.getEarlistEnd(3)
                    flow = min(f1, f2, f3)
                    person.timeFlow(flow)
                    print(str(flow) + "초 대기")

                    doNothingTime += flow
    machineController.reset()
    print(person.usedTime)
    return person.usedTime, bevWaitTime, bevEndTime, teamWaitTime, doNothingTime
