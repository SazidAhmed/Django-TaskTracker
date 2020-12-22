
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#models
from apps.core.views import register, login

urlpatterns = [
    # super adminpanel
    path('admin/', admin.site.urls),
    # Core Urls
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="access/login.html"), name='login'),
    # path('login/', login, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="access/password_reset_form.html"),name='password_reset'),
    path('password_reset_email_sent/',auth_views.PasswordResetDoneView.as_view(template_name="access/password_reset_email_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="access/password_reset_new_password.html"),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="access/password_reset_completed.html"),name='password_reset_complete'),

    # Website Urls
    path('', include('apps.website.urls')),

    # Adminpanel Urls
    path('adminpanel/', include('apps.adminpanel.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)