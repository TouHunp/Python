import io
import sys
import requests
# import requests.packages.urllib3
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
requests.packages.urllib3.disable_warnings()

def getStockData(stockNo,item,num):
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo=" + stockNo + "&date=20210701"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if(response.status_code==200):
        dict = response.json() # dict['stat'], dict['date'], dict['title'], dict['fields'], dict['data']
        data = np.array(dict[item]) #只取某一個key的值，ex: 收盤價 dict[‘data’]
        selected_data = data[:,num]  #只取某一行的值，ex: 收盤價
        selected_data = np.asarray(selected_data, dtype=float) #將字串轉換成浮點數
        return  selected_data

global dataset, stockList
stockList = ["2610", "2618", "2603", "2609", "2615"]
dataset  = {}
buy_hold_return = {}
buy_hold_std = {}
for stock in stockList:
    dataset[stock] = getStockData(stock, "data", 6)
    buy_hold_return[stock] = (dataset[stock][21]-dataset[stock][0])/dataset[stock][0]
    buy_hold_std[stock] = np.std(dataset[stock])

for stock in stockList:
    print(stock)
    print(dataset[stock])
    print(buy_hold_return[stock])
    print(buy_hold_std[stock])

from pymoo.factory import get_crossover, get_mutation, get_sampling
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as np

global PopulationSize, NGEN, CXPB, MUTPB

#族群數，演化代數，交配率，變異率
PopulationSize, NGEN, CXPB, MUTPB, = 10 , 50, 0.9, 0.01

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
        super().__init__(n_var=5)

    def _evaluate(self, x, out, *args, **kwargs):
        population = x.astype(int)
        fvalue_list = []
        for individual in population:
            cost = 0
            price = 0
            for i, g in enumerate(individual):
                if(g==1):
                    cost += dataset[stockList[i]][0]
                    price += dataset[stockList[i]][21]
            if(cost==0):
                fvalue = 10
            else:
                fvalue = -(price-cost)/cost
            fvalue_list.append(fvalue)
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