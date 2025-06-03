from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionnaireSerializer
from .models import Questionnaire
from responses.serializers import GetResponseSerializer

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
