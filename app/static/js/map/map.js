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
