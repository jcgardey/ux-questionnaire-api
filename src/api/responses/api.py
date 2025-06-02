from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateQuestionnaireResponseSerializer
from django.shortcuts import get_object_or_404
from .models import QuestionnaireResponse
from .serializers import AddResponseItemsSerializer
import csv
from django.http import HttpResponse
from questionnaire.models import QuestionnaireItem

class CreateQuestionnaireResponseAPI(APIView):
    def post(self, request, questionnaire_id):
        request.data['questionnaire'] = questionnaire_id
        serializer = CreateQuestionnaireResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddItemsToQuestionnaireResponseAPI(APIView):
    def put(self, request, questionnaire_response_id):
        questionnaire_response = get_object_or_404(QuestionnaireResponse, pk=questionnaire_response_id)
        serializer = AddResponseItemsSerializer(data=request.data, context={'questionnaire_response': questionnaire_response})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Items added."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ExportQuestionnaireResponsesAPI(APIView):
    def get(self, request):
        responses = QuestionnaireResponse.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questionnaire_responses.csv"'

        writer = csv.writer(response)

        all_questionnaire_items = list(map(lambda i: i.code, QuestionnaireItem.objects.all().order_by('code')))
        # Write header
        writer.writerow([
            'age', 'gender', 'role', 'agile_experience',
            'project_type', 'project_type_other', 'sprint_planning_experience', *all_questionnaire_items
        ])
        # Write data rows
        for r in responses:
            writer.writerow([
                r.age,
                r.gender,
                r.role,
                r.agile_experience,
                r.project_type,
                r.project_type_other,
                r.sprint_planning_experience,
                *[r.has_item_with_code(code) for code in all_questionnaire_items]
            ])
        return response