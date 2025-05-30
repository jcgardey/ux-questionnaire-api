from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Questionnaire, QuestionnaireItem

class QuestionnaireCreateAPITest(APITestCase):
    def test_create_questionnaire_with_items(self):
        url = reverse('questionnaire-create')
        data = {
            "name": "Test Questionnaire",
            "items": [
                {
                    "description": "Item 1",
                    "contribution": "Contribution 1",
                    "severity": "L",
                    "category": "TE",
                    "effort": 1,
                    "code": "ITEM1" 
                },
                {
                    "description": "Item 2",
                    "contribution": "Contribution 2",
                    "severity": "M",
                    "category": "UX",
                    "effort": 2,
                    "code": "ITEM2" 
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Questionnaire.objects.filter(name="Test Questionnaire").exists())
        questionnaire = Questionnaire.objects.get(name="Test Questionnaire")
        self.assertEqual(questionnaire.items.count(), 2)
        item_descriptions = questionnaire.items.values_list('description', flat=True)
        self.assertIn("Item 1", item_descriptions)
        self.assertIn("Item 2", item_descriptions)
    
    # ...existing code...

    def test_create_questionnaire_with_invalid_item(self):
        url = reverse('questionnaire-create')
        data = {
            "name": "Test Questionnaire Invalid",
            "items": [
                {
                    "description": "Valid Item",
                    "contribution": "Contribution 1",
                    "severity": "L",
                    "category": "TE",
                    "effort": 1,
                },
                {
                    # Missing 'description' field, which should be required
                    "contribution": "Contribution 2",
                    "severity": "M",
                    "category": "UX",
                    "effort": 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Questionnaire.objects.filter(name="Test Questionnaire Invalid").exists())

    # ...existing code...

    def test_create_questionnaire_with_invalid_category_or_severity(self):
        url = reverse('questionnaire-create')
        data = {
            "name": "Test Questionnaire Invalid Fields",
            "items": [
                {
                    "description": "Item with invalid category",
                    "contribution": "Contribution 1",
                    "severity": "L",
                    "category": "INVALID",  # Invalid category
                    "effort": 1
                },
                {
                    "description": "Item with invalid severity",
                    "contribution": "Contribution 2",
                    "severity": "INVALID",  # Invalid severity
                    "category": "UX",
                    "effort": 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Questionnaire.objects.filter(name="Test Questionnaire Invalid Fields").exists())
