from rest_framework import serializers
from .models import Questionnaire

from .models import Questionnaire, QuestionnaireItem

class QuestionnaireItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireItem
        exclude = ['questionnaire', 'id', 'created_at']

class QuestionnaireSerializer(serializers.ModelSerializer):
    items = QuestionnaireItemSerializer(many=True, write_only=True)

    class Meta:
        model = Questionnaire
        fields = ['id', 'name', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        questionnaire = Questionnaire.objects.create(**validated_data)
        for item_data in items_data:
            QuestionnaireItem.objects.create(questionnaire=questionnaire, **item_data)
        return questionnaire