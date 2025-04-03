import argparse

def get_args(n, m,job_num_list, n_name, ni,total_ni, CMT, CMT_M, MT, PT):
    parser = argparse.ArgumentParser()
    # params for FJSPF:
    parser.add_argument('--n', default=n, type=int, help='job number')
    parser.add_argument('--m', default=m, type=int, help='Machine number')
    parser.add_argument('--job_num_list', default= job_num_list, type= list)
    parser.add_argument('--n_name', default=n_name, type=list, help='Operation number of each job')
    parser.add_argument('--ni', default=ni, type=list, help='Operation number of each job')
    parser.add_argument('--total_ni', default= total_ni, type= list)
    parser.add_argument('--MT', default=MT, type=list, help='processing machine of operations')
    parser.add_argument('--PT', default=PT, type=list, help='fuzzy processing machine of operations')
    parser.add_argument('--CMT',default= CMT, type= list)
    parser.add_argument('--CMT_M', default=CMT_M, type= list)


    # Params for Algorithms
    parser.add_argument('--pop_size', default= 120, type=int, help='Population size of the genetic algorithm')         # 100
    parser.add_argument('--gene_size', default= 1, type=int, help='generation size of the genetic algorithm')      #100
    parser.add_argument('--pc_max', default=0.8, type=float, help='Crossover rate')                                 #0.8
    parser.add_argument('--pm_max', default=0.05, type=float, help='mutation rate')                                 #0.2
    parser.add_argument('--pc_min', default=0.7, type=float, help='Crossover rate')                                 # 0.7
    parser.add_argument('--pm_min', default=0.01, type=float, help='mutation rate')                                  # 0.1
    parser.add_argument('--pc', default=0.8, type=float, help='Crossover rate')                                 # 0.7
    parser.add_argument('--pm', default=0.05, type=float, help='mutation rate')                                  # 0.1

    parser.add_argument('--p_GS', default=0.2, type=float, help='globel initial rate')                              # 0.2
    parser.add_argument('--p_LS', default=0.2, type=float, help='Local initial rate')   #percent of three init ways
    parser.add_argument('--p_RS', default=0.6, type=float, help='random initial rate')


    parser.add_argument('--p_NDscore', default= 0.2, type= int, help= 'Scores obtained by non-dominant sorting in both non-dominant and goal ways')
    parser.add_argument('--threshold_Antibody_similarity', default= 0.7, type= int, help= 'A threshold used to determine whether antibodies are similar to each other')
    parser.add_argument('--fecundity_coefficient', default= 0.5, type= int, help='in front of affinity, Weigh the coefficient between concentration and affinity')
    parser.add_argument('--p_elite', default=0.2, type=int, help='percent of elite choice')
    parser.add_argument('--clone_size', default= 60, type=int, help='total size of clone number')
    parser.add_argument('--p_pop_population', default= 0.1, type= float, help = 'The percentage that pops up when refreshing the population')
    parser.add_argument('--max_best_times', default= 1000, type= int, help='The maximum number of times that the optimal solution can be maintained unchanged')

    parser.add_argument('--fitness_0', default= 0.8, type= float, help='The proportion of the first objective function in the fitness function')
    parser.add_argument('--fitness_1', default= 0.1, type= float, help='The proportion of the second objective function in the fitness function')
    parser.add_argument('--fitness_2', default= 0.1, type= float, help='The proportion of the third objective function in the fitness function')
    args = parser.parse_args()
    return args
