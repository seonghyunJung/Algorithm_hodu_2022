# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Machine:
    isUsing = False# 사용중인지?
    usingTime = 10# 사용하는데 필요한 초
    remainingTime = usingTime# 사용 끝날때까지 남은 시간

    def __init__(self, usingTime, remainingTime = 0):
        self.usingTime = usingTime
        self.remainingTime = remainingTime

    def use(self, time):
        self.isUsing = True
        self.remainingTime -= time
        if(self.remainingTime <= 0):
            overUse = abs(self.remainingTime)
            self.isUsing = False
            self.remainingTime = self.usingTime
            return overUse

class Beverage:
    name = ""
    recipe = [] # 레시피, 실행 시간
    human_or_machine = [] # 사람이 하는일인지 기계가 하는일인지, 사람은 True, 기계는 false

    def __init__(self, name,  recipe, human_or_machine):
        self.name = name
        self.recipe = recipe
        self.human_or_machine = human_or_machine
    
    def lenRecipe(self):
        return len(self.recipe)


class MachineController:
    machineEspresso = []
    machineBlender = []
    machines = [machineEspresso, machineBlender]

    def find(self, machineKind:int):
        for machine in self.machines[machineKind]:
            if machine.isUsing == False:
                self.sendBackward(machineKind)
                return machine
        return None

    def sendBackward(self, machineKind:int):
        self.machines[machineKind].append(self.machines[machineKind].pop(0))

class Person:
    order = []
    remainingTime = 0

    def do(self):
        pass




# if __name__ == '__main__':
#     print()
