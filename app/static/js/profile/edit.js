const form = document.getElementById('edit_form'); // reg form
const alertBox = document.getElementById('alertBox')
const url = window.location.href


const alerts = (type, text) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
};


form.addEventListener('submit', (e)=>{

    e.preventDefault();

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value; // csrf
    const email = document.getElementById('id_email')
    const avatar = document.getElementById('id_avatar')
    const old_password = document.getElementById('id_password')
    const new_password1 = document.getElementById('id_password1')
    const new_password2 = document.getElementById('id_password2')


    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf);
    fd.append('avatar', avatar.files[0]);
    fd.append('old_password', old_password.value);
    fd.append('password1', new_password1.value);
    fd.append('password2', new_password2.value);
    fd.append('email', email.value);

    $.ajax({
        type:"POST",
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: (response)=>{
            message = response['message']
            console.log(message)
            if (response['status'] == 'error') {
                alerts('danger', message)
            } else { 
                alerts('success', message)
                setInterval(()=>{
                    $(location).prop('href','/');
                }, 2500);
            }
        },
        error: (response)=>{
            console.log(response)
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});

