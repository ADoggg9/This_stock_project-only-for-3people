from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
import PyQt5.uic as uic
from lib.share import SI
from Manage_class import Manage_Trade


class Input_balance:

    def __init__(self):
        self.ui = uic.loadUi('inputbalance.ui')
        self.ui.btn_balance.clicked.connect(self.check_balance)
        self.ui.balance.returnPressed.connect(self.check_balance)

    def check_balance(self):
        SI.balance = float(self.ui.balance.text().strip())
        if SI.balance < 0:
            QMessageBox.warning(self.ui, 'failed', '输入金额要大于0')
            return
        SI.Menu = Menu()
        SI.Manage = Manage_Trade(balance=SI.balance, stockholding_loc='holding.csv', predictloc='predict.csv')
        SI.Manage.rank_stock()
        SI.Menu.ui.show()
        SI.Input_balance.ui.close()


class Menu:

    def __init__(self):
        self.ui = uic.loadUi('menu.ui')
        self.ui.Exit.triggered.connect(self.EXIT)
        self.ui.btn_showhold.clicked.connect(self.Showhold)
        self.ui.btn_prebuys.clicked.connect(self.Showprebuy)
        self.ui.btn_showpredict.clicked.connect(self.Showpredict)
        self.ui.btn_showsells.clicked.connect(self.Showsells)

    def EXIT(self):
        self.ui.close()

    def Showhold(self):
        SI.Show_Holding = Show_holding()
        SI.Show_Holding.ui.show()

    def Showprebuy(self):
        SI.Show_PreBuys = Show_prebuys()
        SI.Show_PreBuys.ui.show()

    def Showpredict(self):
        SI.Show_Predict = Show_predict()
        SI.Show_Predict.ui.show()

    def Showsells(self):
        SI.Show_Sells = Show_Sells()
        SI.Show_Sells.ui.show()


class Show_holding:

    def __init__(self):
        self.ui = uic.loadUi('showhold.ui')
        for i in range(len(SI.Manage.stockholding_list)):
            self.ui.HoldingTable.insertRow(i)
            self.ui.HoldingTable.setItem(i, 0, QTableWidgetItem(str(SI.Manage.stockholding_list[i].StockID)))
            self.ui.HoldingTable.setItem(i, 1, QTableWidgetItem(str(SI.Manage.stockholding_list[i].pur_price)))
            self.ui.HoldingTable.setItem(i, 2, QTableWidgetItem(str(SI.Manage.stockholding_list[i].hold_num)))
            self.ui.HoldingTable.setItem(i, 3, QTableWidgetItem(
                str(SI.Manage.stockholding_list[i].pur_price * SI.Manage.stockholding_list[i].hold_num)))


class Show_prebuys:

    def __init__(self):
        self.ui = uic.loadUi('recombuys.ui')
        for i in range(len(SI.Manage.buys)):
            self.ui.SrecommendTable.insertRow(i)
            self.ui.SrecommendTable.setItem(i, 0, QTableWidgetItem(str(SI.Manage.buys[i].StockID)))
            self.ui.SrecommendTable.setItem(i, 1, QTableWidgetItem(str(SI.Manage.buys[i].pur_price)))
            self.ui.SrecommendTable.setItem(i, 2, QTableWidgetItem(str(SI.Manage.buys[i].hold_num)))
            self.ui.SrecommendTable.setItem(i, 3, QTableWidgetItem(
                str(SI.Manage.buys[i].pur_price * SI.Manage.buys[i].hold_num)))
        self.ui.btn_buy.clicked.connect(self.buy)
        self.ui.btn_unbuy.clicked.connect(self.unbuy)


    def buy(self):
        choice = QMessageBox.question(self.ui, '确认', '确认入仓以上股票')
        if choice == QMessageBox.Yes:
            SI.Manage.check_buys()
            self.ui.close()

    def unbuy(self):
        choice = QMessageBox.question(self.ui, '确认', '确认放弃入仓')
        if choice == QMessageBox.Yes:
            self.ui.close()


class Show_Sells:

    def __init__(self):
        self.ui = uic.loadUi('showsells.ui')
        for i in range(len(SI.Manage.sells)):
            self.ui.SellTable.insertRow(i)
            self.ui.SellTable.setItem(i, 0, QTableWidgetItem(str(SI.Manage.sells[i].StockID)))
            self.ui.SellTable.setItem(i, 1, QTableWidgetItem(str(SI.Manage.sells[i].pur_price)))
            self.ui.SellTable.setItem(i, 2, QTableWidgetItem(str(SI.Manage.sells[i].hold_num)))
            self.ui.SellTable.setItem(i, 3, QTableWidgetItem(str(SI.Manage.sells_price[i])))
        self.ui.btn_sell.clicked.connect(self.sell)

    def sell(self):
        choice = QMessageBox.question(self.ui, '确认', '确认抛售以上股票')
        if choice == QMessageBox.Yes:

            self.ui.close()


class Show_predict:

    def __init__(self):
        self.ui = uic.loadUi('showpredict.ui')