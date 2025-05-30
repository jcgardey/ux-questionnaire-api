from rest_framework import serializers
from .models import QuestionnaireResponse, QuestionnaireResponseItem
from rest_framework import serializers
from questionnaire.models import QuestionnaireItem


class CreateQuestionnaireResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireResponse
        fields = [
            'id',
            'age',
            'gender',
            'role',
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
        invalid_ids = [pk for pk in value if not QuestionnaireItem.objects.filter(pk=pk).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid QuestionnaireItem ids: {invalid_ids}")
        return value

    def create(self, validated_data):
        questionnare_response = self.context['questionnaire_response']
        items = validated_data['items']
        created = []
        for item_id in items:
            item = QuestionnaireItem.objects.get(pk=item_id)
            obj, _ = QuestionnaireResponseItem.objects.get_or_create(
                response=questionnare_response,
                questionnaire_item=item
            )
            created.append(obj)
        return created