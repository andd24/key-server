from datetime import datetime
from keyapi.models import Interview
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.forms import ValidationError

class InterviewView(ViewSet):
    def list(self, request):
        interviews = Interview.objects.all()
        project = request.query_params.get('project_id', None)
        complete = request.query_params.get('complete', None)
        if project is not None:
            interviews = interviews.filter(project_id=project)
        if complete is not None:
            interviews = interviews.filter(complete=True)
        if project is not None and complete is not None:
            interviews = interviews.filter(project_id=project, complete=True)
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            interview = Interview.objects.get(pk=pk)
            serializer = InterviewSerializer(interview)
            return Response(serializer.data)
        except Interview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        # user = KeyUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateInterviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # format, imgstr = request.data["image_url"].split(';base64,')
            # ext = format.split('/')[-1]
            # imgdata = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            interview = serializer.save()
            interview.questions.set(request.data["questions"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        try:
            interview = Interview.objects.get(pk=pk)
            serializer = CreateInterviewSerializer(interview, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_interview = serializer.save()
            updated_interview.questions.set(request.data["questions"])
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        interview.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def complete(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        interview.complete = True
        interview.collection_date = datetime.date
        interview.save()
        return Response({'message': 'Interview has been completed'}, status=status.HTTP_204_NO_CONTENT)
        
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'
        depth = 2
        
class CreateInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['project', 'subject', 'location', 'scheduled_date', 'questions']