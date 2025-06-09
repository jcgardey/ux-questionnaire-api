from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import QuestionnaireResponse

class QuestionnaireResponseAPITest(APITestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(selectable_items=2, avaible_effort=100)
    def test_create_questionnaire_response(self):
        url = reverse('create-questionnaire-response', args=[self.questionnaire.pk])  # Update if your URL name is different
        data = {
            "age": 30,
            "gender": "F",
            "role": "DEV",
            "role_experience": "1-3",
            "agile_experience": "NEVER",
            "project_type": "WEB",
            "project_type_other": "",
            "sprint_planning_experience": "NEVER"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuestionnaireResponse.objects.count(), 1)
        self.assertEqual(QuestionnaireResponse.objects.first().age, 30)

    def test_create_questionnaire_response_missing_fields(self):
        url = reverse('create-questionnaire-response', args=[self.questionnaire.pk])
        # Remove required fields
        data = {
            "age": 25,
            # "gender" is missing
            "role": "DEV",
            "agile_experience": "NEVER",
            "project_type": "WEB",
            "project_type_other": "",
            # "sprint_planning_experience" is missing
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gender', response.data)
        self.assertIn('sprint_planning_experience', response.data)


from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import QuestionnaireResponse, QuestionnaireResponseItem
from questionnaire.models import QuestionnaireItem, Questionnaire

class AddItemsToQuestionnaireResponseAPITest(APITestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(selectable_items=2, avaible_effort=100)
        self.response = QuestionnaireResponse.objects.create(
            age=28,
            gender='L',
            role='DEV',
            agile_experience='NEVER',
            project_type='WEB',
            project_type_other='',
            sprint_planning_experience='NEVER',
            questionnaire=self.questionnaire
        )
        self.item1 = QuestionnaireItem.objects.create(description='Item 1', effort=10, questionnaire=self.questionnaire)
        self.item2 = QuestionnaireItem.objects.create(description='Item 2', effort=20, questionnaire=self.questionnaire)
        self.item3 = QuestionnaireItem.objects.create(description='Item 3', effort=90, questionnaire=self.questionnaire)

    def test_edit_response_items(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])
        data = {"items": [self.item1.pk, self.item2.pk]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(QuestionnaireResponseItem.objects.filter(response=self.response).count(), 2)

        response = self.client.put(url, {"items": [self.item1.pk]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(QuestionnaireResponseItem.objects.filter(response=self.response).count(), 1)

    def test_add_items_invalid_item(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])

        data = {"items": [9999]}  # Non-existent item
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)        

    def test_add_items_exceeds_maximum(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])
        # Try to add more items than selectable_items allows
        data = {"items": [self.item1.pk, self.item2.pk, self.item3.pk]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items_exceeds_maximum', str(response.data[0]))

    def test_add_items_exceeds_effort(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])
        # Try to add more items than selectable_items allows
        data = {"items": [self.item2.pk, self.item3.pk]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('effort_exceeds_maximum', str(response.data[0]))