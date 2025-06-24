from rest_framework import serializers
from .models import InformacionCientifica

class InformacionCientificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacionCientifica
        fields = '__all__'