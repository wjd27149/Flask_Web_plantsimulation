import matplotlib.pyplot as plt
import numpy as np
import random
import os
import time           
def Gantt_chart(CHS, m: int, n: int):
    '''绘制甘特图
    '''
    # 定义颜色列表
    colors = ['green', 'orange', 'purple', 'cyan', 'magenta', 'brown', 'lime', 'pink', 'teal', 'lavender']
    plt.figure(figsize=(m*2, m))
    #   绘制常规工序
    for i in range(len(CHS.jobs)):
        sum = len(CHS.jobs[i].start)
        t = 0
        for j in range(sum):
            a = CHS.jobs[i].start[j]
            b = CHS.jobs[i].end[j]
            c = CHS.jobs[i].mac_list[j]

            plt.barh(c - 1,height=0.8, left=a , width= b - a, align='center',
                        color=colors[i], edgecolor='k')
            plt.text(x=(b - a) / 2 + a, y=c - 1, s=f"{CHS.jobs[i].name}/{t}",
                        horizontalalignment='center',fontsize=8)
            t += 1
            # print(f' operation: {CHS.jobs[i].index}  on {c} mac start_time: {a} end_time: {b} op_time: {b-a}')
    
    #绘制换模工序
    for i in (CHS.CMT_M):
        i = i - 1
        for j in range(len(CHS.machines[i].CM_start)):
            a = CHS.machines[i].CM_start[j]
            b = CHS.machines[i].CM_end[j]
            plt.barh(i ,height=0.8, left=a , width= b - a, align='center',
                        color='r', edgecolor='k')
            plt.text(x=(b - a) / 2 + a, y=i , s=f"CMT",
                        horizontalalignment='center',fontsize=8)        
    
    plt.yticks(list(range(m)),
        ['machine%d'% (i+1) for i in range(m)])
    plt.rcParams['font.sans-serif'] = 'SimHei' 
    plt.title(f'最大完工时间 : {CHS.C_max}/min     机器总时间负荷 : {CHS.load}/min     总换模时间 : {CHS.total_CMT}/min')
    plt.xlabel('时间/min', fontdict={'fontsize': 12})
    # 1. 定义正确的目标目录路径（注意路径分隔符和目录名一致性）
    target_dir = os.path.join("APP", "static", "static_result_chart")  # 与makedirs保持一致

    # 2. 创建目录（确保路径正确）
    os.makedirs(target_dir, exist_ok=True)  # 使用相同的target_dir变量

    # 3. 定义最终保存路径
    target_path = os.path.join(target_dir, 'nsga.png')  # 使用os.path.join确保跨平台兼容

    # 4. 保存图片（添加bbox_inches='tight'避免截断内容）
    plt.savefig(target_path, bbox_inches='tight', dpi=300)  # 添加dpi提高图片质量

    # 5. 显示图片（可选）
    # plt.show()

    # 6. 打印确认信息
    print(f"图片已保存到: {os.path.abspath(target_path)}")

# 3-objective
def Tri_Dominate(Pop1,Pop2):
    '''
    :param Pop1:
    :param Pop2:
    :return: If Pop1 dominate Pop2, return True
    '''
    if (Pop1.fitness[0]<Pop2.fitness[0] and Pop1.fitness[1]<Pop2.fitness[1] and Pop1.fitness[2]<Pop2.fitness[2]) or \
        (Pop1.fitness[0] <= Pop2.fitness[0] and Pop1.fitness[1] < Pop2.fitness[1] and Pop1.fitness[2]<Pop2.fitness[2]) or \
        (Pop1.fitness[0] < Pop2.fitness[0] and Pop1.fitness[1] <= Pop2.fitness[1] and Pop1.fitness[2]<Pop2.fitness[2]) or \
            (Pop1.fitness[0] < Pop2.fitness[0] and Pop1.fitness[1] <Pop2.fitness[1] and Pop1.fitness[2]<=Pop2.fitness[2]) or \
            (Pop1.fitness[0] <= Pop2.fitness[0] and Pop1.fitness[1] <= Pop2.fitness[1] and Pop1.fitness[2]<Pop2.fitness[2]) or \
            (Pop1.fitness[0] < Pop2.fitness[0] and Pop1.fitness[1] <= Pop2.fitness[1] and Pop1.fitness[2]<=Pop2.fitness[2]) or \
            (Pop1.fitness[0] <=Pop2.fitness[0] and Pop1.fitness[1] < Pop2.fitness[1] and Pop1.fitness[2]<=Pop2.fitness[2]):
        return True
    else:
        return False
    
def fast_non_dominated_sort(Pop):
    S=[[] for i in range(len(Pop))]
    front = [[]]
    n=[0 for i in range(len(Pop))]
    rank = [0 for i in range(len(Pop))]

    for p in range(len(Pop)):
        S[p]=[]
        n[p]=0
        for q in range(len(Pop)):
            if Tri_Dominate(Pop[p],Pop[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif Tri_Dominate(Pop[q],Pop[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front) - 1]
    NDSet=[]
    for Fi in front:
        NDSeti=[]
        for pi in Fi:
            NDSeti.append(Pop[pi])
        NDSet.append(NDSeti)
    return NDSet

# 交叉变异
# POX:precedence preserving order-based crossover
# p1: 染色体p1 chs1     p2: 染色体p2 chs2     n: number of job 
def POX(p1, p2, n: int):
    jobsRange = range(0, n)
    sizeJobset1 = random.randint(1, n)
    jobset1 = random.sample(jobsRange, sizeJobset1)
    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return o1, o2

def Job_Crossover(p1 ,p2, n: int):
    jobsRange = range(0, n)
    sizeJobset1 = random.randint(0, n)
    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]
    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return o1 ,o2
    '''
工序变异：
swap_mutation p: chs
NB_mutation: neigborhood mutation       pm: 变异率
'''
def swap_mutation(p):
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)
    if pos1 == pos2:
        return p
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    offspring = p[:pos1] + [p[pos2]] + \
                p[pos1 + 1:pos2] + [p[pos1]] + \
                p[pos2 + 1:]
    return offspring

def MB_mutation(p1: list, pm):
    D = len(p1)
    c1 = p1.copy()
    r = np.random.uniform(size=D)
    for idx1, val in enumerate(p1):
        if r[idx1] <= pm:
            idx2 = np.random.choice(np.delete(np.arange(D), idx1))
            c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
    return c1

def Crossover_Machine(CHS1, CHS2):        #随机选择k个元素互换
    length = len(CHS1)
    T_r = [j for j in range(length)]
    T_ = random.sample(T_r,k= random.randint(1, length))     # 不重复的
    # 将父代的染色体复制到子代中去，保持他们的顺序和位置
    for i in T_:
        K, K_2 = CHS1[i], CHS2[i]
        CHS1[i], CHS2[i] = K_2, K
    return CHS1, CHS2

def Mutation_Machine(CHS: list, Processing_Time, J_site):
    length = len(CHS)
    T_r = [j for j in range(length)]
    T_ = random.sample(T_r,k= random.randint(1, length))     # 不重复的
    for i in T_:
        O_site = J_site[i]
        pt = Processing_Time[O_site[0]][O_site[1]]
        pt_find =pt[0]
        len_pt =len(pt ) -1
        k , m =1 ,0                 #遍历所有要变异的机器号，找到最小的加工时间对应的index
        while k< len_pt:
            if pt_find > pt[k]:
                pt_find = pt[k]
                m = k
            k += 1
        CHS[i] = m
    return CHS

#Function to calculate crowding distance
def crowding_distance(NDSet: list):
    Distance=[0]*len(NDSet)
    NDSet_obj={}
    for i in range(len(NDSet)):
        NDSet_obj[i]=NDSet[i].fitness
    ## 使用 items() 方法将字典转换为包含键值对的列表
    ND=sorted(NDSet_obj.items(),key=lambda x:x[1][0])
    Distance[ND[0][0]]=1e+20
    Distance[ND[-1][0]] = 1e+20
    for i in range(1,len(ND)-1):
        if Distance[ND[i][0]]==0:
            Distance[ND[i][0]]=abs(ND[i+1][1][0]-ND[i-1][1][0])+abs(ND[i+1][1][1]-ND[i-1][1][1])+abs(ND[i+1][1][2]-ND[i-1][1][2])
    distance=dict(enumerate(Distance))
    New_distance=sorted(distance.items(),key=lambda x:x[1],reverse=True)
    L=[_[0] for _ in New_distance]
    return L

def generate_and_write_txt(folder_path, file_name, content):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)
    lists_name = ["lists_best_CMAX", "lists_best_LOAD","lists_best_TOTAL_CMT","lists_best_GOAL", "lists_best_TIME"]

    with open(file_path, 'w') as file:
        file.write("final result: \n")
        data = content.copy()                                   #使用 copy() 以确保不影响原始数据。
        for row in zip(*data):                                  # zip(*data) 是用于解压缩迭代器的一种常见技巧。它将一个二维列表（或其他可迭代对象的序列）进行转置
            averages = [round(sum(item) / len(item), ndigits=2) for item in row]
            line = ' '.join(map(str, averages))
            file.write(line + '\n')
        file.write('\n')

        for i in range(len(content)):
            file.write(lists_name[i] + " :\n")
            for j in range(len(content[i])):
                file.write(f"gear {j}: ")
                for k in range(len(content[i][j])):
                    file.write(str(content[i][j][k]) + " ")
                file.write('\n')
            file.write('\n')

# 改变products.txt文件里的工件数量n

def change_n(n : int):
    # 读取文件
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建完整的文件路径
    file_path = os.path.join(script_dir, 'products.txt')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 修改数据
    for i, line in enumerate(lines):
        if i > 0:  # 跳过表头
            parts = line.split()
            parts[1] = str(n)
            lines[i] = ' '.join(parts) + '\n'
    # 保存修改后的数据
    with open(file_path, 'w') as file:
        file.writelines(lines)

def NGSAII_generate_and_write_txt(folder_path, file_name, content):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)
    lists_name = ["lists_best_CMAX", "lists_best_LOAD","lists_best_TOTAL_CMT","lists_best_GOAL", "lists_best_TIME"]

    with open(file_path, 'w') as file:
        file.write("final result: \n")
        data = content.copy()                                   #使用 copy() 以确保不影响原始数据。
        for row in data:                                  # zip(*data) 是用于解压缩迭代器的一种常见技巧。它将一个二维列表（或其他可迭代对象的序列）进行转置
            averages = [round(sum(row) / len(row), ndigits=2)]
            line = ' '.join(map(str, averages))
            file.write(line + '\n')
        file.write('\n')

        for i in range(len(content)):
            file.write(lists_name[i] + " :\n")

            for k in range(len(content[i])):
                file.write(str(content[i][k]) + " ")
            file.write('\n')