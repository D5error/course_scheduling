'''
描述：排课系统模型求解
'''
from load import generate_schedule


if __name__ == "__main__":
    A = [0.10, 0.20, 0.26, 0.30, 0.14] # 表示老师对于课程在每个时段的课程满意度的集合
    B = [0.14, 0.26, 0.20, 0.30, 0.10] # 表示学生对于课程在每个时段的课程满意度的集合
    W = ["星期一", "星期二", "星期三", "星期四", "星期五"] # 星期
    P = ["8:00-9:40", "10:10-11:50", "14:20-16:00", "16:30-18:10", "19:00-21:35"] # 时段
    p = 0.50 # 教师评价的比重
    q = 0.50 # 学生评价的比重
    S = [["23级智科一班", "23级智科二班"],
         ["23级智能交通一班", "23级智能交通二班"],
         ["22级智科一班", "22级智科二班"],
         ["22级交通一班", "22级交通二班"],
         ["21级智科一班", "21级智科二班"],
         ["21级交通一班", "21级交通二班"],
         ["20级智科一班", "20级智科二班"],
         ["20级交通一班", "20级交通二班"]] # 班级
    generate_schedule(r"./23学年秋使用的课表.xlsx",A, B, W, P, S, p, q)