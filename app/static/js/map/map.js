const mapButton = document.getElementsByName('objbut')
const url = window.location.href

const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value

let myMap

ymaps.ready(init);
function init() {
    myMap = new ymaps.Map("map", {
        center: [55.755864, 37.617698],
        zoom: 10,
    });
    geobj = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [55.755864, 37.617698]
        },
        properties: {
            iconContent: `Москва`,
        }
    }, {
        preset: 'islands#blackStretchyIcon',
        draggable: true
    }),
    myMap.geoObjects.add(geobj)
}

$('.objbut').on('click', function (event) { // при клике на кнопку, отправляем первичный ключ и получаем данные. 
    event.preventDefault();
    let pk = $(this).data('pk')
    $.ajax({
        url: `${url}get/${pk}`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf,
        },
        success: (res) => {
            data = res.data[0];
            // console.log(data)

            if (myMap){ // Если карта существует
                myMap.destroy();
            }
            
            ymaps.ready(init);
            function init() {
                // console.log(data.scale_yan_map)
                myMap = new ymaps.Map("map", {
                    center: [data.cen_x, data.cen_y],
                    zoom: data.scale_yan_map
                });
                geobj = new ymaps.GeoObject({
                    // Описание геометрии.
                    geometry: {
                        type: "Point",
                        coordinates: [data.cen_x, data.cen_y]
                    },
                    // Свойства.
                    properties: {
                        // Контент метки.
                        iconContent: `${data.name}`,
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
                        `,
                    }
                }, {
                    // Опции.
                    // Иконка метки будет растягиваться под размер ее содержимого.
                    preset: 'islands#blackStretchyIcon',
                    // Метку можно перемещать.
                    draggable: true
                }),
                myMap.geoObjects.add(geobj)
            }
        },
        error: (res) => {
            console.log('error')
        }
    })
})


const searchForm = document.getElementById('search-form')
const resultsBox = document.getElementById('results-box')
const searchInput = document.getElementById('search-input')

// console.log(`${url}search/2`)
const sendSearchData = (message) => {
    $.ajax({
        type: 'POST', // метод пост
        url: `${url}search/`, // куда хотим отправить
        data: {
            'csrfmiddlewaretoken': csrf, // найденный токен 
            'message': message, // передаем значение в views.py
        },
        success: (res) => {
            const data = res.data // присваиваем в переменную data наш результат.
            console.log()
            if (Array.isArray(data)) { // если это массив
                resultsBox.innerHTML = "" // чтобы после пустого инпута все исчезалось
                data.forEach(data=>{ // вывод через цикл результат

                    // resultsBox.innerHTML += `
                    // <button data-pk='${data.id}' data-name='${data.name}' data-email = '${data.email}' data-contact='${data.contact_number_object}' data-desc='${data.short_descr}' data-address='${data.address}' data-x='${data.cen_x}' data-y='${data.cen_y}' data-scale='${data.scale_yan_map}' class = 'search_button btn btn-primary mt-2'>
                    //     <p>${data.name}</p>
                    // </button>
                    // `
                    const btn = document.createElement('button');
                    btn.className='search_button btn btn-primary mt-2'
                    btn.innerHTML=`${data.name}`
                    btn.addEventListener('click', ()=>{
                        
                        if (myMap){ // Если карта существует
                            myMap.destroy();
                        }
                        
                        ymaps.ready(init);
                        function init() {
                            // console.log(data.scale_yan_map)
                            myMap = new ymaps.Map("map", {
                                center: [data.cen_x, data.cen_y],
                                zoom: data.scale_yan_map
                            });
                            geobj = new ymaps.GeoObject({
                                // Описание геометрии.
                                geometry: {
                                    type: "Point",
                                    coordinates: [data.cen_x, data.cen_y]
                                },
                                // Свойства.
                                properties: {
                                    // Контент метки.
                                    iconContent: `${data.name}`,
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
                                    `,
                                }
                            }, {
                                // Опции.
                                // Иконка метки будет растягиваться под размер ее содержимого.
                                preset: 'islands#blackStretchyIcon',
                                // Метку можно перемещать.
                                draggable: true
                            }),
                            myMap.geoObjects.add(geobj)
                        }

                    });
                    resultsBox.appendChild(btn);
                    
                })
            } else { // иначе выводим ничего не найдено
                if (searchInput.value.length > 0) { // если пустой инпут
                    resultsBox.innerHTML = `<b>${data}</b>` // выводим сообщение из вьюхи
                }
                else {
                    resultsBox.classList.add('not_visible')
                }
            }
        },
        error: (err) => {
            // console.log(err)
        },
    })
}

searchInput.addEventListener('keyup', e => { // Событие для поля ввода при нажатии.
    console.log(e.target.value)

    if (resultsBox.classList.contains('not_visible')) { // если результ бокс имеет класс not_visible, то мы ее удаляем.
        resultsBox.classList.remove('not_visible')
    }

    sendSearchData(e.target.value)
})

function hello(){
    console.log('hello')
}



