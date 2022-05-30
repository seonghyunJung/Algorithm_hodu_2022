# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Machine:
    isUsing = False
    usingTime = 10
    remainingTime = usingTime

    def use(self, time):
        self.isUsing = True
        self.remainingTime -= time
        if(self.remainingTime <= 0):
            overUse = abs(self.remainingTime)
            self.isUsing = False
            self.remainingTime = self.usingTime
            return overUse

class Beverage:
    recipe = []

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




if __name__ == '__main__':
    print()
