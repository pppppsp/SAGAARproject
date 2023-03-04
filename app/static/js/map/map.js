const mapButton = document.getElementsByName('objbut') // получение кнопки с названием спорткомплекса 
const url = window.location.href // данное местоположение пользователя

const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value // получение значения токена

let myMap

ymaps.ready(init);
function init() { // первоначальная карта
    myMap = new ymaps.Map("map", {
        center: [55.755864, 37.617698], // координаты Москвы
        zoom: 10, // увеличение или уменьшение карты
    });
    geobj = new ymaps.GeoObject({
        geometry: {
            type: "Point", // тип указателя 
            coordinates: [55.755864, 37.617698] // координаты, где она будет поставлена
        },
        properties: {
            iconContent: `Москва`, // значение внутри указателя
        }
    }, {
        preset: 'islands#blackStretchyIcon', // тема
    }),
    myMap.geoObjects.add(geobj)
}

$('.objbut').on('click', function (event) { // при клике на кнопку, отправляем первичный ключ и получаем данные. 
    event.preventDefault(); // убираем обновление страниц
    let pk = $(this).data('pk') // запись первичного ключа
    $.ajax({
        url: `${url}get/${pk}`, // нужная ссылка - вызов вьюхи
        type: 'POST', // метод отправки данных POST
        data: { // Данные
            'csrfmiddlewaretoken': csrf, // токен
        },
        success: (res) => { // успешный ответ
            data = res.data[0]; // ответ приходит в виде массива и записываем в переменную data
            // console.log(data)

            if (myMap){ // Если карта существует 
                myMap.destroy(); // удаление карты
            }
            
            ymaps.ready(init);
            function init() {
                // console.log(data.scale_yan_map)
                myMap = new ymaps.Map("map", {
                    center: [data.cen_x, data.cen_y], // координаты местоположения спорткомплекса
                    zoom: data.scale_yan_map // увеличение или уменьшение карты
                });
                geobj = new ymaps.GeoObject({ 
                    // Описание геометрии.
                    geometry: {
                        type: "Point", // тип указателя 
                        coordinates: [data.cen_x, data.cen_y] // координаты, где она будет поставлена
                    },
                    // Свойства.
                    properties: {
                        // Контент метки.
                        iconContent: `${data.name}`, // внутри указателя название  
                        balloonContent: `<h5 style = 'color:#6610f2; font-weight:bold;'>${data.name}</h5> 
                        <p>
                            <b style = 'color:#6610f2'>Электронная почта:</b> ${data.email} <br/>
                            <b style = 'color:#6610f2'>Контактный телефон объекта:</b> ${data.contact_number_object}
                        </p>
                        <p>
                            <b style = 'color:#6610f2'>Краткое описание:</b> ${data.short_descr}
                        </p>
                        <p> 
                            <b style = 'color:#6610f2'>Адрес:</b> ${data.address}
                        </p>
                        `, // содержимое указателя
                    }
                }, {
                    // Опции.
                    // Иконка метки будет растягиваться под размер ее содержимого.
                    preset: 'islands#blackStretchyIcon',
                }),
                myMap.geoObjects.add(geobj)
            }
        },
        error: (res) => { // ответ в виде ошибки 
            console.log('error')
        }
    })
})


const searchForm = document.getElementById('search-form') // поисковая форма
const resultsBox = document.getElementById('results-box') // див с результатами
const searchInput = document.getElementById('search-input') // поисковик


const sendSearchData = (message) => { // переменная с функцией
    $.ajax({
        type: 'POST', // метод пост
        url: `${url}search/`, // куда хотим отправить
        data: {
            'csrfmiddlewaretoken': csrf, // найденный токен 
            'message': message, // передаем значение в views.py
        },
        success: (res) => { // успешный ответ
            const data = res.data // присваиваем в переменную data наш результат.
            if (Array.isArray(data)) { // если это массив
                resultsBox.innerHTML = "" // чтобы после пустого инпута все исчезалось
                data.forEach(data=>{ // вывод через цикл результат

                    const btn = document.createElement('button'); // создание разметки кнопки 
                    btn.className='search_button btn btn-primary m-1' // классы для кнопки
                    btn.innerHTML=`${data.name}` // содержимое кнопки
                    btn.addEventListener('click', ()=>{ // событие для кнопки
                        
                        if (myMap){ // Если карта существует
                            myMap.destroy();// удаление карты
                        }
                        
                        ymaps.ready(init);
                        function init() {
                            // console.log(data.scale_yan_map)
                            myMap = new ymaps.Map("map", {
                                center: [data.cen_x, data.cen_y], // координаты местоположения спорткомплекса
                                zoom: data.scale_yan_map // увеличение или уменьшение карты
                            });
                            geobj = new ymaps.GeoObject({
                                // Описание геометрии.
                                geometry: {
                                    type: "Point", // тип указателя 
                                    coordinates: [data.cen_x, data.cen_y] // координаты, где она будет поставлена
                                },
                                // Свойства.
                                properties: {
                                    // Контент метки.
                                    iconContent: `${data.name}`, // внутри указателя название  
                                    balloonContent: `<h5 style = 'color:#6610f2; font-weight:bold;'>${data.name}</h5>
                                    <p>
                                        <b style = 'color:#6610f2'>Электронная почта:</b> ${data.email} <br/>
                                        <b style = 'color:#6610f2'>Контактный телефон объекта:</b> ${data.contact_number_object}
                                    </p>
                                    <p>
                                        <b style = 'color:#6610f2'>Краткое описание:</b> ${data.short_descr}
                                    </p>
                                    <p> 
                                        <b style = 'color:#6610f2'>Адрес:</b> ${data.address}
                                    </p>
                                    `, // содержимое указателя
                                }
                            }, {
                                // Опции.
                                // Иконка метки будет растягиваться под размер ее содержимого.
                                preset: 'islands#blackStretchyIcon',
                            }),
                            myMap.geoObjects.add(geobj)
                        }

                    });
                    resultsBox.appendChild(btn); // добавляем в коробку с результатами нашу кнопку с событием
                    
                })
            } else { // иначе выводим ничего не найдено
                if (searchInput.value.length > 0) { // если пустой инпут
                    resultsBox.innerHTML = `<b>${data}</b>` // выводим сообщение из вьюхи
                }
                else {
                    resultsBox.classList.add('not_visible')  // делаем коробку display none
                }
            }
        },
        error: (err) => { // ответ в виде ошибки 
            console.log(err)
        },
    })
}

searchInput.addEventListener('keyup', e => { // Событие для поля ввода при нажатии.
    console.log(e.target.value)

    if (resultsBox.classList.contains('not_visible')) { // если результ бокс имеет класс not_visible, то мы ее удаляем.
        resultsBox.classList.remove('not_visible')
    }

    sendSearchData(e.target.value) // отправки содержимых инпута в функцию
})



