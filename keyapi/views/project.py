from django.forms import ValidationError
from keyapi.models import Project, KeyUser
from django.contrib.auth.models import User
from keyapi.views.key_user import KeyUserSerializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.files.base import ContentFile
import uuid
import base64

class ProjectView(ViewSet):
    def retrieve(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        projects = Project.objects.all()
        user = request.query_params.get('user_id', None)
        title = request.query_params.get('q', None)
        public = request.query_params.get('public', None)
        field = request.query_params.get('field', None)
        if title is not None and public is not None:
            projects = projects.filter(title__icontains=f"{title}", public=True)
        if field is not None and public is not None:
            projects = projects.filter(field_id=field, public=True)
        if user is not None:
            projects = projects.filter(user_id=user)
        if public is not None:
            projects = projects.filter(public=True)
        if user is not None and public is not None:
            projects = projects.filter(user_id=user, public=True)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = KeyUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateProjectSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # format, imgstr = request.data["image_url"].split(';base64,')
            # ext = format.split('/')[-1]
            # imgdata = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            serializer.save(user=user)
            # if request.auth.user.is_staff == 1:
            #     post = serializer.save(approved=True)
            # post.tags.set(request.data["tags"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = CreateProjectSerializer(project, data=request.data)
            serializer.is_valid(raise_exception=True)
            # updated_project = serializer.save()
            # updated_post.tags.set(request.data["tags"])
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def publish(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.public = True
        project.save()
        return Response({'message': 'Project has been published'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def unpublish(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.public = False
        project.save()
        return Response({'message': 'Project has been unpublished'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def conclusions(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.conclusions = request.data
        project.save()
        return Response({'message': 'Conclusions have been added'}, status=status.HTTP_204_NO_CONTENT)

class ProjectSerializer(serializers.ModelSerializer):
    # event_count = serializers.IntegerField(default=None)
    # user_event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Project
        fields = '__all__'
        depth = 3

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'imgurl', 'field']