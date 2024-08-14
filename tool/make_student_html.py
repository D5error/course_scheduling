from .make_file import *


def make_student_html(data, name, C, T, W, P, S, rooms, weeks_of_class):
    # 类型转换
    C = C.tolist()
    T = T.tolist()
    rooms = rooms.tolist()
    weeks_of_class = weeks_of_class.tolist()

    # 提取课程表信息
    courses = []
    for item in data:
        i, j, k, l, r = item
        i = int(i)
        j = int(j)
        k = int(k)
        l = int(l)
        r = int(r)
        if S[r] != name:
            continue
        courses.append({"course": C[i], "teacher": T[j], "day": W[k], "part": l, "class": S[r], "room": rooms[j], "weeksofclass": weeks_of_class[j]})

    # 生成HTML内容
    with open("./htmlConfig/timetable.html", 'r', encoding="utf-8") as f:
        html_content = f.read()
    html_content += f"""
    班级：{name}</h1>
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

    # 生成文件夹
    make_file("result/css")
    make_file("result/学生课程表")

    # 导入css
    with open("./css/timetable.css", "r", encoding="utf-8") as css:
        css = css.read()
    with open("result/css/timetable.css", "w", encoding="utf-8") as f:
        f.write(css)

    # 生成html    
    with open(f"./result/学生课程表/{name}.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    # print(f"课程表已生成，请打开 './result/学生课程表/{name}.html' 查看。")
