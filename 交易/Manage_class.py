import datetime
import os
import numpy as np
import pandas as pd
import stock_class


class Manage_Trade:
    balance: float  # 资金
    stockholding_loc: str  # 存储持仓数据文件的路径
    stockholding_list = []  # 持仓股票列表
    del stockholding_list[:]  # 清空列表防止里面又脏数据
    predictloc: str  # 预测结果信息储存列表（假设第一列为股票编号、第二列为具体股票预测结果的文件路径、第三列为历史数据）
    sells = []  # 卖出股票列表
    sells_price = []  # 记录对应股票的卖出价格
    buys = []  # 买入股票列表
    rank_count: float   # 记录一组预测总得分

    def __init__(self, balance, stockholding_loc, predictloc):
        self.balance = balance
        self.stockholding_loc = stockholding_loc
        self.predictloc = predictloc
        # 读取已持有股票信息,将信息存在自身的stockholding_list中，该部分考虑加入初始化中
        stockholding_data = pd.read_csv(self.stockholding_loc, engine='python').values
        for i in range(len(stockholding_data)):
            stockID = stockholding_data[i][0]  # 假设第一列为股票的编号
            historyloc = stockholding_data[i][1]  # 第二列为存该股票历史数据的地址
            pur_price = stockholding_data[i][2]  # 假设第三列为购买时的价格
            pur_num = stockholding_data[i][3]  # 假设第四列为购买数量
            sell_time = stockholding_data[i][4]  # 假设第五列为交易时间
            # sell_time.replace('/', '-')
            the_stock = stock_class.Stock(stockID, historyloc, pur_price, num=pur_num, time=sell_time, hold=True)
            if the_stock.sell_time.date() == datetime.date.today():
                selldata = pd.read_csv(the_stock.Historyloc, engine='python').values
                sellprice = selldata[0][1]  # 股票历史数据文件第2列为价格
                self.sells_price.append(sellprice)
                self.sells.append(the_stock)
            else:
                self.stockholding_list.append(the_stock)

    # 更新读取已持有股票信息（更新stockholding_list）
    def updata_holding(self):
        # 将stockholding_list清空
        self.stockholding_list.clear()
        # 将新的持股数据逐一读入
        stockholding_data = pd.read_csv(self.stockholding_loc, engine='python').values
        for i in range(len(stockholding_data)):
            stockID = stockholding_data[i][0]  # 假设第一列为股票的编号
            historyloc = stockholding_data[i][1]  # 第二列为存该股票历史数据的地址
            pur_price = stockholding_data[i][2]  # 假设第三列为购买时的价格
            pur_num = stockholding_data[i][3]  # 假设第四列为购买数量
            sell_time = stockholding_data[i][4]  # 假设第五列为交易时间
            the_stock = stock_class.Stock(stockID, historyloc, pur_price, num=pur_num, time=sell_time, hold=True)
            self.stockholding_list.append(the_stock)

    # 展示持仓的股票信息
    def show_holding(self):
        if len(self.stockholding_list) > 0:
            print('持有股票信息如下：')
            print('序号  \t股票编号\t\t购买单价\t\t持有数量\t\t持有价值')
            for i in range(len(self.stockholding_list)):
                print(i + 1, '\t\t', self.stockholding_list[i].StockID,
                      '\t\t\t', self.stockholding_list[i].pur_price,
                      '\t\t', self.stockholding_list[i].hold_num,
                      '\t\t', self.stockholding_list[i].pur_price * self.stockholding_list[i].hold_num)
        else:
            print('未持有任何股票')

    # 判断特定编号的股票是否已持有,持有则返回该股票在stockholding_list中所有此股票编号的股票位置数组，未持有则返回空数组
    def if_holding(self, stockID):
        hold = []
        for i in range(len(self.stockholding_list)):
            if stockID == self.stockholding_list[i].StockID:
                hold.append(i)
        return hold

    # 读取预测信息并评分
    def rank_stock(self):
        predict_data = pd.read_csv(self.predictloc, engine='python').values
        self.rank_count = 0.0
        for i in range(len(predict_data)):
            stockID = predict_data[i][0]
            predict = pd.read_csv(predict_data[i][1], engine='python').values  # 读取对应股票具体预测数据
            history = predict_data[i][2]  # 读取对应股票历史数据

            # 看该股票是否为已持有股票,
            hold = self.if_holding(stockID)

            # 寻找最大价格
            max_price = predict[0][1]  # 假设第二列是现价，初始为预测开始时的价格
            max_time = predict[0][0]  # 假设第一列为对应时间
            for j in range(len(predict)):
                if predict[j][1] > max_price:
                    max_price = predict[j][1]
                    max_time = predict[j][0]

            # 计算得分,假设第三列为交易量        差价*权重*(增长率*权重+交易量*权重)为了使得当预测下跌时得分为0，其中*1均为假设的权重
            # 此处公式后续需要扩充修改
            rank = (max_price - predict[0][1]) * 1 * (
                    ((max_price - predict[0][1]) / predict[0][1]) * 1 + predict[0][2] * 1)
            self.rank_count += rank
            # 如果股票未持有并且下跌则不进行操作
            if len(hold) == 0 and rank == 0:
                continue

            # 如果未持有并且上涨
            if len(hold) == 0 and rank > 0:
                the_stock = stock_class.Stock(stockID, history, predict[0][1], time=max_time, rank=rank)
                self.buys.append(the_stock)  # 此时将先存如buys中作为待定购买项

            # 如果已持并且下跌则抛售
            if len(hold) != 0 and rank == 0:
                for j in range(len(hold)):
                    self.sells.append(self.stockholding_list[hold[j]])  # 讲准备抛售股票入队sells
                    self.sells_price.append(predict[0][1])  # predict[0][3]中就是当前的股票价格
                    self.stockholding_list.pop(hold[j])  # 将准备抛售的股票从stockholding_list出队

            # 如果持有其上涨则准备补仓
            if len(hold) != 0 and rank > 0:
                the_stock = stock_class.Stock(stockID, history, predict[0][1], time=max_time, rank=rank)
                self.buys.append(the_stock)  # 准备补仓股票入队buys

        # 所有推荐购买股票已入buys，开始按照rank分配资金
        for i in range(len(self.buys)):
            # num = ((self.buys[i].Rank / self.rank_count) * self.balance) / self.buys[i].pur_price
            num = (self.balance / len(self.buys)) / self.buys[i].pur_price
            self.buys[i].hold_num = num

    # 像屏幕输出准备买入和卖出的股票
    def show_buys(self):

        if len(self.buys) > 0:  # buys非空则输出推荐购买股票
            print('准备买入的股票如下:')
            print('序号  \t股票编号\t\t购买单价\t\t购买数量\t\t购买金额')
            for i in range(len(self.buys)):
                print(i + 1, '\t\t', self.buys[i].StockID,
                      '\t\t\t', self.buys[i].pur_price,
                      '\t\t', self.buys[i].hold_num,
                      '\t\t', self.buys[i].pur_price * self.buys[i].hold_num)
        else:  # buys为空
            print('当前无推荐购买股票')

    def show_sells(self):
        if len(self.sells):
            print('准备卖出的股票如下:')
            print('序号  \t股票编号\t\t购买单价\t\t抛售数量\t\t预计卖价')
            for i in range(len(self.sells)):
                print(i + 1, '\t\t', self.sells[i].StockID,
                      '\t\t\t', self.sells[i].pur_price,
                      '\t\t', self.sells[i].hold_num,
                      '\t\t', self.sells_price[i])
        else:
            print('无需抛售股票')

    # 更新holding.csv文件
    def update_holding_csv(self):
        df = pd.DataFrame(columns=('stockID', 'historyloc', 'pur_price', 'hold_num', 'sell_time'))
        for i in range(len(self.stockholding_list)):
            df.loc[i] = [self.stockholding_list[i].StockID,
                         self.stockholding_list[i].Historyloc,
                         self.stockholding_list[i].pur_price,
                         self.stockholding_list[i].hold_num,
                         self.stockholding_list[i].sell_time]
        df.to_csv(self.stockholding_loc, mode='w', index=0)
        self.updata_holding()  # 同时更新类中的holdinglist

    # 确定买入推荐股票
    def check_buys(self):
            while self.buys:
                self.stockholding_list.append(self.buys[0])
                self.buys.pop(0)
            self.update_holding_csv()  # 更新持股信息并写入文件
            self.show_holding()

