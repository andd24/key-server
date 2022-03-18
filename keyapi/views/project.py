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
        # category = request.query_params.get('category_id', None)
        user = request.query_params.get('user_id', None)
        # tag = request.query_params.get('tag_id', None)
        # title = request.query_params.get('q', None)
        # approved = request.query_params.get('approved', None)
        # if title is not None:
        #     posts = posts.filter(title__icontains=f"{title}")
        # if category is not None:
        #     posts = posts.filter(category_id=category)
        if user is not None:
            projects = projects.filter(user_id=user)
        # if tag is not None:
        #     posts = posts.filter(tags=tag)
        # if approved is not None:
        #     posts = posts.filter(approved=True)
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

    # @action(methods=['get'], detail=False)
    # def subscribed(self, request):
    #     """Only get posts whose authors are associated with the current user's subscriptions"""

    #     rare_user = RareUser.objects.get(pk=request.auth.user.id)

    #     follower = RareUserSerializer(rare_user)

    #     posts = Post.objects.filter(
    #         user__pk__in=follower.data['following'])
        
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
        
    # @action(methods=['put'], detail=True)
    # def edit_tags(self, request, pk):
    #     """Put request to is_staff"""

    #     post = Post.objects.get(pk=pk)
    #     post.tags.set(request.data)
    #     post.save()

    #     return Response({'message': 'Tags have been edited'}, status=status.HTTP_204_NO_CONTENT)
    
    # @action(methods=['put'], detail=True)
    # def approve(self, request, pk):
    #     post = Post.objects.get(pk=pk)
    #     post.approved = True
    #     post.save()
    #     return Response({'message': 'Post has been approved by admin'}, status=status.HTTP_204_NO_CONTENT)
    
    # @action(methods=['put'], detail=True)
    # def unapprove(self, request, pk):
    #     post = Post.objects.get(pk=pk)
    #     post.approved = False
    #     post.save()
    #     return Response({'message': 'Post has been unapproved by admin'}, status=status.HTTP_204_NO_CONTENT)

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