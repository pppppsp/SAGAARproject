
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
const first_name = document.getElementById('id_first_name');
const last_name = document.getElementById('id_last_name');
const patronymic = document.getElementById('id_patronymic');
const username = document.getElementById('id_username');
const avatar = document.getElementById('id_avatar');
const password1 = document.getElementById('id_password1');
const password2 = document.getElementById('id_password2');
const email = document.getElementById('id_email');
//

const url = window.location.href // местоположение

form.addEventListener('submit', (e)=>{

    e.preventDefault()

    const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf);
        fd.append('first_name', first_name.value);
        fd.append('last_name', last_name.value);
        fd.append('patronymic', patronymic.value);
        fd.append('username', username.value);
        fd.append('avatar', avatar.files[0]);
        fd.append('password1', password1.value);
        fd.append('password2', password2.value);
        fd.append('email', email.value);

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){

            const textSuccess = `Успешная регистрация, ${response.name}!`;
            alerts('success', textSuccess);


            setInterval(()=>{
                $(location).prop('href','login/');
            }, 3500);
            
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

