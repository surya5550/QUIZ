from rest_framework import serializers
from .models import User, Category, Quiz, Question, Submission, SubmissionAnswer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username','email','password','role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        
        # Hide correct_option if user is not staff/admin
        if not request.user.is_staff:
            data.pop("correct_option", None)
        return data



class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class SubmissionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAnswer
        fields = ('question','selected_option')


class SubmissionSerializer(serializers.ModelSerializer):
    answers = SubmissionAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Submission
        fields = ('id','quiz','score','total_questions','answers','created_at')
        read_only_fields = ('score','total_questions','created_at')

    def create(self, validated_data):
        return super().create(validated_data)
