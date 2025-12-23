from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import FacultyViewSet, ProfessorViewSet, StudentViewSet, SubjectViewSet, DashboardView

router = routers.DefaultRouter()
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'professors', ProfessorViewSet, basename='professor')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]
