from .models import Lesson,AISummary
from .services import generate_lesson_summary, generate_quiz_questions

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Lesson)
def auto_generate_ai_summary(sender, instance, created, **kwargs):
    if created:
        summary,points=generate_lesson_summary(instance.content)

        AISummary.objects.create(
            lesson=instance,
            summary_text=summary,
            key_points=points)

        raw_quiz =generate_quiz_questions(instance.content)

        print(f"AI Quiz Generated: {raw_quiz}")




