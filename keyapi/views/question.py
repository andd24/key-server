from keyapi.models import Question
from rest_framework import serializers, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class QuestionView(ViewSet):
    def list(self, request):
        questions = Question.objects.all()
        search = request.query_params.get('q', None)
        if search is not None:
            questions = questions.filter(question__icontains=f"{search}")
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        try:
            serializer = CreateQuestionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            questions = Question.objects.get(pk=pk)
            serializer = CreateQuestionSerializer(questions, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        questions = Question.objects.get(pk=pk)
        questions.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'