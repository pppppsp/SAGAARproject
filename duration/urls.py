from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name = 'home'),
    path('comments/', views.getCommentsAllView, name = 'coms'),

    path('load/', views.load_db, name = 'load'),
    path('direct_map/', views.mapView, name = 'map'),
    path('direct_map/get/<int:id>', views.getObjView, name = 'get'),
    path('direct_map/search/', views.searchObjView, name = 'search'),

    path('profile/edit/', views.editProfileView, name = 'edit_data'),
    path('add_comment', views.createUserCommentView, name = 'com'),
    path('profile/', views.getProfileView, name = 'profile'),
    path('account/reg', views.CreateUserView, name = 'reg'),
    path('account/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('account/', include('django.contrib.auth.urls')), # connect auth
    
]

# Для изображений ***** 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# ***
