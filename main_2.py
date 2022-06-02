# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math

class Beverage:
    name = ""
    recipe = []
    step = 0
    endStep = 0
    waiting = False
    def __init__(self): #, name:str, recipe:list, step:int = 0
        # self.name = name
        # self.recipe = recipe
        self.step = 0
        self.waiting = False
        self.endStep = len(self.recipe)

    def accomplishOneStep(self):
        self.waiting = False
        self.step += 1
        if self.step >= self.endStep:
            # print(self.name + " 완료") ##
            return True
        return False

    def getCurrentStep(self):
        return self.recipe[self.step]

class Machine:
    name = ""
    isUsing = False
    usingTime = 10
    remainingTime = usingTime
    beverage = None

    def __init__(self, name:str, usingTime:int):
        self.name = name
        self.usingTime = usingTime;

    def setBeverage(self, beverage:Beverage):
        self.beverage = beverage

    def use(self, time=0):
        self.isUsing = True
        self.remainingTime -= time
        if(self.remainingTime <= 0):
            print(self.name + " 사용 완료")
            overUse = abs(self.remainingTime)
            self.isUsing = False
            self.remainingTime = self.usingTime
            # self.beverage.recipe.pop(0)
            self.beverage.accomplishOneStep() #모든 음료는 마무리 동작으로 끝난다 가정
            return overUse

class Action:
    name = "행동"
    actType = 0 #0: 사람, 1이상: 기계 종류
    usingTime = 0

    def __init__(self, name:str, actType:int, usingTime):
        self.name = name
        self.actType = actType
        self.usingTime = usingTime

class MachineController:
    machineEspresso = []
    machineBlender = []
    machines = []
    def __init__(self, machineEspresso, machineBlender):
        self.machineEspresso = machineEspresso
        self.machineBlender = machineBlender
        self.machines = [self.machineEspresso, self.machineBlender]

    def find(self, machineKind:int):
        for machine in self.machines[machineKind-1]:
            if machine.isUsing == False:
                self.sendBackward(machineKind-1)
                return machine
        return None

    def timeFlow(self, time):
        for machinesOneType in self.machines:
            for machine in machinesOneType:
                if machine.isUsing:
                    machine.use(time)

    def getEarlistEnd(self, machineKind:int):
        res = 10000 #무한
        for machine in self.machines[machineKind-1]:
            if machine.isUsing:
                res = min(res, machine.remainingTime)
            # else:
            #     return 0
        return res

    def sendBackward(self, machineKind:int):
        self.machines[machineKind-1].append(self.machines[machineKind-1].pop(0))

class Person:
    remainingTime = 0
    usedTime = 0

    def __init__(self):
        self.usedTime = 0

    def do(self, beverage:Beverage):
        #대기 중인 음료이면 건너뛰기
        if beverage.waiting:
            return 0
        res = 1
        doing = beverage.getCurrentStep()
        self.usedTime += doing.usingTime
        #사람 동작인 경우
        if doing.actType == 0:
            if beverage.accomplishOneStep(): #하나 동작 후 음료 완성했으면 알리기
               res = 2 #성공 및 음료 완성
            machineController.timeFlow(doing.usingTime)
            print(beverage.name + ") " + doing.name) ##
        else:
            machine = machineController.find(doing.actType)
            if machine is None:
                return 0 #실패 시 0 반환
            machine.setBeverage(beverage)
            machine.use()
            beverage.waiting = True
            print(beverage.name + ") " + doing.name) ##
        return res

    def timeFlow(self, time):
        self.usedTime += time
        machineController.timeFlow(time)

#동작 정의
ACT_ESPRESSO_MACHINE = Action("에스프레소 머신 작동시키기",1,0)
ACT_BLENDER_MACHINE = Action("블렌더 작동시키기",2,0)
ACT_WATER = Action("에스프레소에 물 넣기",0,10)
ACT_END = Action("음료 마무리 하여 손님에게 제공",0,10)

#음료
class BevAmericanoIce(Beverage):
    name = "아메리카노(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_WATER, ACT_END]
class BevAmericanoHot(Beverage):
    name = "아메리카노(HOT)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_WATER, ACT_END]



if __name__ == '__main__':
    # 객체 생성
    machineController = MachineController([Machine("에스프레소 머신1", 10), Machine("에스프레소 머신1", 10)],
                                          [Machine("블렌더1", 30), Machine("블렌더2", 30)])
    person = Person()

    # order = [] #주문 (음료 큐)
    order = [BevAmericanoIce(), BevAmericanoIce(), BevAmericanoHot()]  # 주문 (음료 큐)
    ##------------------우리가 짜야하는 알고리즘(예시로 그냥 무작정 앞에서부터 하는 알고리즘---------------##
    while len(order) > 0:
        for b in order:
            res = person.do(b)
            if res != 0:
                if res == 2:
                    order.remove(b)
                break
        #할 수 있는게 없는 경우, 시간 보내기
        if res == 0:
            # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
            f1 = machineController.getEarlistEnd(1)
            f2 = machineController.getEarlistEnd(2)
            f = min(f1, f2)
            person.timeFlow(f)
    print(person.usedTime)



