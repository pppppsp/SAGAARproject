from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser, CommentUser, ContactUs

class CreateUserForm(UserCreationForm):
    avatar = forms.ImageField(label='Выберите аватарку')
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'avatar',
            'username',
            'password1',
            'password2',
        ]
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'form-control mt-2'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'form-control mt-2'}),
            'patronymic':forms.TextInput(attrs={'placeholder':'Введите отчество', 'class':'form-control', 'style':'margin-top:32px;'}),
            'username':forms.TextInput(attrs={'placeholder':'Введите логин', 'class':'form-control mt-2'}),
            'email':forms.TextInput(attrs={'placeholder':'Введите почту', 'class':'form-control mt-2'}),
        }


class CreateCommentUser(forms.ModelForm):
    class Meta: 
        model = CommentUser
        fields = [
            'comment',
        ]
        widgets = {
            'comment':forms.Textarea(attrs={
                'placeholder':'Введите отзыв',
                'class':'form-control',
                'style':'resize:none;'
            })
        }


class CreateQuestionsUserForm(forms.ModelForm):
    class Meta: 
        model = ContactUs
        fields = [
            'name',
            'email',
            'desc',
        ]
        widgets = {
            'name':forms.TextInput(attrs={
                'placeholder':'Введите имя',
                'class':'form-control',
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'Введите электронный почтовый ящик',
                'class':'form-control',
            }),
            'desc':forms.Textarea(attrs={
                'placeholder':'Введите сообщение',
                'class':'form-control',
                'style':'resize:none;'
            }),
        }
        