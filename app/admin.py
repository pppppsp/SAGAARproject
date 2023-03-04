from django.contrib import admin
from app.models import *

admin.site.register(CustomUser)

@admin.register(ContactUs)
class CommentUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'desc']

@admin.register(CommentUser)
class CommentUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date_comment', 'posted']

@admin.register(Datas)
class DatasAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'name_in_english',
        'active',
        'short_descr',
        'detail_descr',
        'short_descr_in_english',
        'detail_descr_in_english',
        'mo',
        'subject_federation',
        'impact',
        'locality',
        'locality_in_english',
        'address',
        'address_in_english',
        'oktmo',
        'fcp',
        'move_with_object',
        'date_start_to_build',
        'date_end_to_build',
        'financing',
        'financing_from_federal_budget',
        'financing_from_federal_budget_mastered',
        'financing_from_subject_federal_budget',
        'financing_from_subject_federal_budget_mastered',
        'financing_from_mun_federal_budget',
        'financing_from_mun_federal_budget_mastered',
        'financing_from_mne_budget_source',
        'financing_from_mne_budget_source_mastered',
        'key_or_nope',
        'vising_organization',
        'vising_organization_in_english',
        'address_vising_organization',
        'address_vising_organization_in_english',
        'phone_number_organization',
        'contact_number_object',
        'job_mon_fri',
        'job_sb',
        'job_vs',
        'square',
        'email',
        'url_site',
        'reestr',
        'type_sport_complex',
        'compet_complex',
        'type_sports',
        'cor_x_object',
        'cor_y_object',
        'scale_yan_map',
        'cen_x',
        'cen_y',
        'min_cor_x',
        'min_cor_y',
        'general_plan',
        'dop_general_plan',
        'materials',
        ]


# Register your models here.
