from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from packageAnalyse.models import Module, Publish, UploadFile


class UploadFileSerializer(ModelSerializer):
    """
    简单上传文件序列化器
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UploadFile
        fields = '__all__'


class PublishSerializer(ModelSerializer):
    """
    简单发布记录序列化器
    """
    file = UploadFileSerializer()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Publish
        fields = '__all__'


class ModuleSerializer(ModelSerializer):
    """
    简单模块序列化器
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    publish = PublishSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'



