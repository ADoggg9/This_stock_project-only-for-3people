import numpy as np
import pandas as pd
import datetime


# 类中信息后面根据需要扩充，修改类中信息后，所有实体化的地方都需要检查修改
class Stock:
    StockID: int  # 股票编号
    Rank: float  # 股票得分
    Historyloc: str  # 历史数据存放路径
    # predict_loc = ''    # 预测
    pur_price: float    # 股票购买价格
    hold_num: float    # 持有量
    holded = False
    sell_time: datetime  # 股票可能的卖出时间

    def __init__(self, stockID: int, historyloc, price: float, time: str, hold=False, num=0, rank=0):
        self.StockID = stockID
        self.Historyloc = historyloc  # 存放历史数据的地址
        self.pur_price = price
        self.holded = hold
        self.hold_num = num
        d_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        self.sell_time = d_time
        self.Rank = rank

    # 读取该只股票历史信息并以numpy格式返回
    def showhistory(self):
        history_data = pd.read_csv(self.Historyloc, engine='python').values
        return history_data

    # 返回该股票预测信息
    # def showpredict(self):
    #    predict_data = pd.read_csv(self.predict_loc).values
    #    return predict_data

    # 更改股票持有信息,买入时更改为True，卖出改为False
    def changehave(self, T):
        self.holded = T