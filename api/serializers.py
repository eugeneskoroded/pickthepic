from rest_framework import serializers


class CollectionSerializer(serializers.Serializer):
    collection_name = serializers.CharField(source='name', max_length=200)
    collection_id = serializers.IntegerField(source='id')
    collection_cover_url = serializers.ImageField(source='cover', use_url=True)
    collection_show = serializers.BooleanField(source='show')


class ImageSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField()
    image_id = serializers.IntegerField(source='id')
    image_url = serializers.ImageField(source='image', use_url=True)
