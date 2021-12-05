from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from db_editor import DBEditor


class Ui_MakePlaylist(object):
    def setupUi(self, MakePlaylist):
        MakePlaylist.setObjectName("MakePlaylist")
        MakePlaylist.resize(510, 300)
        self.centralwidget = QtWidgets.QWidget(MakePlaylist)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_file = QtWidgets.QPushButton(self.centralwidget)
        self.add_file.setObjectName("add_file")
        self.horizontalLayout.addWidget(self.add_file)
        self.del_file = QtWidgets.QPushButton(self.centralwidget)
        self.del_file.setObjectName("del_file")
        self.horizontalLayout.addWidget(self.del_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.name_playlist_text = QtWidgets.QLabel(self.centralwidget)
        self.name_playlist_text.setObjectName("name_playlist_text")
        self.horizontalLayout_2.addWidget(self.name_playlist_text)
        self.playlist_name = QtWidgets.QLineEdit(self.centralwidget)
        self.playlist_name.setObjectName("playlist_name")
        self.horizontalLayout_2.addWidget(self.playlist_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.info = QtWidgets.QLabel(self.centralwidget)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)
        self.files = QtWidgets.QListWidget(self.centralwidget)
        self.files.setObjectName("files")
        self.verticalLayout.addWidget(self.files)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.make_playlist = QtWidgets.QPushButton(self.centralwidget)
        self.make_playlist.setObjectName("make_playlist")
        self.horizontalLayout_3.addWidget(self.make_playlist)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MakePlaylist.setCentralWidget(self.centralwidget)

        self.retranslateUi(MakePlaylist)
        QtCore.QMetaObject.connectSlotsByName(MakePlaylist)

    def retranslateUi(self, MakePlaylist):
        _translate = QtCore.QCoreApplication.translate
        MakePlaylist.setWindowTitle(_translate("MakePlaylist", "Создать плейлист"))
        self.add_file.setText(_translate("MakePlaylist", "Добавит Файл"))
        self.del_file.setText(_translate("MakePlaylist", "Удалить Файл"))
        self.name_playlist_text.setText(_translate("MakePlaylist", "Имя Плейлиста"))
        self.info.setText(_translate("MakePlaylist",
                                     "Чтобы удалить файл надо: дважды нажать на файл в списке и нажать кнопку \'Удалить Файл\'"))
        self.make_playlist.setText(_translate("MakePlaylist", "Создать"))


class MakePlaylist(QMainWindow, Ui_MakePlaylist):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.ico'))
        self.setupUi(self)
        self.dbe = DBEditor()
        self.musics = []
        self.f_name = ''
        self.flag = False
        self.add_file.clicked.connect(self.run_add_file)
        self.make_playlist.clicked.connect(self.run)
        self.del_file.clicked.connect(self.run_del_file)
        self.files.doubleClicked.connect(self.set_flag)

    def run_add_file(self):
        name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        if name not in self.musics and name:
            self.musics.append(name)
            self.files.addItem(name.split('/')[-1])

    def run_del_file(self):
        if self.flag:
            index = self.files.currentIndex().row()
            del self.musics[index]
            self.files.takeItem(index)
        self.flag = False

    def run(self):
        if self.musics:
            if self.playlist_name.text() != '':
                self.dbe.make_playlist(self.playlist_name.text(), self.musics)
            else:
                self.dbe.make_playlist('Новый плейлист', self.musics)
        self.hide()

    def set_flag(self):
        self.flag = True
