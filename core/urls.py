from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tarsene/', views.search, name='search'),
    path('kategorii/', views.categories_list, name='categories_list'),
    re_path(r'^kategorii/(?P<slug>[\w-]+)/$', views.category_detail, name='category_detail'),
    path('kontakti/', views.contact, name='contact'),
    
    # Registration
    path('registratsiya/', views.register_choice, name='register_choice'),
    path('registratsiya/klient/', views.register_client, name='register_client'),
    path('registratsiya/professional/', views.register_professional, name='register_professional'),
    path('registratsiya/professional/profil/', views.register_professional_profile, name='register_professional_profile'),
    
    # Auth
    path('vhod/', views.user_login, name='login'),
    path('izhod/', views.user_logout, name='logout'),
    
    # Profile
    path('moyat-profil/', views.my_profile, name='my_profile'),
    re_path(r'^professional/(?P<slug>[\w-]+)/$', views.professional_profile, name='professional_profile'),
    re_path(r'^professional/(?P<slug>[\w-]+)/dobavi-snimki/$', views.professional_add_images, name='professional_add_images'),
    path('iztrii-snimka/<int:image_id>/', views.delete_image, name='delete_image'),
    
    # Legal pages
    path('usloviya-za-polzvane/', views.terms_of_service, name='terms_of_service'),
    path('politika-poveritelnost/', views.privacy_policy, name='privacy_policy'),
    path('politika-biskvitki/', views.cookie_policy, name='cookie_policy'),
    path('gdpr/', views.gdpr, name='gdpr'),
]
