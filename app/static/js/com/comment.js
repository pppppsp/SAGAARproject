
const form = document.getElementById('p-form'); // получение формы 
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
const comment = document.getElementById('id_comment');
//

const url = window.location.href // местоположение

form.addEventListener('submit', (e)=>{ // событие при submit

    e.preventDefault() // убираем обновление страницы

    const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf);
        fd.append('comment', comment.value);

    $.ajax({
        type: 'POST', // метод отправки данных POST
        url: url, // нужная ссылка - вызов вьюхи
        data: fd, // Данные
        success: function(response){ // успешный ответ
            // console.log(response)
            const textSuccess = `Успешно отправлено! Отзыв в рассмотрении.`;
            alerts('success', textSuccess); 

            comment.value = ""
            
        },
        error: function(error){ 
            // console.log(error);
            const textError = `Введите корректные данные!`;
            alerts('danger', textError);
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});

