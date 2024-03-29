class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print("Поиск ид юзера")
        return str(self.__user['id'])

    def get_name(self):
        print("Поиск имени юзера")
        return str(self.__user['name'])

    def get_admin(self):
        print("Проверка на админку")
        return str(self.__user['admin'])
