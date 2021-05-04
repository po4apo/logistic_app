import sys
import sqlite3 as sql

#ИМПОРТ ВСЕХ НЕОБХОДИМЫХ МОДУЛЕЙ PyQt5 ДЛЯ ПРИЛОЖЕНИЯ
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from src.ui_main import Ui_MainWindow # КОД ГЛАВНОГО ОКНА, Сгенерированный QT DESIGNER

from src.ui_dialog import Ui_Dialog # ОКНО ДИАЛОГОВОГО БЛОКА

from src.ui_error import Ui_Error # ОКНО ERRORBOX

from src.ui_function import * # ФАЙЛ, В НЕМ ВЫПОЛНЕНЫ ФУНКЦИИ, НАЖАТИЯ КНОПОК И ТД

#DIALOGBOX, КОТОРЫЙ СОЗДАЕТ ДИАЛОГОВОЕ ОКНО ПРИ ВЫЗОВЕ. 
class dialogUi(QDialog):
    def __init__(self, parent=None):

        super(dialogUi, self).__init__(parent)
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.d.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> КНОПКА ЗАКРЫТЬ ПРИЛОЖЕНИЕ 
        self.d.bn_close.clicked.connect(lambda: self.close())

        # -----> ДАННАЯ ФУНКЦИЯ ПРОВЕРЯЕТ СОТСТОЯНИЕ НАЖАТИЙ КНОПКИ НА ДИАЛОГОВОМ БЛОКЕ
        self.d.bn_east.clicked.connect(lambda: self.east_pressed())
        self.d.bn_west.clicked.connect(lambda: self.close())
        ##############################################################################################

    def east_pressed(self):
        self.returned_value = True
        self.close()

    ##################################################################################################
        self.dragPos = self.pos()   # НАЧАЛЬНОЕ ПОЛОЖЕНИЕ ДИАЛОГОВОГО ОКНА 
        def movedialogWindow(event):
            # ИЗМЕНЕНИЕ КООРДИНАТ ОУНА
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()


        self.d.frame_top.mouseMoveEvent = movedialogWindow  #ВЫЗОВ ФУНКЦИИ ПЕРЕМЕЩЕНИЯ

    #----> ФУНКЦИЯ ОПРЕДЕЛЕНИЯ КООРДИНАТ МЫШИ
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    #################################################################################################
    # ДИАЛОГОВОЕ ОКНО ПРЕДНАЗНАЧЕНО ДЛЯ ВЫЗОВА В ЛЮБОЙ МОМЕНТ РАБОТЫ ПРИЛОЖЕНИЯ 
    # С ВОЗМОЖНОСТЬЮ ИЗМЕНИТЬ СОСТОЯНИЕ ПРЕДСТАВЛЕННОГО ТЕКСТА, ИМЕНИ КНОПОК И Т.Д

    # -------> НАСТРОЙКА КОНФИГУРАЦИИ ДИАЛОГБОКСА
    def dialogConstrict(self, heading, message, icon, btn1, btn2):
        self.d.lab_heading.setText(heading)
        self.d.lab_message.setText(message)
        self.d.bn_east.setText(btn2)
        self.d.bn_west.setText(btn1)
        pixmap = QtGui.QPixmap(icon)
        self.d.lab_icon.setPixmap(pixmap)
    ##################################################################################################



#ERRORBOX СОЗДАЕТ ОКНО ПО ШАБЛОНУ, ЧТОБЫ ПОКАЗАТЬ, ЧТО ДЕЙСТВИЕ ПОЛЬЗОВАТЕЛЯ НЕПРАВИЛЬНО.
class errorUi(QDialog):
    def __init__(self, parent=None):

        super(errorUi, self).__init__(parent)
        self.e = Ui_Error()
        self.e.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.e.bn_ok.clicked.connect(lambda: self.close())

        self.dragPos = self.pos()   # НАЧАЛЬНОЕ ПОЛОЖЕНИЕ ОКНА 
        def moveWindow(event):
            # ПЕРЕМЕЩЕНИЕ ОКНА
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # ПЕРЕМЕЩАЕМЫЙ ВИДЖЕТ
        self.e.frame_top.mouseMoveEvent = moveWindow  #ВЫЗОВ ФУНКЦИИ ПЕРЕМЕЩЕНИЯ
        ################
    #----> ФУНКЦИЯ ОПРЕДЕЛЕНИЯ КООРДИНАТ МЫШИ
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
#############################################

    # -------> НАСТРОЙКА КОНФИГУРАЦИИ ОКНА ERRORBOX
    def errorConstrict(self, heading, icon, btnOk):
        self.e.lab_heading.setText(heading)
        self.e.bn_ok.setText(btnOk)
        pixmap2 = QtGui.QPixmap(icon)
        self.e.lab_icon.setPixmap(pixmap2)


# ГЛАВНОЕ ОКНО НАШЕГО ПРИЛОЖЕНИЯ: 
class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # ----> УСТАНОВИТЬ НАЗВАНИЕ ОКНА И ЗНАЧОК
        applicationName = "Транспортно Логистическая Система"
        self.setWindowTitle(applicationName) # УСТАНАВЛИВАЕТ ИМЯ ПРИЛОЖЕНИЯ В ВЕРХНЕЙ ПАНЕЛИ ОКНА
        # ВЫ УВИДИТЕ ИМЯ, ВВЕДЕННОЕ ЗДЕСЬ В TASKBAR, TITLEBAR, И Т.Д
        UIFunction.labelTitle(self, applicationName) # УСТАНОВКА НАЗВАНИЯ НА ПОЛЬЗОВАТЕЛЬСКОЙ ПАНЕЛИ ИНСТРУМЕНТОВ

        ###############################

        # -----> ВИДЖЕТ И ВКЛАДКА НАЧАЛЬНОЙ STACKED WIDGET СТРАНИЦЫ 
        UIFunction.initStackTab(self)
        ############################################################

        # ----> НЕКОТОРЫЕ ИНСТРУМЕНТЫ, КАК ПЕРЕТАСКИВАТЬ, МАКСИМИЗИРОВАТЬ, МИНИМИЗИРОВАТЬ, ЗАКРЫТЬ И СКРЫТЬ ВЕРХНЮЮ ПАНЕЛЬ
        # ЭТО ОКНО ИНИЦИАЛИЗИРУЕТ НЕОБХОДИМЫЕ КНОПКИ ДЛЯ ГЛАВНОГО ОКНА
        UIFunction.constantFunction(self)
        #############################################################

        # ----> СОБЫТИЯ НАЖАТИЙ НА КНОПКИ МЕНЮ 
        self.ui.bn_cargolist.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_cargolist'))
        self.ui.bn_cargopage.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_cargopage'))
        #############################################################
        
        #----> ОБЛЕГЧАЕТ ЗАУПСК ОКНА ОШИБОК И ДИАЛОГОВОГО ОКНА
        self.diag = dialogUi()
        self.error = errorUi()
        #############################################################


        # ---> ПЕРЕМЕЩЕНИЕ ОКНА, КОГДА ЛЕВАЯ КНОПКА МЫШИ ЗАЖАТА
        self.dragPos = self.pos()
        def moveWindow(event):

            if UIFunction.returStatus() == 1: 
                UIFunction.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # ВЫЗОВ ФУНКЦИИ ДЛЯ ИЗМЕНЕНИЯ ПОЛОЖЕНИЯ ОКНА
        self.ui.frame_appname.mouseMoveEvent = moveWindow 

        # НАЗНАЧЕНИЕ СОБЫТИЙ ДЛЯ ПОЛЬЗОВАЛЬТЕЛЬСКИХ СТРАНИЦ БАЗЫ ДАННЫХ ТЛС
        # КНОПКА СЛЕДУЮЩАЯ КАРТОЧКА CARGO В БД
        self.ui.bn_cargocards_page_next.clicked.connect(self.increment_current_cargopage)
        # КНОПКА ПРЕДЫДУЩАЯ КАРТОЧКА CARGO В БД
        self.ui.bn_cargocards_page_previous.clicked.connect(self.decrement_current_cargopage)
        # СОБЫТИЕ НАЖАТИЯ НА СТРОЧКУ В ТАБЛИЦЕ СПИСОК CARGO
        self.ui.cargolist_table_widget.clicked.connect(self.onclick_cargocards_page)
        # КНОПКА ДОБАВИТЬ КАРТОЧКУ В CARGO БД
        self.ui.bn_cargocard_delete.clicked.connect(self.delete_cargocards_page)
        # КНОПКА СОЗДАТЬ КАРТОЧКУ В CARGO БД
        self.ui.bn_cargocard_create.clicked.connect(self.insert_cargocards_page)
        # КНОПКА ИЗМЕНИТЬ КАРТОЧКУ В CARGO БД
        self.ui.bn_cargocard_edit.clicked.connect(self.update_cargocards_page)
        # ОБНОВИТЬ СОДЕРЖИМОЕ ОКОН ПРИЛОЖЕНИЯ
        self.reload_contents()

    #----> ПОЛОЖЕНИЯ ОКНА, НЕОБХОДИМО ДЛЯ РАБОТЫ ПЕРЕМЕЩЕНИЯ
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    #############################################################


    #-----> ПАРАМЕТРИЗИРОВАННЫЙ ВЫЗОВ ДИАЛОГОВОГО ОКНА
    def dialogexec(self, heading, message, icon, btn1, btn2):
        self.diag.returned_value = False
        dialogUi.dialogConstrict(self.diag, heading, message, icon, btn1, btn2)
        self.diag.exec_()
        return self.diag.returned_value
    #############################################################


    #-----> ПАРАМЕТРИЗИРОВАННЫЙ ВЫЗОВ ОКНА ERRORBOX
    def errorexec(self, heading, icon, btnOk):
        errorUi.errorConstrict(self.error, heading, icon, btnOk)
        self.error.exec_()
    ##############################################################

    # НАСТРОЙКА ТАБЛИЧНОГО ВИДЖЕТА НА СТР1
    def configure_table_widget(self):
        self.ui.cargolist_table_widget
        self.ui.cargolist_table_widget.setAutoFillBackground(True)
        self.ui.cargolist_table_widget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.ui.cargolist_table_widget.setColumnWidth(0, 25)
        self.ui.cargolist_table_widget.setColumnWidth(1, 150)
        self.ui.cargolist_table_widget.setColumnWidth(2, 150)
        self.ui.cargolist_table_widget.setColumnWidth(3, 150)
        self.ui.cargolist_table_widget.horizontalHeader().setStretchLastSection(True)

    # ЗАПРОС В БД И ЗАПОЛНЕНИЕ ТАБЛИЧНОГО ВИДЖЕТА НА СТР1
    def fill_in_table_widget(self):
        with sql.connect('db.sqlite') as con:
            cur = con.cursor()
            cur.execute(f'''
            select 
            page.id, csc.name, page.date_sent, page.date_arrival, des.address
            from
            (select 
            id, name, weight, estimated_cost, date_sent, date_arrival, cargo_size_category, status, car, departure_warehouse, destination_warehouse
            from cargo) as page
            join cargo_size_category as csc on page.cargo_size_category = csc.id
            join warehouse as des on page.destination_warehouse = des.id
            ''')
            total_cargos = cur.fetchall()
            for i, row_values in enumerate(total_cargos):
                self.ui.cargolist_table_widget.insertRow(i)
                for j, item in enumerate(row_values):
                    self.ui.cargolist_table_widget.setItem(i , j, QtWidgets.QTableWidgetItem(f'{item}'))

    # ВЫЗОВЕТСЯ ПРИ НАЖАТИИ НА СТРОЧКУ В ТАБЛИЦЕ НА СТР1
    def onclick_cargocards_page(self, index):
        try:
            cur_item = self.ui.cargolist_table_widget.item(index.row(), 0).text()
            self.ui.line_cargopage_current.setText(cur_item)
            self.reload_cargopage_contents()
            self.ui.bn_cargopage.click()
        except AttributeError:
            return

    # ЗАПРОС МАКСИМАЛЬНОГО И МИНИМАЛЬНОГО ТЕКУЩЕГО ID В ТАБЛИЦЕ CARGO В БД
    def count_cargos_total(self):
        with sql.connect('db.sqlite') as con:
            cur = con.cursor()
            cur.execute('select max(id) from cargo')
            max_id = cur.fetchone()[0]
            if max_id:
                self.ui.line_cargopage_total.setText(str(max_id))
                cur.execute('select min(id) from cargo')
                self.minimal_cargo_id = cur.fetchone()[0]
                self.ui.line_cargopage_current.setText(str(self.minimal_cargo_id))
                self.reload_cargopage_contents()

    # ПОИСК СТРОКИ В ТАБЛИЦЕ CARGO В БД C МЕНЬШИМ ID, ЧЕМ ТЕКУЩЕЕ
    def decrement_current_cargopage(self):
        current_id = int(self.ui.line_cargopage_current.text())

        if current_id > self.minimal_cargo_id:
            self.ui.line_cargopage_current.setText(str(current_id - 1))
            try:
                self.reload_cargopage_contents()
            except TypeError:
                self.decrement_current_cargopage()

    # ПОИСК СТРОКИ В ТАБЛИЦЕ CARGO В БД C БОЛЬШИМ ID, ЧЕМ ТЕКУЩЕЕ
    def increment_current_cargopage(self):
        current_id = int(self.ui.line_cargopage_current.text())
        self.maximal_cargo_id = int(self.ui.line_cargopage_total.text())
        if current_id < self.maximal_cargo_id:
            self.ui.line_cargopage_current.setText(str(current_id +1))
            try:
                self.reload_cargopage_contents()
            except TypeError:
                self.increment_current_cargopage()

    # ОБНОВИТЬ СОДЕРЖИМОЕ СТР2
    def reload_cargopage_contents(self):
        with sql.connect('db.sqlite') as con:
            cur = con.cursor()
            current_id = int(self.ui.line_cargopage_current.text())
            cur.execute(f'''
            select 
            page.id, page.name, page.weight, page.estimated_cost, page.date_sent, page.date_arrival,
            csc.name, st.name, car.name, dep.address, des.address
            from
            (select 
            id, name, weight, estimated_cost, date_sent, date_arrival, cargo_size_category, status, car, departure_warehouse, destination_warehouse
            from cargo where id = {current_id}) as page
            join cargo_size_category as csc on page.cargo_size_category = csc.id
            join status as st on page.status = st.id
            join car on page.car = car.id
            join warehouse as dep on page.departure_warehouse = dep.id
            join warehouse as des on page.destination_warehouse = des.id
            ''')
            page = cur.fetchone()
            self.ui.line_home_value01.setText(str(page[1]))
            self.ui.line_home_value02.setText(str(page[2]))
            self.ui.line_home_value03.setText(str(page[3]))
            self.ui.line_home_value04.setText(str(page[4]))
            self.ui.line_home_value05.setText(str(page[5]))
            self.ui.line_home_value06.setText(str(page[6]))
            self.ui.line_home_value07.setText(str(page[7]))
            self.ui.line_home_value08.setText(str(page[8]))
            self.ui.line_home_value09.setText(str(page[9]))
            self.ui.line_home_value10.setText(str(page[10]))

    # УДАЛИТЬ ЗАПИСЬ С УКАЗАННЫМ ID НА СТР2 ИЗ ТАБЛИЦЫ CARGO В БД
    def delete_cargocards_page(self):
        current_id = int(self.ui.line_cargopage_current.text())
        answer = self.dialogexec("Внимание", 
            f"Запись ID={current_id} будет удалена. Продолжить?",
                "icons/1x/errorAsset 55.png", "Нет", "Да")
        if answer:
            with sql.connect('db.sqlite') as con:
                cur = con.cursor()
                cur.execute(f'delete from cargo where id = {current_id}')
        self.reload_contents()

    # ВСТАВИТЬ ЗАПИСЬ С УКАЗАННЫМ ID НА СТР2 ИЗ ТАБЛИЦЫ CARGO В БД
    def insert_cargocards_page(self):
        values = list()
        values.append(self.ui.line_home_value01.text())
        values.append(self.ui.line_home_value02.text())
        values.append(self.ui.line_home_value03.text())
        values.append(self.ui.line_home_value04.text())
        values.append(self.ui.line_home_value05.text())
        values.append(self.ui.line_home_value06.text())
        values.append(self.ui.line_home_value07.text())
        values.append(self.ui.line_home_value08.text())
        values.append(self.ui.line_home_value09.text())
        values.append(self.ui.line_home_value10.text())

        try:
            with sql.connect('db.sqlite') as con:
                cur = con.cursor()
                self._query = f'select id from cargo_size_category where name = "{values[5]}"'
                cur.execute(self._query)
                values[5] = cur.fetchone()[0]

                self._query = f'select id from status where name = "{values[6]}"'
                cur.execute(self._query)
                values[6] = cur.fetchone()[0]

                self._query = f'select id from car where name = "{values[7]}"'
                cur.execute(self._query)
                values[7] = cur.fetchone()[0]  

                self._query = f'select id from warehouse where address = "{values[8]}"'
                cur.execute(self._query)
                values[8] = cur.fetchone()[0]   

                self._query = f'select id from warehouse where address = "{values[9]}"'
                cur.execute(self._query)
                values[9] = cur.fetchone()[0]      
        except Exception as e:
            self.errorexec(f"{e}\n\n{self._query}", "icons/1x/errorAsset 55.png", "Ок")
            return

        insert_query = """
        INSERT INTO cargo (            
        name, weight, estimated_cost, date_sent, date_arrival, cargo_size_category, 
        status, car, departure_warehouse, destination_warehouse
            )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """

        try:
            with sql.connect('db.sqlite') as con:
                cur = con.cursor()
                cur.execute(insert_query, values)
        except Exception as e:
            self.errorexec(f"{e}", "icons/1x/errorAsset 55.png", "Ок")
            return

        self.reload_contents()
        self.ui.line_cargopage_current.setText(str(cur.lastrowid))
        self.reload_cargopage_contents()

    # ИЗМЕНИТЬ ЗАПИСЬ С УКАЗАННЫМ ID НА СТР2 ИЗ ТАБЛИЦЫ CARGO В БД
    def update_cargocards_page(self):
        current_id = int(self.ui.line_cargopage_current.text())

        answer = self.dialogexec("Внимание", 
            f"Запись ID={current_id} будет изменена. Продолжить?",
                "icons/1x/errorAsset 55.png", "Нет", "Да")
        if not answer:
            return

        values = list()
        values.append(self.ui.line_home_value01.text())
        values.append(self.ui.line_home_value02.text())
        values.append(self.ui.line_home_value03.text())
        values.append(self.ui.line_home_value04.text())
        values.append(self.ui.line_home_value05.text())
        values.append(self.ui.line_home_value06.text())
        values.append(self.ui.line_home_value07.text())
        values.append(self.ui.line_home_value08.text())
        values.append(self.ui.line_home_value09.text())
        values.append(self.ui.line_home_value10.text())

        try:
            with sql.connect('db.sqlite') as con:
                cur = con.cursor()
                self._query = f'select id from cargo_size_category where name = "{values[5]}"'
                cur.execute(self._query)
                values[5] = cur.fetchone()[0]

                self._query = f'select id from status where name = "{values[6]}"'
                cur.execute(self._query)
                values[6] = cur.fetchone()[0]

                self._query = f'select id from car where name = "{values[7]}"'
                cur.execute(self._query)
                values[7] = cur.fetchone()[0]  

                self._query = f'select id from warehouse where address = "{values[8]}"'
                cur.execute(self._query)
                values[8] = cur.fetchone()[0]   

                self._query = f'select id from warehouse where address = "{values[9]}"'
                cur.execute(self._query)
                values[9] = cur.fetchone()[0]      
        except Exception as e:
            self.errorexec(f"{e}\n\n{self._query}", "icons/1x/errorAsset 55.png", "Ок")
            return

        update_query = f"""
        UPDATE cargo SET            
        name = ?, 
        weight = ?, 
        estimated_cost = ?, 
        date_sent = ?, 
        date_arrival = ?, 
        cargo_size_category = ?, 
        status = ?, 
        car = ?, 
        departure_warehouse = ?, 
        destination_warehouse = ?
        WHERE ID = {current_id}
        """

        try:
            with sql.connect('db.sqlite') as con:
                cur = con.cursor()
                cur.execute(update_query, values)
        except Exception as e:
            self.errorexec(f"{e}", "icons/1x/errorAsset 55.png", "Ок")
            return

        self.reload_contents()
        self.reload_cargopage_contents()        

    # ОБНОВИТЬ ОТОБРАЖАЕМОЕ СОЖЕРЖИМОЕ ПРИЛОЖЕНИЯ
    def reload_contents(self):
        self.clear_cargolist_table_widget()
        self.clear_cargocards_page()
        self.count_cargos_total()
        self.configure_table_widget()  
        self.fill_in_table_widget()

    # ОЧИСТИТЬ ОТОБРАЖАЕМОЕ СОЖЕРЖИМОЕ СТР2
    def clear_cargocards_page(self):
        self.ui.line_home_value01.setText(str(" "))
        self.ui.line_home_value02.setText(str(" "))
        self.ui.line_home_value03.setText(str(" "))
        self.ui.line_home_value04.setText(str(" "))
        self.ui.line_home_value05.setText(str(" "))
        self.ui.line_home_value06.setText(str(" "))
        self.ui.line_home_value07.setText(str(" "))
        self.ui.line_home_value08.setText(str(" "))
        self.ui.line_home_value09.setText(str(" "))
        self.ui.line_home_value10.setText(str(" "))

    # ОЧИСТИТЬ ОТОБРАЖАЕМОЕ СОЖЕРЖИМОЕ СТР1
    def clear_cargolist_table_widget(self):
        while self.ui.cargolist_table_widget.rowCount() > 0:
            self.ui.cargolist_table_widget.removeRow(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
