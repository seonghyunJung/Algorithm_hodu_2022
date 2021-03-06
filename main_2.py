# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import json

class Beverage:
    name = ""
    recipe = []
    step = 0
    endStep = 0
    waiting = False

    def __init__(self, name="", recipe=None):  # , name:str, recipe:list, step:int = 0
        if name != "":
            self.name = name
        if recipe is not None:
            self.recipe = recipe
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
    # usingTime = 10
    # remainingTime = usingTime
    beverage = None

    def __init__(self, name: str, usingTime: int):
        self.name = name
        self.usingTime = usingTime
        self.remainingTime = usingTime

    def setBeverage(self, beverage: Beverage):
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
            self.beverage.accomplishOneStep()  # 모든 음료는 마무리 동작으로 끝난다 가정
            return overUse

    def reset(self):
        self.isUsing = False
        self.beverage = None
        self.remainingTime = self.usingTime

dictAct = {}

class Action:
    name = "행동"
    actType = 0  # 0: 사람, 1이상: 기계 종류
    usingTime = 0

    def __init__(self, name: str, actType: int, usingTime):
        dictAct[name] = self
        self.name = name
        self.actType = actType
        self.usingTime = usingTime


class MachineController:
    machineEspresso = []
    machineBlender = []
    machineTea = []
    machines = []

    def __init__(self, machineEspresso, machineBlender, machineTea):
        self.machineEspresso = machineEspresso
        self.machineBlender = machineBlender
        self.machineTea = machineTea
        self.machines = [self.machineEspresso,
                         self.machineBlender, self.machineTea]

    def find(self, machineKind: int):
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

    def getEarlistEnd(self, machineKind: int):
        res = 10000  # 무한
        for machine in self.machines[machineKind-1]:
            if machine.isUsing:
                res = min(res, machine.remainingTime)
            # else:
            #     return 0
        return res

    def sendBackward(self, machineKind: int):
        self.machines[machineKind -
                      1].append(self.machines[machineKind-1].pop(0))

    def reset(self):
        for machinesOneType in self.machines:
            for machine in machinesOneType:
                machine.reset()


class Person:
    remainingTime = 0
    usedTime = 0

    def __init__(self, machineController):
        self.usedTime = 0
        self.machineController = machineController

    def do(self, beverage: Beverage):
        # 대기 중인 음료이면 건너뛰기
        if beverage.waiting:
            return 0
        res = 1
        doing = beverage.getCurrentStep()
        self.usedTime += doing.usingTime
        # 사람 동작인 경우
        if doing.actType == 0:
            if beverage.accomplishOneStep():  # 하나 동작 후 음료 완성했으면 알리기
                res = 2  # 성공 및 음료 완성
            self.machineController.timeFlow(doing.usingTime)
            print(beverage.name + " " + doing.name)
        else:
            machine = self.machineController.find(doing.actType)
            if machine is None:
                return 0  # 실패 시 0 반환
            machine.setBeverage(beverage)
            machine.use()
            beverage.waiting = True
            print(beverage.name + " " + doing.name)
        return res

    def timeFlow(self, time):
        self.usedTime += time
        self.machineController.timeFlow(time)


# 동작 정의
ACT_ESPRESSO_MACHINE = Action("에스프레소 머신 작동시키기", 1, 0)
ACT_BLENDER_MACHINE = Action("블렌더 작동시키기", 2, 0)
ACT_POUR_BEVERAGE = Action("컵에 음료 붓기", 0, 5)
ACT_POUR_ESPRESSO = Action("에스프레소 붓기", 0, 3)
ACT_POUR_HOT_WATER_IN_CUP = Action("컵에 뜨거운 물 붓기", 0, 5)
ACT_POUR_HOT_WATER_IN_MUG = Action("머그잔에 뜨거운 물 붓기", 0, 5)  # 티 우리기 위함
ACT_POUR_WATER_IN_CUP = Action("컵에 시원한 물 붓기", 0, 5)
ACT_PUT_ICE_IN_CUP = Action("컵에 얼음 넣기", 0, 5)  # 아이스 음료 만들 때
ACT_PUT_ICE_IN_BLENDER = Action("블렌더에 얼음 넣기", 0, 5)  # 블렌딩 음료 만들 때
ACT_END = Action("음료 마무리 하여 손님에게 제공", 0, 5)
ACT_POUR_MILK_IN_CUP = Action("컵에 우유 넣기", 0, 5)  # 라떼 만들 때
ACT_POUR_MILK_IN_BLENDER = Action("블렌더에 우유 넣기", 0, 5)   # 블렌딩 음료 만들 때
ACT_STEAM_MILK = Action("우유 스팀하기", 0, 40)
ACT_PUT_SUGAR_SYRUP = Action("설탕시럽 넣기", 0, 3)
ACT_PUT_VANILLA_SYRUP = Action("바닐라시럽 넣기", 0, 3)
ACT_PUT_CHOCOLATE_SYRUP = Action("초콜릿시럽 넣기", 0, 3)
ACT_PUT_WHITE_CHOCOLATE_SYRUP = Action("화이트 초콜릿시럽 넣기", 0, 3)
ACT_CHOCOLATE_DRIZZLE = Action("초콜릿 드리즐 뿌리기", 0, 5)
ACT_CARAMEL_DRIZZLE = Action("카라멜 드리즐 뿌리기", 0, 5)
ACT_PUT_CHOCOLATE_CHIP = Action("초콜릿 칩 넣기", 0, 3)
ACT_PUT_CHOCOLATE_CHIP_ON_TOP = Action("음료 위에 초콜릿 칩 올리기", 0, 3)
ACT_PUT_CONDENSED_MILK = Action("연유 넣기", 0, 3)
ACT_PUT_WHIPPING_CREAM = Action("휘핑크림 올리기", 0, 5)
ACT_STIR = Action("휘젓기", 0, 3)
ACT_PREP_TEA = Action("티백 꺼내서 넣기", 0, 5)
ACT_BREW_TEA_FOR_ICE = Action("티 우리기", 3, 0)
ACT_POUR_COLD_BREW = Action("컵에 콜드브루 커피 붓기", 0, 5)
ACT_PUT_GREEN_TEA_POWDER = Action("그린티 파우더 넣기", 0, 5)
ACT_PEEL_BANANA = Action("바나나 껍질 벗기기", 0, 5)
ACT_POUR_MAGO_JUICE = Action("망고 베이스 넣기", 0, 5)

# 음료
class BevAmericanoIce(Beverage):
    name = "아메리카노(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_POUR_WATER_IN_CUP,
              ACT_POUR_ESPRESSO, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevAmericanoHot(Beverage):
    name = "아메리카노(HOT)"
    recipe = [ACT_ESPRESSO_MACHINE,
              ACT_POUR_HOT_WATER_IN_CUP, ACT_POUR_ESPRESSO, ACT_END]


class BevLatteIce(Beverage):
    name = "카페라떼(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_POUR_MILK_IN_CUP,
              ACT_POUR_ESPRESSO, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevLatteHot(Beverage):
    name = "카페라떼(HOT)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_STEAM_MILK,
              ACT_POUR_ESPRESSO, ACT_POUR_MILK_IN_CUP, ACT_END]


class BevDolceLatteIce(Beverage):
    name = "돌체라떼(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_CONDENSED_MILK, ACT_POUR_MILK_IN_CUP,
              ACT_STIR, ACT_PUT_ICE_IN_CUP, ACT_POUR_ESPRESSO, ACT_END]


class BevDolceLatteHot(Beverage):
    name = "돌체라떼(HOT)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_CONDENSED_MILK, ACT_STEAM_MILK,
              ACT_POUR_MILK_IN_CUP, ACT_STIR, ACT_POUR_ESPRESSO, ACT_END]


class BevCaffeMochaIce(Beverage):
    name = "카페모카(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_CHOCOLATE_SYRUP, ACT_POUR_ESPRESSO, ACT_STIR,
              ACT_POUR_MILK_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_PUT_WHIPPING_CREAM, ACT_CHOCOLATE_DRIZZLE, ACT_END]


class BevCaffeMochaHot(Beverage):
    name = "카페모카(HOT)"
    recipe = [ACT_PUT_CHOCOLATE_SYRUP, ACT_ESPRESSO_MACHINE, ACT_STEAM_MILK, ACT_POUR_ESPRESSO,
              ACT_STIR, ACT_POUR_MILK_IN_CUP, ACT_PUT_WHIPPING_CREAM, ACT_CHOCOLATE_DRIZZLE, ACT_END]


class BevWhiteChocoMochaIce(Beverage):
    name = "화이트 초콜릿 모카(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_WHITE_CHOCOLATE_SYRUP, ACT_POUR_ESPRESSO,
              ACT_STIR, ACT_POUR_MILK_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_PUT_WHIPPING_CREAM, ACT_END]


class BevWhiteChocoMochaHot(Beverage):
    name = "화이트 초콜릿 모카(HOT)"
    recipe = [ACT_PUT_WHITE_CHOCOLATE_SYRUP, ACT_ESPRESSO_MACHINE, ACT_STEAM_MILK,
              ACT_POUR_ESPRESSO, ACT_STIR, ACT_POUR_MILK_IN_CUP, ACT_PUT_WHIPPING_CREAM, ACT_END]


class BevCaramelMacchiatoIce(Beverage):
    name = "카라멜 마키아또(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_VANILLA_SYRUP, ACT_POUR_MILK_IN_CUP,
              ACT_STIR, ACT_PUT_ICE_IN_CUP, ACT_POUR_ESPRESSO, ACT_CARAMEL_DRIZZLE, ACT_END]


class BevCaramelMacchiatoHot(Beverage):
    name = "카라멜 마키아또(HOT)"
    recipe = [ACT_PUT_VANILLA_SYRUP, ACT_ESPRESSO_MACHINE, ACT_STEAM_MILK,
              ACT_POUR_MILK_IN_CUP, ACT_POUR_ESPRESSO, ACT_CARAMEL_DRIZZLE, ACT_END]


class BevJavaChipFrappuccino(Beverage):
    name = "자바칩 프라푸치노"
    recipe = [ACT_POUR_MILK_IN_BLENDER, ACT_PUT_CHOCOLATE_SYRUP, ACT_PUT_CHOCOLATE_CHIP, ACT_PUT_ICE_IN_BLENDER,
              ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_PUT_CHOCOLATE_CHIP_ON_TOP, ACT_END]


class BevEspressoFrappuccino(Beverage):
    name = "에스프레소 프라푸치노"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_POUR_MILK_IN_BLENDER, ACT_PUT_SUGAR_SYRUP, ACT_POUR_ESPRESSO,
              ACT_PUT_ICE_IN_BLENDER, ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_END]


class BevMochaFrappuccino(Beverage):
    name = "모카 프라푸치노"
    recipe = [ACT_POUR_MILK_IN_BLENDER, ACT_PUT_CHOCOLATE_SYRUP, ACT_PUT_ICE_IN_BLENDER,
              ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_CHOCOLATE_DRIZZLE, ACT_END]


class BevCaramelFrappuccino(Beverage):
    name = "카라멜 프라푸치노"
    recipe = [ACT_POUR_MILK_IN_BLENDER, ACT_PUT_VANILLA_SYRUP, ACT_PUT_ICE_IN_BLENDER,
              ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_CARAMEL_DRIZZLE, ACT_END]


class BevWhiteChocoMochaFrappuccino(Beverage):
    name = "화이트 초콜릿 모카 프라푸치노"
    recipe = [ACT_POUR_MILK_IN_BLENDER, ACT_PUT_WHITE_CHOCOLATE_SYRUP, ACT_PUT_ICE_IN_BLENDER,
              ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_END]


class BevGreenTeaFrappuccino(Beverage):
    name = "그린티 프라푸치노"
    recipe = [ACT_POUR_MILK_IN_BLENDER, ACT_PUT_GREEN_TEA_POWDER, ACT_PUT_ICE_IN_BLENDER,
              ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_PUT_WHIPPING_CREAM, ACT_END]


class BevMangoBananaBlended(Beverage):
    name = "망고 바나나 블렌디드"
    recipe = [ACT_PEEL_BANANA, ACT_POUR_MILK_IN_BLENDER, ACT_POUR_MAGO_JUICE,
              ACT_PUT_ICE_IN_BLENDER, ACT_BLENDER_MACHINE, ACT_POUR_BEVERAGE, ACT_END]


class BevMintBlendTeaIce(Beverage):
    name = "민트 블렌드 티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevMintBlendTeaHot(Beverage):
    name = "민트 블렌드 티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevEarlGreyTeaIce(Beverage):
    name = "얼그레이 티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevEarlGreyTeaHot(Beverage):
    name = "얼그레이 티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevYouthberryTeaIce(Beverage):
    name = "유스베리 티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevYouthberryTeaHot(Beverage):
    name = "유스베리 티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevEnglishBreakfastTeaIce(Beverage):
    name = "잉글리쉬브렉퍼스트 티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevEnglishBreakfastTeaHot(Beverage):
    name = "잉글리쉬브렉퍼스트 티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevGreenTeaIce(Beverage):
    name = "제주 그린티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevGreenTeaHot(Beverage):
    name = "제주 그린티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevChamomileTeaIce(Beverage):
    name = "캐모마일티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevChamomileTeaHot(Beverage):
    name = "캐모마일티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevHibiscusTeaIce(Beverage):
    name = "히비스커스티(ICE)"
    recipe = [ACT_POUR_HOT_WATER_IN_MUG, ACT_PREP_TEA, ACT_BREW_TEA_FOR_ICE,
              ACT_POUR_BEVERAGE, ACT_POUR_WATER_IN_CUP, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevHibiscusTeaHot(Beverage):
    name = "히비스커스티(HOT)"
    recipe = [ACT_POUR_HOT_WATER_IN_CUP, ACT_PREP_TEA, ACT_END]


class BevGreenTeaLatteIce(Beverage):
    name = "그린티 라떼(ICE)"
    recipe = [ACT_PUT_GREEN_TEA_POWDER, ACT_POUR_MILK_IN_CUP,
              ACT_STIR, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevGreenTeaLatteHot(Beverage):
    name = "그린티 라떼(HOT)"
    recipe = [ACT_PUT_GREEN_TEA_POWDER, ACT_STEAM_MILK,
              ACT_POUR_MILK_IN_CUP, ACT_STIR, ACT_END]


class BevSignatureChocoIce(Beverage):
    name = "시그니처 초콜릿(ICE)"
    recipe = [ACT_PUT_CHOCOLATE_SYRUP, ACT_POUR_MILK_IN_CUP, ACT_STIR,
              ACT_PUT_ICE_IN_CUP, ACT_PUT_WHIPPING_CREAM, ACT_CHOCOLATE_DRIZZLE, ACT_END]


class BevSignatureChocoHot(Beverage):
    name = "시그니처 초콜릿(HOT)"
    recipe = [ACT_PUT_CHOCOLATE_SYRUP, ACT_STEAM_MILK, ACT_POUR_MILK_IN_CUP,
              ACT_STIR, ACT_PUT_WHIPPING_CREAM, ACT_CHOCOLATE_DRIZZLE, ACT_END]


class BevColdBrew(Beverage):
    name = "콜드브루"
    recipe = [ACT_POUR_COLD_BREW, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevVanillaLatteIce(Beverage):
    name = "바닐라 라떼(ICE)"
    recipe = [ACT_ESPRESSO_MACHINE, ACT_PUT_VANILLA_SYRUP, ACT_POUR_MILK_IN_CUP,
              ACT_STIR, ACT_POUR_ESPRESSO, ACT_PUT_ICE_IN_CUP, ACT_END]


class BevVanillaLatteHot(Beverage):
    name = "바닐라 라떼(HOT)"
    recipe = [ACT_PUT_VANILLA_SYRUP, ACT_ESPRESSO_MACHINE,
              ACT_STEAM_MILK, ACT_STIR, ACT_POUR_MILK_IN_CUP, ACT_END]


bevList = [BevAmericanoIce(),BevAmericanoHot(),BevLatteIce(),BevLatteHot(),BevDolceLatteIce(),BevDolceLatteHot(),BevCaffeMochaIce(),BevCaffeMochaHot(),BevWhiteChocoMochaIce(),BevWhiteChocoMochaHot(),BevCaramelMacchiatoIce(),BevCaramelMacchiatoHot(),BevJavaChipFrappuccino(),BevEspressoFrappuccino(),BevMochaFrappuccino(),BevCaramelFrappuccino(),BevWhiteChocoMochaFrappuccino(),BevGreenTeaFrappuccino(),BevMangoBananaBlended(),BevMintBlendTeaIce(),BevMintBlendTeaHot(),BevEarlGreyTeaIce(),BevEarlGreyTeaHot(),BevYouthberryTeaIce(),BevYouthberryTeaHot(),BevEnglishBreakfastTeaIce(),BevEnglishBreakfastTeaHot(),BevGreenTeaIce(),BevGreenTeaHot(),BevChamomileTeaIce(),BevChamomileTeaHot(), BevHibiscusTeaIce(),BevHibiscusTeaHot(),BevGreenTeaLatteIce(),BevGreenTeaLatteHot(),BevSignatureChocoIce(), BevSignatureChocoHot(),BevColdBrew(),BevVanillaLatteIce(),BevVanillaLatteHot()]

#유저 커스텀 파일 읽기
with open("Custom.json", 'r', encoding='UTF-8') as custom:
    customData = json.load(custom)
    
    # 커스텀 기계 추가
    machineList = [[],[]]
    for cmachine in customData["machine"]:
        ctype = cmachine["type"]
        cname = cmachine["name"]
        ctime = cmachine["time"]
        if ctype <= 2:
            machineList[ctype].append(Machine(cname, ctime))

    machineController = MachineController(machineList[0], machineList[1],
                                          [Machine("티 우리기1", 300), Machine("티 우리기2", 300), Machine("티 우리기3", 300),
                                           Machine("티 우리기4", 300), Machine("티 우리기5", 300)])
    # 커스텀 동작 추가
    for cact in customData["action"]:
        cname = cact["name"]
        ctime = cact["time"]
        Action(cname, 0, ctime) # 자동으로 act dictionary에 추가
    # 커스텀 음료 추가
    for cbev in customData["beverage"]:
        cname = cbev["name"]
        crecipe = cbev["recipe"]

        recipe = []
        for act in crecipe:
            recipe.append(dictAct.get(act))
        recipe.append(ACT_END)

        bev = Beverage(cname, recipe)
        bevList.append(bev)



if __name__ == '__main__':
    # 객체 생성
    machineController = MachineController([Machine("에스프레소 머신1", 10), Machine("에스프레소 머신2", 10)],
                                          [Machine("블렌더1", 30),
                                           Machine("블렌더2", 30)],
                                          [Machine("티 우리기1", 300), Machine("티 우리기2", 300), Machine("티 우리기3", 300), Machine("티 우리기4", 300), Machine("티 우리기5", 300)])
    person = Person(machineController)

    # order = [] #주문 (음료 큐)
    order = [BevAmericanoIce(), BevAmericanoIce(),
             BevAmericanoHot()]  # 주문 (음료 큐)
    ##------------------우리가 짜야하는 알고리즘(예시로 그냥 무작정 앞에서부터 하는 알고리즘---------------##
    while len(order) > 0:
        for b in order:
            res = person.do(b)
            if res != 0:
                if res == 2:
                    order.remove(b)
                break
        # 할 수 있는게 없는 경우, 시간 보내기
        if res == 0:
            # 기계 남은 시간 중 가장 짧은 시간만큼 기다리기
            f1 = machineController.getEarlistEnd(1)
            f2 = machineController.getEarlistEnd(2)
            f = min(f1, f2)
            person.timeFlow(f)
    print(person.usedTime)
