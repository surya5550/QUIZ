from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import User, Category, Quiz, Question, Submission, SubmissionAnswer
from .serializers import (
    UserRegisterSerializer, CategorySerializer, QuizSerializer,
    QuestionSerializer, SubmissionSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminRole


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def user_register(self, request):
        data = request.data.copy()
        data['role'] = 'user'
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'User registered', 'id': user.id})

    @action(detail=False, methods=['post'])
    def admin_register(self, request):
        data = request.data.copy()
        data['role'] = 'admin'
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'Admin registered', 'id': user.id})



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # login required

    def create(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'Only admins can create categories.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'Only admins can update categories.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'Only admins can delete categories.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        quiz = self.get_object()
        quiz.is_active = True
        quiz.save()
        return Response({'detail': 'Quiz activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        quiz = self.get_object()
        quiz.is_active = False
        quiz.save()
        return Response({'detail': 'Quiz deactivated'})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create','update','destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticated()]


class SubmissionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # admin sees all, users see their own
        if request.user.role == 'admin':
            subs = Submission.objects.all()
        else:
            subs = Submission.objects.filter(user=request.user)
        return Response(SubmissionSerializer(subs, many=True).data)

    def create(self, request):
        quiz = get_object_or_404(Quiz, id=request.data.get('quiz'), is_active=True)
        answers = request.data.get('answers', [])
        questions = quiz.questions.filter(is_active=True)
        question_map = {q.id: q for q in questions}

        correct = 0
        with transaction.atomic():
            submission = Submission.objects.create(user=request.user, quiz=quiz, total_questions=len(questions))
            for ans in answers:
                q = question_map.get(ans['question'])
                if not q:
                    continue
                SubmissionAnswer.objects.create(submission=submission, question=q, selected_option=ans['selected_option'])
                if ans['selected_option'] == q.correct_option:
                    correct += 1
            submission.score = round((correct/len(questions))*100, 2) if questions else 0
            submission.save()
        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
