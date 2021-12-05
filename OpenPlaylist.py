from os import listdir

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from db_editor import DBEditor


class Ui_OpenPlaylist(object):
    def setupUi(self, OpenPlaylist):
        OpenPlaylist.setObjectName("OpenPlaylist")
        OpenPlaylist.resize(481, 320)
        self.centralwidget = QtWidgets.QWidget(OpenPlaylist)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.playlists = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlists.sizePolicy().hasHeightForWidth())
        self.playlists.setSizePolicy(sizePolicy)
        self.playlists.setMinimumSize(QtCore.QSize(0, 250))
        self.playlists.setObjectName("playlists")
        self.verticalLayout.addWidget(self.playlists)
        self.info = QtWidgets.QLabel(self.centralwidget)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.open = QtWidgets.QPushButton(self.centralwidget)
        self.open.setObjectName("open")
        self.horizontalLayout.addWidget(self.open)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        OpenPlaylist.setCentralWidget(self.centralwidget)

        self.retranslateUi(OpenPlaylist)
        QtCore.QMetaObject.connectSlotsByName(OpenPlaylist)

    def retranslateUi(self, OpenPlaylist):
        _translate = QtCore.QCoreApplication.translate
        OpenPlaylist.setWindowTitle(_translate("OpenPlaylist", "Открыть плейлист"))
        self.info.setText(_translate(
            "OpenPlaylist", "Чтобы выбрать плейлист нужно дважды нажать на плейлист в списке и нажать Открыть"))
        self.open.setText(_translate("OpenPlaylist", "Открыть"))


class OpenPlaylist(QMainWindow, Ui_OpenPlaylist):
    def __init__(self, mw):
        super().__init__()
        self.setWindowIcon(QIcon('icon.ico'))
        self.mw = mw
        self.setupUi(self)
        self.db = DBEditor()
        self.pl_name = None
        self.flag = False
        self.write_names()
        self.res = []
        self.open.clicked.connect(self.run)
        self.playlists.itemDoubleClicked.connect(self.select_name)

    def write_names(self):
        names = self.db.names()
        for i in names:
            self.playlists.addItem(str(i[0]))
        self.playlists.addItem('Выбрать каталог')

    def run(self):
        if self.pl_name == 'Выбрать каталог':
            self.pl_name = QFileDialog.getOpenFileName(self, 'Выбрать каталог', '')[0]
            self.flag = True
        self.end()
        self.flag = False
        self.hide()

    def select_name(self, item):
        self.pl_name = item.text()

    def end(self):
        if self.pl_name:
            res = []
            if self.flag:
                dirr = '/'.join(self.pl_name.split('/')[:len(self.pl_name.split('/')) - 1])
                a = listdir(dirr)
                self.mw.objects.clear()
                for i in a:
                    self.mw.objects.addItem(i)
                    res.append(QMediaContent(QUrl(f'{dirr}/{i}')))
                self.res = res
                self.mw.super_flag = False
            else:
                self.res = self.db.open_playlist(self.pl_name)
                self.mw.objects.clear()
                self.mw.super_flag = True
                for i in self.res:
                    self.mw.objects.addItem(str(i.canonicalUrl().toString().split('/')[-1]))
            self.mw.playlist.clear()
            for i in self.res:
                self.mw.playlist.addMedia(i)
            self.mw.index = 0
            self.mw.player.setMedia(self.mw.playlist.media(self.mw.index))
            self.mw.status_bar.setText(self.mw.playlist.media(self.mw.index).canonicalUrl().toString().split('/')[-1])
            self.mw.player.play()
        self.mw.pl_name = self.pl_name
        self.mw.pl = [i.canonicalUrl().toString() for i in self.res]
        self.mw.objects.setCurrentRow(self.mw.index)
        self.pl_name = None
