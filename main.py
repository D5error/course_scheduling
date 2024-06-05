'''
描述：排课系统模型求解
'''
from load import *
from solve import *
from display import *


if __name__ == "__main__":
    load_schedule(r"./data.xlsx")
    data = solve()
    display(data)