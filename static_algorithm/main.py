from ga import *

if __name__ == "__main__":
    # n_list = [2,3,4,5,6,8]
    n_list = [5,6,8]
    n_index = 0
    max_index = len(n_list)

    while(n_index < max_index):
        change_n(n = n_list[n_index])
        n, m, job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT = get_instance(); 
        args = get_args(n, m, job_num_list , n_name, ni, total_ni, CMT, CMT_M, MT, PT)

        # gear: 0   有分层 有自适应因子
        # gear: 1   无分层 有自适应因子
        # gear: 2   有分层 无自适应因子
        # gear: 3   无分层 无自适应因子

        initial_circle = 50
        gear_ = [0, 1, 2, 3]
        lists_best_CMAX = [list() for _ in range(len(gear_))]
        lists_best_LOAD = [list() for _ in range(len(gear_))]
        lists_best_TOTAL_CMT = [list() for _ in range(len(gear_))]
        lists_best_GOAL = [list() for _ in range(len(gear_))]
        lists_best_TIME = [list() for _ in range(len(gear_))]
        for index, gear in enumerate(gear_):
            # 重置circle
            circle = initial_circle    
            while(circle > 0):
                time_start = time.time()
                A = Algorithm(args= args)
                A.initial()
                while not (A.circle_over()):
                    if(gear == 0 or gear == 2):
                        A.divide_population(gear= gear)
                    elif(gear == 1 or gear == 3):
                        A.divide_population_1(gear= gear)
                lists_best_CMAX[index].append(A.best_chs.C_max)
                lists_best_LOAD[index].append(A.best_chs.load)
                lists_best_TOTAL_CMT[index].append(A.best_chs.total_CMT)
                lists_best_GOAL[index].append(round(A.best_chs.goal, ndigits= 2))
                time_end = time.time()
                lists_best_TIME[index].append(round(time_end - time_start, ndigits= 2))   #你想要限制小数点的位数，可以使用 round() 函数

                circle -= 1

        job_num_str = "_".join(map(str, job_num_list)) + f"_{initial_circle}"       # 字符串拼接

        folder_path = os.path.join("data_", job_num_str )
        content = []
        content.extend([lists_best_CMAX,lists_best_LOAD,lists_best_TOTAL_CMT,lists_best_GOAL,lists_best_TIME])   # equal to result_list = [list1, list2]  and result_list.append(list1) result_list.append(list2)
        # print(content)
        generate_and_write_txt(folder_path= folder_path, file_name= "data.txt", content= content)

        n_index += 1
    
    