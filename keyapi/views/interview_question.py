from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.forms import ValidationError
from keyapi.models import InterviewQuestion


class InterviewQuestionView(ViewSet):
    def list (self, request):
        """handles the GET all for InterviewQuestions"""
        interview_questions = InterviewQuestion.objects.all()
        interview = request.query_params.get('interview_id', None)
        search = request.query_params.get('q', None)
        if search is not None:
            interview_questions = interview_questions.filter(question__icontains=f"{search}", interview_id=interview)
        if interview is not None:
            interview_questions = interview_questions.filter(interview_id=interview)
        serializer = InterviewQuestionSerializer(interview_questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles the GET for single InterviewQuestions"""
        try:
            InterviewQuestions = InterviewQuestion.objects.get(pk=pk)
            serializer = InterviewQuestionSerializer(InterviewQuestions)
            return Response(serializer.data)
        except InterviewQuestion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        
        try:
            serializer = CreateInterviewQuestionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            InterviewQuestions = InterviewQuestion.objects.get(pk=pk)
            serializer = CreateInterviewQuestionSerializer(InterviewQuestions, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        InterviewQuestions = InterviewQuestion.objects.get(pk=pk)
        InterviewQuestions.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def answer(self, request, pk):
        interviewquestion = InterviewQuestion.objects.get(pk=pk)
        interviewquestion.answer = request.data
        interviewquestion.save()
        return Response({'message': 'Interview question has been answered'}, status=status.HTTP_204_NO_CONTENT)
    
class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ('id', 'interview', 'question', 'answer')
        depth = 2

class CreateInterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ('user', 'interview', 'question', 'answer')