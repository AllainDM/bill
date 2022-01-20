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
