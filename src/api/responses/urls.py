from django.urls import path
from .api import CreateQuestionnaireResponseAPI, AddItemsToQuestionnaireResponseAPI 

urlpatterns = [
    path('new', CreateQuestionnaireResponseAPI.as_view(), name='create-questionnaire-response'),
    path('<int:questionnaire_response_id>/add-items/', AddItemsToQuestionnaireResponseAPI.as_view(), name='questionnaire-response-add-items'),
]