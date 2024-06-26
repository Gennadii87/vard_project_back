from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_mybase.urls import router_mybase
from app_url_save_file.urls import router_url_save
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.registry.extend(router_mybase.registry)
router.registry.extend(router_url_save.registry)

router.register(r'auth-login', views.LoginAuthTokenSet, basename='auth-login')
router.register(r'account', views.UserAccountViewSet, basename='account')
router.register(r'user', views.UserViewSet)
router.register(r'file', views.FileViewSet)
router.register(r'access', views.AccessViewSet)
router.register(r'feedback', views.FeedbackViewSet)
router.register(r'chart', views.ChartViewSet)
router.register(r'dashboard', views.DashboardViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'read-comment', views.ReadCommentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your description here",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
