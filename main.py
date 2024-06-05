'''
描述：排课系统模型求解
'''

from load import *
from solve import *
from display import *

if __name__ == "__main__":

    p = 0.5 # 教师对于时段评价的比重
    q = 0.5 # 学生对于时段评价的比重
    load_schedule(r"./data.xlsx")
    data = solve(p, q)
    display(data)