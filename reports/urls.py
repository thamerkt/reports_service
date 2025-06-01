from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RapportViewSet, RapportDataViewSet

router = DefaultRouter()
router.register(r'rapports', RapportViewSet, basename="rapports")
router.register(r'rapport-data', RapportDataViewSet, basename="rapport-data")

urlpatterns = [
    path('', include(router.urls)),
]
