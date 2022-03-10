import sqlite3
import os
from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


# Конфигурация
DATABASE = '/tmp/bill.db'
DEBUG = True
SECRET_KEY = "afaabvoirj__bill__allaindemoupu@mail.ru"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'bill.db')))

login_manager = LoginManager(app)
# Перенаправление при неавторизации
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    print(user_id)
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Формирование ответа в виде словаря, а не кортежа
    return conn


# Вторая функция возвращающая словарь
def connect_db2():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# Функция из видео про фласк, она нужн для загрузки "меню" из БД для отображения на главной странице
# При создании экземпляра класса FDataBase, аргументом передается результат вызова функции соединения с БД
# У меня получается два разных способа соединения с БД
# По курсу фласка через FDataBase, а я делал отдельно, нужно будет перенести все на FDataBase
def get_db():
    "Соединение с БД, если оно еще не установленно"
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Чтение всех записей из таблицы
def read_sql3_bill(table):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite с использованием аргумента для определения таблицы")
    query = f"""SELECT * FROM {table} ORDER BY rowid DESC"""
    cur.execute(query)
    records = cur.fetchall()
    print(query)
    print(records)
    print("Количество записей:", len(records))
    cur.close()
    return records


# Добавление нового роутера
def write_sql3_bill_router(data_tuple):
    con = connect_db2()
    cur = con.cursor()
    query = f"""INSERT INTO router (lan_mac, wan_mac, model, user_id, monter, comment, status, date) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


# Добавление новой приставки
def write_sql3_bill_tvip(data_tuple):
    # def write_sql3_bill_tvip(mac, user_id, monter, comment, status, status_num):
    con = connect_db2()
    cur = con.cursor()
    # query = f"""INSERT INTO bill_tvip VALUES ("{mac}", "{user_id}", "{monter}", "{comment}", "{status}", "{status_num}")"""
    # {mac}, {user_id}, {monter}, {comment}, {status}, {status_num}
    query = f"""INSERT INTO tv (mac, user_id, monter, comment, status, date) 
    VALUES (?, ?, ?, ?, ?, ?)"""
    # data_tuple = (mac, user_id, monter, comment, status, status_num)
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


def update_sql3_bill_tvip(data_tuple):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite для обновления")
    query = f"""Update tv set date = ?, user_id = ?, status = ?, monter = ? WHERE rowid = ?"""
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


def update_sql3_bill_router(data_tuple):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite для обновления")
    query = f"""Update router set date = ?, user_id = ?, status = ?, monter = ? WHERE rowid = ?"""
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


def delete_sql3_bill(num, table):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite")
    query = f"""DELETE FROM {table} WHERE rowid = {num}"""
    cur.execute(query)
    con.commit()
    print(query)
    cur.close()
    return


def save_comments_sql3_bill(data_tuple, table):
    con = connect_db2()
    cur = con.cursor()
    query = f"""INSERT INTO {table} (comment, id) 
        VALUES (?, ?)"""
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


# Читаем все записи комментариев для выбранного id
def read_comments_sql3_bill(table, id, rowid="rowid"):
    con = connect_db2()
    cur = con.cursor()
    query = f"""SELECT * FROM {table} where {rowid} = {id}"""
    cur.execute(query)
    records = cur.fetchall()
    print(query)
    cur.close()
    return records


def update_comments_sql3_bill(comment, table, id):
    con = connect_db2()
    cur = con.cursor()
    print(f"Подключен к SQLite для обновления комментария в таблице {table}")
    print(comment)
    print(table)
    print(id)
    query = f"""Update {table} set comment = {comment} WHERE rowid = {id}"""
    cur.execute(query)
    con.commit()
    print(query)
    cur.close()
    return


# Функция автоопределения статуса, работает как для тв так и для роутеров
# Если есть ид пользователя == установлен, нет ид есть монтажник == на руках, иначе == в офисе
def check_tv_status(monter, id_user):
    print(f"ид юзера в проверочной функции:", id_user)
    if id_user:
        print("Вызоз функции проверки. ид юзера есть")
        return "Установлен" # Установлен
    elif monter:
        print("Вызоз функции проверки. ид юзера НЕТУ, но есть монтер")
        return "На руках"  # На руках
    else:
        print("Вызоз функции проверки. Ничего нету")
        return "В офисе" # В офисе


@app.route("/index")
@app.route("/")
@login_required
def index():
    # db = get_db()
    # dbase = FDataBase(db)
    return render_template('index.html', title="Главная")


@app.route("/tv")
@login_required
def index_tv():
    # db = get_db()
    # dbase = FDataBase(db)
    return render_template('tv.html', title="ТВ Приставки")


@app.route("/router")
@login_required
def index_router():
    # db = get_db()
    # dbase = FDataBase(db)
    return render_template('router.html', title="Роутеры")


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установленно'''
    if hasattr(g, "link_db"):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    '''Установление соединяния с БД перед выполнением запроса'''
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == "Allain" and request.form['psw'] == "123":
#         session["userLogged"] = request.form["username"]
#         return redirect(url_for("profile", username=session["userLogged"]))
#     return render_template("login.html", title="Авторизация")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByName(request.form['login'])
        print("Класс FDataBase найден")
        print(user)
        print(request.form['psw'])
        if user and check_password_hash(user[2], request.form['psw']):
            print("Проверка выполненна")
            user_login = UserLogin().create(user)
            print("Создание экземпляра класса прошло успешно")
            print(user_login)
            print(current_user)
            login_user(user_login)
            return redirect(url_for('index_tv'))
        # Могновенные сообщения, курс по Фласку
        # flash("Неверная пара логин/пароль", "error")
        print("ошибка")

    # return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")
    return render_template("login.html", title="Авторизация")


@app.route("/regi", methods=["POST", "GET"])
def register():
    logpsw = 'pbkdf2:sha256:260000$l4FRf4DJeWkAXRN6$b8dc2cd889245f35e87132754e91f784724ccbbf905007e0187d411dea5dc2c7'
    if request.method == "POST":
        if check_password_hash(logpsw, request.form['logpsw']):
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['login'], hash, request.form['name'])

            return redirect(url_for('index_tv'))
    return render_template("reg.html", title="Регистрация")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    print("пользователь вышел из аккаунта")
    # flash("Вы вышли из аккаунта", "success")
    # return redirect(url_for('index'))
    return render_template("login.html", title="Авторизация")


@app.route("/start")
def start():
    # print("Первый запрос")
    response = read_sql3_bill("tv")
    # print(jsonify(response))
    print(f"Текущий пользователь:", current_user.get_name())
    # user_id = current_user.get_id()
    return jsonify(response)


@app.route("/start_router")
def start_router():
    response = read_sql3_bill("router")
    # print(jsonify(response))
    return jsonify(response)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        print(f"Ид приставки", request.get_json())
        print(request)
        user_admin = current_user.get_admin()
        if user_admin == "1":
            delete_sql3_bill(request.get_json(), "tv")
            print("Admin")
        else:
            print("no Admin")

    return "ok"


@app.route("/delete_router", methods=["POST", "GET"])
def delete_router():
    if request.method == "POST":
        # print(f"Ид роутера", request.get_json())
        print(request)
        user_admin = current_user.get_admin()
        if user_admin == "1":
            delete_sql3_bill(request.get_json(), "router")
            print("Admin")
        else:
            print("no Admin")

    return "ok"


@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        data = request.get_json()
        data["status"] = check_tv_status(data["monter"], data["user_id"])
        # Добавляем пользователя к комментарию
        new_comment = str(current_user.get_name()) + ": " + data["comment"]
        data_tuple = (data["mac"], data["user_id"], data["monter"], new_comment, data["status"], data["date"])
        write_sql3_bill_tvip(data_tuple)
    return "ok"


@app.route("/add_router", methods=["POST", "GET"])
def add_router():
    if request.method == "POST":
        data = request.get_json()
        # функция check_tv_status одинаково работает и для роутеров
        data["status"] = check_tv_status(data["monter"], data["user_id"])
        # Добавляем пользователя к комментарию
        new_comment = str(current_user.get_name()) + ": " + data["comment"]
        print(new_comment)
        # data["status"] больше не приходит с фронта, она добавляется результатом выполнения функции
        data_tuple = (data["lan_mac"], data["wan_mac"], data["model"],data["user_id"], data["monter"], new_comment,
                      data["status"], data["date"])
        write_sql3_bill_router(data_tuple)
    return "ok"


@app.route("/save", methods=["POST", "GET"])
def save():
    if request.method == "POST":
        data = request.get_json()
        data["status"] = check_tv_status(data["monter"], data["idUser"])
        # id посылаем последним, чтоб было удобнее использовать его в поиске
        data_tuple = (data["date"], data["idUser"], data["status"], data["monter"], data["id"])
        update_sql3_bill_tvip(data_tuple)
    return "ok"


@app.route("/save_router", methods=["POST", "GET"])
def save_router():
    if request.method == "POST":
        data = request.get_json()
        data["status"] = check_tv_status(data["monter"], data["idUser"])
        # id посылаем последним, чтоб было удобнее использовать его в поиске
        data_tuple = (data["date"], data["idUser"], data["status"], data["monter"], data["id"])
        update_sql3_bill_router(data_tuple)
    return "ok"


@app.route("/save_comment_old", methods=["POST", "GET"])
def save_comment_old():
    if request.method == "POST":
        data = request.get_json()
        data_tuple = (data["comment"], data["id"])
        # Сохраним в одной из таблиц comments
        save_comments_sql3_bill(data_tuple, data["table"])
        # Сложная схема но...
        # Нужно извлечь все комменты для этого id и записать их в основную таблицу
        comments = read_comments_sql3_bill(data["table"], data["id"], "id")
        all_comments = ""
        if data["table"] == "commentsRouter":
            base_comments = read_comments_sql3_bill("router", data["id"], "rowid")
            all_comments += base_comments[0][6]
        elif data["table"] == "commentsTV":
            base_comments = read_comments_sql3_bill("tv", data["id"], "rowid")
            all_comments += base_comments[0][4]
        for x in comments:
            print(type(x[1]))
            all_comments += x[1]
        new_comments = f"'{all_comments}'"
        if data["table"] == "commentsRouter":
            update_comments_sql3_bill(new_comments, "router", data["id"])
        elif data["table"] == "commentsTV":
            update_comments_sql3_bill(new_comments, "tv", data["id"])
    return "ok"


@app.route("/save_comment", methods=["POST", "GET"])
def save_comment():
    if request.method == "POST":
        data = request.get_json()
        base_comments = read_comments_sql3_bill(data["table"], data["id"])
        all_comments = ""
        if data["table"] == "router":
            all_comments += base_comments[0][6]
        if data["table"] == "tv":
            all_comments += base_comments[0][4]
        print(f"base_comments:", base_comments)
        print(f"all_comments:", all_comments)
        print("Смотри выше")
        all_comments += str(current_user.get_name())
        all_comments += ": "
        all_comments += data["comment"]
        print(f"all_comments:", all_comments)
        new_comments = f"'{all_comments}'"
        if data["table"] == "router":
            update_comments_sql3_bill(new_comments, "router", data["id"])
        if data["table"] == "tv":
            update_comments_sql3_bill(new_comments, "tv", data["id"])
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')