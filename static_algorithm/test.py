# n = 8
# m = 7
# n_name = {'300': 3, '500': 3, '800': 2}
# ni = [3, 4, 5]


# os_list = []
# temp_list : list = list(n_name.values())
# #更改 n=8 ni = [4, 4, 4] 有八个工件，每个工件有4个步骤 长度为24
# temp = 0
# for i in range(n):
#     abs = [i] * ni[temp]
#     os_list .extend(abs)
#     if(i == sum(temp_list[: temp+1]) - 1):
#         temp += 1

# print(os_list)


# li = []
# for i in range(len(li)):
#     print(i)

# a1 = [2, 0, 1, 0, 2, 0, 1, 0, 2, 2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 2, 0]
# a2 = [1, 2, 1, 2, 1, 0, 0, 2, 0, 2, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 0] 
# concentration_ = 0
# concentration_ += sum(x == y for x, y in zip(a1, a2))
# print(concentration_)
# #sum_of_a = sum(chs.a for chs in chs_list)

# list1 = [0, 2, 5, 0, 5, 0, 5, 1, 4, 3, 4, 3, 1, 3, 2, 1, 5, 2, 0, 2, 1, 4, 4, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 2, 0]
# from collections import Counter

# # 给定列表
# list1 = [0, 2, 5, 0, 5, 0, 5, 1, 4, 3, 4, 3, 1, 3, 2, 1, 5, 2, 0, 2, 1, 4, 4, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 2, 0]

# # 使用 Counter 计数
# count_dict1 = Counter(list1[0:int(len(list1)/2)])
# count_dict2 = Counter(list1[int(len(list1) / 2) : ])

# # 输出每个数字的个数
# for num, count in count_dict1.items():
#     print(f"Number {num}: {count}")

# # 输出每个数字的个数
# for num, count in count_dict2.items():
#     print(f"Number {num}: {count}")

# # 有问题染色体 random 生成
# list2 =  [5, 0, 4, 1, 0, 3, 7, 2, 8, 6, 6, 2, 6, 7, 7, 4, 3, 4, 6, 1, 4, 3, 7, 5, 1, 8, 8, 1, 5, 2, 3, 8, 0, 2, 0, 5] \
#  + [1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 2, 1, 1, 0, 1, 1, 1, 0, 1, 1]

# lists_best_CMAX = [list() for _ in range(3)]
# print(lists_best_CMAX)
# list1 = [[115, 120, 116, 129, 123, 129, 117, 129, 115, 129], [123, 129, 123, 123, 129, 129, 123, 115, 123, 129], [112, 129, 123, 116, 120, 129, 120, 129, 129, 117], [123, 117, 118, 123, 129, 122, 129, 129, 129, 129]]
# list2 = [[113.5, 117.0, 114.19999999999999, 119.3, 117.6, 119.3, 115.39999999999999, 119.3, 113.5, 119.3], [117.6, 121.3, 117.6, 117.6, 120.8, 121.3, 117.6, 113.5, 117.6, 119.3], [112.89999999999999, 119.3, 117.6, 114.19999999999999, 117.0, 119.3, 115.5, 119.3, 120.8, 115.39999999999999], [117.6, 114.89999999999999, 116.1, 117.6, 121.3, 118.89999999999999, 119.3, 119.3, 119.3, 119.3]]
# list3 = [[7.64, 7.25, 7.2, 7.08, 7.09, 7.26, 7.13, 7.31, 8.14, 7.14], [2.98, 2.91, 2.97, 2.98, 2.96, 2.95, 2.93, 3.17, 3.05, 3.54], [7.96, 7.73, 7.22, 7.25, 7.41, 7.15, 7.81, 7.35, 9.78, 10.23], [3.01, 3.08, 3.33, 4.03, 3.97, 3.85, 3.7, 3.81, 3.67, 3.72]]

# lists = [list1, list2, list3]
# cmax = []
# goal = []
# time = []
# list_ = [list() for _ in range(3)]
# for index, i in enumerate(lists):
#     for j in i:
#         s = sum(j)
#         temp = s / len(j)
#         list_[index].append(temp)
# print(list_)

# n_list = [1,2,3]
# def change_n():
#     # 读取文件
#     index = 0

#     file_path = 'products.txt'
#     while(index < 3):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             lines = file.readlines()

#         # 修改数据
#         for i, line in enumerate(lines):
#             if i > 0:  # 跳过表头
#                 parts = line.split()
#                 parts[1] = str(n_list[index])
#                 lines[i] = ' '.join(parts) + '\n'
#         save_path = f'products_{str(n_list[index])}.txt'
#         # 保存修改后的数据
#         with open(save_path, 'w') as file:
#             file.writelines(lines)
            
#         index += 1

# change_n()

import numpy as np
import matplotlib.pyplot as plt
# 定义文件名列表
file_names = ['2_2_2_50', '3_3_3_50', '4_4_4_50', '5_5_5_50', '6_6_6_50', '8_8_8_50']

empty_list = [[] for _ in range(5)]
growth_rate = [[] for _ in range(5)]
# 循环处理每个文件
for file_name in file_names:
    # 构造文件路径
    file_path = f'data_/{file_name}/data.txt'
    
    # 读取数据
    with open(file_path, 'r') as file:
        # 跳过第一行
        next(file)
        # 读取后三行数据
        data = np.loadtxt(file, max_rows=4)
    
    # 转置数据
    transposed_data = data.T
    print(transposed_data)

    empty_list[0].append(transposed_data[0])
    empty_list[1].append(transposed_data[1])
    empty_list[2].append(transposed_data[2])
    empty_list[3].append(transposed_data[3])
    empty_list[4].append(transposed_data[4])

    growth_rate[0].append(abs(transposed_data[0][-1] - transposed_data[0][0]) / transposed_data[0][-1] * 100)
    growth_rate[1].append(abs(transposed_data[1][-1] - transposed_data[1][0]) / transposed_data[1][-1] * 100)
    growth_rate[2].append(abs(transposed_data[2][-1] - transposed_data[2][0]) / transposed_data[2][-1] * 100)
    growth_rate[3].append(abs(transposed_data[3][-1] - transposed_data[3][0]) / transposed_data[3][-1] * 100)
    growth_rate[4].append(abs(transposed_data[4][-1] - transposed_data[4][0]) / transposed_data[4][-1] * 100)


plt.rcParams['font.family'] = 'SimHei'  # 设置中文字体为黑体
# 数据
categories = ['2', '3', '4', '5', '6', '8']
data_name = ['实验组','对照组1','对照组2','对照组3']
ylabel_name = ['最大完工时间/min','机器总时间负荷/min','总换模时间/min','总目标函数','程序运行时间/s']
growth_data_name = ['优化率/%','增长率/%']
growth_ylabel_name = ['最大完工时间','机器总时间负荷','总换模时间','总目标函数','程序运行时间']
for i in range(len(empty_list)):
    values1 = empty_list[i]

    # 绘图
    fig, ax = plt.subplots()

    # 自定义连接点的形状
    marker_shapes = ['^', 'x', '*', 'd']
    line_styles = ['-', '--', ':', '-.']

    # 遍历每一列数据，绘制连接线图
    for j, col in enumerate(np.array(values1).T):
        ax.plot(categories, col, linestyle=line_styles[j],marker=marker_shapes[j], label=f'{data_name[j]}')

    # 设置标题和标签
    ax.set_xlabel('Ni/一个批次的数量')
    ax.set_ylabel(f'{ylabel_name[i]}')


    ax.legend()

    # 显示图形
    # plt.show()

for i in range(2):

    # 绘图
    fig, ax = plt.subplots()

    # 自定义连接点的形状
    marker_shapes = ['^', 'x', '*', 'd']
    line_styles = ['-', '--', ':', '-.']

    if i == 0:
        ax.plot(categories, growth_rate[0], linestyle=line_styles[0],marker=marker_shapes[0], label=f'{growth_ylabel_name[0]}')
        ax.plot(categories, growth_rate[1], linestyle=line_styles[1],marker=marker_shapes[1], label=f'{growth_ylabel_name[1]}')
        ax.plot(categories, growth_rate[2], linestyle=line_styles[2],marker=marker_shapes[2], label=f'{growth_ylabel_name[2]}')
    elif i == 1:
        ax.plot(categories, growth_rate[4], linestyle=line_styles[3],marker=marker_shapes[3], label=f'{growth_ylabel_name[-1]}')
    # 设置标题和标签
    ax.set_xlabel('Ni/一个批次的数量')
    ax.set_ylabel(f'{growth_data_name[i]}')

    ax.legend()

    # 显示图形
    plt.show() 

