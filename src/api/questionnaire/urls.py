from django.urls import path
from .api import CreateQuestionnaireAPI, GetQuestionnaireAPI, GetQuestionnaireResponsesAPI, ExportQuestionnaireResponsesAPI

urlpatterns = [
    path('new', CreateQuestionnaireAPI.as_view(), name='questionnaire-create'),
    path('', GetQuestionnaireAPI.as_view(), name='get-last-questionnaire'),
    path('responses', GetQuestionnaireResponsesAPI.as_view(), name='get-questionnaire-responses'),
    path('responses/export', ExportQuestionnaireResponsesAPI.as_view(), name='export-questionnaire-responses'),
]