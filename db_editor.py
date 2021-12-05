import sqlite3

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent

NAME_DB = 'playlists.db'


class DBEditor:
    def __init__(self):
        self.con = sqlite3.connect(NAME_DB)
        self.cur = self.con.cursor()

    def names(self):
        result = self.cur.execute(f"""SELECT name_playlist FROM playlists""").fetchall()
        return result

    def open_playlist(self, name):
        res = []
        result = self.cur.execute(f"""SELECT data FROM playlists WHERE name_playlist='{name}'""").fetchall()
        result = result[0][0].split(':;:')
        for i in result:
            res.append(QMediaContent(QUrl(i)))
        return res

    def make_playlist(self, name_playlist, data):
        data = ':;:'.join(data)
        name = self.cur.execute(f"""SELECT name_playlist FROM playlists""").fetchall()
        name = [i[0] for i in name]
        if name_playlist in name:
            name_playlist = name_playlist + '2'
            while name_playlist in name:
                name_playlist = str(name_playlist[:len(name_playlist) - 1]) + str(int(name_playlist[-1]) + 1)
        result = self.cur.execute(f"""INSERT INTO playlists(name_playlist,data) VALUES("{name_playlist}",'{data}')""")
        self.con.commit()

    def del_playlist(self, name):
        self.cur.execute(f"""DELETE FROM playlists WHERE name_playlist = '{name}'""")
        self.con.commit()
