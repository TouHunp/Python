from pymoo.factory import get_crossover, get_mutation, get_sampling
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as np

global PopulationSize, NGEN, CXPB, MUTPB

#族群數，演化代數，交配率，變異率
PopulationSize, NGEN, CXPB, MUTPB, = 10 , 10, 0.9, 0.01

sampling = get_sampling("bin_random")

# 交配設定, https://pymoo.org/operators/crossover.html
crossover = get_crossover("real_one_point",  prob=CXPB)

# 變異設定
mutation = get_mutation("bin_bitflip", prob = MUTPB)

# 建立演算法物件
algorithm = GA(
                pop_size = PopulationSize, # 族群數
                sampling = sampling,
                crossover = crossover, # 交配物件
                mutation = mutation, # 變異物件
                eliminate_duplicates = True
            )

# 定義問題
class trade_problem(Problem):
    def __init__(self):
        # n_var = 基因數, 變數參考 https://pymoo.org/problems/definition.html
        super().__init__(n_var=10)

    # 評估函數請參考 https://pymoo.org/getting_started/part_2.html
    def _evaluate(self, x, out, *args, **kwargs):
        population = x.astype(int)
        # 計算population中的每個individual的fitness value
        fvalue_list = []
        for individual in population:
            fvalue = 0
            x,y = 0,0
            #前五個為x,後五個為y
            for i in range(0,5):
                x = x * 2 + int(individual[i])
                print(int(individual[i]))
            for i in range(5,10):
                y = y * 2 + int(individual[i])
            fvalue =x * x - 5 * x * y + 5 * y * y
            fvalue_list.append(fvalue)
        print(population)
        out["F"] = np.column_stack( [fvalue_list] )
problem = trade_problem()

# 執行最佳化, https://pymoo.org/interface/minimize.html
res = minimize(problem, # 問題
            algorithm, # 使用演算法
            ('n_gen', NGEN), # 選出最佳化的數量，設定為族群數
            #seed = 1, #亂數碼
            verbose=False
        )

print("Best solution found: %s" % res.X.astype(int))
print("Function value: %s" % res.F)
# res的用法請參考 https://pymoo.org/interface/result.html