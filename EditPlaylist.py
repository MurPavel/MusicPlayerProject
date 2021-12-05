from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from db_editor import DBEditor


class Ui_EditPlaylist(object):
    def setupUi(self, EditPlaylist):
        EditPlaylist.setObjectName("EditPlaylist")
        EditPlaylist.resize(510, 300)
        self.centralwidget = QtWidgets.QWidget(EditPlaylist)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.name_playlist_text = QtWidgets.QLabel(self.centralwidget)
        self.name_playlist_text.setObjectName("name_playlist_text")
        self.horizontalLayout_2.addWidget(self.name_playlist_text)
        self.playlist_name = QtWidgets.QLineEdit(self.centralwidget)
        self.playlist_name.setObjectName("playlist_name")
        self.horizontalLayout_2.addWidget(self.playlist_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_file = QtWidgets.QPushButton(self.centralwidget)
        self.add_file.setObjectName("add_file")
        self.horizontalLayout.addWidget(self.add_file)
        self.del_file = QtWidgets.QPushButton(self.centralwidget)
        self.del_file.setObjectName("del_file")
        self.horizontalLayout.addWidget(self.del_file)
        self.del_playlist = QtWidgets.QPushButton(self.centralwidget)
        self.del_playlist.setObjectName("del_playlist")
        self.horizontalLayout.addWidget(self.del_playlist)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.info = QtWidgets.QLabel(self.centralwidget)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)
        self.files = QtWidgets.QListWidget(self.centralwidget)
        self.files.setObjectName("files")
        self.verticalLayout.addWidget(self.files)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.save_playlist = QtWidgets.QPushButton(self.centralwidget)
        self.save_playlist.setObjectName("save_playlist")
        self.horizontalLayout_4.addWidget(self.save_playlist)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        EditPlaylist.setCentralWidget(self.centralwidget)

        self.retranslateUi(EditPlaylist)
        QtCore.QMetaObject.connectSlotsByName(EditPlaylist)

    def retranslateUi(self, EditPlaylist):
        _translate = QtCore.QCoreApplication.translate
        EditPlaylist.setWindowTitle(_translate("EditPlaylist", "Редактировать плейлист"))
        self.name_playlist_text.setText(_translate("EditPlaylist", "Имя Плейлиста"))
        self.add_file.setText(_translate("EditPlaylist", "Добавит Файл"))
        self.del_file.setText(_translate("EditPlaylist", "Удалить Файл"))
        self.del_playlist.setText(_translate("EditPlaylist", "Удалить плейлист"))
        self.info.setText(_translate("EditPlaylist",
                                     "Чтобы удалить файл надо: дважды нажать на файл в списке и нажать кнопку \'Удалить Файл\'"))
        self.save_playlist.setText(_translate("EditPlaylist", "Сохранить"))


class EditPlaylist(QMainWindow, Ui_EditPlaylist):
    def __init__(self, mw):
        super().__init__()
        self.setWindowIcon(QIcon('icon.ico'))
        self.mw = mw
        self.setupUi(self)
        self.dbe = DBEditor()
        self.musics = self.mw.pl
        for i in self.musics:
            self.files.addItem(i.split('/')[-1])
        self.f_name = ''
        self.flag = False
        self.playlist_name.setText(self.mw.pl_name)
        self.add_file.clicked.connect(self.run_add_file)
        self.save_playlist.clicked.connect(self.run)
        self.del_file.clicked.connect(self.run_del_file)
        self.files.doubleClicked.connect(self.set_flag)
        self.del_playlist.clicked.connect(self.win_del_playlist)

    def run_add_file(self):
        name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        if name not in self.musics and name:
            self.musics.append(name)
            self.files.addItem(name.split('/')[-1])

    def win_del_playlist(self):
        valid = QMessageBox.question(self, 'Удалить', "Действительно удалить плейлист?",
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.dbe.del_playlist(self.mw.pl_name)
            self.hide()

    def run_del_file(self):
        if self.flag:
            index = self.files.currentIndex().row()
            del self.musics[index]
            self.files.takeItem(index)
        self.flag = False

    def run(self):
        self.mw.player.stop()
        self.mw.objects.clear()
        self.dbe.del_playlist(self.mw.pl_name)
        if self.musics:
            if self.playlist_name.text() != '':
                self.dbe.make_playlist(self.playlist_name.text(), self.musics)
            else:
                self.dbe.make_playlist('Новый плейлист', self.musics)
        self.mw.playlist.clear()
        self.mw.index = 0
        self.mw.content = QMediaContent()
        self.mw.player.setMedia(self.mw.content)
        self.mw.status_bar.setText('Нет открытых файлов')
        self.mw.run_open_playlist()
        self.hide()

    def set_flag(self):
        self.flag = True
