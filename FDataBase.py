import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addUser(self, login, hpsw, name):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE login LIKE '{login}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким логином уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (login, hpsw, name))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUserByName(self, name):
        # try:
        print("Ищем в таблице")
        print("Пользователь:", name)
        # self.__cur.execute(f"""SELECT * FROM users WHERE login LIKE "%{name}%" LIMIT 1""")
        print("Поиск 1 в таблице произведен")
        self.__cur.execute(f"SELECT * FROM users WHERE login = '{name}' LIMIT 1")
        print("Поиск в таблице произведен")
        res = self.__cur.fetchone()
        if not res:
            print("Пользователь не найден")
            return False

        return res
        # except sqlite3.Error as e:
        #     print("Ошибка получения данных из БД " +str(e))

        return False
