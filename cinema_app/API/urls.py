from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from .resources import UserRegistrationView, HallModelViewSet, FilmModelViewSet, SessionModelViewSet, PurchaseModelViewSet

router = routers.SimpleRouter()
router.register(r'hall', HallModelViewSet)
router.register('film', FilmModelViewSet)
router.register('session', SessionModelViewSet)
router.register(r'session/(?P<session_id>\d+)/purchase', PurchaseModelViewSet)
router.register('registration', UserRegistrationView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthToken.as_view())
]
