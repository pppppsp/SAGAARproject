
const form = document.getElementById('p-form'); // reg form
const alertBox = document.getElementById('alertBox')

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

form.addEventListener('submit', (e)=>{

    e.preventDefault()

    const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf);
        fd.append('comment', comment.value);

    $.ajax({
        type: 'POST',
        url: url,
        data: fd,
        success: function(response){
            console.log(response)
            const textSuccess = `Успешно отправлено! Отзыв в рассмотрении.`;
            alerts('success', textSuccess);


            setInterval(()=>{
                comment.value = ""
            }, 2500);
            
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

