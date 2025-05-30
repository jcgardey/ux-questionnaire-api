from django.urls import path
from .api import CreateQuestionnaireAPI

urlpatterns = [
    path('new', CreateQuestionnaireAPI.as_view(), name='questionnaire-create'),
]