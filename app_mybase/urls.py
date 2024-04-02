from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router_mybase = DefaultRouter()
router_mybase.register(r'database-connection', views.DatabaseConnectionViewSet)
router_mybase.register(r'sql-request', views.SqlQueryViewSet, basename='sql-query')
urlpatterns = [
    path('api/v1/', include(router_mybase.urls)),
]