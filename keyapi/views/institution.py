from keyapi.models import Institution
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class InstitutionView(ViewSet):
    def list(self, request):
        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            institution = Institution.objects.get(pk=pk)
            serializer = InstitutionSerializer(institution)
            return Response(serializer.data)
        except Institution.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'