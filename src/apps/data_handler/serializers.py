from rest_framework import serializers

from .models import BaseModel


def getGenericSerializer(model_arg):
    """
    takes a model argument (model_arg) and returns
    a dynamically created GenericSerializer class
    using the serializers.ModelSerializer
    """
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields = '__all__'

    return GenericSerializer

class ImportDataSerializer(serializers.Serializer):
    file = serializers.FileField()

class ImportDataDetailSerializer(serializers.Serializer):
    class Meta:
        model = BaseModel
        fields = ['table', 'guid', 'meta']

    table = serializers.CharField(max_length=255)
    guid = serializers.CharField(max_length=36)
    meta = serializers.DictField()
