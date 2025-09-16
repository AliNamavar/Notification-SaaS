from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='SiginUp'),
    path('login/', views.LoginView.as_view(), name='login')
]
