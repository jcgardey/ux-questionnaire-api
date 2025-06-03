from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionnaireSerializer
from .models import Questionnaire
from responses.serializers import GetResponseSerializer

import csv
from django.http import HttpResponse
from questionnaire.models import QuestionnaireItem

class CreateQuestionnaireAPI(APIView):
    def post(self, request, format=None):
        serializer = QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            questionnaire = serializer.save()
            return Response({'id': questionnaire.id, 'name': questionnaire.name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetQuestionnaireAPI(APIView):
    
    def get(self, request):
        try:
            questionnaire = Questionnaire.objects.all().last()
            serializer = QuestionnaireSerializer(questionnaire)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Questionnaire.DoesNotExist:
            return Response({'error': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)
        
class GetQuestionnaireResponsesAPI(APIView):

    def get(self, request):
        try:
            questionnaire = Questionnaire.objects.all().last()
            serializer = GetResponseSerializer(questionnaire.questionnaire_responses.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Questionnaire.DoesNotExist:
            return Response({'error': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)

class ExportQuestionnaireResponsesAPI(APIView):
    def get(self, request):
        questionnaire = Questionnaire.objects.all().last()
        responses = questionnaire.questionnaire_responses.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questionnaire_responses.csv"'

        writer = csv.writer(response)

        all_questionnaire_items = list(map(lambda i: i.code, questionnaire.items.all().order_by('code')))
        # Write header
        writer.writerow([
            'Fecha', 'Edad', 'Genero', 'Role', 'Experiencia en el rol', 'Experiencia con métodos ágiles',
            'Tipo de proyecto', 'Otro tipo de proyecto', 'Experiencia Planificacion', *all_questionnaire_items
        ])
        # Write data rows
        for r in responses:
            writer.writerow([
                r.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                r.age,
                r.gender,
                r.role,
                r.role_experience,
                r.agile_experience,
                r.project_type,
                r.project_type_other,
                r.sprint_planning_experience,
                *[r.has_item_with_code(code) for code in all_questionnaire_items]
            ])
        return response