'''
描述：导入数据，可视化结果
'''
import openpyxl
import os
import pandas as pd
import numpy as np
from .solve import *



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


def generate_schedule(path, list_A, list_B, list_W, list_P,list_S, float_p=0.5, float_q=0.5):
    global C # 课程
    global T # 教师
    global W # 星期
    global P # 时段
    global S # 班级
    global Rooms # 教室
    global WeeksOfClass # 上课周次
    global A # 教师满意度
    global B # 学生满意度
    global p # 教师评价的比重
    global q # 学生评价的比重
    global GradeMajor # 年级专业

    # 处理数据
    df = pd.read_excel(path, sheet_name=0, skiprows=2)
    df["任课教师"] = df["任课教师"].fillna("空")
    df["上课地点"] = df["上课地点"].fillna("空")
    df["上课周次"] = df["上课周次"].fillna("空")

    # 年级专业的所在行的范围
    index = pd.Series(df[df["年级专业"].notna()]["年级专业"].index)
    index.loc[len(index)] = max(df.index) + 1
    grade_row_range = [(int(index.loc[i]), int(index.loc[i + 1]) - 1) for i in range(len(index) - 1)]

    # 提取数据
    for i, item in enumerate(grade_row_range):
        # 当前年级专业的行范围
        start = item[0]
        end = item[1]

        C = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["课程"].str.strip()
        T = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["任课教师"].str.strip()
        W = pd.Series(list_W)
        P = pd.Series(list_P)
        Rooms = df.loc[start: end, ["课程", "任课教师", "上课地点"]]["上课地点"].str.strip()
        WeeksOfClass = df.loc[start: end, ["课程", "上课周次"]]["上课周次"].str.strip()
        GradeMajor = pd.Series([str(df.loc[start, "年级专业"])]).str.strip()
        S = pd.Series(list_S[i])
        A = list_A
        B = list_B
        p = float_p
        q = float_q

        # 对当前班级专业求解
        data = solve()
        if data == None:
            return
        
        # 生成班级课程表
        for s in S:
            make_html(data, s, isClass=True)

        # 生成教师课程表
        for j in T:
            make_html(data, j, isTeacher=True)
    

def make_html(data, name, isClass=False, isTeacher=False):
    # 类型转换
    C = load.C.tolist()
    T = load.T.tolist()
    W = load.W.tolist()
    P = load.P.tolist()
    S = load.S.tolist()
    Rooms = load.Rooms.tolist()
    WeeksOfClass = load.WeeksOfClass.tolist()

    # 提取课程表信息
    courses = []
    for item in data:
        i, j, k, l, r = item
        i = int(i)
        j = int(j)
        k = int(k)
        l = int(l)
        r = int(r)
        if isClass and S[r] != name:
            continue
        if isTeacher and T[j] != name:
            continue
        courses.append({"course": C[i], "teacher": T[j], "day": W[k], "part": l, "class": S[r], "room": Rooms[j], "weeksofclass": WeeksOfClass[j]})
    
    # 生成HTML内容
    html_content = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>课程表</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 2px solid #fff;
                padding: 40px;
                text-align: center;
            }
            th {
                background-color: #ffffff;
            }
            .course {
                background-color: #4196ff;
                color: #ffffff;
            }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">
    """
    if isClass:
        html_content += f"""
        班级：{name}</h1>
            <table>
                <tr>
                    <th>时间</th>
        """
    else:
        html_content += f"""
        年级专业：{GradeMajor.tolist()[0]}<br>教师：{name}</h1>
            <table>
                <tr>
                    <th>时间</th>
        """

    # 添加天数列
    for day in W:
        html_content += f"<th>{day}</th>\n"
    html_content += "</tr>\n"

    # 添加时间行
    for i, part in enumerate(P):
        html_content += f"<tr>\n    <td>{part}</td>\n"
        for day in W:
            course_name = ""
            same_class = [] # 同时上课的班级
            course = None
            for _course in courses:
                if _course["day"] == day and _course["part"] == i:
                    course_name = _course["course"]
                    course = _course
                    same_class.append(_course["class"])
            if course_name:
                html_content += f"<td class='course'>课程：{course_name}<br>教师：{course['teacher']}<br>班级：{'，'.join(same_class)}<br>教室：{course['room']}<br>上课周次：{course['weeksofclass']}</td>\n"
            else:
                html_content += "<td></td>\n"
        html_content += "</tr>\n"

    html_content += """
        </table>
    </body>
    </html>
    """

    # 创建文件夹
    if not os.path.exists("result/学生课程表"):
        os.makedirs("result/学生课程表")
    if not os.path.exists("result/教师课程表"):
        os.makedirs("result/教师课程表")

    # 将HTML内容写入文件
    if isTeacher:
        if not os.path.exists(f"result/教师课程表/{GradeMajor.tolist()[0]}"):
                os.makedirs(f"result/教师课程表/{GradeMajor.tolist()[0]}")   
        with open(f"./result/教师课程表/{GradeMajor.tolist()[0]}/{name}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"课程表已生成，请打开 './result/教师课程表/{GradeMajor.tolist()[0]}/{name}.html' 查看。")
        
    else:
        with open(f"./result/学生课程表/{name}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"课程表已生成，请打开 './result/学生课程表/{name}.html' 查看。")
