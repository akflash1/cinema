from django.contrib import admin
from django.urls import path

from cinema_app.views import Login, Logout, Register, HallCreateView, SessionCreateView, FilmCreateView, FilmListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('create_hall', HallCreateView.as_view(), name='create_hall'),
    path('create_session', SessionCreateView.as_view(), name='create_session'),
    path('create_film', FilmCreateView.as_view(), name='create_film'),
    path('', FilmListView.as_view(), name='index'),
]
