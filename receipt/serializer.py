from rest_framework import serializers
from .models import Block, Delimeter, Document
from .custom_validators import validate_file_extension

class BlockSerializer (serializers.ModelSerializer):
    class Meta:
        model= Block
        fields=["begin_row","begin_column","end_row", "end_column"]

class DelimeterSerializer (serializers.ModelSerializer):
    class Meta:
        model= Delimeter
        fields=["value","count"]

class DocumentSerializer (serializers.ModelSerializer):
    class Meta:
        model= Document
        fields=["id","name","description"]

class NewDocumentSerializer (serializers.Serializer):
    file = serializers.FileField(max_length=256, allow_empty_file=False, use_url=False, validators=[validate_file_extension])


