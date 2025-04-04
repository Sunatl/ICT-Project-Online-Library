from django.urls import path
from .views import Singup
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path("sing",Singup.as_view(),name="sing"),
    path("sings/",PasswordChangeView.as_view(),name="password_change"),
    path("singss/",PasswordChangeDoneView.as_view(),name="password_change_done"),
    path("sings1/",PasswordResetView.as_view(template_name="registration/password_reset_form.html",email_template_name="registration/password_reset_email.html",success_url=reverse_lazy("password_reset_done")),name="password_reset"),
    path("sings2/",PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
    path("password_reset/<uidb64>/token/",PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",success_url=reverse_lazy("password_reset_complate")),name="password_reset_confirm"),
    path("sings3/",PasswordResetCompleteView.as_view(template_name="registration/password_reset_complate.html"),name="password_reset_complate"),
]
