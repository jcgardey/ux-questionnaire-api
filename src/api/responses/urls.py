from django.urls import path
from .api import CreateQuestionnaireResponseAPI, AddItemsToQuestionnaireResponseAPI, DeleteQuestionnaireResponseAPI

urlpatterns = [
    path('questionnaire/<int:questionnaire_id>/new', CreateQuestionnaireResponseAPI.as_view(), name='create-questionnaire-response'),
    path('<int:questionnaire_response_id>/add-items', AddItemsToQuestionnaireResponseAPI.as_view(), name='questionnaire-response-add-items'),
    path('<int:questionnaire_response_id>/delete', DeleteQuestionnaireResponseAPI.as_view(), name='delete-questionnaire-response'),
]