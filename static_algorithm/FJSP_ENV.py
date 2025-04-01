from instance import *
from Params import *
from utils import *

class Job:
    def __init__(self, index: int, name: str,job_num_index : int, proc_time: list, proc_machine: list) -> None:
        """
        index: job's index : 1 2 3 4 5
        proc_machine(2 dimention): the machine index corresponding to the job: [[4, 6, 7], [1, 5, 7, 8], [2, 7, 8]]   
        proc_time(2 dimention): the time corresjob_num_indexponding to the job: [[25, 21, 28], [65, 70, 70, 75], [35, 55, 40]]
        """
        self.start = []
        self.end = []
        self.proc_time = proc_time
        self.proc_machine = proc_machine
        self.index = index
        self.name = name
        self.job_num_index = job_num_index
        self.cur_op = 0
        self.endtime = 0        # the last endtime in the situation now
        self.mac_list = []      # The serial number list of the operating machine on the workpiece
         
    def update(self, start_time: int, end_time: int):
        self.start.append(start_time)
        self.end.append(end_time)
        self.cur_op += 1
        self.mac_list.append(self.cur_proc_machine)
        self.endtime = end_time

    def get_next_info(self, machine_index: int):
        """
        machine_index : which index choose to use  for example:(we can choose 0/1/2 in the list[4, 6, 7] not 4/6/7)
        return next time's proc_time and the proc_machine
        """        
        self.cur_proc_time = self.proc_time[self.cur_op][machine_index]
        self.cur_proc_machine = self.proc_machine[self.cur_op][machine_index]

        return self.cur_proc_time, self.cur_proc_machine


class Machine:
    def __init__(self, index: int) -> None:
        """
        index: machine's index : 1 2 3 4 5
        """
        # 工作总时间 包括换模
        self.start = []
        self.end = []

        # 换模时间
        self.CM_start = []
        self.CM_end = []

        self.index = index
        self.job_name_list = []      # The serial kind list of the job on the operating machine
    
    def update(self, start_time: int, end_time: int, job_num_index: int):
        self.start.append(start_time)
        self.end.append(end_time)

        # 每次更新后要排序
        self.start = sorted(self.start)
        self.end =sorted(self.end)
        self.job_name_list.append(job_num_index)

    def find_start_time(self, op_time: int, job_endtime: int):
        """
        we donot know the job's start time if we only use job class to classify
        but if we use machine for assistance ,like this method, it can be easy
        """
        # This machine has not been used, there are two possibilities, first, the workpiece has just started processing (0), 
        # second, the workpiece has been processed several rounds, this time it is the machine's turn (job end time).
        if self.end == []:
            return max(0, job_endtime)    

        else:# think about the jobs Front insertion
            if job_endtime > self.end[-1]:
                return job_endtime
            else:
                s = len(self.end) - 2   # from the last but one
                start_ = self.end[-1]
                while s >= 0:
                    if job_endtime + op_time > self.start[s + 1]:
                        break
                    if  self.end[s] > job_endtime and self.end[s] + op_time <= self.start[s + 1]:
                        start_ = self.end[s]
                    elif self.end[s] < job_endtime and self.end[s] + op_time <= self.start[s + 1]:
                        start_ = job_endtime
                    s -= 1

                return start_
      
# 一个染色体对应的一种情况
class Chromosome:
    def __init__(self, CHS: list, args, J_site: list) -> None:
        self.CHS = CHS
        self.J_site = J_site

        self.n = args.n
        self.m = args.m
        self.n_name = args.n_name
        self.ni = args.ni
        self.CMT = args.CMT
        self.CMT_M = args.CMT_M
        self.PT = args.PT
        self.MT = args.MT
        self.job_num_list = args.job_num_list
        self.fitness_0 = args.fitness_0
        self.fitness_1 = args.fitness_1
        self.fitness_2 = args.fitness_2
        # print(self.fitness_0, self.fitness_1, self.fitness_2)
        
    # 每次decode 之前一定要先setup
    
    def FJSP_setup(self):
        # to store all the jobs and machines       
        self.jobs = []
        self.machines = []

        # 抗原（染色体）得分
        self.goal = 0
        self.score = 1
        self.reciprocal_score = 0
        # 抗原非浓度大小
        self.unconcentration = 0
        # 抗原繁殖力大小
        self.fecundity = 0

        self.decode_judge = False
        
        self.CHS_half_length = int(len(self.CHS) / 2)

        self.C_max = 0      #makespan
        self.total_CMT = 0
        self.load=0         # Total load of machines
        self.max_EndM=None  # the last end machine
        self.mac_load=[0]*self.m    # load of each machine  快速init list 的方法
        self.max_load = 0           # max_load of machine
        self.names_list = []
        self.job_num_index_list = []

        for k, v in self.n_name.items():
            for i in range(1, v + 1):
                self.names_list.append(f"{k}_{i}")

        t = 0
        for i in self.job_num_list:
            self.job_num_index_list.extend([t] * i)
            t += 1

        for i in range(self.n):
            ji = Job(i,name= self.names_list[i],job_num_index=self.job_num_index_list[i], proc_time= self.PT[i],proc_machine= self.MT[i])
            self.jobs.append(ji)

        for i in range(self.m):
            mi = Machine(i)
            self.machines.append(mi)

    def get_CMT_time(self, job_index: int, mac_index: int):
        change_time = int(self.CMT[job_index][mac_index - self.CMT_M[0]])
        return change_time

    # decode of chs[i]
    def solution(self, job_index: int, machine_index: int):
        ji:Job = self.jobs[job_index]   #Type Hinting
        cur_pro_time, mac_index = ji.get_next_info(machine_index)        #mac_index is the real one, machine_index is not 

        mi:Machine = self.machines[mac_index - 1]       ## mac_index is the real one,因为索引的缘故，从1 开始 所以要减去 1 [1,2,3] - 1 = [0, 1, 2]

        start_time = mi.find_start_time(cur_pro_time, ji.endtime)
        endtime = start_time + cur_pro_time

        # 换模 时间的计算
        # 判断换模时间 mac_index 是实际的数 不用-1
        if (mac_index) in self.CMT_M:
            CM_time = self.get_CMT_time(job_index= ji.job_num_index, mac_index= mac_index)
            # print(f'cm_time: {CM_time}')
            if(len(mi.job_name_list) > 0):              #machine 前面有job来过
                if(mi.job_name_list[-1] != ji.job_num_index):
                    if(start_time - mi.end[-1] < CM_time):
                        start_time = start_time + CM_time - (start_time - mi.end[-1])
                        endtime = start_time + cur_pro_time                        
                    mi.CM_start.append(mi.end[-1])
                    mi.CM_end.append(mi.end[-1] + CM_time)
                    # 解决方法 在machine start end中也update cmt 让他参与排序
                    mi.update(mi.end[-1], mi.end[-1] + CM_time, ji.job_num_index)
                    #  如果前后job_num_index不一致  不是job_name 换模时间增加 
                    self.total_CMT += CM_time

            else:
                if(start_time < CM_time):
                    start_time = CM_time
                    endtime = start_time + cur_pro_time  
                mi.CM_start.append(0)
                mi.CM_end.append(CM_time) 
                self.total_CMT += CM_time                  

        ji.update(start_time, endtime)
        mi.update(start_time, endtime, ji.job_num_index)

        self.mac_load[mi.index] += cur_pro_time
        self.load += cur_pro_time
        if endtime > self.C_max:
            self.max_EndM = mac_index
            self.C_max = endtime
        self.max_load = max(self.mac_load)  #update max_load of machine
    
    def decode(self):
        for i in range(self.CHS_half_length):
            job_index = self.CHS[i]
            O_num = self.jobs[job_index].cur_op
            machine_index = self.J_site.index((job_index, O_num))  
            mac_index = self.CHS[machine_index + self.CHS_half_length]

            self.solution(job_index= job_index, machine_index= mac_index)
        self.fitness = list([self.C_max,self.load, self.total_CMT]) 
        self.goal = self.fitness_0 * self.fitness[0] + self.fitness_1 * self.fitness[1] + self.fitness_2 * self.fitness[2]
        self.decode_judge = True
    
# 初始化有问题 全局或者局部有一个有问题
class Test_Algorithm:
    def __init__(self, args) -> None:
        self.args = args

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

    def random_initial(self):
        # self.initial_os_list.copy() 是对 self.initial_os_list 的浅拷贝，
        #如果你不使用 copy()，那么它们将引用相同的列表对象
        random_os_list = self.initial_os_list.copy()
        random.shuffle(random_os_list)
        # print(random_os_list,'\n',self.initial_os_list)
        ms = []

        for i in range(self.half_length):
            ms.append(random.randint(0, self.ms_list_length[i] - 1))
        self.CHS_list = random_os_list + ms   

        print("random initial chs is : ", self.CHS_list[:self.half_length],'\n',self.CHS_list[self.half_length:])
        self.CHS = Chromosome(CHS= self.CHS_list, args= self.args, J_site= self.J_site)

if __name__ == "__main__":
    n, m, job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT = get_instance(); 
    args = get_args(n, m, job_num_list , n_name, ni, total_ni, CMT, CMT_M, MT, PT)

    # print(f"n: {n}\n m : {m}\n job_num_list: {job_num_list} \n "
    #     f"n_name : {n_name} \n ni: {ni}\n total_ni: {total_ni}\n "
    #     f"CMT: {CMT}\n CMT_M: {CMT_M} \n MT: {MT} \n PT: {PT}")
    # Al = Test_Algorithm(args= args)
    # Al.random_initial()

    # Al.CHS.decode()
    # Gantt_chart(Al.CHS, m ,n)

#     list2 = [2, 6, 0, 7, 0, 8, 7, 3, 4, 8, 3, 4, 8, 1, 5, 6, 1, 2, 1, 4, 5, 8, 3, 2, 1, 5, 7, 7, 6, 0, 0, 2, 5, 4, 3, 6] + \
#  [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    bl = Test_Algorithm(args= args)
    
    list3 = [7, 0, 2, 3, 0, 2, 7, 6, 5, 1, 0, 2, 3, 8, 6, 5, 6, 7, 8, 5, 7, 4, 3, 1, 0, 6, 2, 8, 8, 4, 3, 4, 1, 1, 4, 5] \
    + [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 1, 0, 1, 2, 0]
    list113 = [8, 5, 5, 8, 5, 4, 4, 8, 0, 6, 6, 8, 1, 3, 0, 4, 3, 2, 1, 0, 7, 2, 6, 6, 3, 5, 2, 1, 4, 7, 1, 3, 0, 7, 7, 2, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 0, 0, 1, 2, 1, 0, 0, 1, 0]

    chs_test = Chromosome(CHS= list113, args= args, J_site= bl.J_site)
    # 更改之后在每次 decode 之前都要setup一次
    chs_test.FJSP_setup()
    chs_test.decode()
    Gantt_chart(chs_test, m ,n)
    chs_test.FJSP_setup()
    chs_test.decode()
    for i , j , k in zip(chs_test.machines[4].end,chs_test.machines[4].start, chs_test.machines[4].job_name_list):
        print( j,"  ",i,"  ",k)
    Gantt_chart(chs_test, m ,n)

        
        