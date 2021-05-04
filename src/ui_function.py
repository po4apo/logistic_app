from main import * 

from src.about import *


GLOBAL_STATE = 0 #НЕОБХОДИМО ДЛЯ ПРОВЕРКИ, ЯВЛЯЕТСЯ ЛИ ОКНО ПОЛНОЭКРАННЫМ
GLOBAL_TITLE_BAR = True #НЕОБХОДИМО ДЛЯ ПРОВЕРКИ, ЯВЛЯЕТСЯ ЛИ ОКНО ПОЛНОЭКРАННЫМ
init = False 

# В ЭТОМ КЛАССЕ ЧАСТЬ ФУНКЦИЙ, НЕОБХОДИМЫХ ДЛЯ ЗАПУСКА НАШЕЙ ПРОГРАММЫ
class UIFunction(MainWindow):

    # ----> НАЧАЛЬНАЯ ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ ВИДЖЕТА СТЕКА
    def initStackTab(self):
        global init
        if init==False:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.lab_tab.setText("Список транспортируемых единиц")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True
    ################################################################################################

    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)
    ################################################################################################


    #----> MAXIMISE/RESTORE ФУНКЦИИ
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore") 
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/restore.png")) #ИЗМЕНИТЬ THE MAXIMISE ИКОНКУ НА RESTOR
            self.ui.frame_drag.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/max.png"))
            self.ui.frame_drag.show()
    ################################################################################################


    def returStatus():
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status


    #-----> ПОВЕДЕНИЕ ПО УМОЛЧАНИЮ
    def constantFunction(self):
        #-----> ДВОЙНОЙ КЛИК МАКСИМИЗИРУЕТ
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        #----> УБРАТЬ СТАНДАРТНЫЙ TITLE BAR 
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        #-----> MINIMIZE ФУНКЦИЯ
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        #-----> MAXIMIZE/RESTORE ФУНКЦИЯ
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        #-----> CLOSE APPLICATION ФУНКЦИЯ
        self.ui.bn_close.clicked.connect(lambda: self.close())
    ################################################################################################################


    #----> ПОИСК СООТВЕТСТВИЙ МЕЖДУ НАЖАТОЙ КНОПКОЙ И СТРАНИЕЙ СТЕК ВИДЖЕТА
    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName=='bn_cargolist':
            if self.ui.frame_bottom_west.width()==80  and index!=0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Список транспортируемых единиц")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName=='bn_cargopage':
            if self.ui.frame_bottom_west.width()==80 and index!=5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("Карточки транспортируемых единиц")
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")
