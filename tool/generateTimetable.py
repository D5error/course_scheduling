import pandas as pd
from .utils import *
from .solve import *


class GenerateTimetable:
    def __init__(self):
        config = load_config()
        self.A = config["teacher_satisfaction"] # 教师满意度
        self.B = config["student_satisfaction"] # 学生满意度
        self.W = config["name_of_days"] # 星期
        self.P = config["sections"] # 上课时段
        self.S = config["classes_name"] # 班级
        self.p = config["teacher_weight"] # 教师评价的比重
        self.q = config["student_weight"] # 学生评价的比重


    def run(self, path):
        # 读取excel表格，同时填充缺失值
        df = read_excel(path, sheet_name=0, skiprows=2)

        # 获取每个年级专业的行区间
        index = pd.Series(df[df["年级专业"].notna()]["年级专业"].index)
        index.loc[len(index)] = max(df.index) + 1
        grade_row_range = [(int(index.loc[i]), int(index.loc[i + 1]) - 1) for i in range(len(index) - 1)]

        # 提取表格中的数据到变量中
        for i, row_range in enumerate(grade_row_range):
            # 当前年级专业的行起始索引和结束索引
            start, end = row_range
            courses_list = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["课程"].str.strip() # 所有课程
            teachers_list = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["任课教师"].str.strip() # 所有教师
            weeks_list = pd.Series(self.W) # 所有星期
            times_list = pd.Series(self.P) # 所有上课时段
            rooms_list = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["上课地点"].str.strip() # 教室名称
            weeks_of_class = df.loc[start: end, ["课程", "上课周次"]]["上课周次"].str.strip() # 上课周次
            grade_major = pd.Series([str(df.loc[start, "年级专业"])]).str.strip() # 年级专业
            classes_list = pd.Series(self.S[i]) # 班级

            # 求解线性规划问题
            data = solve(
                A=self.A, 
                B=self.B,
                C=courses_list,
                W=weeks_list, 
                T=teachers_list, 
                P=times_list, 
                S=classes_list, 
                p=self.p, 
                q=self.q
            )
            
            # pd.Series转换为list
            courses_list = courses_list.tolist()
            teachers_list = teachers_list.tolist()
            rooms_list = rooms_list.tolist()
            weeks_of_class = weeks_of_class.tolist()

            # 生成班级课程表
            make_css("result/css")
            for classs in classes_list:
                make_html(STUDENT, data, classs, courses_list, teachers_list, weeks_list, times_list, classes_list, rooms_list, weeks_of_class, grade_major)

            # 生成教师课程表
            make_css("result/教师课程表/css")
            for teacher in teachers_list:
                make_html(TEACHER, data, teacher, courses_list, teachers_list, weeks_list, times_list, classes_list, rooms_list, weeks_of_class, grade_major)
