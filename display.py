'''
描述：结果可视化
'''
import load
import os


def make_html(data, name, isClass=False, isTeacher=False):
    C = load.C
    T = load.T
    W = load.W
    P = load.P
    S = load.S

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
        courses.append({"course": C[i], "teacher": T[j], "day": W[k], "part": l, "class": S[r], "classroom": load.Rooms[i]})
    
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
        教师：{name}</h1>
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
            for course in courses:
                if course["day"] == day and course["part"] == i:
                    course_name = course["course"]
                    break
            if course_name:
                html_content += f"<td class='course'>课程：{course_name}<br>教师：{course['teacher']}<br>班级：{course['class']}<br>教室：{course['classroom']}</td>\n"
            else:
                html_content += "<td></td>\n"
        html_content += "</tr>\n"

    html_content += """
        </table>
    </body>
    </html>
    """
    if not os.path.exists("result"):
        os.makedirs("result")

    # 将HTML内容写入文件
    with open(f"./result/{name}.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"课程表已生成，请打开 './result/{name}.html' 查看。")


def display(data):
    if data == None:
        return
    
    # 生成班级课表
    for s in load.S:
        make_html(data, s, isClass=True)

    # 生成教师课表
    for j in load.T:
        make_html(data, j, isTeacher=True)
