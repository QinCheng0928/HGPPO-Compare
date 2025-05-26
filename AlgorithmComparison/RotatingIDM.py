import numpy as np
from highway_env.vehicle.behavior import IDMVehicle
from highway_env.vehicle.controller import MDPVehicle

# ======================================================
# action对应关系
# ACTIONS_LONGI = {0: "SLOWER", 1: "IDLE", 2: "FASTER"}
# ======================================================

# ======================================================
# Rotating-IDM（Rotating Intelligent Driver Model）算法实现
# ======================================================


def rotating_predict(env):
    # IDM 参数
    a_max = 1.5          # 最大加速度
    b = 2.0              # 舒适减速度
    v0 = 10.0            # 期望速度 (m/s)
    T = 2.5              # 安全时间头距 (s)
    s0 = 6.0             # 最小间距 (m)
    delta = 4            # 加速度指数

    cav = []
    hv = []
    for vehicle in env.road.vehicles:
        if isinstance(vehicle, MDPVehicle):
            cav.append(vehicle)
        elif isinstance(vehicle, IDMVehicle):
            hv.append(vehicle)
            
    # 默认 IDLE        
    actions = [1 for _ in range(len(cav))]  

    for i, ego in enumerate(cav):
        if "o" in ego.lane_index[0] and "ir" in ego.lane_index[1]:
            # 如果车辆未通过冲突点
            # 获得当前车辆的纵向坐标
            ego_lane = ego.lane_index
            ego_lane_obj = env.road.network.get_lane(ego_lane)
            s_ego, _ = ego_lane_obj.local_coordinates(ego.position)

            # 寻找前车
            front_vehicle = None
            min_delta_s = float('inf')

            for other in env.road.vehicles:
                if other is ego:
                    continue
                # 如果其他车通过冲突点
                if not ("o" in other.lane_index[0] and "ir" in other.lane_index[1]):
                    continue
                # 如果其他车未通过冲突点，获取其他车的纵坐标
                other_lane_obj = env.road.network.get_lane(other.lane_index)
                s_other, _ = other_lane_obj.local_coordinates(other.position)
                delta_s = s_other - s_ego
                if delta_s > 0 and delta_s < min_delta_s:
                    min_delta_s = delta_s
                    front_vehicle = other

            # IDM 加速度计算
            v = ego.speed
            if front_vehicle:
                v_front = front_vehicle.speed
                delta_v = v - v_front
                s = max(min_delta_s, 0.1)

                s_star = s0 + v * T + (v * delta_v) / (2 * np.sqrt(a_max * b))
                accel = a_max * (1 - (v / v0) ** delta - (s_star / s) ** 2)
            else:
                accel = a_max * (1 - (v / v0) ** delta)

            # 将加速度映射为动作
            if accel < -1.0:
                actions[i] = 0  # SLOWER
            elif accel > 1.0:
                actions[i] = 2  # FASTER
            else:
                actions[i] = 1  # IDLE
        else:
            # 如果车辆通过冲突点
            actions[i] = 2      # FASTER

    return tuple(actions)