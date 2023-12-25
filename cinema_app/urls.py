from django.urls import path, include

urlpatterns = [
    path('api/', include('cinema_app.API.urls')),
]