from django.contrib import admin

# Register your models here.
from .models import User, Category, Quiz, Question, Submission, SubmissionAnswer

# Register models to appear in Django admin
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(SubmissionAnswer)
