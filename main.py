import numpy as np
import math
import matplotlib.pyplot as plt

# 그래프 설정
fig = plt.figure(figsize=(12, 8))
ax0 = fig.add_subplot(121, projection="3d", title="graphene")  # 3D설정
ax0.view_init(elev=90, azim=0)  # 보는 각도 설정
ax1 = fig.add_subplot(122, title="z-potential")  # z-potential 그래프
ax2 = fig.add_subplot(122 title="x-potential")


lattice_constant = 0.142  # 격자 상수
x_step = lattice_constant * 3  # 직사각형으로 나눴을 때 x파장
y_step = lattice_constant * np.sqrt(3)  # 직사각형으로 나눴을 때 y파장
x_range = np.arange(0, 10, x_step)  # x좌표 형성 한계
y_range = np.arange(0, 10, y_step)  # y좌표 형성 한계
x_grid = []  # x좌표 담을곳
y_grid = []  # y좌표 담을곳
c = lattice_constant  # 식이 길어서 변수 짧게
for x in list(x_range) + list(-x_range)[1:]:  # +-x_range 에 대해서 반복, x는 시작 좌표
    for y in list(y_range) + list(-y_range)[1:]:  # +-y_range 에 대해서 반복, y는 시작 좌표
        x_grid.extend([x + c, x + 2 * c, x + c / 2, x + c * 5 / 2])  # 나눈 격자에 대한 x 상대적 위치
        y_grid.extend([y, y, y + np.sqrt(3) * c / 2, y + np.sqrt(3) * c / 2])  # 나눈 격자에 대한 y 상대적 위치

ax0.scatter(x_grid, y_grid, 0, c="k")  # 탄소 그래프 점 찍기(검정색)
ax0.scatter(0, 0, 0.1, c="r")  # 팁 원자 점 찍기(빨간색)

graphene_xyz = list(zip(x_grid, y_grid, [0.0 for x in range(len(x_grid))]))  # 그래핀 원자들의 좌표(xyz)


def potential_3d(cor1, cor2, d=0.205, x=0.4073, sigma=2.5):  # cor1, cor2: 좌표 2개, d: DIJ, x: xIJ, sigma: 몇 시그마까지 할지
    distance = np.sqrt(math.pow((cor1[0]-cor2[0]), 2) + math.pow((cor1[1]-cor2[1]), 2) + math.pow((cor1[2]-cor2[2]), 2))
    if distance < sigma * math.pow(2, -1/6) * x:  # 시그마 안의 거리에 있는 원자는 그냥 포텐셜 값 구하기
        return d * (math.pow((x/distance), 12) - 2 * math.pow((x/distance), 6))
    else:  # 시그마 값 넘는 원자는 potential 0 으로 취급
        return 0


z_potential_min = 0  # potential 합이 최소일 때 z값
potential_sum_min = 100  # 최소인 potential 합
for z in np.arange(0.3, 0.6, 0.001):  # z의 범위[nm]
    potential_sum = 0  # potential의 합 초기화
    for i in range(len(graphene_xyz)):  # 그래핀 원자 수만큼 반복
        potential_sum += potential_3d(graphene_xyz[i], (0, 0, z))  # i번째 그래핀 원자와 팁원자(0, 0, z)간의 거리를 함수로 구해서 누적
    print(potential_sum, z)
    ax1.scatter(z, potential_sum)  # 두번째 그래프 점 찍기
    if potential_sum_min > potential_sum:  # 여태까지의 최소값이 구한 값보다 크다면(최솟값을 갱신하면)
        z_potential_min = z  # z값 저장
        potential_sum_min = potential_sum  # potential값 저장


plt.show()


# z_potential_min에서 xy 움직이면서 potential 측정.

