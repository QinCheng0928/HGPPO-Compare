# 获取项目的根目录,并将根目录添加到系统路径中
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("root_dir:", root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 导入算法模块
from AlgorithmComparison.FCFS import FCFS
from AlgorithmComparison.RotatingIDM import RotatingIDM

# 导入仿真环境
import highway_env

# 忽略一些版本兼容的错误
import warnings
warnings.filterwarnings("ignore")




# ================================
# 选择算法进行对比
# 可选：FCFS, Rotating-IDM
# ================================
SELECTED_ALGORITHM = "FCFS"

def main():
    # 选择算法
    algo_map = {
        'FCFS': FCFS,
        'Rotating-IDM': RotatingIDM,
    }

    # 错误处理，抛出异常
    if SELECTED_ALGORITHM not in algo_map:
        raise ValueError(f"Unknown algorithm '{SELECTED_ALGORITHM}'")
    
    AlgoClass = algo_map[SELECTED_ALGORITHM]
    model = AlgoClass()
    model.run()

    
if __name__ == '__main__':
    main()