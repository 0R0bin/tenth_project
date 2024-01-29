import accounts.views as accViews
import app_projects.views as projectsViews
import tickets.views as tViews

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()
router.register(r'user', accViews.UserViewSet, basename='user')
router.register(r'signup', accViews.CreateUserViewSet, basename='signup')
router.register(r'projects', projectsViews.ProjectsViewSet, basename='projects')
router.register(r'projects/(?P<project_id>[0-9]+)/users', projectsViews.ContributorsViewSet, basename='contributors')
router.register(r'projects/(?P<project_id>[0-9]+)/issues', tViews.IssuesViewSet, basename='issues')
router.register(r'projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/comments', tViews.CommentViewSet, basename='comments')

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'', include(router.urls)),
    path(r'login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]