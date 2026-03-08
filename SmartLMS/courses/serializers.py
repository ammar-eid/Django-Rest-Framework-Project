from rest_framework import serializers
from .models import Lesson,AISummary,QuizQuestion,Course


class AISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AISummary
        fields = ['summary_text','key_points']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title','description']

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['question_text','option_a','option_b','option_c','option_d','correct_answer']

class LessonSerializer(serializers.ModelSerializer):
    ai_data=AISummarySerializer(read_only=True)
    quiz_questions=QuizQuestionSerializer(many=True,read_only=True)

    class Meta:
        model = Lesson
        fields = ['id','title','content','ai_data','quiz_questions']


