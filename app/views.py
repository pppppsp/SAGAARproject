from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import pandas as pd
from app.models import CustomUser
from app.forms import CreateUserForm, CreateCommentUser, CreateQuestionsUserForm, EditProfileData
from django.core.validators import validate_email

def pieData(): # получение данных для пирога
    for_pie_labels = [] # список для названий спорткомплексов 
    for_pie_data = [] # пустой список для данных спорткомплексов

    query_datas = Datas.objects.order_by("-financing")[:7] # получение 7 записей спорткомплексов с сортировкой по финансам в порядке убывания

    for q in query_datas: # запись через цикл 
        for_pie_labels.append(q.name) # добавление в список для названий
        for_pie_data.append(q.financing) # добавление в список для данных

    
    return for_pie_data, for_pie_labels # возвращаем списки


def lineData(): # получение данных для графика
    for_line_labels = [] # список для названий спорткомплексов 
    for_line_data = [] # пустой список для данных спорткомплексов
    
    query_datas = Datas.objects.order_by("-financing_from_subject_federal_budget")[:10] # получение 10 записей спорткомплексов с сортировкой по финансам в порядке убывания

    for q in query_datas: # запись через цикл 
        for_line_labels.append(q.name) # добавление в список для названий
        for_line_data.append(q.financing_from_subject_federal_budget) # добавление в список для данных

    return for_line_data, for_line_labels # возвращаем списки
 

def main(req): # main page_name
    
    page_name = "index.html" # ссылка на страницу

    pie_result = pieData() # вызов функции пирожка
    line_result = lineData() # вызов функции графика


    obj_users = CustomUser.objects.all().count() # получение всех пользователей
    obj_datas = Datas.objects.all().count() # получение всех спорткомплексов
    obj_active_datas = Datas.objects.filter(active = 'Y').count() # получение активных спорткомплексов
    obj_comment = CommentUser.getCommentsForIndex() # получение трех отзывов

    form = CreateQuestionsUserForm # форму связи записываем в переменную

    if req.method == 'POST': # если приходит метод POST
        message = {} # пустой словарь для отправки
        form = CreateQuestionsUserForm(req.POST) # отправляем в forms.py для проверки и результат в переменную form
        if form.is_valid():
            form.save() # сохраняем данные
            message['status'] = 'ok' # статус успеха
            return JsonResponse(message) # отправка словаря в виде json
        else: # иначе 
            return HttpResponseBadRequest() # иначе возвращаем плохой запрос

    values = { # переменная словарь для отправки на страницу
        'user':obj_users, # Количество пользователей
        'dat':obj_datas,  # Количество спорткомлексов
        'active_sport':obj_active_datas, # Количество активных спорткомлексов
        'labels':pie_result[1], # Атрибуты для пирога
        'data':pie_result[0], # Данные для пирога
        'line_labels':line_result[1], # Атрибуты для графика
        'line_data':line_result[0], # Данные для графика
        'form':form, # Форма с связью
        'comment':obj_comment, # Отправка трёх отзывов
    }

    return render(req, page_name, values) # рендеринг страницы


@login_required # обязательная авторизация
def editProfileView(req):
    
    page_name = 'edit_data.html' # ссылка на страницу

    if req.method == 'POST': # если приходит POST
        data = {}  # пустой словарь для отправки
        user = CustomUser.objects.get(pk=req.user.pk) # получение пользователя
        if user.check_password(req.POST['old_password']): # если старый пароль соответствует настоящему
            new_p1 = req.POST.get('password1')
            new_p2 = req.POST.get('password2')
            if req.FILES: # если существует файл аватарка
                form = EditProfileData(req.POST, req.FILES) # отправка на проверку
                if form.is_valid(): # если валидна
                    user.email = form.data['email'] # запись в переменную с пользователем и сохраняем с статусом ОК
                    user.avatar = req.FILES.get('avatar')
                    user.set_password(new_p2)
                    user.save()
                    data['message'] = f'Вы успешно сменили данные, {req.user.first_name}!'  # сообщение для пользователя
                    data['status'] = 'ok' # статус
                    return JsonResponse(data)
                else:
                    data['message'] = 'Введите правильные данные.'  # сообщение для пользователя
                    data['status'] = 'error' # статус
                    return JsonResponse(data)
            else: # пытался сделать владиацию на электронную почту, не получилось пока. 
                if new_p1 == new_p2: # проверка совпадений новых паролей.
                    user.email = req.POST['email'] # сохранение в пользователя
                    user.set_password(new_p2) # сохранение в пользователя
                    user.save() # save
                    data['message'] = f'Вы успешно сменили данные, {req.user.first_name}!'  # сообщение для пользователя
                    data['status'] = 'ok' # статус
                    return JsonResponse(data)
                else: 
                    data['message'] = 'Новые пароли не совпадают.' # сообщение для пользователя
                    data['status'] = 'error' # статус 
                    return JsonResponse(data)    
        else:
            data['message'] = 'Неверный старый пароль.' # сообщение для пользователя
            data['status'] = 'error' # статус
            return JsonResponse(data)
    else:
        form = EditProfileData()

    values = { # переменная словарь для отправки на страницу 
        'form':form
    }
    return render(req, page_name, values)


def CreateUserView(req): #регистрация

    page_name = 'registration/reg.html' # ссылка на страницу

    userForm = CreateUserForm()
    if req.user.is_authenticated: # если пользователь зареган, то 
        return redirect('home') # перенаправление
    else: # иначе 
        if req.method == 'POST': # если приходит метод POST
            data = {} # пустой словарь для отправки
            
            form = CreateUserForm(req.POST, req.FILES) # отправляем в forms.py для проверки и результат в переменную form
            if form.is_valid(): # Если форма хорошая, валидная, то 
                form.save() # сохраняем полученные данные
                data['name'] = form.data['first_name'] # запись имени пользователя для уведомления
                data['status'] = 'ok' # крутой статус ок
                return JsonResponse(data) # отправка словаря в виде json
            else: # иначе
                return  HttpResponseBadRequest() # иначе возвращаем плохой запрос
    

    values = { # переменная словарь для отправки на страницу
        'form': userForm
    }

    return render(req, page_name, values) # рендеринг страницы


@login_required # обязательная авторизация
def getProfileView(req): # профиль

    page_name = 'profile.html' # страница

    return render(req, page_name)


@login_required # обязательная авторизация
def createUserCommentView(req): # добавление комментария

    page_name = 'add_comment.html' # страница

    if req.method == 'POST': # если приходит метод POST
        data = {} # пустой словарь для отправки
        form = CreateCommentUser(req.POST) # отправляем в forms.py для проверки и результат в переменную form
        if form.is_valid(): # Если форма хорошая, валидная, то 
            obj = CommentUser.objects.create( # создаем переменную obj, чтобы записать в неё данные и 
                user_id = req.user.id,
                comment = form.data['comment'],
            )
            obj.save() # сохранить
            data['status'] = 'ok' # крутой статус
            return JsonResponse(data) # отправляем json 
        else: # иначе
            return HttpResponseBadRequest() # иначе возвращаем плохой запрос
    else: # иначе
        form = CreateCommentUser # запись формы в переменную form для возвращения.
    
    values = { # переменная словарь для отправки на страницу
        'form':form
    }

    return render(req, page_name, values) # рендеринг страницы


def getCommentsAllView(req): # получение страницы со всеми отзывами

    page_name = 'comments.html' # сама страница

    obj = CommentUser.objects.filter(posted=True).order_by('-create_date_comment') # простой запрос, где идет получение отзывов, которые одобрены и по дате отправки.
    
    values = { # переменная словарь для отправки на страницу
        'obj':obj
    }
    return render(req, page_name, values) # рендеринг страницы


def create_db(file_path): # загрузка данных в бд

    df = pd.read_csv(file_path, delimiter=',') # разбиваем столбцы убирая , 
    df = df.fillna(0) # избавление от NaN на 0
    list_of_csv = [list(row) for row in df.values] # через цикл заполняем список и записываем в переменную.

    for l in list_of_csv: # Через цикл сохраняем в бд 
        obj = Datas.objects.create(
            name = l[1],
            name_in_english = l[2],
            active = l[3],
            short_descr = l[4],
            detail_descr = l[5],
            short_descr_in_english = l[6],
            detail_descr_in_english = l[7],
            mo = l[8],
            subject_federation = l[9],
            impact = l[10],
            locality = l[11],
            locality_in_english = l[12],
            address = l[13],
            address_in_english = l[14],
            oktmo = l[15],
            fcp = l[16],
            move_with_object = l[17],
            date_start_to_build = l[18],
            date_end_to_build = l[19],
            financing = l[20],
            financing_from_federal_budget = l[21],
            financing_from_federal_budget_mastered = l[22],
            financing_from_subject_federal_budget = l[23],
            financing_from_subject_federal_budget_mastered = l[24],
            financing_from_mun_federal_budget = l[25],
            financing_from_mun_federal_budget_mastered = l[26],
            financing_from_mne_budget_source = l[27],
            financing_from_mne_budget_source_mastered = l[28],
            key_or_nope = l[29],
            vising_organization = l[30],
            vising_organization_in_english = l[31],
            address_vising_organization = l[32],
            address_vising_organization_in_english = l[33],
            phone_number_organization = l[34],
            contact_number_object = l[35],
            job_mon_fri = l[36],
            job_sb = l[37],
            job_vs = l[38],
            square = l[39],
            email = l[40],
            url_site = l[41],
            reestr = l[42],
            type_sport_complex = l[43],
            compet_complex = l[44],
            type_sports = l[45],
            cor_x_object = l[46],
            cor_y_object = l[47],
            scale_yan_map = l[48],
            cen_x = l[50],
            cen_y = l[49],
            min_cor_x = l[52],
            min_cor_y = l[51],
            general_plan = l[53],
            dop_general_plan = l[54],
            materials = l[55],
        )
        obj.save()


@login_required() # обязательная авторизация
def load_db(req):  # страница с загрузкой csv файла

    page_name = 'load.html' # сама страница

    if req.user.is_superuser: # проверка на администратора
        if req.method == "POST": # если приходит метод POST
            file = req.FILES['file'] # записываем в переменную file
            create_db(file) # отправляем в функцию.
        return render(req, page_name) # рендеринг страницы
    else: # иначе
        return HttpResponseBadRequest() # иначе возвращаем плохой запрос


def mapView(req): ## получение всех комплексов

    page_name = "map.html" # страница

    obj_datas = Datas.objects.all() # получение всех спорткомплексов

    values = { # переменная словарь для отправки на страницу
        'objects':obj_datas
    }

    return render(req, page_name, values) # ну тут понятно


def getObjView(req, id): ## получение нужного комплекса
    if req.method == 'POST': # если приходит метод POST
        obj = list(Datas.objects.filter(pk=id).values()) # возвращаем словарь и записываем в виде списка
        return JsonResponse({'data':obj}, safe=False) # отправляем json. Safe = False любой объект может быть передан для сериализации
    else: 
        return HttpResponseBadRequest() # иначе возвращаем плохой запрос
    

def searchObjView(req): # поисковик
    if req.method == 'POST': # если приходит метод POST
        res = None # Переменная с None. Для результатов
        search_obj = req.POST.get('message') # Получаем послание от пользователя
        query = Datas.objects.filter(name__icontains=search_obj)[:4] # сам запрос с посланием от пользователя (Запрос ILIKE)
        if len(query) > 0 and len(search_obj) > 0: # если строки в запросе и строчки пользователя больше 0
            data = [] # переменная список
            for q in query: # цикл q по данным
                item = { # записываем нужные атрибуты в item(словарь)
                    'id':q.id,
                    'name':q.name,
                    'email':q.email,
                    'contact_number_object':q.contact_number_object,
                    'short_descr':q.short_descr,
                    'address':q.address,
                    'cen_x':q.cen_x,
                    'cen_y':q.cen_y,
                    'scale_yan_map':q.scale_yan_map,
                }
                data.append(item) # добавление в список data
            res = data # записываем в res
        else: # иначе
            res = 'Спорткомплекс не найден' # Если не найдено, то записываем это сообщение
        
        return JsonResponse({'data':res}) # возвращаем в json виде 
    return JsonResponse({}) # пустой json










