from keyapi.models import Field
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class FieldView(ViewSet):
    def list(self, request):
        fields = Field.objects.all()
        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            field = Field.objects.get(pk=pk)
            serializer = FieldSerializer(field)
            return Response(serializer.data)
        except Field.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'