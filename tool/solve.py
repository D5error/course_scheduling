import pulp


def string_to_int(list):
    return range(len(list))


def solve(A, B, C, W, T, P, S, p, q):
    """
    A: 教师满意度
    B: 学生满意度
    C: 课程
    W: 星期
    T: 时间
    P: 节数
    S: 班级
    p: 教师权重
    q: 学生权重
    """

    # 定义线性规划问题
    prob = pulp.LpProblem("SchedulingSystem", pulp.LpMaximize)

    # 班级名称
    class_name = S

    # excel表格中的数据是中文，需要转换为数字
    C = string_to_int(C)
    W = string_to_int(W)
    T = string_to_int(T)
    P = string_to_int(P)
    S = string_to_int(S)

    # 定义决策变量，且为非负二元变量
    x = pulp.LpVariable.dict("x_ijklr", (C,T, W, P, S), cat=pulp.LpBinary)
    

    # 添加目标函数
    prob += pulp.lpSum((p * A[l] + q * B[l]) * x[(i, j, k, l, r)] 
                       for i in C for j in T for k in W for l in P for r in S if i == j)
    
    # 约束1：对于每门课程，每个班每天最多上一次
    for i in C:
        for k in W:
            for r in S:
                prob += (pulp.lpSum(x[i, j, k, l, r] for j in T for l in P if i == j) <= 1)

    # 约束2：每个班一周上1次课程
    for i in C:
        for r in S:
            prob += (pulp.lpSum(x[i, j, k, l, r] for j in T for k in W for l in P if i == j) <= 1)

    # 约束3：多个班级可以上同时间的由同一老师教授的同一课程
    for i in C:
        for j in T:
            for k in W:
                for l in P:
                    prob += (pulp.lpSum(x[i, j, k, l, r] for r in S if i == j) <= len(S))

    # 约束4：同一个老师对同一个班教授的同一门课程每天最多上一次
    for i in C:
        for j in T:
            for k in W:
                for r in S:
                    prob += (pulp.lpSum(x[i, j, k, l, r] for l in P if i == j) <= 1)

    # 约束5：每个班每周最少上2次课，最多上20次课
    for r in S:
        prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for j in T for k in W for l in P if i == j) <= 20)
        prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for j in T for k in W for l in P if i == j) >= 2)

    # 约束6：每个班每天最多上5次课
    for k in W:
        for r in S:
            prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for j in T for l in P if i == j) <= 5)

    # 约束7：每个老师对每个班一周最多上4次课
    for j in T:
        for r in S:
            prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for k in W for l in P if i == j) <= 4)

    # 约束8：每个老师每周最多上12次课，最少上2次课
    # for j in T:
    #     prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for l in P for k in W for r in S if i == j) <= 12)
    #     prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for l in P for k in W for r in S if i == j) >= 2)

    # 约束9：每个班每周最多4个早八
    for r in S:
        l = P[0]
        prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for j in T for k in W if i == j) <= 4)

    # 约束10：每个老师每天最多上3次课
    for j in T:
        for k in W:
            prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for l in P for r in S if i == j) <= 3)

    # 约束11：每个老师每天最多给每一个班上2次课
    for j in T:
        for k in W:
            for r in S:
                prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for l in P if i == j) <= 2)

    # 约束12：每个老师一周最多上4个早八
    for j in T:
        for k in W:
            l = P[0]
            prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for r in S if i == j) <= 4)

    # 约束13：非负性
    for i in C:
        for j in T:
             if i == j:
                for k in W:
                    for l in P:
                        for r in S:
                            prob += (pulp.lpSum(x[i, j, k, l, r]) >= 0)

    # 约束14：二元性
        # 已在定义变量时给出

    # 约束15：每个班的同一课程都不能由其他老师来教授
        # 定义目标函数时和其它约束条件已给出

    # 约束16：每个班在同一星期的同一时段最多上一门课程
    for k in W:
        for l in P:
            for r in S:
                prob += (pulp.lpSum(x[i, j, k, l, r] for i in C for j in T if i == j) <= 1)

    # 求解问题
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # 打印结果
    print(pulp.LpStatus[prob.status])
    # 求解成功
    if pulp.LpStatus[prob.status] == "Optimal":
        result_ijklr = []

        # 提取ijklr
        for v in prob.variables():
            if(v.varValue == 1):
                result_ijklr.append(v.name.split("_")[-5 :])

        # 打印结果
        for name in class_name: 
            print(name, end=', ')
        print("：目标函数的最大值 =", pulp.value(prob.objective))

        return result_ijklr

    # 求解失败
    raise RuntimeError("无可行解\n\n\n求解失败！")
