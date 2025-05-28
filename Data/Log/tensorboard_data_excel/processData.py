import pandas as pd

DELETE_WallTime_COLUMNS = 0

file_name = {
    "A2C": {
        "A2C_v0.xlsx",
        "A2C_v1.xlsx",
        "A2C_v2.xlsx"
    },
    "DQN": {
        "DQN_v0.xlsx",
        "DQN_v1.xlsx",
        "DQN_v2.xlsx"
    },
    "HGPPO": {
        "HGPPO_v0.xlsx",
        "HGPPO_v1.xlsx"
    },
    "PPO": {
        "PPO_v0.xlsx",
        "PPO_v1.xlsx",
        "PPO_v2.xlsx"
    },
    "RecurrentPPO": {
        "RecurrentPPO_v0.xlsx",
        "RecurrentPPO_v1.xlsx",
        "RecurrentPPO_v2.xlsx"
    }
}


def deleteWallTimeColumns():
    df = pd.read_excel("your_file.xlsx")
    if "Wall time" in df.columns:
        df = df.drop(columns=["Wall time"])
    df.to_excel("modified_file.xlsx", index=False)

if __name__ == "__main__":
    # 选择操作类型
    SELECT_OPTIONS = 0
    
    if SELECT_OPTIONS == 0:
        deleteWallTimeColumns()