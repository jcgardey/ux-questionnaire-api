from rest_framework import serializers
from .models import QuestionnaireResponse, QuestionnaireResponseItem
from rest_framework import serializers
from questionnaire.models import QuestionnaireItem
from questionnaire.serializers import QuestionnaireItemSerializer
from functools import reduce


class CreateQuestionnaireResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireResponse
        fields = [
            'id',
            'age',
            'gender',
            'questionnaire',
            'role',
            'role_experience',
            'agile_experience',
            'project_type',
            'project_type_other',
            'sprint_planning_experience',
        ]



class AddResponseItemsSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_items(self, value):
        questionnare_response = self.context['questionnaire_response']
        invalid_ids = [pk for pk in value if not QuestionnaireItem.objects.filter(pk=pk).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid QuestionnaireItem ids: {invalid_ids}")
        if len(value) > questionnare_response.questionnaire.selectable_items:
            raise serializers.ValidationError("items_exceeds_maximum")
        
        items = [QuestionnaireItem.objects.get(pk=pk) for pk in value]
        accumulated_effort = reduce(lambda acc, item:  acc + item.effort, items, 0)
        if (accumulated_effort > questionnare_response.questionnaire.avaible_effort):
            raise serializers.ValidationError("effort_exceeds_maximum")
        return items

    def create(self, validated_data):
        questionnare_response = self.context['questionnaire_response']
        items = validated_data['items']
        created = []
        for item in items:
            obj, _ = QuestionnaireResponseItem.objects.get_or_create(
                response=questionnare_response,
                questionnaire_item=item
            )
            created.append(obj)
        return created
    
class QuestionnaireResponseItemSerializer(serializers.ModelSerializer):
    questionnaire_item = QuestionnaireItemSerializer()

    class Meta:
        model = QuestionnaireResponseItem
        exclude = ['response']
    
class GetResponseSerializer(serializers.ModelSerializer):
    response_items = QuestionnaireResponseItemSerializer(many=True)

    class Meta:
        model = QuestionnaireResponse
        fields = '__all__'