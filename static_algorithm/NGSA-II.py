from FJSP_ENV import *
import copy
from utils import *

class NGSAII:
    def __init__(self, args) -> None:
        self.args = args

        self.pop_size = args.pop_size
        self.gene_size = args.gene_size         # 算法循环gene_size次退出
        self.cur_gene = 0
        self.continue_best_times = 0
        self.pc = args.pc
        self.pm = args.pm

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
        #更改 n=8 ni = [4, 4, 4] 有八个工件,每个工件有4个步骤 长度为24 存储self.initial_os_list
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
            # self.initial_os_list.copy() 是对 self.initial_os_list 的浅拷贝,
            #如果你不使用 copy(),那么它们将引用相同的列表对象
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
    
    
    # 计策：先全部变异 再 全部两两一起交叉
    def operate(self):

        operated_population = []      
        while(len(operated_population) < self.pop_size):    

            # 随机选择两个个体（pop1 和 pop2）作为父代。这两个父代个体将被用于进行交叉和变异操作,生成新的子代个体。这种随机选择的方法有助于维持种群的多样性
            pop1,pop2=random.choice(self.Population),random.choice(self.Population)
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
        
    """按照goal的大小来排序"""
    def ngsaii_main(self):
        # 初始化
        self.initial()
        for i in range(self.gene_size):
            self.offspring_pop = self.operate()
            Total_pop = self.Population + self.offspring_pop
            # print(Total_pop)

            for element in Total_pop:
                element.FJSP_setup()
                element.decode()
            NDSet= fast_non_dominated_sort(Total_pop)    # all nondominated set fronts of R_pop

            j=0
            self.Population=[]
            while len(self.Population)+len(NDSet[j])<=self.pop_size:   # until parent population is filled
                self.Population.extend(NDSet[j])
                j+=1
            if len(self.Population)<self.pop_size:
                Ds=crowding_distance(copy.copy(NDSet[j]))       # calcalted crowding-distance   快速非支配排序  按照dsistance的大小排序
                k = 0                                           # F1、F2前端的所有都会进入下一轮筛选。而F3中会有部分被淘汰掉
                while len(self.Population) < self.pop_size:
                    self.Population.append(NDSet[j][Ds[k]])
                    k += 1

            """至关重要,重新更新种群,防止再次openrate,cur_op超过4,导致J_site 报错 ValueError: (2, 4) is not in list"""
            if i != self.gene_size - 1:
                for element in self.Population:
                    self.Population.append(Chromosome(element.CHS, self.args,J_site= self.J_site) )
                    self.Population.pop(0)  #进来一个，弹出一个

        result_pop = fast_non_dominated_sort(self.Population)[0][0]       #   处于第一序列第一个的解集
        return result_pop

if __name__ == "__main__":

    # n_list = [2,3,4,5,6,8]
    n_list = [3]
    n_index = 0
    max_index = len(n_list)

    while(n_index < max_index):
        change_n(n = n_list[n_index])
        n, m, job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT = get_instance(); 
        args = get_args(n, m, job_num_list , n_name, ni, total_ni, CMT, CMT_M, MT, PT)

        initial_circle = 1

        lists_best_CMAX = []
        lists_best_LOAD = []
        lists_best_TOTAL_CMT = []
        lists_best_GOAL = []
        lists_best_TIME = []

        # 重置circle
        circle = initial_circle    
        while(circle > 0):

            time_start = time.time()
            a = NGSAII(args= args) 
            
            result = a.ngsaii_main()
            lists_best_CMAX.append(result.C_max)
            lists_best_LOAD.append(result.load)
            lists_best_TOTAL_CMT.append(result.total_CMT)
            lists_best_GOAL.append(round(result.goal, ndigits= 2))
            time_end = time.time()
            lists_best_TIME.append(round(time_end - time_start, ndigits= 2))   #你想要限制小数点的位数，可以使用 round() 函数

            circle -= 1

        job_num_str =f"NGSAII_" "_".join(map(str, job_num_list)) + f"_{initial_circle}"       # 字符串拼接

        folder_path = os.path.join("data_", job_num_str )
        content = []
        content.extend([lists_best_CMAX,lists_best_LOAD,lists_best_TOTAL_CMT,lists_best_GOAL,lists_best_TIME])   # equal to result_list = [list1, list2]  and result_list.append(list1) result_list.append(list2)
        print(F"content:  {content}")
        NGSAII_generate_and_write_txt(folder_path= folder_path, file_name= "data.txt", content= content)

        n_index += 1
