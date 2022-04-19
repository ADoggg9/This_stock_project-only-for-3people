import ui
from lib.share import SI
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication([])
    SI.Input_balance = ui.Input_balance()
    SI.Input_balance.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()

