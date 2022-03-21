console.log('Скрипт для роутеров успешно загружен');

// Массив с маками роутеров, для проверки совпадения до отправки на сервер
let arrMacRouter = [];

// Первичная загрузка шапки таблицы
// <th class="table-th" id='th-date'>Дата</th>
function tableStart(tab) {
    document.getElementById(`${tab}`).innerHTML = `<tr class="table-color">
            <th class="table-th" id='th-model'>Модель</th>
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
    startName("start_name")
};

// Запрос имени пользователя 
function startName(type) {
    const req = new XMLHttpRequest();
    req.open("GET", `/${type}`);
    req.addEventListener('load', () => {
          const response = JSON.parse(req.responseText);
          console.log(response);
          document.getElementById("user-name").innerText = `Пользователь: ${response}`
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
};

// Отображение ответа с сервера
// Таблица с БД
// 0 - порядковый номер в таблице
// 1 - wan мак адрес  Делаем конвертацию на фронте
// 2 - lan мак адрес
// 3 - модель роутера
// 4 - ид пользователя
// 5 - монтажник
// 6 - комментарий
// 7 - статус
// нет - id статуса (для упрощения поиска в БД)
// 8 - дата
function output(res) {
    // Убираем лишние шапки табличек
    let tab1 = false;
    let tab2 = false;
    let tab3 = false;
    let tab4 = false;
    // Обязательно очистим все таблицы, иначе будет баг с удалением/перепещением последней записи
    document.getElementById('tab1').innerHTML = "";
    document.getElementById('tab2').innerHTML = "";
    document.getElementById('tab3').innerHTML = "";
    document.getElementById('tab4').innerHTML = "";

    arrMacRouter = []; // Очистим общий массив с маками роутеров

    res.forEach((item, num) => {
        arrMacRouter.push(res[num][2]);
        // console.log(arrMacRouter);
        // Убираю параметр status_id из-за сложностей в автоопределении статуса на беке
        // console.log(`Статус ид: ${item[6]}`);
        // Распределяем по табличкам согласно статусу
        // 1 - пусто
        // 2 - В офисе
        // 3 - На руках
        // 4 - Установлен
        let tab;
        // Если у приставки статус, для таблички которого нет шапки, то она создается
        if (item[7] == "В офисе") {
            if (tab1 == false) {
                tableStart("tab1");
                tab1 = true;
            }
            tab = document.getElementById('tab1');
        } else if (item[7] == "На руках") {
            if (tab2 == false) {
                tableStart("tab2");
                tab2 = true;
            }
            tab = document.getElementById('tab2');
        } else if (item[7] == "Установлен") { 
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
        // <td id='th-mac'>${res[num][2]}</td> 
        // <td id='th-date'>${res[num][8]}</td> 
        // <td id='th-commTEST${res[num][0]}'><button>Доб коммент.</button></td>
        
        tab.insertAdjacentHTML("beforeend", 
                `<tr class="table-color">
                <th id='th-model'>${res[num][3]}</th>
                <td id='th-mac'>lan: ${res[num][2]}<br> <a href="https://bill.unetcom.ru/?mod=usr&act=list&go=1&search_segment=1&searchid=&search_kurator=0&search_region=0&search_district=&objid=&street=&objectname=&par=&flor=&flat=&wherefind=fullname&part=all&query=&searchip=&searchmac=${res[num][1]}&searchphonenum=&searchemail=&search_service=&search_tarif_type=now&search_tarifperiod_datestart=&search_tarifperiod_dateend=&abonement_when=now&search_abonement_id=&userstatus=-2&statusdatefrom=&statusdateto=&cli_type=-1&paytype=-1&speedtype=&isvip=&minbalanceznak=%3E&minbalance=&dc_nickname=&user_comment=&go=1&go=%CD%E0%E9%F2%E8+%EF%EE%EB%FC%E7%EE%E2%E0%F2%E5%EB%FF" target="_blank">wan: ${res[num][1]}</a></td> 
                <td id='th-status'>${res[num][7]} <a href="https://bill.unetcom.ru/?mod=usr&act=viewinfo&uid=${res[num][4]}" target="_blank">${res[num][4]}</a></td> 
                <td id='th-monter'><select id="monter${res[num][0]}">
                    <option value="001">${res[num][5]}</option>
                    <option value="002"></option>
                    <option value="003">Волосевич Дмитрий</option>
                    <option value="004">Комиссаров Александр</option>
                    <option value="005">Маснык Игорь</option>
                    <option value="006">Куропятников Сергей</option>
                    <option value="007">Павлов Юра</option>
                    <option value="008">Соловьев Александр</option>
                    <option value="009">Черных Анатолий</option>
                    <option value="010">Шестаков Владимир</option>
                    <option value="011">неизвестно</option>
                    <option value="012"></option>
                </select></td>
                <td id='th-id'><input type="text" class="input-id" id="idUser${res[num][0]}" size="6px" value="${res[num][4]}"></td> 
                <td><span id='th-comm${res[num][0]}' class="add-comm">добавить</br></span>${res[num][6]}</td> 
                <td id='th-sav${res[num][0]}'><button class="btn-save">Сохранить</button></td>
                <td id='th-arch${res[num][0]}'><button class="btn-arch">В архив</button></td>
                <td id='th-del${res[num][0]}'><button class="btn-del">Удалить</button></td>
                </tr>`
        );
        //Вызов функций навешивания событий на кнопки
        btnDelete(res[num][0]);
        btnSave(res[num][0]);
        btnComm(res[num][0]);
        btnArch(res[num][0]);
    });
};

start("start_router");

// Список архивных роутеров
document.getElementById('router-archive').addEventListener("click", () => {
    // a = document.querySelector('container-added')
    // console.log(a)
    const req = new XMLHttpRequest();
    req.open("GET", `/router_archive`);
    req.addEventListener('load', () => {
          const response = JSON.parse(req.responseText);
          console.log(response);
          outputArchive(response);
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();

    
});

function outputArchive(response) {

    tab = document.getElementById('tab5');

    tableStart("tab5");

    document.getElementById('tab1').innerHTML = "";
    document.getElementById('tab2').innerHTML = "";
    document.getElementById('tab3').innerHTML = "";
    document.getElementById('tab4').innerHTML = "";

    response.forEach((item, num) => {
        tab.insertAdjacentHTML("beforeend", 
                `<tr class="table-color">
                <th id='th-model'>${response[num][4]}</th>
                <td id='th-mac'>lan: ${response[num][3]}<br> <a href="https://bill.unetcom.ru/?mod=usr&act=list&go=1&search_segment=1&searchid=&search_kurator=0&search_region=0&search_district=&objid=&street=&objectname=&par=&flor=&flat=&wherefind=fullname&part=all&query=&searchip=&searchmac=${response[num][2]}&searchphonenum=&searchemail=&search_service=&search_tarif_type=now&search_tarifperiod_datestart=&search_tarifperiod_dateend=&abonement_when=now&search_abonement_id=&userstatus=-2&statusdatefrom=&statusdateto=&cli_type=-1&paytype=-1&speedtype=&isvip=&minbalanceznak=%3E&minbalance=&dc_nickname=&user_comment=&go=1&go=%CD%E0%E9%F2%E8+%EF%EE%EB%FC%E7%EE%E2%E0%F2%E5%EB%FF" target="_blank">wan: ${response[num][2]}</a></td> 
                <td id='th-status'>В архиве</a></td> 
                <td id='th-monter'>${response[num][6]}</td>
                <td id='th-id'><a href="https://bill.unetcom.ru/?mod=usr&act=viewinfo&uid=${response[num][5]}" target="_blank">${response[num][5]}</a></td> 
                <td><span id='th-comm${response[num][1]}'</span>${response[num][7]}</td> 
                
                </tr>`)
    })

    
}

// Сбор инфы для отправки на сервер
document.getElementById('add').addEventListener('click', () => {

    // let mac = document.getElementById('mac').value.toLowerCase();
    let mac2 = document.getElementById('mac').value;
    let mac =  mac2.toLowerCase();
    // console.log(typeof(mac));
    // String(mac);
    // mac.toLowerCase();
    if (mac == '') {
        alert('Укажите мак адрес.');
        return;
    } else if (arrMacRouter.includes(`${mac}`)) {
        alert("Такой мак уже есть.");
        return;
    }  else if (mac.length < 12) {
        alert("Слишком короткий мак адрес.");
        return;
    } else if (mac.length > 12) {
        alert("Слишком длинный мак адрес.");
        return;
    }

    console.log(arrMacRouter.includes(`${mac}`));
    // arrMacRouter.indexOf('mac');

    let wanMac = convertMac(mac);

    let mon = document.getElementById('monter');
    let monter = mon.options[mon.selectedIndex].text;

    let mod = document.getElementById('model');
    let model = mod.options[mod.selectedIndex].text;

    if (model == '') {
        alert('Укажите модель роутера');
        return;
    };
  
    let date = new Date().toLocaleString("ru");

    // Возьмем комент со странички и добавим ему время
    let comment = document.getElementById('comment').value;
    if (comment !== "") {
        comment = `${date}: ${comment} </br>`;
    } else {
        comment = `Добавленно: ${date} </br>`;
    };
    

    let post = {
        lan_mac: mac,
        wan_mac: wanMac,
        model: model,
        user_id: '',
        monter: monter,
        comment: comment,
        // status: status,
        // status_id: status_id,
        date: date
    };
    // console.log(post);

    result = confirm(`
    Проверьте данные: 
    Монтажник: ${post["monter"]} 
    Модель: ${post["model"]}
    Мак: ${post["lan_mac"]}
    Комментарий: ${document.getElementById('comment').value}`)

    if (result) {
        postMain(post, "add_router");
        // Удалим коммент на страничке
        document.getElementById('comment').value = '';
    };
    

    // Делаем запрос для получения обновленной информации
    // !!! Не работает, нужно поработать на коллбеком
    // !!!  Два раза отображает таблицу
    // start();
});

// Конвертируем lan mac в wan mac.

function hex2dec(hex) { // 16 в 10
  return parseInt(hex,16); 
}

function dec2hex(hex) { // 10 в 16
  return Number(hex).toString(16);
}

function convertMac(mac) { // Функция преобразует мак в десятичное и обратно, между добавляя 1 к значению
    let macConvert = hex2dec(mac);
    
    macConvert += 1;
    macConvert = dec2hex(macConvert);

    // Если вначале мака нули, то они удаляются, возвращаем просто считая сколько осталось символов и добавляя нужное количество до 12ти
    if (macConvert.length < 12) {
        let a = ""
        for (let x = 1; x <= 12 - macConvert.length; x++) {
            a += "0"
        }
        macConvert = a + macConvert;
    }
    // console.log(`Мак: ${macConvert}`)
    return macConvert
}

// Кнопка удалить. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждого роутера, при переборе массива с роутерами(function output).
function btnDelete(num) {
    document.getElementById(`th-del${num}`).addEventListener('click', () => {
        postMain(num, "delete_router");
    });
};

// Кнопка сохранить. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждого роутера, при переборе массива с роутерами(function output).
function btnSave(num) {
    document.getElementById(`th-sav${num}`).addEventListener('click', () => {
        saveTV(num);
    });
};

// Кнопка добавить комментарий. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждого роутера, при переборе массива с роутерами(function output).
function btnComm(num) {
    document.getElementById(`th-comm${num}`).addEventListener('click', () => {
        newComment(num);
    });
};

// Кнопка отправить в архив. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждого роутера, при переборе массива с роутерами(function output).
function btnArch(num) {
    
    document.getElementById(`th-arch${num}`).addEventListener('click', () => {
        a = document.getElementById(`idUser${num}`);
        // console.log(a);
        postMain(num, "to_archive_router");

    });
};

function saveTV(num) {
    // console.log(`Сохранить tv с ид: ${num}`);
    date = new Date().toLocaleString("ru");
    idUser = document.getElementById(`idUser${num}`).value;
    // console.log(`Ид юзера: ${idUser}`);

    let mon = document.getElementById(`monter${num}`);
    let monter = mon.options[mon.selectedIndex].text;

    let post = {
        date: date,
        id: num,
        idUser: idUser,
        monter: monter,
    }
    postMain(post, "save_router");

};



function newComment(num) {
    let comment = prompt("Введите комментарий");
    // console.log(comment);
    date = new Date().toLocaleString("ru");
    console.log(date);
    if (comment == null) {
        return;
    } else {
        comment = `${date}: ${comment} </br>`;
        console.log(comment);
        let post = {
            comment: comment,
            id: num,
            table: "router"
        };
        postMain(post, "save_comment");
        // console.log(comment);
        // console.log(num);
    }
    
};

// POST запрос на сервер, первый агрумент ид Приставки, второй "тип" запроса(добавить, удалить, отредактировать...)
function postMain(router, postType) {
    const request = new XMLHttpRequest();
    request.open('POST', `/${postType}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(router))
    request.send(JSON.stringify(router));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        start("start_router");
    });
};

