from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateQuestionnaireResponseSerializer
from django.shortcuts import get_object_or_404
from .models import QuestionnaireResponse
from .serializers import AddResponseItemsSerializer

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
        questionnaire_response.response_items.all().delete()  # Clear existing items before adding new ones
        serializer = AddResponseItemsSerializer(data=request.data, context={'questionnaire_response': questionnaire_response})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Items added."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteQuestionnaireResponseAPI(APIView):

    def delete(self, request, questionnaire_response_id):
        questionnaire_response = get_object_or_404(QuestionnaireResponse, pk=questionnaire_response_id)
        questionnaire_response.delete()
        return Response({"detail": "Questionnaire response deleted."}, status=status.HTTP_204_NO_CONTENT)
