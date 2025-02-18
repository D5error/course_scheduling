import pandas as pd
import yaml
import os


def read_excel(path, sheet_name, skiprows):
    df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skiprows)
    df["任课教师"] = df["任课教师"].fillna("空")
    df["上课地点"] = df["上课地点"].fillna("空")
    df["上课周次"] = df["上课周次"].fillna("空")
    return df


def load_config():
    with open("./config.yaml", "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)

    return {
        "teacher_satisfaction": data["teacher_satisfaction"],
        "student_satisfaction": data["student_satisfaction"],
        "name_of_days": data["name_of_days"],
        "sections": data["sections"],
        "teacher_weight": data["teacher_weight"],
        "student_weight": data["student_weight"],
        "classes_name": data["classes_name"]
    }


def make_file(path):
    if not os.path.exists(path):
        os.makedirs(path)

def make_css(dir):
    make_file(dir)
    with open("./assets/css/timetable.css", "r", encoding="utf-8") as css:
        css = css.read()
    with open(f"{dir}/timetable.css", "w", encoding="utf-8") as f:
        f.write(css)


TEACHER = 1
STUDENT = 2
def make_html(role, data, name, courses_list, teachers_list, weeks_list, times_list, classes_list, rooms_list, weeks_of_class, grade_major):
    # 提取课程表信息
    courses = []
    for item in data:
        i, j, k, l, r = map(int, item)
        if (role == TEACHER and teachers_list[j] == name) or (role == STUDENT and classes_list[r] == name):
            courses.append({
                "course": courses_list[i], 
                "teacher": teachers_list[j], 
                "day": weeks_list[k], 
                "part": l, 
                "class": classes_list[r], 
                "room": rooms_list[j], 
                "weeksofclass": weeks_of_class[j]
            })
    
    # 生成HTML内容
    with open("./assets/timetable.html", 'r', encoding="utf-8") as f:
        html_content = f.read()
    if role == TEACHER:
        grade_major = grade_major[0]
        html_content += f"年级专业：{grade_major}<br>教师：{name}</h1><table><tr><th>时间</th>"
    else:
        html_content += f"班级：{name}</h1><table><tr><th>时间</th>"

    for day in weeks_list:
        html_content += f"<th>{day}</th>\n"  # 添加天数列
    html_content += "</tr>\n"

    # 添加时间行
    for i, part in enumerate(times_list):
        html_content += f"<tr>\n<td>{part}</td>\n"
        for day in weeks_list:
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
    html_content += "</table></body></html>"

    if role == TEACHER:
        make_file(f"result/教师课程表/{grade_major}")
        with open(f"./result/教师课程表/{grade_major}/{name}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
    else:
        make_file("result/学生课程表")
        with open(f"./result/学生课程表/{name}.html", "w", encoding="utf-8") as file:
            file.write(html_content)