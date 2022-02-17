import sqlite3

class Settings():

    def __init__(self):
        self.conn = sqlite3.connect('settings.sqlite')
        self.cur = self.conn.cursor()
        set = self.cur.execute('SELECT * FROM Main')
        row = self.cur.fetchone()
        self.key = row[1]
        self.url = row[2]
        self.lang = row[3]


    def get_api_key(self):
        return self.key


    def get_lang(self):
        return self.lang


    def change_key(self, value):
        try:
            self.cur.execute('UPDATE Main SET key = ?', (value,))
        except:
            return False
        else:
            self.conn.commit()
            self.key = value
            return True


    def change_lang(self, value):
        try:
            self.cur.execute('UPDATE Main SET lang = ?', (value,))
        except:
            return False
        else:
            self.conn.commit()
            self.lang = value
            return True

    def close_connection(self):
        self.conn.close()
