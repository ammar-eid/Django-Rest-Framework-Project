from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='instructor_courses')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class AISummary(models.Model):
    lesson=models.OneToOneField(Lesson,on_delete=models.CASCADE,related_name='ai_data')
    summary_text=models.TextField() #generated from AI
    key_points=models.JSONField(default=list)
    generated_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.lesson.title}"

class QuizQuestion(models.Model):
    lesson= models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='quiz_questions')
    question_text=models.TextField()
    option_a=models.CharField(max_length=255)
    option_b=models.CharField(max_length=255)
    option_c=models.CharField(max_length=255)
    option_d=models.CharField(max_length=255)
    correct_answer=models.CharField(max_length=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question for {self.lesson.title}"

class Enrollment(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='enrollments')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollment_students')
    created_at=models.DateTimeField(auto_now_add=True)
    is_completed=models.BooleanField(default=False)

    class Meta:
        unique_together=('student','course')


