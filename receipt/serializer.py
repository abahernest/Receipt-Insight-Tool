from rest_framework import serializers
from .models import Block, Delimeter, Document

class BlockSerializer (serializers.ModelSerializer):
    class Meta:
        model= Block
        fields=["id","document_id","start_axis","end_axis","created_at", "updated_at"]

class DelimeterSerializer (serializers.ModelSerializer):
    class Meta:
        model= Delimeter
        fields=["id","value", "created_at", "updated_at"]

class DocumentSerializer (serializers.ModelSerializer):
    class Meta:
        model= Document
        fields=["id","name","description", "created_at", "updated_at"]