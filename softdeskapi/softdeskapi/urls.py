import accounts.views as accViews
import app_projects.views as projectsViews
import tickets.views as tViews

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Fonction utilisée pour afficher la doc
schema_view = get_schema_view(
   openapi.Info(
      title="API SoftDesk",
      default_version='v1.0',
      description="API développée pour OpenClassroom",
      terms_of_service="",
      contact=openapi.Contact(email="robinsenechal0@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Router (DRF)
router = routers.SimpleRouter()
router.register(r'user', accViews.UserViewSet, basename='user')
router.register(r'signup', accViews.CreateUserViewSet, basename='signup')
router.register(r'projects', projectsViews.ProjectsViewSet, basename='projects')
router.register(r'projects/(?P<project_id>[0-9]+)/users',
                projectsViews.ContributorsViewSet, basename='contributors')
router.register(r'projects/(?P<project_id>[0-9]+)/issues', tViews.IssuesViewSet, basename='issues')
router.register(r'projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/comments',
                tViews.CommentViewSet, basename='comments')

# Définition des URLs
urlpatterns = [
    # Global & Utils
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls')),
    # API DRF
    path(r'api/', include(router.urls)),
    # JWT
    path(r'api/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Documentation
    path(r'doc_swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'doc_redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
