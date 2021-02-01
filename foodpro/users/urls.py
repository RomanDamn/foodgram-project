from django.contrib.auth import views as view
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('login/', view.LoginView.as_view(), name='login'),
    path('logout/', view.LogoutView.as_view(), name='logout'),
    path('password_change/', view.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change_done/', view.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', view.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/', view.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
]
