from django.shortcuts import render, redirect
from app.models import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import pandas as pd
from app.models import CustomUser
from app.forms import CreateUserForm, CreateCommentUser, CreateQuestionsUserForm


def pieData(): # получение данных для пирога
    for_pie_labels = []
    for_pie_data = []

    query_datas = Datas.objects.order_by("-financing")[:7]

    for q in query_datas:
        for_pie_labels.append(q.name)
        for_pie_data.append(q.financing)

    
    return for_pie_data, for_pie_labels


def lineData(): # получение данных для графика
    for_line_labels = []
    for_line_data = []
    
    query_datas = Datas.objects.order_by("-financing_from_subject_federal_budget")[:10]

    for q in query_datas:
        for_line_labels.append(q.name)
        for_line_data.append(q.financing_from_subject_federal_budget)

    return for_line_data, for_line_labels
 

def main(req): # main page_name
    
    page_name = "index.html"

    pie_result = pieData() # получение данных для пирога
    line_result = lineData()


    obj_users = CustomUser.objects.all().count()
    obj_datas = Datas.objects.all().count()
    obj_active_datas = Datas.objects.filter(active = 'Y').count()
    obj_comment = CommentUser.getCommentsForIndex()

    form = CreateQuestionsUserForm

    if req.method == 'POST':
        message = {}
        form = CreateQuestionsUserForm(req.POST)
        if form.is_valid():
            form.save()
            message['status'] = 'ok'
            return JsonResponse(message)
        else: 
            return HttpResponseBadRequest()

    values = {
        'user':obj_users, 
        'dat':obj_datas, 
        'active_sport':obj_active_datas, 
        'labels':pie_result[1], 
        'data':pie_result[0],
        'line_labels':line_result[1],
        'line_data':line_result[0],
        'form':form,
        'comment':obj_comment,
    }

    return render(req, page_name, values)


def CreateUserView(req): #регистрация

    page_name = 'registration/reg.html' # ссылка на страницу

    userForm = CreateUserForm()
    if req.user.is_authenticated: # если пользователь зареган, то 
        return redirect('home') # перенаправление
    else: 
        if req.method == 'POST':
            data = {}
            
            form = CreateUserForm(req.POST, req.FILES)
            if form.is_valid():
                form.save()
                data['name'] = form.data['first_name']
                data['status'] = 'ok'
                return JsonResponse(data)
            else: 
                return  HttpResponseBadRequest()
    

    values = {
        'form': userForm
    }

    return render(req, page_name, values)


@login_required
def getProfileView(req): # профиль

    page_name = 'profile.html'

    return render(req, page_name)


@login_required
def createUserCommentView(req): # добавление комментария

    page_name = 'add_comment.html'

    if req.method == 'POST':
        data = {}
        form = CreateCommentUser(req.POST)
        if form.is_valid():
            obj = CommentUser.objects.create(
                user_id = req.user.id,
                comment = form.data['comment'],
            )
            obj.save()
            data['status'] = 'ok'
            return JsonResponse(data)
        else: 
            return HttpResponseBadRequest()
    else: 
        form = CreateCommentUser
    
    values = {
        'form':form
    }

    return render(req, page_name, values)


def getCommentsAllView(req):

    page_name = 'comments.html'

    obj = CommentUser.objects.filter(posted=True).order_by('-create_date_comment')
    
    values = {
        'obj':obj
    }
    return render(req, page_name, values)


def create_db(file_path): # загрузка данных в бд

    df = pd.read_csv(file_path, delimiter=',')
    df = df.fillna(0)
    list_of_csv = [list(row) for row in df.values]

    for l in list_of_csv:
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


@login_required(login_url='login')
def load_db(req): 

    page_name = 'load.html'

    if req.user.is_superuser:
        if req.method == "POST":
            file = req.FILES['file']
            create_db(file) # загрузка данных в бд
        return render(req, page_name)
    else: 
        return HttpResponseNotFound('Error')


def mapView(req): ## получение всех комплексов

    page_name = "map.html"

    obj_datas = Datas.objects.all()

    values = {
        'objects':obj_datas
    }

    return render(req, page_name, values)


def getObjView(req, id): ## получение нужного комплекса
    if req.method == 'POST':
        obj = list(Datas.objects.filter(pk=id).values()) 
        return JsonResponse({'data':obj}, safe=False)
    else: 
        return HttpResponseNotFound('Error')
    









