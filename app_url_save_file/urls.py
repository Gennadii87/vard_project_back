from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_url_save_file import views


router_url_save = DefaultRouter()
router_url_save.register(r'load-url-file', views.UrlFileLoadViewSet, basename='load-url-file')
urlpatterns = [
    path('api/v1/', include(router_url_save.urls)),
]