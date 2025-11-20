
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.contrib.sitemaps.views import sitemap
from members.sitemaps import LivroSitemap, StaticViewSitemap
from django.views.generic import TemplateView

sitemaps = {
    'livros': LivroSitemap,
    'static': StaticViewSitemap,
}

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/painel-admin/'
        return '/'

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # Sistema de recuperação de password
    path('accounts/password-reset/', 
         PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='/accounts/password-reset/done/'
         ), 
         name='password_reset'),
    path('accounts/password-reset/done/', 
         PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/accounts/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    path('accounts/password-reset-complete/', 
         PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('members.urls')),
    path('admin/', admin.site.urls),
]