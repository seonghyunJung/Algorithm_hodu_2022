# =========================== utility 사용법 ===================================
#  
# < read_data_to_2d/3d_array 함수 >
# from utility import read_data_to_2d_array, read_data_to_3d_array
# 를 사용해 import 한 뒤 
# team, order = read_data_to_2d_array(file_path)
# 또는
# team, order = read_data_to_3d_array(file_path)
# 코드를 통해 사용하시면 됩니다. 입력과 출력은 각 함수에 명시되어있습니다.
# 
# =============================================================================

def read_data_to_2d_array(file_path="Testing_data(정상 주문)/testing_data(1만(정상)).txt"):
    # 입력: file path
    # 출력: team(2d array), order(2d array)
    team = []
    order = []

    with open(file_path, "r") as f:
        while True:
          team_input = f.readline()
          temp_team = []
          order_temp = []
          if team_input == '':
            break
          for _ in range(int(team_input.strip())):
              temp = list(map(int, f.readline().strip().split())) # 개행문자 없애고, 띄어쓰기 단위로 끊은 뒤, 각 값을 int로 형변환, list로 형변환
              order_temp.extend(temp) # 팀 extend (이전 팀 리스트와 합치기)
              temp_team.append(len(temp)) # 팀 길이 저장
          team.append(temp_team)
          order.append(order_temp)
          f.readline() # -1 행 제거
    return team, order



def read_data_to_3d_array(file_path="Testing_data(정상 주문)/testing_data(1만(정상)).txt"):
    # 입력: file path
    # 출력: team(2d array), order(3d array)
    team = []
    order = []

    with open(file_path, "r") as f:
        while True:
          team_input = f.readline()
          temp_team = []
          order_temp = []
          if team_input == '':
            break
          for _ in range(int(team_input.strip())):
              temp = list(map(int, f.readline().strip().split())) # 개행문자 없애고, 띄어쓰기 단위로 끊은 뒤, 각 값을 int로 형변환, list로 형변환
              order_temp.append(temp) # 팀 append
              temp_team.append(len(temp)) # 팀 길이 저장
          team.append(temp_team)
          order.append(order_temp)
          f.readline() # -1 행 제거
    return team, order

if __name__ == '__main__':
    file_path = "Testing_data(정상 주문)/testing_data(1만(정상)).txt"
    team, order = read_data_to_2d_array(file_path)
    print("1d")
    print("team:",team[:5])
    print("order:",order[:10])

    print()

    team, order = read_data_to_3d_array(file_path)
    print("2d")
    print("team:",team[:5])
    print("order:",order[:10])
