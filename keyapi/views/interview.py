from keyapi.models import Interview
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.forms import ValidationError

class InterviewView(ViewSet):
    def list(self, request):
        interviews = Interview.objects.all()
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
            serializer.save()
            # if request.auth.user.is_staff == 1:
            #     post = serializer.save(approved=True)
            # post.tags.set(request.data["tags"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'
        depth = 2
        
class CreateInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['project', 'subject', 'location', 'scheduled_date']