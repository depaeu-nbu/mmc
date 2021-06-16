from rest_framework import serializers

from .models import SKU

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(label="ID")
    name = serializers.CharField(label="分类")

class ChannelSerializer(serializers.Serializer):
    url = serializers.CharField(read_only=True, label="链接地址")
    category = CategorySerializer()

class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ["id", "name", "price", "comments", "default_image_url"]