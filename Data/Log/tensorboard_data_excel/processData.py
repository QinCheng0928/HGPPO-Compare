import pandas as pd
import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 原始文件名
file_name = {
    "A2C": {
        "A2C_v0.csv",
        "A2C_v1.csv",
        "A2C_v2.csv"
    },
    "DQN": {
        "DQN_v0.csv",
        "DQN_v1.csv",
        "DQN_v2.csv"
    },
    "HGPPO": {
        "HGPPO_v0.csv",
        "HGPPO_v1.csv"
    },
    "PPO": {
        "PPO_v0.csv",
        "PPO_v1.csv",
        "PPO_v2.csv"
    },
    "RecurrentPPO": {
        "RecurrentPPO_v0.csv",
        "RecurrentPPO_v1.csv",
        "RecurrentPPO_v2.csv"
    }
}

def calculate_confidence_interval(df, step_col='Step', confidence=0.6):
    value_columns = df.columns.difference([step_col])
    n = len(value_columns)
    mean_vals = df[value_columns].mean(axis=1)
    std_vals = df[value_columns].std(axis=1, ddof=1)
    se = std_vals / np.sqrt(n)
    alpha = 1 - confidence
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    ci_lower = mean_vals - t_crit * se
    ci_upper = mean_vals + t_crit * se
    return mean_vals, ci_lower, ci_upper

def plot_mean_with_ci():
    plt.figure(figsize=(12, 8))
    
    for key in file_name.keys():
        file_path = os.path.join(script_dir, f"{key}_merged.csv")
        if not os.path.exists(file_path):
            print(f"[ERROR]文件不存在：{file_path}，跳过")
            continue

        df = pd.read_csv(file_path)
        steps = df['Step']
        mean_vals = df['Mean']
        ci_lower = df['CI_lower']
        ci_upper = df['CI_upper']

        plt.plot(steps, mean_vals, label=f"{key} 平均值")
        plt.fill_between(steps, ci_lower, ci_upper, alpha=0.3)

    plt.xlabel('Step')
    plt.ylabel('数值')
    plt.title(f'平均值及置信区间')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def process_all():
    step_threshold = 30000  # 加在这里，便于复用

    # 1. 删除无用列 “Wall time”
    for key, files in file_name.items():
        for file in files:
            file_path = os.path.join(script_dir, file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                if "Wall time" in df.columns:
                    df = df.drop(columns=["Wall time"])
                    df.to_csv(file_path, index=False)
                    print(f"已删除文件 {file_path} 中的 “Wall time” 列")
                else:
                    print(f"[ERROR]文件 {file_path} 中未找到 “Wall time” 列")
            else:
                print(f"[ERROR]文件未找到：{file_path}")

    # 2. 合并文件并计算置信区间
    for key, files in file_name.items():
        merged_df = None
        for file in sorted(files):
            file_path = os.path.join(script_dir, file)
            if not os.path.exists(file_path):
                print(f"[ERROR]合并时文件未找到：{file_path}，跳过")
                continue
            df = pd.read_csv(file_path)
            temp_df = df[["Step", "Value"]].copy()
            col_name = os.path.splitext(file)[0]
            temp_df = temp_df.rename(columns={"Value": col_name})
            if merged_df is None:
                merged_df = temp_df
            else:
                merged_df = pd.merge(merged_df, temp_df, on="Step", how="outer")

        if merged_df is not None:
            merged_df = merged_df.sort_values("Step")

            # 3. 计算置信区间
            mean_vals, ci_lower, ci_upper = calculate_confidence_interval(merged_df, step_col='Step')
            merged_df['Mean'] = mean_vals
            merged_df['CI_lower'] = ci_lower
            merged_df['CI_upper'] = ci_upper

            # ✅ 仅保留符合条件的数据
            merged_df = merged_df[(merged_df['Step'] <= step_threshold) & 
                                  merged_df['Mean'].notna() & 
                                  merged_df['CI_lower'].notna() & 
                                  merged_df['CI_upper'].notna()]

            # 4. 保存带置信区间的合并文件（只保存过滤后的数据）
            output_file = os.path.join(script_dir, f"{key}_merged.csv")
            merged_df.to_csv(output_file, index=False)
            print(f"已保存过滤后的带置信区间的合并文件：{output_file}")

    # 5. 绘图
    plot_mean_with_ci()


if __name__ == "__main__":
    process_all()

