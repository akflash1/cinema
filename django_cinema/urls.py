from django.contrib import admin
from django.urls import path, include

from cinema_app.views import Login, Logout, Register, HallCreateView, SessionCreateView, FilmCreateView, FilmListView, \
    FilmDetailView, PurchaseCreateView, SessionUpdateView, HallUpdateView, CartListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('create_hall', HallCreateView.as_view(), name='create_hall'),
    path('create_session', SessionCreateView.as_view(), name='create_session'),
    path('create_film', FilmCreateView.as_view(), name='create_film'),
    path('show_purchase/<int:pk>', FilmDetailView.as_view(), name='purchase_detail'),
    path('create_purchase/<int:session_id>', PurchaseCreateView.as_view(), name='purchase_create'),
    path('update_session/<int:pk>', SessionUpdateView.as_view(), name='update_session'),
    path('update_hall/<int:pk>', HallUpdateView.as_view(), name='update_hall'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('', FilmListView.as_view(), name='base'),
    path('', include('cinema_app.urls')),
]
