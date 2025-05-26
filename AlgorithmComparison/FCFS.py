import numpy as np
from highway_env.vehicle.behavior import IDMVehicle
from highway_env.vehicle.controller import MDPVehicle

# ======================================================
# action对应关系
# ACTIONS_LONGI = {0: "SLOWER", 1: "IDLE", 2: "FASTER"}
# ======================================================

# ======================================================
# FCFS（First-Come, First-Served）算法实现
# ======================================================

IDLE_velocity = 30
SLOWER_velocity = 20

def fcfs_predict(env):
    # 获取当前环境中的所有车辆，按照类别保存
    cav = []
    hv = []
    for vehicle in env.road.vehicles:
        if isinstance(vehicle, MDPVehicle):
            cav.append(vehicle)
        elif isinstance(vehicle, IDMVehicle):
            hv.append(vehicle)
    actions = [None for _ in range(len(cav))]
    
    # 检查 HV 是否要通过路口
    for vehicle in hv:
        # 判断车辆是否通过路口
        if "o" in vehicle.lane_index[0] and "ir" in vehicle.lane_index[1]:
            # HV到交叉口的距离
            dist = env.config["access_length"] - vehicle.lane.local_coordinates(vehicle.position)[0]
            # 如果距离小于20米，则认为HV要通过路口
            # 未通过的cav如果距交叉口太远则保持，比较近则减速，太近的减速
            # 通过的cav继续加速
            if dist < 20:
                for i, veh in enumerate(cav):
                    if "o" in veh.lane_index[0] and "ir" in veh.lane_index[1]:
                        tag_action = env.config["access_length"] - veh.lane.local_coordinates(veh.position)[0]
                        actions[i] = 2 if tag_action > IDLE_velocity else (1 if tag_action > SLOWER_velocity else 0)
                    else:
                        actions[i] = 2
                return tuple(actions)


    # 正常执行 FCFS 通行逻辑
    shortest_index = -1
    shortest_dis = env.config["access_length"] * 2
    for i, veh in enumerate(cav):
        if "o" in veh.lane_index[0] and "ir" in veh.lane_index[1]:
            dist = env.config["access_length"] - veh.lane.local_coordinates(veh.position)[0]
            if dist < shortest_dis:
                shortest_dis = dist
                shortest_index = i
        else:
            actions[i] = 2
            
    actions[shortest_index] = 2
    for i in range(len(actions)):
        if actions[i] is None:
            tag_action = env.config["access_length"] - env.controlled_vehicles[i].lane.local_coordinates(env.controlled_vehicles[i].position)[0]
            actions[i] = 2 if tag_action > IDLE_velocity else (1 if tag_action > SLOWER_velocity else 0)

    return tuple(actions)




