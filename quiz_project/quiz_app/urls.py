from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CategoryViewSet, QuizViewSet, QuestionViewSet, SubmissionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'submissions', SubmissionViewSet, basename='submission')

register = RegisterView.as_view({'post':'user_register'})
admin_register = RegisterView.as_view({'post':'admin_register'})

urlpatterns = [
    path('auth/register/', register),
    path('auth/register/admin/', admin_register),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),
]
