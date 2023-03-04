from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser): # пользователь
    patronymic = models.CharField('Отчество', max_length=50, null=True) # отчество
    avatar = models.ImageField('Аватарка', upload_to='users/', null=True) # аватарка

    def __str__(self): # функция для возврата в виде строки
        return f'{self.last_name} {self.first_name} {self.patronymic}' 


class CommentUser(models.Model): # комментарии
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь') # пользователь
    create_date_comment = models.DateTimeField('Дата создания комментария',auto_now_add=True) # дата создания комментария
    posted = models.BooleanField('Отображается или нет', default=False) # одобрение
    comment = models.TextField('Комментарий', max_length=500) # сообщение

    def __str__(self): # функция для возврата в виде строки
        return f'{self.user} - {self.comment}'

    @staticmethod
    def getCommentsForIndex():
        return CommentUser.objects.filter(posted=True).order_by("-create_date_comment")[:3] # запрос для возврата с одобренными отзывами

    class Meta: # отображение модели на русском языке
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class ContactUs(models.Model): # связаться с нами
    name = models.CharField('Имя', max_length=50)
    email = models.EmailField('Почта',) # почта
    created = models.DateTimeField('Дата отправки', auto_now_add=True) # дата отправки
    desc = models.TextField('Сообщение', max_length=175) # содержимое

    def __str__(self): # функция для возврата в виде строки
        return f'{self.name} - {self.email}'


    class Meta:  # отображение модели на русском языке
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'



class Datas(models.Model): # Данные из csv  
    name = models.CharField('Название', max_length=55,null=True, blank=True) # лень дальше комментировать, ну вроде понятно снизу все
    name_in_english = models.CharField('Название (in english)', max_length=55,null=True, blank=True)
    active = models.CharField('Активный', max_length=255,null=True, blank=True)
    short_descr = models.CharField('Краткое описание', max_length=155,null=True, blank=True)
    detail_descr = models.TextField('Детальное описание',null=True, blank=True)
    short_descr_in_english = models.CharField('Краткое описание (in english)', max_length=100,null=True, blank=True)
    detail_descr_in_english = models.TextField('Детальное описание (in english)',null=True, blank=True)
    mo = models.CharField('МО', max_length=255,null=True, blank=True)
    subject_federation = models.CharField('Субъект федерации', max_length=100,null=True, blank=True)
    impact = models.CharField('Значимость', max_length=155,null=True, blank=True)
    locality = models.CharField('Населённый пункт',max_length=355,null=True, blank=True)
    locality_in_english = models.CharField('Населённый пункт (in english)', max_length=355,null=True, blank=True)
    address = models.CharField('Адрес', max_length=155,null=True, blank=True)
    address_in_english = models.CharField('Адрес', max_length=155,null=True, blank=True)
    oktmo = models.CharField('ОКТМО', max_length=255,null=True, blank=True)
    fcp = models.CharField('ФЦП (Федеральная целевая программа)', max_length=155,null=True, blank=True)
    move_with_object = models.CharField('Действия с объектом', max_length=255,null=True, blank=True)
    date_start_to_build = models.CharField('Дата начала строительства / реконструкции', max_length=255,null=True, blank=True)
    date_end_to_build = models.CharField('Дата завершения строительства / реконструкции', max_length=255,null=True, blank=True)
    financing = models.FloatField('Общий объём финансирования',null=True, blank=True)
    financing_from_federal_budget = models.FloatField('Финансирование из федерального бюджета',null=True, blank=True)
    financing_from_federal_budget_mastered = models.FloatField('Финансирование из федерального бюджета (из них освоено)',null=True, blank=True)
    financing_from_subject_federal_budget = models.FloatField('Финансирование из бюджета субъекта федерации',null=True, blank=True)
    financing_from_subject_federal_budget_mastered = models.FloatField('Финансирование из бюджета субъекта федерации (из них освоено.)',null=True, blank=True)
    financing_from_mun_federal_budget = models.FloatField('Финансирование из бюджета муниципального образования',null=True, blank=True)
    financing_from_mun_federal_budget_mastered = models.FloatField('Финансирование из бюджета муниципального образования (из них освоено)',null=True, blank=True)
    financing_from_mne_budget_source = models.FloatField('Финансирование из внебюджетных источников',null=True, blank=True)
    financing_from_mne_budget_source_mastered = models.FloatField('Финансирование из внебюджетных источников (из них освоено)' , default=0,null=True, blank=True)
    key_or_nope = models.CharField('Ключевой или нет?', max_length=255,null=True, blank=True)
    vising_organization = models.CharField('Курирующий орган', max_length=255,null=True, blank=True)
    vising_organization_in_english = models.CharField('Курирующий орган (in english)', max_length=255,null=True, blank=True)
    address_vising_organization = models.CharField('Адрес курирующего органа', max_length=255,null=True, blank=True)
    address_vising_organization_in_english = models.CharField('Адрес курирующего органа (in english)', max_length=255,null=True, blank=True)
    phone_number_organization = models.CharField('Телефон курирующего органа', max_length=30,null=True, blank=True)
    contact_number_object = models.CharField('Контактный телефон объекта', max_length=30,null=True, blank=True)
    job_mon_fri = models.CharField('Режим работы Пн.-Пт.', max_length=255,null=True, blank=True)
    job_sb = models.CharField('Режим работы Сб', max_length=255,null=True, blank=True)
    job_vs = models.CharField('Режим работы Вс', max_length=255,null=True, blank=True)
    square = models.FloatField('Площадь',null=True, blank=True)
    email = models.EmailField('E-mail',null=True, blank=True)
    url_site = models.CharField('URL сайта', max_length=255,null=True, blank=True)
    reestr = models.CharField('Внесён в реестр?', max_length=255,null=True, blank=True)
    type_sport_complex = models.CharField('Тип спортивного комплекса', max_length=255,null=True, blank=True)
    compet_complex = models.TextField('Какие соревнования проводятся?',null=True, blank=True)
    type_sports = models.TextField('Виды спорта',null=True, blank=True)
    cor_x_object = models.DecimalField('Яндекс координата объекта X',null=True, blank=True, max_digits=9, decimal_places=6)
    cor_y_object = models.DecimalField('Яндекс координата объекта Y',null=True, blank=True, max_digits=9, decimal_places=6)
    scale_yan_map = models.FloatField('Маштаб Яндекс-карты',null=True, blank=True)
    cen_x = models.DecimalField('Яндекс координата центра X',null=True, blank=True, max_digits=9, decimal_places=6)
    cen_y = models.DecimalField('Яндекс координата центра Y',null=True, blank=True, max_digits=9, decimal_places=6)
    min_cor_x = models.DecimalField('Мини координата X',null=True, blank=True, max_digits=9, decimal_places=6)
    min_cor_y = models.DecimalField('Мини координата Y',null=True, blank=True, max_digits=9, decimal_places=6)
    general_plan = models.TextField('Генеральный план',null=True, blank=True)
    dop_general_plan = models.TextField('Дополнительные планы',null=True, blank=True)
    materials = models.CharField('Прочие материалы', max_length=255)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Данные от CSV файла'
        verbose_name_plural = 'Данные от CSV файла'


    # "Фото:","URL фото галереи объекта:","Видео:","Панорамы:","Web-трансляции:","Прочие материалы:"

