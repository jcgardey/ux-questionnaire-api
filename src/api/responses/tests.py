from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import QuestionnaireResponse

class QuestionnaireResponseAPITest(APITestCase):
    def test_create_questionnaire_response(self):
        url = reverse('create-questionnaire-response')  # Update if your URL name is different
        data = {
            "age": 30,
            "gender": "L",
            "role": "DEV",
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
        url = reverse('create-questionnaire-response')
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
from questionnaire.models import QuestionnaireItem

class AddItemsToQuestionnaireResponseAPITest(APITestCase):
    def setUp(self):
        self.response = QuestionnaireResponse.objects.create(
            age=28,
            gender='L',
            role='DEV',
            agile_experience='NEVER',
            project_type='WEB',
            project_type_other='',
            sprint_planning_experience='NEVER'
        )
        self.item1 = QuestionnaireItem.objects.create(text='Item 1')
        self.item2 = QuestionnaireItem.objects.create(text='Item 2')

    def test_add_items_to_response(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])
        data = {"items": [self.item1.pk, self.item2.pk]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(QuestionnaireResponseItem.objects.filter(response=self.response).count(), 2)

    def test_add_items_invalid_item(self):
        url = reverse('questionnaire-response-add-items', args=[self.response.pk])
        data = {"items": [9999]}  # Non-existent item
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)