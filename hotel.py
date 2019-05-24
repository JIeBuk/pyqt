from PyQt5.QtWidgets import QApplication,QLabel,QLineEdit, QMainWindow,QPushButton, QGridLayout, QWidget, QTableWidget,QDateEdit, QTableWidgetItem,QTimeEdit,QComboBox,QMessageBox
from PyQt5.QtCore import QSize, Qt

from xml.dom import minidom
import xml.etree.cElementTree as ET
import os
import sys 

       
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        super().__init__()
        self.initUI()
        


    def initUI(self):
        self.listclients_window=None
        self.delete_window=None
        self.rooms = ('101','102','103','104','105','201','202','203','204','205','301','302','303','304','305')
        
        self.setMinimumSize(QSize(600, 200))             # Устанавливаем размеры
        self.setWindowTitle("Электронная гостиница")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        self.createbtns()
        self.createedits()
        self.createtitles()

        central_widget.setLayout(self.grid_layout)

    def close_app(self):
        self.close()
        

    def register(self):
        pass
        
    def deleteclient(self):
        if self.delete_window == None:
            self.delete_window = DeleteWindow()
        self.delete_window.show()
        
    
    def getclients(self):
        self.listclients_window = ClientsWindow()
        self.listclients_window.show()


    
    def getdata(self):
        self.clients = []
        fio_clients = []
        room_clients = []
        days_clients = []
        
        self.XML_FILE = os.path.join('clients.xml')
        self.tree = ET.ElementTree(file = self.XML_FILE)
        self.root = self.tree.getroot()
        
        for contact in self.root.iter('FIO'):
            fio_clients.append(contact.text)
        for contact in self.root.iter('room'):
            room_clients.append(contact.text)
        for contact in self.root.iter('days'):
            days_clients.append(contact.text)
        
        self.clients= list(zip(fio_clients,room_clients,days_clients))
        
    def getprice(self,c):
        c=int(c)
        c= 23*c
        c = str(c)
        return c
    
    def checkint(self,i):
        try:
            int(i)
            return True
        except:
            Q = QMessageBox.information(self, 'Ок', 'Некоректные данные!', QMessageBox.Ok)
            return False
        
    def checknoroom(self,number):
        if number in self.rooms:
            return True
        else:
            Q = QMessageBox.information(self, 'Ок', 'Нет такого номера!', QMessageBox.Ok)
            return False
        
    def checkfreeroom(self,r):
        for i in self.clients:
            if r == i[1]:
                Q = QMessageBox.information(self, 'Ок', 'Номер занят!', QMessageBox.Ok)
                return False
        return True
        
    def insert_client(self):
        def indent(elem, level=0):

            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
        FIO =[]
        FIO.append(self.f_edit.text())
        FIO.append(self.i_edit.text())
        FIO.append(self.o_edit.text())
        FIO = ' '.join(FIO)
        new_el = ET.Element('contact')
        new_sub = ET.SubElement(new_el, 'FIO')
        new_sub.text = FIO
        new_sub = ET.SubElement(new_el, 'room')
        new_sub.text = self.room_edit.text()
        new_sub = ET.SubElement(new_el, 'days')
        new_sub.text = self.days_edit.text()
        self.root.append(new_el)
        indent(self.root)
        self.tree.write(self.XML_FILE)
        
    
    def register(self):
        
        
        
        if '' in (i.text() for i in self.edit_list):
            Q = QMessageBox.information(self, 'Ок', 'Введите данные!', QMessageBox.Ok)
            return
        else:
            a = self.checkint(self.room_edit.text())
            if not a: return
            b = self.checkint(self.days_edit.text())
            if not b: return
            d = self.checknoroom(self.room_edit.text())
            if not d: return
            self.getdata()
            c = self.checkfreeroom(self.room_edit.text())
            if not c: return
            self.insert_client()
            c = self.getprice(self.days_edit.text())
            Q = QMessageBox.information(self, 'Ок', 'Клиент заселен!с вас '+c+'$!', QMessageBox.Ok)
            for i in self.edit_list:
                i.clear()
        
        
    def createbtns(self):
        self.btn_register = QPushButton("register")
        self.btn_register.clicked.connect(self.register)
        self.btn_delete = QPushButton("delete client")
        self.btn_delete.clicked.connect(self.deleteclient)
        self.btn_list = QPushButton("clients")
        self.btn_list.clicked.connect(self.getclients)
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close_app)

        self.grid_layout.addWidget(self.btn_register,3,3)
        self.grid_layout.addWidget(self.btn_delete,6,0,2,1)
        self.grid_layout.addWidget(self.btn_list,6,1,2,1)
        self.grid_layout.addWidget(self.btn_close,6,3,2,1)

        
    def createtitles(self):
        self.title1 =QLabel("Фамилия:")
        self.title2 =QLabel("Имя:")
        self.title3 =QLabel("Отчество")
        
        self.title4 =QLabel("№ комнаты")
        self.title5 =QLabel("количество дней")

        self.grid_layout.addWidget(self.title1,0,0)
        self.grid_layout.addWidget(self.title2,0,1)
        self.grid_layout.addWidget(self.title3,0,2)
        self.grid_layout.addWidget(self.title4,2,0)
        self.grid_layout.addWidget(self.title5,2,1)

        
    def createedits(self):
        self.f_edit = QLineEdit()
        self.i_edit = QLineEdit()
        self.o_edit = QLineEdit()
        self.room_edit = QLineEdit()
        self.days_edit = QLineEdit()
        self.edit_list = [self.f_edit,self.i_edit,self.o_edit,self.room_edit,self.days_edit]
        self.grid_layout.addWidget(self.f_edit,1,0)
        self.grid_layout.addWidget(self.i_edit,1,1)
        self.grid_layout.addWidget(self.o_edit,1,2)
        self.grid_layout.addWidget(self.room_edit,3,0)
        self.grid_layout.addWidget(self.days_edit,3,1)
        

class DeleteWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(280, 150))             # Устанавливаем размеры
        self.setWindowTitle("выселение")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.create_interface()
        
        central_widget.setLayout(self.grid_layout)
    
    def getFromEdit(self):
        if '' in (i.text() for i in self.edit_list):
            Q = QMessageBox.information(self, 'Ок', 'Введите данные!', QMessageBox.Ok)
            return False
        else:
            self.FIO =[]
            self.FIO.append(self.edit1.text())
            self.FIO.append(self.edit2.text())
            self.FIO.append(self.edit3.text())
            self.FIO = ' '.join(self.FIO)
            return True
        pass

    def delete(self):
        
        a = self.getFromEdit()
        print(self.FIO)
        if not a:
            return
        else:
            mw.getdata()
            print(self.FIO)
            for i in range(len(mw.clients)):
                
                if self.FIO == mw.clients[i][0]:
                    
                    mw.root.remove(mw.root[i])
                    Q = QMessageBox.information(self, 'Ок', 'клиент выселен из номера '+str(mw.clients[i][1])+'!', QMessageBox.Ok)
                    mw.tree.write(mw.XML_FILE)
                    for i in self.edit_list:
                        i.clear()
                    return
            Q = QMessageBox.information(self, 'Ок', 'Такой клиент у нас не заселен', QMessageBox.Ok)
                    
            

        
    def close_app(self):
        self.hide()
        
    def create_interface(self):
        self.title1 =QLabel("Фамилия")
        self.title2 =QLabel("Имя")
        self.title3 =QLabel("Отчество")
        
        
        self.grid_layout.addWidget(self.title1, 0, 0,1,2)
        self.grid_layout.addWidget(self.title2, 0, 2,1,2)
        self.grid_layout.addWidget(self.title3, 0, 4,1,2)
        
        self.edit1 =QLineEdit()
        self.edit2 =QLineEdit()
        self.edit3 =QLineEdit()
        self.edit_list = (self.edit1,self.edit2,self.edit3)
        self.grid_layout.addWidget(self.edit1, 1, 0,1,2)
        self.grid_layout.addWidget(self.edit2, 1, 2,1,2)
        self.grid_layout.addWidget(self.edit3, 1, 4,1,2)
        
        
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)
         
        self.btn_insert = QPushButton("выселить")
        self.btn_insert.clicked.connect(self.delete)

        self.grid_layout.addWidget(self.btn_insert,2, 2,1,2)
        self.grid_layout.addWidget(self.btn_close,2, 5)

class ClientsWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(300, 400))             # Устанавливаем размеры
        self.setWindowTitle("Клиенты")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.createinterface()
        self.insertdataform()
        
        self.grid_layout.addWidget(self.btn_close,6, 1)
        
        central_widget.setLayout(self.grid_layout)
    
    def insertdataform(self):
        mw.getdata()
        
        for i in range(len(mw.clients)):
                self.table.setItem(i,0, QTableWidgetItem(mw.clients[i][0]))
                self.table.setItem(i,1, QTableWidgetItem(mw.clients[i][1]))
        string=[]
        l = [i[1] for i in mw.clients]
        for i in mw.rooms:
            if i not in l:
                    string.append(i)
        string = ', '.join(string)
        self.title2.setText('Список свободных комнат: '+ string)
        self.table.resizeColumnsToContents()
                
        

    def createinterface(self):
        self.table = QTableWidget(self)  
        self.table.setColumnCount(2)     
        self.table.setRowCount(20)        
 
        self.table.setHorizontalHeaderLabels(["FIO","No room"])
        self.table.resizeColumnsToContents()
        self.grid_layout.addWidget(self.table, 1, 0,1,3)
        
        self.title1 =QLabel("Список клиентов")
        self.title2 =QLabel("Список свободных комнат:")
        
        self.grid_layout.addWidget(self.title1, 0, 0,1,3)
        self.grid_layout.addWidget(self.title2, 5, 0,1,3)             
        
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)

        
    def close_app(self):
        self.hide()        



    
        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

