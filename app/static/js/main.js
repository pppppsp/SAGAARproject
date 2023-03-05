
const form = document.getElementById('question-form'); // получение формы 
const alertBox = document.getElementById('alertBox') // контейнер с уведомлением

const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value; // csrf


const alerts = (type, text) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
};


//поля формы
const name = document.getElementById('id_name');
const email = document.getElementById('id_email');
const desc = document.getElementById('id_desc');
//

const url = window.location.href // местоположение

form.addEventListener('submit', (e)=>{

    e.preventDefault() // убираем обновление страницы

    const fd = new FormData()

    fd.append('csrfmiddlewaretoken', csrf);
    fd.append('name', name.value);
    fd.append('email', email.value);
    fd.append('desc', desc.value);

    $.ajax({
        type: 'POST', // метод отправки данных POST
        url: url, // нужная ссылка - вызов вьюхи
        data: fd,  // Данные
        success: function(response){ // успешный ответ

            const textSuccess = `Успешно отправлено, ${name.value}!`;
            alerts('success', textSuccess);
            name.value=""
            email.value=""
            desc.value=""

        },
        error: function(error){
            console.log(error);
            const textError = `Введите корректные данные!`;
            alerts('danger', textError);
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});

