from django.contrib import admin

from .models import Lesson, Course, QuizQuestion,AISummary

# Register your models here.

admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(QuizQuestion)
admin.site.register(AISummary)

