'''
描述：导入数据
'''
import openpyxl
import pandas as pd


# 资源
C = [] # 表示所有课程的集合
T = [] # 表示所有教师的集合
W = [] # 表示所有星期的集合
P = [] # 表示所有上课时段的列表
S = [] # 表示所有班级的集合
# 评价与比重
A = [] # 表示老师对于课程在每个时段的课程满意度的集合
B = [] # 表示学生对于课程在每个时段的课程满意度的集合
p = None # 教师评价的比重
q = None # 学生评价的比重

def load_schedule(path):
    global C # 课程
    global T # 教师
    global W # 星期
    global P # 时段
    global S # 班级
    global Rooms # 教室
    global A # 教师满意度
    global B # 学生满意度
    global p
    global q
    df = pd.read_excel(path, sheet_name=0)
    C = df[df["课程"].notna()]["课程"]
    T = df[df["教师"].notna()]["教师"]
    W = df[df["星期"].notna()]["星期"]
    P = df[df["时段"].notna()]["时段"]
    Rooms = df[df["教室"].notna()]["教室"]
    S = df[df["班级"].notna()]["班级"]
    A = df[df["教师满意度"].notna()]["教师满意度"]
    B = df[df["学生满意度"].notna()]["学生满意度"]
    p = df[df["教师评价比重"].notna()]["教师评价比重"]
    q = df[df["学生评价比重"].notna()]["学生评价比重"]
