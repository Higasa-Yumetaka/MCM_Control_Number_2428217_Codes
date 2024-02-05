"""
Establish a physical model and environmental model of the submersible to simulate the movement of the submersible in the ocean
Run this program to simulate the motion of a single submersible
"""

import math

import gsw
import matplotlib.pyplot as plt
import numpy as np

alpha = np.array([0.15, 0.8])
beta = 0.83
gamma = np.array([0, 0.1])
max_speed = 2.5  # Maximum speed in meters per second (m/s)
sub_mass = 21000.0  # The maximum mass of the submersible, in kilograms (kg)
"""
In the case of sub_mass = 21000 (kg) and the volume of the submersible is 23 cubic meters (m^3),
, the maximum depth (neutral buoyancy point) that 
the submersible can reach when it carries 2350 kilograms (kg) of water is about 5000 meters (m)
"""
max_water_onboard = 5000  # The maximum amount of water the submersible can carry, in kilograms (kg)
water_onboard = 2350.0
sub_volume = 23.0  # The volume of the submersible in cubic meters (m^3)

g = 9.81  # Acceleration due to gravity in meters per second squared (m/s^2)
# In this model, we assumed that the acceleration due to gravity is constant


class Submersible:
    """
    Kinematic model of the submersible:

    position:
    The three-dimensional Cartesian coordinate system (x, y, z) is used to describe the position of the submarine,
    where the (x, y) plane is the horizontal plane, the z-axis is the direction perpendicular to the horizontal plane,
    and the unit is meters (m)
    The positive direction of the (x, y) axis is from the initial position of the submersible to the northwest,
    and the positive direction of the z axis is from the sea level to the seabed.

    speed_s:
    The vector (vx, vy, vz) in the three-dimensional Cartesian coordinate system is used to describe the speed of the submersible.
    Its direction is described in the same way as its position, and the unit is meters per second (m/s).

    acceleration_z:
    The vector (ax, ay, az) in the three-dimensional Cartesian coordinate system is used to describe the acceleration of the submersible in the vertical direction.
    The direction is described in the same way as the position, and the unit is meters per second squared (m/s^2)

    mass:
    The mass of the submersible in kilograms (kg)

    volume:
    The volume of the submersible in cubic meters (m^3)
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
        self.acceleration_z = np.random.normal(_acceleration, abs(0.2 * _acceleration))
        self.position[0] += self.speed[0] * dt + np.random.normal(0, 1)
        self.position[1] += self.speed[1] * dt + np.random.normal(0, 1)
        self.position[2] += self.speed[2] * dt + 0.5 * self.acceleration_z * dt * dt
        self.speed[0] = np.random.normal(_speed_oc[0], 1)
        self.speed[1] = np.random.normal(_speed_oc[0], 1)
        self.speed[2] = self.speed[2] + self.acceleration_z * dt
        self.mass = _mass

    def update_water(self, dt, drag, buoyancy):
        """
        Update submersible mass to control dive speed
        :param dt: time slice length
        :param drag: resistance
        :param buoyancy: buoyancy
        :return: None
        """
        delta_w = self.mass + self.water - (((self.mass + self.water) - drag - buoyancy) * dt) / (
                max_speed - self.speed[2])
        if delta_w >= 0:
            if self.water - delta_w >= 0:
                self.water -= delta_w
            else:
                self.water = 0
        else:
            if self.water + abs(delta_w) <= max_water_onboard:
                self.water += abs(delta_w)
        # print("delta_w ", delta_w, " water ", self.water)


class Environment:
    """
    Environmental parameter model:

    speed_oc:
    The vector (vx, vy) in the Cartesian coordinate system is used to describe the flow velocity of seawater.
    Its direction is described in the same way as the horizontal position of the submersible,
    and the unit is meters per second (m/s).

    temperature:
    The temperature of seawater in degrees Celsius (℃)

    salinity:
    Salinity of seawater in parts per thousand (PPT)

    pressure:
    The pressure of seawater on the submersible, in dBar

    position:
    The three-dimensional Cartesian coordinate system (x, y, z) is used to describe the position of the submarine,
    where the (x, y) plane is the horizontal plane,
    the z-axis is the direction perpendicular to the horizontal plane, and the unit is meters (m)
    """

    def __init__(self, _speed_oc, _temperature, _salinity, _pressure, _latitude):
        self.speed_oc = _speed_oc
        self.temperature = _temperature
        self.salinity = _salinity
        self.pressure = _pressure
        self.latitude = _latitude

    def update_env(self, _pressure):
        self.pressure = _pressure


def cal_neutral_buoyancy(env, sub, target_depth):
    """
    Calculate the neutral buoyancy depth of a submersible
    :param env: environment object
    :param sub: submersible object
    :param target_depth: target dive depth
    :return: neutral buoyancy depth
    """
    # Read environment object parameters
    temperature = env.temperature
    salinity = env.salinity
    pressure = env.pressure
    # Read submersible object parameters
    volume = sub.volume
    mass = sub.mass + sub.water

    # Calculate the neutral buoyancy depth of a submersible
    density_sub = mass / volume
    for i in range(int(target_depth * 2)):
        pressure = gsw.p_from_z(-i, env.latitude)
        # Calculate seawater density
        density = gsw.rho(temperature, salinity, pressure)
        if density_sub < density:
            neutral_buoyancy = i
            return neutral_buoyancy
    return math.inf


def cal_acc(env, sub):
    """
    Calculate the acceleration of the submersible's descent to
    :param env: environment object
    :param sub: submersible object
    :return: acceleration of the submersible's descent
    """
    # environmental parameters
    temperature = env.temperature
    salinity = env.salinity
    pressure = env.pressure
    # submersible parameters
    sub_m = sub.mass
    water = sub.water
    mass = sub_m + water  # The total mass of the submersible, in kilograms (kg)
    volume = sub.volume
    # Calculate seawater density
    # Here we use Python’s marine science library gsw to perform calculations related to the marine environment.
    density = gsw.rho(temperature, salinity, pressure)
    # Calculate the buoyancy force of seawater on the submersible
    buoyancy = density * 9.8 * volume
    # Calculate the resistance of seawater to a submersible
    # shape resistance
    Cd = 0.0475  # 潜水器的阻力系数
    viscous_drag = 0.5 * Cd * density * 2 * math.pi * ((math.sqrt(3 * sub.volume / (4 * math.pi))) ** 3) * abs(sub.speed
                                                                                                               [2]) ** 2
    # print("viscous_drag {}".format(viscous_drag))
    # sub.update_water(dt, viscous_drag, buoyancy)
    # Calculate the gravity of a submersible
    gravity = mass * g
    # Calculate the vertical acceleration of the submersible
    if sub.speed[2] >= 0:
        acceleration = (gravity - buoyancy - viscous_drag) / mass
    else:
        acceleration = (gravity - buoyancy + viscous_drag) / mass
    return acceleration


def cal_speed_oc(env, sub):
    """
    Calculate the effect of ocean current speed on a submersible
    The calculation takes into account the influence of the Coriolis force at different latitudes
    :param env: environment object
    :param sub: submersible object
    :return: ocean current speed
    """
    speed_oc = env.speed_oc
    latitude = env.latitude

    depth = sub.position[2]
    # Calculate the Coriolis force
    # print("latitude ", latitude)
    f = 2 * 7.292e-5 * math.sin(latitude)
    # Calculate the effect of the Coriolis force on a submersible
    Az = np.array([10e-6, 10e-5])
    Az = np.random.uniform(Az[0], Az[1])
    DE = math.pi * math.sqrt(2 * Az / abs(f))
    theta = math.atan2(speed_oc[1], speed_oc[0])
    speed_oc[0] = env.speed_oc[0] * math.cos(theta + (math.pi / DE) * (-depth)) * math.e ** (math.pi * (-depth) / DE)
    speed_oc[1] = env.speed_oc[1] * math.sin(theta + (math.pi / DE) * (-depth)) * math.e ** (math.pi * (-depth) / DE)
    return speed_oc


def emulate_once(env, sub, dt):
    """
    Simulate the movement of a submersible
    :param env: environment object
    :param sub: submersible object
    :param dt: time slice length
    :return: None
    """
    # 读取环境参数
    speed_oc = cal_speed_oc(env, sub)
    # 读取潜水器参数
    mass = sub.mass
    # sub.update_mass(dt, env)
    # 计算潜水器的垂直加速度
    acceleration = cal_acc(env, sub)
    # 对潜水器的垂直加速度进行随机扰动
    acceleration = np.random.normal(acceleration, 0.1)
    # 更新潜水器的状态
    sub.update_sub(acceleration, mass, speed_oc, dt)
    sub.position_history.append(sub.position.copy())
    # 计算压力值
    pressure = gsw.p_from_z(-sub.position[2], env.latitude)
    # 更新环境的状态
    env.update_env(pressure)


def emulate(_start_position=np.array([0, 0, 0]), _target_depth=5000, _speed_oc=np.array([2.0, 2.0]),
            _temp_range=np.array([0.0, 3.0]), _salinity=37.0, _pressure=10.0, _latitude=np.array([36.5, 40.0]),
            _sub_mass=21000.0, _sub_volume=23.0, _water_onboard=2350.0):
    """
    Simulate the movement of a submersible
    :param _start_position: initial position
    :param _target_depth: target dive depth
    :param _speed_oc: ocean current speed
    :param _temp_range: temperature range
    :param _salinity: salinity
    :param _pressure: atmospheric pressure
    :param _latitude: latitude
    :param _sub_mass: submersible mass
    :param _sub_volume: submersible volume
    :param _water_onboard: water carried by the submersible
    :return: final position of the submersible
    """
    _start_position = _start_position * 1.0
    _target_depth = _target_depth * 1.0
    # Initialize environment object
    speed_oc = _speed_oc.copy()
    # Initial random perturbation of seawater velocity
    speed_oc[0] = np.random.uniform(-speed_oc[0], speed_oc[0])
    speed_oc[1] = np.random.uniform(-speed_oc[1], speed_oc[1])

    temperature = np.random.uniform(_temp_range[0], _temp_range[1])  # Temperature in degrees Celsius (℃)
    salinity = np.random.normal(_salinity, 0.1)  # Salinity in parts per thousand (PPT)
    pressure = _pressure  # Initial pressure in dBar
    latitude = np.random.uniform(_latitude[0], _latitude[1])  # Define the submersible's movement area
    env_Ionian = Environment(speed_oc, temperature, salinity, pressure, latitude)
    # Initialize submersible object
    sub = Submersible(_start_position, np.array([0.0, 0.0, 0.0]), _sub_mass, _sub_volume,
                      _water_onboard)

    time = 0.0  # Time in seconds (s)
    while sub.position[2] <= _target_depth:
        if sub.position[2] <= 5:
            dt = 0.1
        else:
            dt = 2.0
        emulate_once(env_Ionian, sub, dt)
        time += dt
    return sub.position


def sensitivity(_speed_oc=2.0, _temperature=1.5,
                _salinity=37.0, _pressure=10.0, _latitude=37.5,
                _sub_mass=21000.0, _sub_volume=23.0, _water_onboard=2350.0):
    """
    Perform sensitivity analysis of the submersible motion model
    :param _speed_oc: ocean current speed
    :param _temperature: temperature
    :param _salinity: salinity
    :param _pressure: atmospheric pressure
    :param _latitude: latitude
    :param _sub_mass: submersible mass
    :param _sub_volume: submersible volume
    :param _water_onboard: water carried by the submersible
    :return: distance from the start position
    """

    _start_position = np.array([0, 0, 0])
    _target_depth = 5000.0
    speed_oc = np.zeros(2) * 1.0
    # Initial random perturbation of seawater velocity
    speed_oc[0] = np.random.uniform(-_speed_oc, _speed_oc)
    speed_oc[1] = np.random.uniform(-_speed_oc, _speed_oc)

    temperature = _temperature * 1.0
    salinity = _salinity * 1.0
    pressure = _pressure * 1.0
    latitude = _latitude * 1.0
    env_Ionian = Environment(speed_oc, temperature, salinity, pressure, latitude)
    # Initialize submersible object
    sub = Submersible(_start_position * 1.0, np.array([0.0, 0.0, 0.0]), _sub_mass * 1.0, _sub_volume * 1.0,
                      _water_onboard * 1.0)

    time = 0.0
    while sub.position[2] <= _target_depth:
        if sub.position[2] <= 5:
            dt = 0.1
        else:
            dt = 2.0
        emulate_once(env_Ionian, sub, dt)
        time += dt
    return np.linalg.norm(sub.position[:2] - _start_position[2])


def main():
    # Initialize environment object
    start_depth = 0.0
    target_depth = 5000.0
    _speed_oc = 2.0  # Initial ocean current speed
    speed_oc = np.zeros(2) * 1.0
    # Initial random perturbation of seawater velocity
    speed_oc[0] = np.random.uniform(-_speed_oc, _speed_oc)
    speed_oc[1] = np.random.uniform(-_speed_oc, _speed_oc)
    temp_range = np.array([0.0, 3.0])  # Temperature range
    temperature = np.random.uniform(temp_range[0], temp_range[1])  # Temperature in degrees Celsius (℃)
    salinity = 37.0
    pressure = 10.0
    latitude = np.array([36.5, 40.0])
    latitude = np.random.uniform(latitude[0], latitude[1])
    env_Ionian = Environment(speed_oc, temperature, salinity, pressure, latitude)

    # Initialize the submersible
    sub = Submersible(np.array([0.0, 0.0, start_depth]), np.array([0.0, 0.0, 0.0]), sub_mass, sub_volume,
                      water_onboard)

    time = 0.0  # Time in seconds (s)
    neutral_buoyancy = cal_neutral_buoyancy(env_Ionian, sub, target_depth)
    if neutral_buoyancy < target_depth:
        target_depth = neutral_buoyancy
    while sub.position[2] <= target_depth:
        if sub.position[2] <= 5:
            dt = 2.0
        else:
            dt = 2.0
        emulate_once(env_Ionian, sub, dt)
        # neutral_buoyancy = cal_neutral_buoyancy(env_Ionian, sub)
        time += dt
        print("neutral_buoyancy ", neutral_buoyancy)
        print("Time ", time, " Position ", sub.position, " speed ", sub.speed, " acc ", sub.acceleration_z, " m ",
              sub.mass)

    # sub.position_history = sub.position_history[::-1]
    print(np.array(sub.position_history))

    # Save the position history of the submersible
    with open('./source/history.csv', 'w') as f:
        for item in sub.position_history:
            f.write(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')

    # Plot the position history of the submersible
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for item in sub.position_history:
        ax.scatter(item[0], item[1], -item[2], c='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-500, 500)
    ax.set_ylim(-500, 500)
    ax.set_zlim(-5000, 2)
    plt.show()


if __name__ == '__main__':
    main()
