from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.index, name='index'),
    path('admin',views.admin,name='admin'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('demart',views.demart,name='demart'),
    path('demartstationary',views.demartstationary,name='demartstationary'),
    path('skincare',views.skincare,name='skincare'),
    path('userreg',views.userreg,name='userreg'),
    path('about',views.about,name='about'),
]