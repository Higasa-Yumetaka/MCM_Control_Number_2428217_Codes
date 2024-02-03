import math
import gsw
import matplotlib.pyplot as plt
import numpy as np

"""
密度计算参数
a: 温度对密度的影响参数
b: 盐度对密度的影响参数
c: 深度对密度的影响参数
"""
alpha = np.array([0.15, 0.8])
beta = 0.83
gamma = np.array([0, 0.1])
max_speed = 2.5  # 最大速度，单位为米每秒(m/s)
sub_mass = 21000  # 潜水器的最大质量，单位为千克(kg)
max_water_onboard = 2500  # 潜水器最大携带水量，单位为千克(kg)
sub_volume = 23.0  # 潜水器的体积，单位为立方米(m^3)

g = 9.81  # 重力加速度，单位为米每秒平方(m/s^2)


class Submersible:
    """
    对潜水器的运动模型：
    position:
    采用三维笛卡尔坐标系(x,y,z)描述潜艇的位置，其中(x,y)平面为水平面，z轴为垂直于水平面的方向，单位为米(m)
    (x,y)轴正方向为由潜水器的初始位置指向西北方位，z轴正方向为由海平面指向海底
    speed_s:
    采用三维笛卡尔坐标系中的向量(vx,vy,vz)描述潜水器的速度，其方向与位置的描述方式相同，单位为米每秒(m/s)
    acceleration_z:
    采用三维笛卡尔坐标系中的向量(ax,ay,az)描述潜水器在垂直方向上的加速度，其方向与位置的描述方式相同，单位为米每秒平方(m/s^2)
    mass:
    潜水器的质量，单位为千克(kg)
    volume:
    潜水器的体积，单位为立方米(m^3)
    """

    def __init__(self, _position, _speed_s, _mass, _volume, _water):
        self.position = _position
        self.speed = _speed_s
        self.mass = _mass
        self.acceleration_z = 0
        self.volume = _volume
        self.water = _water
        self.position_history = []

    def update_sub(self, _acceleration, _mass, _speed_oc, dt):
        self.acceleration_z = np.random.normal(_acceleration, 0.3)  # _acceleration
        self.position[0] += self.speed[0] * dt + np.random.normal(0, 1)  # _speed_oc[0]
        self.position[1] += self.speed[1] * dt + np.random.normal(0, 1)  # _speed_oc[1]
        self.position[2] += self.speed[2] * dt + 0.5 * self.acceleration_z * dt * dt
        self.speed[0] = np.random.normal(_speed_oc[0], 1)  # _speed_oc[0]
        self.speed[1] = np.random.normal(_speed_oc[0], 1)  # _speed_oc[1]
        # self.speed[2] = min(self.speed[2] + self.acceleration_z * dt, max_speed)
        self.speed[2] = self.speed[2] + self.acceleration_z * dt
        self.mass = _mass  # 更新潜水器的质量，待做


class Environment:
    """
    对环境的描述：
    speed_oc:
    采用而维笛卡尔坐标系中的向量(vx,vy)描述海水的流速，其方向与潜水器的水平位置描述方式相同，单位为米每秒(m/s)
    temperature:
    海水的温度，单位为摄氏度(℃)
    salinity:
    海水的盐度，单位为千分比(PPT)
    pressure:
    海水对潜水器的压力，单位为dbar
    position:
    采用三维笛卡尔坐标系(x,y,z)描述潜艇的位置，其中(x,y)平面为水平面，z轴为垂直于水平面的方向，单位为米(m)
    """

    def __init__(self, _speed_oc, _temperature, _salinity, _pressure, _latitude):
        self.speed_oc = _speed_oc
        self.temperature = _temperature
        self.salinity = _salinity
        self.pressure = _pressure
        self.latitude = _latitude

    def update_mass(self, _max_speed):
        """
        更新潜水器的质量
        :param _max_speed: 潜水器的最大速度
        :return: None
        """

    def update_env(self, _pressure):
        self.pressure = _pressure


def cal_neutral_buoyancy(env, sub):
    """
    计算潜水器的中性浮力深度
    :param env: 环境
    :param sub: 潜水器
    :return: 潜水器的中性浮力
    """
    # 读取环境参数
    temperature = env.temperature
    salinity = env.salinity
    pressure = env.pressure
    # 读取潜水器参数
    volume = sub.volume
    mass = sub.mass
    water = sub.water
    # 计算海水密度
    density = gsw.rho(temperature, salinity, pressure)
    # 计算潜水器的中性浮力深度
    neutral_buoyancy = (mass + water) / (density * volume)
    return neutral_buoyancy


def cal_acc(env, sub):
    """
    模拟潜水器的运动
    :param env: 环境
    :param sub: 潜水器
    :return: 潜水器的垂直加速度
    """
    # 读取环境参数
    temperature = env.temperature
    salinity = env.salinity
    pressure = env.pressure
    # 读取潜水器参数
    sub_m = sub.mass
    water = sub.water
    mass = sub_m + water  # 潜水器的质量，单位为千克(kg)
    volume = sub.volume
    # 计算海水密度
    density = gsw.rho(temperature, salinity, pressure)
    # 计算海水对潜水器的浮力
    buoyancy = density * 9.8 * volume
    # 计算海水对潜水器的阻力
    # 形状阻力
    Cd = 0.0475  # 潜水器的阻力系数
    viscous_drag = 0.5 * Cd * density * 2 * math.pi * (math.sqrt(3 * sub.volume / (4 * math.pi))) ** 3 * sub.speed[
        2] ** 2
    # print("viscous_drag {}".format(viscous_drag))
    # 计算潜水器的重力
    gravity = mass * g
    # 计算潜水器的垂直加速度
    acceleration = (gravity - buoyancy - viscous_drag) / mass
    return acceleration


def cal_speed_oc(env, sub):
    """
    计算洋流速度对潜水器的影响
    :param env: 环境
    :param sub: 潜水器
    :return:
    """
    # 读取环境参数
    speed_oc = env.speed_oc
    latitude = env.latitude
    la = np.random.uniform(latitude[0], latitude[1])
    # 读取潜水器参数
    depth = sub.position[2]
    # 计算科里奥利力
    f = 2 * 7.292e-5 * math.sin(la)
    # 计算科里奥利力对潜水器的影响
    Az = np.array([10e-6, 10e-5])
    Az = np.random.uniform(Az[0], Az[1])
    DE = math.pi * math.sqrt(2 * Az / abs(f))
    theta = math.atan2(speed_oc[1], speed_oc[0])
    speed_oc[0] = env.speed_oc[0] * math.cos(theta + (math.pi / DE) * (-depth)) * math.e ** (math.pi * (-depth) / DE)
    speed_oc[1] = env.speed_oc[1] * math.sin(theta + (math.pi / DE) * (-depth)) * math.e ** (math.pi * (-depth) / DE)
    return speed_oc


def emulate_once(env, sub, dt):
    """
    模拟潜水器的运动
    :param env: 环境
    :param sub: 潜水器
    :param dt: 时间间隔
    :return: None
    """
    # 读取环境参数
    speed_oc = cal_speed_oc(env, sub)

    # 读取潜水器参数
    mass = sub.mass

    # 计算潜水器的垂直加速度
    acceleration = cal_acc(env, sub)
    # 对潜水器的垂直加速度进行随机扰动
    acceleration = np.random.normal(acceleration, 0.1)

    # 更新潜水器的状态
    depth_1 = sub.position[2]
    sub.update_sub(acceleration, mass, speed_oc, dt)
    depth_2 = sub.position[2]
    sub.position_history.append(sub.position.copy())

    delta_h = abs(depth_2 - depth_1)  # 潜水器的垂直位移
    pressure = env.pressure  # 读取环境的压力
    pressure += (gsw.rho(env.temperature, env.salinity, pressure) * g * delta_h) / 10e4

    # 更新环境的状态
    env.update_env(pressure)
    print("pressure {}".format(pressure))


def emulate(start_depth=0, target_depth=5000):
    start_depth = start_depth * 1.0
    target_depth = target_depth * 1.0
    # 初始化环境
    _speed_oc = np.array([2.0, 2.0])  # 定义最大海水流速，单位为米每秒(m/s)
    speed_oc = _speed_oc.copy()
    # 对海水流速进行初始随机扰动
    speed_oc[0] = np.random.uniform(-speed_oc[0], speed_oc[0])
    speed_oc[1] = np.random.uniform(-speed_oc[1], speed_oc[1])
    temp_range = np.array([0.0, 3.0])  # 温度范围，单位为摄氏度(℃)
    temperature = np.random.uniform(temp_range[0], temp_range[1])  # 温度，单位为摄氏度(℃)
    salinity = np.random.normal(37.0, 0.01)  # 盐度，单位为千分比(PPT)
    pressure = 10.0  # 初始压力，单位为dbar
    latitude = np.array([36.5, 40.0])  # 定义潜水器的运动区域
    env_Ionian = Environment(speed_oc, temperature, salinity, pressure, latitude)
    # 初始化潜水器
    sub = Submersible(np.array([0.0, 0.0, start_depth]), np.array([0.0, 0.0, 0.0]), sub_mass, sub_volume,
                      max_water_onboard)
    time = 0.0  # 时间，单位为秒(s)
    while sub.position[2] <= target_depth:
        if sub.position[2] <= 5:
            dt = 0.1
        else:
            dt = 2.0
        emulate_once(env_Ionian, sub, dt)
        time += dt
    return sub.position


def main():
    # 初始化环境
    start_depth = 0.0
    target_depth = 5000.0
    _speed_oc = np.array([2.0, 2.0])  # 定义最大海水流速，单位为米每秒(m/s)
    speed_oc = _speed_oc.copy()
    # 对海水流速进行初始随机扰动
    speed_oc[0] = np.random.uniform(-speed_oc[0], speed_oc[0])
    speed_oc[1] = np.random.uniform(-speed_oc[1], speed_oc[1])
    temp_range = np.array([0.0, 3.0])  # 温度范围，单位为摄氏度(℃)
    temperature = np.random.uniform(temp_range[0], temp_range[1])  # 温度，单位为摄氏度(℃)
    salinity = 37.0  # 盐度，单位为千分比(PPT)
    pressure = 10.0  # 初始压力，单位为dbar
    latitude = np.array([36.5, 40.0])  # 定义潜水器的运动区域
    env_Ionian = Environment(speed_oc, temperature, salinity, pressure, latitude)

    # 初始化潜水器
    sub = Submersible(np.array([0.0, 0.0, start_depth]), np.array([0.0, 0.0, 0.0]), sub_mass, sub_volume,
                      max_water_onboard)

    time = 0.0  # 时间，单位为秒(s)
    while sub.position[2] <= target_depth:
        if sub.position[2] <= 5:
            dt = 0.1
        else:
            dt = 2.0
        emulate_once(env_Ionian, sub, dt)
        time += dt
    # return sub.position
        print("Time ", time, " Position ", sub.position, " speed ", sub.speed, " acc ", sub.acceleration_z, " m ",
              sub.mass)

    # sub.position_history = sub.position_history[::-1]
    print(np.array(sub.position_history))

    # 将position_history输出为csv文件
    with open('./source/history.csv', 'w') as f:
        for item in sub.position_history:
            f.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')

    # 将潜水器的运动轨迹可视化
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for item in sub.position_history:
        ax.scatter(item[0], item[1], -item[2], c='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # 固定显示的坐标轴范围
    # ax.set_xlim(-5, 5)
    # ax.set_ylim(-5, 5)
    # ax.set_zlim(-3000, 2)
    # plt.show()


if __name__ == '__main__':
    main()
