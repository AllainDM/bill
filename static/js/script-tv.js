console.log('Скрипт для приставок успешно загружен');

// Первичная загрузка шапки таблицы
// <th class="table-th" id='th-date'>Дата</th>
function tableStart(tab) {
    document.getElementById(`${tab}`).innerHTML = `<tr class="table-color">
            <th class="table-th" id='th-mac'>Мак адрес</th>
            <th class="table-th" id='th-status'>Статус</th>
            <th class="table-th" id='th-monter'>Монтажник</th>
            <th class="table-th" id='th-id'>ИД</th>
            <th class="table-th" id='th-comment'>Комментарий</th>
            <th class="table-th" id='th-btn'></th>
        </tr>`;
}
// Отображаем таблички под разные статусы
// tableStart("tab1");

// Запрос на сервер при загрузке страницы
function start(type) {
    const req = new XMLHttpRequest();
    req.open("GET", `/${type}`);
     req.addEventListener('load', () => {
          const response = JSON.parse(req.responseText);
          console.log(response);
          output(response);
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
};

// Выход
// Кнопка выхода напрямую делает запрос на бек `http://127.0.0.1:5000/logout`
// function logout() {
//     const req = new XMLHttpRequest();
//     req.open("GET", `http://127.0.0.1:5000/logout`);
//      req.addEventListener('load', () => {
//           console.log("Выход из профиля");
//     });
//     req.addEventListener('error', () => {
//         console.log('error')
//     });
//     req.send();
// }

// Отображение ответа с сервера
// Таблица с БД
// 0 - порядковый номер в таблице
// 1 - мак адрес
// 2 - ид пользователя
// 3 - монтажник
// 4 - комментарий
// 5 - статус
//  - id статуса (для упрощения поиска в БД)
// 6 - дата
function output(res) {
    // Убираем лишние шапки табличек
    let tab1 = false;
    let tab2 = false;
    let tab3 = false;
    let tab4 = false;
    res.forEach((item, num) => {
        // Убираю параметр status_id из-за сложностей в автоопределении статуса на беке
        // console.log(`Статус ид: ${item[6]}`);
        // Распределяем по табличкам согласно статусу
        // 1 - пусто
        // 2 - В офисе
        // 3 - На руках
        // 4 - Установлен
        let tab;
        // Если у приставки статус, для таблички которого нет шапки, то она создается
        if (item[5] == "В офисе") {
            if (tab1 == false) {
                tableStart("tab1");
                tab1 = true;
            }
            tab = document.getElementById('tab1');
        } else if (item[5] == "На руках") {
            if (tab2 == false) {
                tableStart("tab2");
                tab2 = true;
            }
            tab = document.getElementById('tab2');
        } else if (item[5] == "Установлен") { 
            if (tab3 == false) {
                tableStart("tab3");
                tab3 = true;
            }
            tab = document.getElementById('tab3');
        } else {
            if (tab4 == false) {
                tableStart("tab4");
                tab4 = true;
            }
            tab = document.getElementById('tab4');
        }
        // Ранее селекту монтер и инпуту для ИД присваивался порядковый номер в массиве, id="monter${num + 1}" и id="idUser${num + 1}", сейчас ид приставки в БД
        // <td id='th-date'>${res[num][6]}</td> 
        tab.insertAdjacentHTML("beforeend", 
                `<tr class="table-color">
                <td id='th-mac'>${res[num][1]}</td> 
                <td id='th-status'>${res[num][5]} <a href="https://bill.unetcom.ru/?mod=usr&act=viewinfo&uid=${res[num][2]}" target="_blank">${res[num][2]}</a> </td> 
                <td id='th-monter'><select id="monter${res[num][0]}">
                    <option value="001">${res[num][3]}</option>
                    <option value="002">Волосевич Дмитрий</option>
                    <option value="003">Комиссаров Александр</option>
                    <option value="004">Маснык Игорь</option>
                    <option value="005">Куропятников Сергей</option>
                    <option value="006">Павлов Юра</option>
                    <option value="007">Соловьев Александр</option>
                    <option value="008">Черных Анатолий</option>
                    <option value="009">Шестаков Владимир</option>
                    <option value="010">неизвестно</option>
                </select></td>
                <td id='th-id'><input type="text" class="input-id" id="idUser${res[num][0]}" size="6px" value="${res[num][2]}"></td> 
                <td id='th-comment'>${res[num][4]}</td> 
                <td id='th-sav${res[num][0]}'><button class="btn-save">Сохранить</button></td>
                <td id='th-comm${res[num][0]}'><button>Доб коммент.</button></td>
                <td id='th-del${res[num][0]}'><button class="btn-del">Удалить</button></td>
                </tr>`
        );
        btnDelete(res[num][0]);
        btnSave(res[num][0]);
        btnComm(res[num][0]);
    });
    //  <td id='th-monter'>${res[num][3]}</td>
    // Вызов функции навешивания событий для кнопок "удалить"
    
    
};

start("start");

// Фукция заменена на общую со вторым аргументом "тип" запроса: postMain
// Добавление приставки на сервер
// POST запрос
// function postTV(tv) {
//     const request = new XMLHttpRequest();
//     request.open('POST', 'http://127.0.0.1:5000/post');
//     request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
//     console.log(JSON.stringify(tv))
//     request.send(JSON.stringify(tv));
// };

// Сбор инфы для отправки на сервер
document.getElementById('add').addEventListener('click', () => {

    let mac = document.getElementById('mac').value;
    if (mac == '') {
        alert('Укажите мак адрес. Так же нужно сделать проверку на правильное написание мак адреса и на его совпадение');
        return;
    };

    let mon = document.getElementById('monter');
    let monter = mon.options[mon.selectedIndex].text;

    // let stat = document.getElementById('status');
    // let status = stat.options[stat.selectedIndex].text;
    // if (status == '') {
    //     alert('Укажите статус(Местонахождение приставки).');
    //     return;
    // };

    let date = new Date().toLocaleString();

    // Возьмем комент со странички и добавим ему время
    let comment = document.getElementById('comment').value;
    if (comment !== "") {
        comment = `${date}: ${comment} </br>`;
    };

    // Удалим коммент на страничке
    document.getElementById('comment').value = '';

    let post = {
        mac: mac,
        user_id: '',
        monter: monter,
        comment: comment,
        // status: status,
        date: date
    };
    console.log(post);

    postMain(post, "post");
});



// Кнопка удалить. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждой приставки, при переборе массива с приставками(function output). 
function btnDelete(num) {
    document.getElementById(`th-del${num}`).addEventListener('click', () => {
        // console.log(`th-del${num}`);
        postMain(num, "delete");
    });
    // console.log(`th-del${num}`);
};

// Кнопка сохранить. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждой приставки, при переборе массива с приставками(function output).
function btnSave(num) {
    document.getElementById(`th-sav${num}`).addEventListener('click', () => {
        saveTV(num);
    });
};

function saveTV(num) {
    console.log(`Сохранить tv с ид: ${num}`);
    date = new Date().toLocaleString();
    idUser = document.getElementById(`idUser${num}`).value;
    console.log(`Ид юзера: ${idUser}`);

    let mon = document.getElementById(`monter${num}`);
    let monter = mon.options[mon.selectedIndex].text;

    let post = {
        date: date,
        id: num,
        idUser: idUser,
        monter: monter,
    }
    postMain(post, "save");

};

function btnComm(num) {
    document.getElementById(`th-comm${num}`).addEventListener('click', () => {
        newComment(num);
    });
};

function newComment(num) {
    let comment = prompt("Введите комментарий");
    date = new Date().toLocaleString();
    if (comment == null) {
        return
    } else {
        comment = `${date}: ${comment} </br>`;
        let post = {
            comment: comment,
            id: num,
            table: "commentsTV"
        };
        postMain(post, "save_comment");
        console.log(comment);
        console.log(num);
    }
    
};

// POST запрос на сервер, первый агрумент ид Приставки, второй "тип" запроса(добавить, удалить, отредактировать...)
function postMain(tv, postType) {
    const request = new XMLHttpRequest();
    request.open('POST', `/${postType}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(tv))
    request.send(JSON.stringify(tv));
    
    request.addEventListener('load', () => {
        console.log("Автообновление");
        start("start");
    });
};

