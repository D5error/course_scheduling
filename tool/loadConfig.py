import yaml


def loadConfig():
    with open("./config.yaml", "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    teacher_satisfaction = data["teacher_satisfaction"]
    student_satisfaction = data["student_satisfaction"]
    name_of_days = data["name_of_days"]
    sections = data["sections"]
    teacher_weight = data["teacher_weight"]
    student_weight = data["student_weight"]
    classes_name = data["classes_name"]
    return teacher_satisfaction, student_satisfaction, name_of_days, sections, classes_name, teacher_weight, student_weight
