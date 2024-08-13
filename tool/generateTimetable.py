import pandas as pd
from .loadConfig import *
from .read_excel import *
from .solve import *
from .make_student_html import *
from .make_teacher_html import *


class generateTimetable:
    def __init__(self):
        self.A, self.B, self.W, self.P, self.S, self.p, self.q = loadConfig()


    def run(self, path):
        df = read_excel(path, sheet_name=0, skiprows=2) # 用字符串填补空数据

        # 年级专业的所在行的范围：每个年级的不同专业的课程表在excel表格的不同行里，把起始行和末尾行提取出来作为元组
        index = pd.Series(df[df["年级专业"].notna()]["年级专业"].index)
        index.loc[len(index)] = max(df.index) + 1
        grade_row_range = [(int(index.loc[i]), int(index.loc[i + 1]) - 1) for i in range(len(index) - 1)]

        # 提取数据
        for i, row_range in enumerate(grade_row_range):
            start, end = row_range # 当前年级专业的行范围
            C = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["课程"].str.strip() # 表示所有课程的集合
            T = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["任课教师"].str.strip() # 表示所有教师的集合
            W = pd.Series(self.W) # 表示所有星期的集合
            P = pd.Series(self.P) # 表示所有上课时段的列表
            rooms = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["上课地点"].str.strip() # 教室名称
            weeks_of_class = df.loc[start: end, ["课程", "上课周次"]]["上课周次"].str.strip() # 上课周次
            grade_major = pd.Series([str(df.loc[start, "年级专业"])]).str.strip() # 年级专业
            S = pd.Series(self.S[i]) # 班级
            A = self.A # 教师满意度
            B = self.B # 学生满意度
            p = self.p # 教师评价的比重
            q = self.q # 学生评价的比重

            # 对当前班级专业求解
            data = solve(A, B, C, W, T, P, S, p, q)
            if data == None:
                print("\n\n\n")
                print("求解失败！")
                return
            
            # 生成班级课程表
            for s in S:
                make_student_html(data, s, C, T, self.W, self.P, self.S, rooms, weeks_of_class)

            # 生成教师课程表
            for j in T:
                make_teacher_html(data, j, C, T, self.W, self.P, self.S, rooms, weeks_of_class, grade_major)
