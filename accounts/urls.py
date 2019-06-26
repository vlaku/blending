from django.conf import settings
from django.conf.urls import include, url
from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views


app_name='accounts'

urlpatterns = [
    path('', accounts_views.AccountHomeView.as_view(), name='home'),
    path('activate/<uidb64>/<token>/', accounts_views.activate, name='activate'),
    path('bye/', accounts_views.logout_farewell, name='farewell'),
    path('contact/', accounts_views.send_email, name='send_email'),
    path('contact2/', accounts_views.send_email2, name='send_email2'),
    path('contact/sent/', accounts_views.thanks, name='thanks'),
    path('email_to_outbox/', accounts_views.email_to_outbox, name='email_to_outbox'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    # path('signout/', accounts_views.signout, name='signout'), # bez ostrzezenia
    path('delete/', accounts_views.UserSignoutView.as_view(), name='delete'), ## deaktywuje, nie usuwa
    path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                                        email_template_name='accounts/password_reset_email.html',
                                                        subject_template_name='accounts/password_reset_subject.txt',
                                                        success_url=reverse_lazy('accounts:password_reset_done')
                                                        ), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
                                                        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                                                        template_name='accounts/password_reset_confirm.html',
                                                        success_url=reverse_lazy('accounts:password_reset_complete')
                                                        ), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
                                                        template_name='accounts/password_reset_complete.html'),
                                                        name='password_reset_complete'),
    path('update/', accounts_views.UserDetailUpdateView.as_view(), name='user-update'),
]

# path('resend-activation/', accounts_views.AccountEmailActivateView.as_view(), name='resend-activation'),
