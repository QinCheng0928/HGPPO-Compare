# 获取项目的根目录,并将根目录添加到系统路径中
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("root_dir:", root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 导入算法模块
from AlgorithmComparison.FCFS import fcfs_predict
from AlgorithmComparison.RotatingIDM import rotating_predict

# 导入仿真环境
import highway_env

# 导入辅助库
import gymnasium as gym
import imageio
import openpyxl
import AlgorithmComparison.utils as utils
import cv2

# 忽略一些版本兼容的错误
import warnings
warnings.filterwarnings("ignore")


# ================================
# 选择算法进行对比
# 可选：FCFS, Rotating-IDM
# ================================
SELECTED_ALGORITHM = "FCFS"

def main():
    # 选择算法，如出现错误，则错误处理，抛出异常
    algorithm_map = {
        'FCFS': fcfs_predict,
        'Rotating': rotating_predict
    }
    if SELECTED_ALGORITHM not in algorithm_map:
        raise ValueError(f"未知的算法：'{SELECTED_ALGORITHM}'，请重新选择算法！")
    
    # 创建环境
    env = gym.make('intersection-multi-agent-v0',render_mode='rgb_array')
    
    # 设置仿真次数
    for i in range(20):
        # 设置视频保存配置
        video_dir = os.path.join(root_dir, 'Data', 'Video', SELECTED_ALGORITHM)
        os.makedirs(video_dir, exist_ok=True)  # 如果目录不存在则创建
        video_name = os.path.join(video_dir, f"{i}.mp4")
        video_writer = imageio.get_writer(video_name, fps=30)
        # 设置excel保存配置
        excel_dir = os.path.join(root_dir, 'Data', 'Excel', SELECTED_ALGORITHM)
        os.makedirs(excel_dir, exist_ok=True)
        excel_name = os.path.join(excel_dir, f"{i}.xlsx")
        workbook = openpyxl.Workbook()
        for sheet_name in workbook.sheetnames:
            std = workbook[sheet_name]
            workbook.remove(std)

            
        row = 0    
        obs, info = env.reset()
        done = truncated = False
        while not (done or truncated):
            if SELECTED_ALGORITHM == "FCFS":
                action = algorithm_map[SELECTED_ALGORITHM](env)
            if SELECTED_ALGORITHM == "Rotating-IDM":
                action = algorithm_map[SELECTED_ALGORITHM](env)
            
            # print(f"第{i}轮仿真，当前状态：{obs}, 当前动作：{action}")
            obs, reward, done , truncated, info = env.step(action)
        
            # 获取当前画面并添加到视频中
            frame = env.render()
            video_writer.append_data(frame)
            
            # 获取当前数据并添加到excel中
            utils.write_excel(workbook, env, row)
            workbook.save(excel_name)
            row += 1
        
        video_writer.close()
        
        print(f"第{i}轮仿真结束，视频和数据已保存！")


    
if __name__ == '__main__':
    main()