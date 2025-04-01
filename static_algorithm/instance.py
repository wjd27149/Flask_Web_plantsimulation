import numpy as np
import os

def get_instance():
    '''
    :param file: Instance of FJSP
    example:
    n : {"300" : 3, "500" : 3, "800" : 2}  300是产品型号 3是该产品需要生产的数量
    m= 7, 7 machines
     job_num_list: [1, 1, 1]   每种零件（job）有多少数量 num_list
    PT=[[   # jobs 1
            [1,2],  # operation 1:  [1,2] indicatas for the first and second available machine's processing time
            [1,3]],
        [   # jobs 2
            [2,3],
            [3,2],]]
    MT=[[   # jobs 1
            [1,3], # operation 1:  [1,2] indicatas for the first and second available machine's index
            [3,2]],
        [   # jobs 2
            [1,2],
            [2,3]]]
    CMT: [['6', '6', '-'], ['8', '8', '-'], ['8', '8', '12']] 在CMT_M中对应换模需要的时间
    CMT_M: [5, 6, 7]  对应CMT中换模机器的序号
    ni=[2,2] # the first job_type has 2 operations, the second job has 2 operations
    total_ni = [4, 4, 4, 4, 4, 4, 4, 4]     # all the job has 4 operations
    '''
    #读取原始数据
    contents_pro = []
    contents_mac = []
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建完整的文件路径
    file_path_pro = os.path.join(script_dir, 'products.txt')
    file_path_mac = os.path.join(script_dir, "machine.txt")
    with open(file_path_pro,"r",encoding="utf-8") as f:
        # 省略第一行
        string = f.readline()
        string = f.readlines()
        for item in string:
            # strip() 处理的时候，如果不带参数，默认是清除两边的空白符，例如：/n, /r, /t, ‘ ‘)
            contents_pro.append(item.strip().split(" "))
    f.close()

    with open(file_path_mac,"r",encoding="utf-8") as f1:
        # 省略第一行
        string = f1.readline()
        string = f1.readlines()
        for item in string:
            contents_mac.append(item.strip().split(" "))
    f1.close()

    n = 0
    job_num_list = []
    n_name = {}
    m = len(contents_mac[0])    
    ni = []
    total_ni = []
    CMT = []
    CMT_M = [5, 6, 7]

    PT = []
    MT = []
    PT_job = []
    MT_job = []
    # t t_index 用于索引ni 是否选了四个切片进入 MT PT
    t = 0
    t_index = 0

    for item in contents_pro:
        ni.append(int(item[2]))
        n_name[item[0]] = int(item[1])
        n += int(item[1])
        CMT.append(item[3: ])

    job_num_list = list(n_name.values())
    for item in contents_mac:
        MT_ = []
        PT_ = []

        for index, value in enumerate(item):
            if value != "-":
                PT_.append(int(value))
                MT_.append(index + 1)
        PT_job.append(PT_)
        MT_job.append(MT_)
        t += 1
        if (t == ni[t_index]):
            MT.extend([MT_job] * job_num_list[t_index])
            PT.extend([PT_job] * job_num_list[t_index])
            t_index += 1
            t = 0
            PT_job = []
            MT_job = []

    for index, value in enumerate(ni):
        total_ni.extend([value] * job_num_list[index])

    return n, m,job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT

if __name__ == "__main__":

    n, m,job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT = get_instance(); 
    result = []

    for key, value in n_name.items():
        prefix = key
        for i in range(1, value + 1):
            result.append(f"{prefix}_{i}")
    print(result)
    print(list(n_name.values()))
    print(f"n: {n}\n m : {m}\n job_num_list: {job_num_list} \n "
        f"n_name : {n_name} \n ni: {ni}\n total_ni: {total_ni}\n "
        f"CMT: {CMT}\n CMT_M: {CMT_M} \n MT: {MT} \n PT: {PT}")

