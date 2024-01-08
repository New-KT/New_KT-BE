from rest_framework import serializers

class UploadDataSerializer(serializers.Serializer):
    json = serializers.JSONField()
    file = serializers.FileField()