import sqlite3
import os
from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from UserLogin import UserLogin


# Конфигурация
DATABASE = '/tmp/bill_tvip.db'
DEBUG = True
SECRET_KEY = "afaabvoirj__bill__allaindemoupu@mail.ru"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'bill_tvip.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    print(user_id)
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row # Формирование ответа в виде словаря, а не кортежа
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


# Функция из видео про фласк, она нужн дл язагрузки "меню" из БД для отображения на главной странице
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


def read_sql3_bill_tvip():
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite")
    query = f"""SELECT * FROM tv"""
    cur.execute(query)
    records = cur.fetchall()
    print(query)
    print(records)
    print(f"Количество записей: {len(records)}")
    print("Количество записей: ", {len(records)})
    print("Количество записей: ", len(records))
    print("Количество записей:", len(records))
    cur.close()
    return records


def write_sql3_bill_tvip(data_tuple):
# def write_sql3_bill_tvip(mac, user_id, monter, comment, status, status_num):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite")
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
    print("Подключен к SQLite для одновления")
    query = f"""Update tv set date = ?, user_id = ?, status = ?, monter = ? WHERE rowid = ?"""
    cur.execute(query, data_tuple)
    con.commit()
    print(query)
    cur.close()
    return


def delete_sql3_bill_tvip(num):
    con = connect_db2()
    cur = con.cursor()
    print("Подключен к SQLite")
    query = f"""DELETE FROM tv WHERE rowid = {num}"""
    cur.execute(query)
    con.commit()
    print(query)
    cur.close()
    return


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
    return render_template('index.html', title="bill-storage v.0.1")


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
            # print(user_login[0])
            login_user(user_login)
            return redirect(url_for('index'))
        # Могновенные сообщения, курс по Фласку
        # flash("Неверная пара логин/пароль", "error")
        print("ошибка")

    # return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")
    return render_template("login.html", title="Авторизация")


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
    print("Первый запрос")
    response = read_sql3_bill_tvip()
    # print(response)
    print(jsonify(response))
    return jsonify(response)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        print(f"Ид приставки", request.get_json())
        print(request)
        print("Запрос")
        delete_sql3_bill_tvip(request.get_json())
    return "ok"


@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        data = request.get_json()
        print(data["mac"])
        print(data["user_id"])
        print(data["monter"])
        print(data["comment"])
        print(data["status"])
        # print(data["status_id"])
        print(data["date"])
        # data["comment"] = "Подменный коммент"
        # if data["user_id"] > 0:
        #     print("Указан ид юзера")
        print(check_tv_status(data["monter"], data["user_id"]))
        data["status"] = check_tv_status(data["monter"], data["user_id"])
        # write_sql3_bill_tvip(test["mac"], test["user_id"], test["monter"], test["comment"], test["status"],
        #                      test["status_num"])
        data_tuple = (data["mac"], data["user_id"], data["monter"], data["comment"], data["status"], data["date"])
        write_sql3_bill_tvip(data_tuple)
        print(data_tuple)
        print("Выше был тюпл")
        # write_sql3_bill_tvip(1,2,3,4,5,6)
    return "ok"


@app.route("/save", methods=["POST", "GET"])
def save():
    if request.method == "POST":
        data = request.get_json()
        data["status"] = check_tv_status(data["monter"], data["idUser"])
        # id посылаем последним, чтоб было удобнее использовать его в поиске
        data_tuple = (data["date"], data["idUser"], data["status"], data["monter"], data["id"])
        print(data["date"])
        print(data["id"])
        print(data["idUser"])
        update_sql3_bill_tvip(data_tuple)
        print(data_tuple)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')