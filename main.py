import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from EditPlaylist import EditPlaylist
from MainWindow import Ui_MainWindow
from MakePlaylist import MakePlaylist
from OpenPlaylist import OpenPlaylist


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.pixmap = QPixmap('image.jpg')
        self.image.setPixmap(self.pixmap)

        self.flag = True
        self.super_flag = False

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.PlaybackMode(QMediaPlaylist.Loop)
        self.index = 0
        self.player.setPlaylist(self.playlist)
        self.content = QMediaContent()
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.pl = []
        self.pl_name = ''

        self.open.clicked.connect(self.run_open_file)
        self.open_playlist.clicked.connect(self.run_open_playlist)
        self.make_playlist.clicked.connect(self.run_make_playlist)
        self.edit_playlist.clicked.connect(self.run_edit_playlist)
        self.play.clicked.connect(self.run_play)
        self.stop.clicked.connect(self.run_stop)
        self.before.clicked.connect(self.run_before)
        self.next.clicked.connect(self.run_next)
        self.rewind_back.clicked.connect(self.run_rewind_back)
        self.rewind_forward.clicked.connect(self.run_rewind_forward)

        self.open_file_action.triggered.connect(self.run_open_file)
        self.open_pleylist_action.triggered.connect(self.run_open_playlist)
        self.make_pleylist_action.triggered.connect(self.run_make_playlist)
        self.edit_playlist_action.triggered.connect(self.run_edit_playlist)

        self.volume.valueChanged.connect(self.volume_change)
        self.speed.valueChanged.connect(self.speed_change)
        self.speed.sliderPressed.connect(self.speed_return)
        self.position.sliderMoved.connect(self.duration_position_changed)

        self.objects.itemDoubleClicked.connect(self.run_select_music)

        self.open_playlist_win = OpenPlaylist(self)
        self.make_playlist_win = MakePlaylist()
        self.edit_playlist_win = EditPlaylist(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.run_rewind_forward()
        elif event.key() == Qt.Key_Left:
            self.run_rewind_back()
        elif event.key() == Qt.Key_Space:
            if self.flag:
                self.run_stop()
            else:
                self.run_play()
        elif event.key() == Qt.Key_Up:
            self.volume.setValue(self.volume.value() + 5)
        elif event.key() == Qt.Key_Down:
            self.volume.setValue(self.volume.value() - 5)
        elif event.key() == Qt.Key_D:
            self.run_next()
        elif event.key() == Qt.Key_A:
            self.run_before()
        elif event.key() == Qt.Key_W:
            self.speed.setValue(self.speed.value() + 5)
        elif event.key() == Qt.Key_S:
            self.speed.setValue(self.speed.value() - 5)

    def position_changed(self, position):
        self.position.setValue(position)
        if self.position.value() >= self.player.duration() - 1000 and self.flag and self.position.value() > 1000:
            self.run_next()

    def duration_changed(self, duration):
        self.position.setRange(0, duration)

    def duration_position_changed(self, value):
        self.player.setPosition(value)

    def run_open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        if name:
            self.status_bar.setText(name.split('/')[-1])
            self.objects.clear()
            self.objects.addItem(name.split('/')[-1])
            self.content = QMediaContent(QUrl(name))
            self.playlist.clear()
            self.playlist.addMedia(self.content)
            self.player.setMedia(self.playlist.media(0))
            self.player.play()
            self.index = 0
            self.pl_name = ''
            self.super_flag = False
            self.objects.setCurrentRow(self.index)

    def run_open_playlist(self):
        self.open_playlist_win = OpenPlaylist(self)
        self.open_playlist_win.show()

    def run_make_playlist(self):
        self.make_playlist_win = MakePlaylist()
        self.make_playlist_win.show()

    def run_edit_playlist(self):
        if self.pl_name and self.super_flag:
            self.edit_playlist_win = EditPlaylist(self)
            self.edit_playlist_win.show()

    def run_play(self):
        self.player.play()
        self.flag = True

    def run_stop(self):
        self.player.pause()
        self.flag = False

    def run_before(self):
        self.player.stop()
        self.index -= 1
        if self.index == - 1:
            self.index = self.playlist.mediaCount() - 1
        self.content = self.playlist.media(self.index)
        self.player.setMedia(self.content)
        self.set_text()
        self.objects.setCurrentRow(self.index)
        self.run_play()

    def run_next(self):
        self.player.stop()
        self.index += 1
        if self.index == self.playlist.mediaCount():
            self.index = 0
        self.content = self.playlist.media(self.index)
        self.player.setMedia(self.content)
        self.set_text()
        self.objects.setCurrentRow(self.index)
        self.run_play()

    def run_rewind_back(self):
        self.player.setPosition(self.player.position() - 5000)

    def run_rewind_forward(self):
        self.player.setPosition(self.player.position() + 5000)

    def volume_change(self, value):
        self.player.setVolume(value)

    def speed_change(self, value):
        self.player.setPlaybackRate(value / 100)

    def speed_return(self):
        self.speed.setValue(100)

    def set_text(self):
        self.status_bar.setText(self.content.canonicalUrl().toString().split('/')[-1])

    def run_select_music(self):
        self.player.stop()
        self.index = self.objects.currentIndex().row()
        self.content = self.playlist.media(self.index)
        self.player.setMedia(self.content)
        self.player.play()
        self.set_text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())
