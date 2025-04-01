from __future__ import annotations      # 使用这个 第5行才不报错
from FJSP_ENV import *
import math

max_values = [0,0,0]
min_values = [99999,99999,99999]

def DISplay(population: list[Chromosome]):
    for index,pop in enumerate(population):
        print(f"{index}:  ", pop.CHS, pop.fitness[0])
    
class Population:
    def __init__(self, population_: list[Chromosome], args, J_site) -> None:
        self.population = population_
        self.args = args
        self.J_site = J_site

        self.avg_fitness = 0
        self.total_reciprocal_score = 0.0
        self.total_unconcentration = 0
        self.total_weight = 0

        # 列举fitness 列表 （包含三个数据） 用于归一化处理
        self.fitness_list = []

        self.size = len(self.population)
        self.clone_population = []
        self.fecundity_weights = []     # 繁殖力的权重list 为了后面轮盘赌选择

        self.threshold_Antibody_similarity = args.threshold_Antibody_similarity
        self.fecundity_coefficient = args.fecundity_coefficient
        self.p_elite = args.p_elite
        self.clone_size = args.clone_size

        self.pm_max = args.pm_max
        self.pc_max = args.pc_max
        self.pm_min = args.pm_min
        self.pc_min = args.pc_min  
        self.gene_size = args.gene_size   

        self.half_length = int(len(self.population[0].CHS) / 2)
    
    def get_avg_fitness(self):
        self.avg_fitness = self.total_score / self.size

    def caculate_score(self):
        self.fitness_list = []
        # 第一步 先划分出非支配 解 第二步 求目标函数值 第三步 求和代表得分
        for pop in self.population:
            pop.FJSP_setup()
            pop.decode()   
            self.fitness_list.append(pop.fitness)

        # Transpose the fitness_list
        # transposed_list = list(zip(*self.fitness_list))

        # # Find the maximum value in each column
        # max_values_ = [max(column) for column in transposed_list]
        # min_values_ = [min(column) for column in transposed_list]
        # for index, s1 in enumerate(max_values_):
        #     if(s1>max_values[index]):
        #         max_values[index] = s1

        # for index, s2 in enumerate(min_values_):
        #     if(s2<min_values[index]):
        #         min_values[index] = s2      
        # goal_list = []
        # for index, pop in enumerate(self.population):  
        #     if(max_values[0] == min_values[0]):a = 0.7 
        #     else: a = 0.7 * (max_values[0] - pop.fitness[0])/(max_values[0] - min_values[0])
        #     if(max_values[1] == min_values[1]):b = 0.05
        #     else: b = 0.05 * (max_values[1] - pop.fitness[1])/(max_values[1] - min_values[1])
        #     if(max_values[2] == min_values[2]):c = 0.25
        #     else: c = 0.25 * (max_values[2] - pop.fitness[2])/(max_values[2] - min_values[2])
        #     pop.goal =  a + b + c
        #     goal_list.append(pop.goal)

        NDSet = fast_non_dominated_sort(self.population)    # all nondominated set fronts of R_pop
        score_ND = 0
        for i in range(len(NDSet)):
            NDSet[i] = sorted(NDSet[i], key=lambda x: x.goal)
            for j in range(len(NDSet[i])):
                NDSet[i][j].score = 1                                                      # 防止重复加分数 先赋值等于1
                NDSet[i][j].score = NDSet[i][j].score + args.p_NDscore * score_ND          #求出非支配解 并且按照同一解集中 cmax的大小排序 然后赋分数
                score_ND += 1
                # print(f"{i} {j}  {NDSet[i][j].fitness} {NDSet[i][j].score}")

        score_FI = 0
        self.population = [item for sublist in NDSet for item in sublist]
        self.population.sort(key=lambda x: x.goal)                 # 重新赋值population 让他保存原来非支配得出的分数并且按照goal重新排序 赋分
        for index,pop in enumerate(self.population):
            pop.score += (1 - args.p_NDscore) * score_FI
            score_FI += 1

        self.population.sort(key=lambda x: x.score)   # 最后按照总得分排序    从小到大排序

    def update_population(self):

        for value in self.population:
            value.reciprocal_score = 1 / value.score
            self.total_reciprocal_score += value.reciprocal_score

        # update concentration
        for index,value in enumerate(self.population):
            concentration_ = 0  # 重置 concentration_ 为零
            for next_value in self.population:
                # if value != next_value:
                # 使用 zip() 函数一次迭代两个 CHS 列表的对应元素
                concentration_ += sum(x == y for x, y in zip(value.CHS, next_value.CHS))
                # print(f'{index}  {value.CHS}   {next_value.CHS}    {concentration_}')

            # 比较阈值来判断是否相似，相似取1 不相似取0
            if concentration_ / self.size <= self.threshold_Antibody_similarity:
                value.unconcentration += 1

            value.unconcentration = value.unconcentration / len(value.CHS)
            self.total_unconcentration += value.unconcentration

        # update fecundity
        for value in self.population:
            if self.total_unconcentration != 0:     #判断是否为0
                value.fecundity = self.fecundity_coefficient * value.reciprocal_score / self.total_reciprocal_score \
                                    + (1 - self.fecundity_coefficient) * value.unconcentration / self.total_unconcentration 
            else:
                value.fecundity = self.fecundity_coefficient * value.reciprocal_score / self.total_reciprocal_score   
            self.total_weight += value.fecundity     
            # print(value.fecundity, value.score)

        for value in self.population:
            self.fecundity_weights.append(value.fecundity / self.total_weight)

    def clone_chs(self):
        # 精英选择策略
        a = int(self.p_elite * self.size)
        self.clone_population.extend(self.population[:a])
        # 轮盘赌策略
        selected_chs_list = random.choices(self.population, weights=self.fecundity_weights, k= self.clone_size - a)
        self.clone_population.extend(selected_chs_list)

    # 计策：先全部变异 再 全部两两一起交叉
    def operate(self, generation: int):
        # 更新 自适应交叉变异因子 和循环轮次有关
        self.pm = max(self.pm_min, self.pm_max * math.cos(math.pi / 2 * (1 - generation / self.gene_size)))
        self.pc = max(self.pc_min, self.pc_max * math.cos(math.pi / 2 * (generation / self.gene_size)))

        operated_population = []        
        while(len(operated_population) < len(self.clone_population)):    

            # 随机选择两个个体（pop1 和 pop2）作为父代。这两个父代个体将被用于进行交叉和变异操作，生成新的子代个体。这种随机选择的方法有助于维持种群的多样性
            pop1,pop2=random.choice(self.clone_population),random.choice(self.clone_population)
            offspring_CHS1:Chromosome = Chromosome(pop1.CHS, self.args,J_site= self.J_site) 
            offspring_CHS2:Chromosome = Chromosome(pop2.CHS, self.args,J_site= self.J_site) 

            #  交叉
            if random.random() < self.pc:         # Crossover rate
                if random.random() < 0.5:
                    p1, p2 = POX(offspring_CHS1.CHS[0: self.half_length], offspring_CHS2.CHS[0: self.half_length], self.args.n)
                else:
                    p1, p2 = Job_Crossover(offspring_CHS1.CHS[0: self.half_length], offspring_CHS2.CHS[0: self.half_length], self.args.n)
                p1_, p2_ = Crossover_Machine(CHS1= offspring_CHS1.CHS[self.half_length: ], CHS2= offspring_CHS2.CHS[self.half_length: ])   # machine cross

                offspring_CHS1.CHS = p1 + p1_
                offspring_CHS2.CHS = p2 + p2_

            # 变异1
            if random.random() < self.pm:  # whether offspring_CHS1 mutation
                if random.random() < 0.5:
                    p11 = swap_mutation(offspring_CHS1.CHS[0:self.half_length])
                else:
                    p11 = MB_mutation(offspring_CHS1.CHS[0:self.half_length], pm= self.pm)
                p12 = Mutation_Machine(offspring_CHS1.CHS[self.half_length:], Processing_Time= self.args.PT, J_site= self.J_site)
                p11.extend(p12)
                offspring_CHS1.CHS = p11
            # 变异2
            if random.random() < self.pm:  # whether offspring_CHS2 mutation
                if random.random() < 0.5:
                    p21 = swap_mutation(offspring_CHS2.CHS[0:self.half_length])
                else:
                    p21 = MB_mutation(offspring_CHS2.CHS[0:self.half_length], pm= self.pm)
                p22 = Mutation_Machine(offspring_CHS2.CHS[self.half_length:], Processing_Time= self.args.PT, J_site= self.J_site)
                p21.extend(p22)
                offspring_CHS2.CHS = p21

            operated_population.extend([offspring_CHS1, offspring_CHS2])
        return operated_population
        

class Algorithm:
    def __init__(self, args) -> None:
        self.args = args
        self.pop_size = args.pop_size
        self.gene_size = args.gene_size         # 算法循环gene_size次退出
        self.cur_gene = 0
        self.continue_best_times = 0

        self.p_GS =args.p_GS
        self.p_LS = args.p_LS
        self.p_RS = args.p_RS
        self.p_pop_population = args.p_pop_population
        self.max_best_times = args.max_best_times

        self.Population = []
        self.chs_setup()
        self.best_chs = None
        

    def chs_setup(self):
        self.ms_list_length = []
        self.J_site = []
        for i in range(args.n):             # 第i个工件 
            for j in range(args.total_ni[i]):     # 第j个工序
                self.ms_list_length.append(len(args.MT[i][j]))  # 用于表示机器选择的列表。每个元素表示相应机器的候选数量。
                self.J_site.append((i ,j))                               # 方便查找

        self.initial_os_list = []
        #更改 n=8 ni = [4, 4, 4] 有八个工件，每个工件有4个步骤 长度为24 存储self.initial_os_list
        # 值是没打乱的模样：[0,0,0,0,1,1,1,1,2,2,2,2......]
        temp = 0
        for i in range(args.n):
            abs = [i] * args.ni[temp]
            self.initial_os_list.extend(abs)
            if(i == sum(args.job_num_list[: temp+1]) - 1):
                temp += 1

        self.half_length = len(self.initial_os_list)  

    def random_initial(self, size: int):
        random_population = []
        for i in range(size):
            # self.initial_os_list.copy() 是对 self.initial_os_list 的浅拷贝，
            #如果你不使用 copy()，那么它们将引用相同的列表对象
            random_os_list = self.initial_os_list.copy()
            random.shuffle(random_os_list)
            # print(random_os_list,'\n',self.initial_os_list)
            ms = []

            for i in range(self.half_length):
                ms.append(random.randint(0, self.ms_list_length[i] - 1))
            self.CHS_list = random_os_list + ms   

            # print("random initial chs is : ", self.CHS_list[:self.half_length],'\n',self.CHS_list[self.half_length:])
            self.pop = Chromosome(CHS= self.CHS_list, args= self.args, J_site= self.J_site)
            
            random_population.append(self.pop)
        return random_population

    def GS_initial(self):
        global_population = []
        for i in range(int(self.p_GS *self.pop_size)):
            Machine_load =[0 ] *self.args.m
            Job_op =[0 ] *self.args.n

            random_os_list = self.initial_os_list.copy()
            random.shuffle(random_os_list)
            ms = [0] * self.half_length
            #       MLoad_op 是一个列表 用来选择
            for pi in random_os_list:
                MLoad_op = []
                for _ in range (len(self.args.MT[pi][Job_op[pi]])):           # _表示 这个列表的数量序号 通过遍历,要取出所有可能的加工时间 选择最小的

                    MLoad_op.append(self.args.PT[pi][Job_op[pi]][_] + Machine_load[self.args.MT[pi][Job_op[pi]][_] -1 ]) 
                # m_idx = MLoad_op.index(min(MLoad_op))       #找到最小值的下标index
                min_value = min(MLoad_op)
                indices_of_min_values = [index for index, value in enumerate(MLoad_op) if value == min_value]
                m_idx = random.choice(indices_of_min_values)

                ms[self.J_site.index((pi,Job_op[pi]))] = m_idx
                Machine_load[m_idx] =min(MLoad_op)
                Job_op[pi]+=1
            
            self.CHS_list = random_os_list + ms 
            self.pop = Chromosome(CHS= self.CHS_list, args= self.args, J_site= self.J_site)
            global_population.append(self.pop)
        return global_population

    def LS_initial(self):
        local_population = []
        for i in range(self.pop_size-int(self.p_GS *self.pop_size)-int(self.p_RS *self.pop_size)):
            random_os_list = self.initial_os_list.copy()
            random.shuffle(random_os_list)
 
            ms =[]
            for PTi in self.args.PT:
                for PTj in PTi:
                    # ms.append(PTj.index(min(PTj)))#min() 函数只返回第一个最小值的索引
                    min_value = min(PTj)
                    indices_of_min_values = [index for index, value in enumerate(PTj) if value == min_value]
                    random_index = random.choice(indices_of_min_values)
                    ms.append(random_index)

            self.CHS_list = random_os_list + ms 
            self.pop = Chromosome(CHS= self.CHS_list, args= self.args, J_site= self.J_site)
            local_population.append(self.pop)
        return local_population

    def initial(self):       # all random initial 
        random_population = self.random_initial(size= int (self.pop_size * self.p_RS))  # random Initial
        global_population = self.GS_initial()  # Globel Initial
        local_population = self.LS_initial()  # Local Initial
        self.Population = random_population + global_population + local_population
        self.Undivided_population = Population(self.Population, self.args, self.J_site)
        self.Undivided_population.caculate_score()

    # 判断是否达到最优条件 是否退出
    # true 代表结束循环   fasle 代表没结束
    def circle_over(self):
        return (self.cur_gene >= self.gene_size or self.continue_best_times >= self.max_best_times)

    # 先计算得分 
    #    按照亲和度 划分一半好种群 一半坏种群  
    # 计算种群 抗原之间的浓度
    # 在好和坏种群之间进行选择 克隆 自适应变异 交叉
    def divide_population(self):
        self.good_population = Population(self.Undivided_population.population[:int(self.Undivided_population.size/2)], self.args, self.J_site)
        self.bad_population = Population(self.Undivided_population.population[int(self.Undivided_population.size/2):], self.args, self.J_site)           # 切片里面的数必须是整数integer 用给int

        self.good_population.update_population()
        self.good_population.clone_chs()
        self.bad_population.update_population()
        self.bad_population.clone_chs()

        good_offspring_pop = self.good_population.operate(generation= self.cur_gene)
        bad_offspring_pop = self.bad_population.operate(generation= self.cur_gene)

        merged_population = Population(population_= good_offspring_pop + bad_offspring_pop, args= self.args, J_site= self.J_site)
        merged_population.caculate_score()

        # print(f'max_score   {merged_population.population[0].score}   fitness {merged_population.population[0].fitness[0]}   goal  {merged_population.population[0].goal}')
        # 为判断是否结束 更新参数 self.continue_best_times
        if(self.best_chs):
            # self.best_chs = max(self.best_chs, merged_population.population[0], key= lambda x: x.score)       
            # merged_population.population按照score 由小到大排序
            if (self.best_chs.score <= merged_population.population[0].score and self.best_chs.goal <= merged_population.population[0].goal):
                self.continue_best_times += 1
            else:
                self.continue_best_times = 0
                self.best_chs = merged_population.population[0]
        else:
            self.best_chs = merged_population.population[0]

        self.cur_gene += 1

        # for i in merged_population.population:
        #     print(f'before pop: {i.decode_judge}   {i.fitness[0]}  {i.score}   {len(merged_population.population)}')
        # 计算要弹出的元素个数  切片方法弹出
        pop_count = int(len(merged_population.population) * self.p_pop_population)
        merged_population.population = merged_population.population[:-pop_count]

        random_new_population = self.random_initial(size= pop_count)
        merged_population.population.extend(random_new_population)

        merged_population.caculate_score()
        
        self.Undivided_population = merged_population
    
if __name__ == "__main__":

    n, m, job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT = get_instance(); 
    args = get_args(n, m, job_num_list , n_name, ni, total_ni, CMT, CMT_M, MT, PT)
    A = Algorithm(args= args)
    A.initial()
    best_chs_list = []
    # Python中，取反操作符是 not 而不是 ! 。 Python 解释器会报错，因为它不识别 ! 作为取反操作符。
    while not (A.circle_over()):
        A.divide_population()
        best_chs_list.append(A.best_chs)
        # print(f'{A.best_chs.score}  {A.best_chs.C_max}   {A.best_chs.goal}')

    best_CMAX = [best.C_max for best in best_chs_list]
    best_GOAL = [best.goal for best in best_chs_list]
    best_LOAD = [best.load for best in best_chs_list]
    best_CMT = [best.total_CMT for best in best_chs_list]


    Gantt_chart(A.best_chs, m ,n)
    print(A.best_chs.CHS)
    print(best_CMAX)
    print(best_LOAD)
    print(best_CMT)
    print(best_GOAL)


        