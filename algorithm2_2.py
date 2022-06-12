from main_2 import *
import copy
import time
import numpy as np
INF = 10000

def algor2_2(order):
    # 객체 생성
    person = Person(machineController)

    bevStartTime = {}
    bevEndTime = []
    bevWaitTime = []
    teamWaitTime = []
    doNothingTime = [0]

    # 팀 단위로 끊는 알고리즘 - 대기 시간이 있으면 기다리기만 함
    def oneStep(order, index):
        if index >= len(order):
            return 0
        # print("<<팀 " + str(index) + ">>")
        oneTeam = order[index]
        b = None
        minLeft = INF
        minInd = INF

        listMState = [True, machineController.find(0) is not None, machineController.find(1) is not None,
                      machineController.find(2) is not None]
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
                bevEndTime.append(person.usedTime)
                bevWaitTime.append(person.usedTime - bevStartTime.get(b))

                oneTeam.remove(b)
                if len(oneTeam) == 0:
                    teamWaitTime.append(person.usedTime)

                    order.remove(oneTeam)
                    print("팀 하나 끝")
                    return 2
            return 1
        # 할 수 있는게 없는 경우
        if res == 0:
            if oneStep(order, index + 1) == 0:
                # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
                f1 = machineController.getEarlistEnd(1)
                f2 = machineController.getEarlistEnd(2)
                f3 = machineController.getEarlistEnd(3)
                flow = min(f1, f2, f3)
                person.timeFlow(flow)
                print(str(flow) + "초 대기")

                doNothingTime[0] += flow
                return 3

    while len(order) > 0:
        for index, oneTeam in enumerate(order):
            while len(oneTeam) > 0:
                oneStep(order, index)

    machineController.reset()
    return person.usedTime, bevWaitTime, bevEndTime, teamWaitTime, doNothingTime[0]

if __name__ == '__main__':
    algor2_2([[BevAmericanoIce(),BevAmericanoIce()],[BevMochaFrappuccino()]])

