from django.urls import path
from .api import CreateQuestionnaireAPI, GetQuestionnaireAPI

urlpatterns = [
    path('new', CreateQuestionnaireAPI.as_view(), name='questionnaire-create'),
    path('', GetQuestionnaireAPI.as_view(), name='get-last-questionnaire'),
]