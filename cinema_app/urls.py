from django.contrib import admin
from django.urls import path, include

from cinema_app.views import Login, Logout, Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
]
