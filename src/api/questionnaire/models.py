from django.db import models


class Questionnaire(models.Model):
    name = models.CharField(max_length=100)


class QuestionnaireItem(models.Model):

    class Severity(models.TextChoices):
        LOW = 'L', 'Low'
        MEDIUM = 'M', 'Medium'
        HIGH = 'H', 'High'

    class Category(models.TextChoices):
        TECH = 'TE', 'Tech'
        UX = 'UX', 'UX'
        MIX = 'MX', 'Mixed'

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    contribution = models.CharField(max_length=500)
    severity = models.CharField(max_length=1, choices=Severity.choices, default=Severity.LOW)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.TECH)
    effort = models.PositiveIntegerField(default=0)