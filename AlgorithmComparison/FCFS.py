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
    cav = []
    hv = []
    for vehicle in env.road.vehicles:
        if isinstance(vehicle, MDPVehicle):
            cav.append(vehicle)
        elif isinstance(vehicle, IDMVehicle):
            hv.append(vehicle)
    
    all_vehicles = []
    for v in hv:
        if "o" in v.lane_index[0] and "ir" in v.lane_index[1]:
            dist = env.config["access_length"] - v.lane.local_coordinates(v.position)[0]
            all_vehicles.append(("hv", None, dist))
    
    for i, v in enumerate(cav):
        if "o" in v.lane_index[0] and "ir" in v.lane_index[1]:
            dist = env.config["access_length"] - v.lane.local_coordinates(v.position)[0]
            all_vehicles.append(("cav", i, dist))

    actions = [None for _ in range(len(cav))]

    # 全部通过加插口，无需通行决策，全部加速
    if not all_vehicles:
        return tuple([2 for _ in cav])  

    # 找最小距离的车
    first = min(all_vehicles, key=lambda x: x[2])

    if first[0] == "hv":
        # HV 优先：所有 CAV 减速或停车
        for i, veh in enumerate(cav):
            dist = env.config["access_length"] - veh.lane.local_coordinates(veh.position)[0]
            actions[i] = 2 if dist > IDLE_velocity else (1 if dist > SLOWER_velocity else 0)
    else:
        # CAV 优先：该车放行，其余减速
        for i, veh in enumerate(cav):
            if i == first[1]:
                actions[i] = 2
            else:
                dist = env.config["access_length"] - veh.lane.local_coordinates(veh.position)[0]
                actions[i] = 2 if dist > IDLE_velocity else (1 if dist > SLOWER_velocity else 0)

    return tuple(actions)





