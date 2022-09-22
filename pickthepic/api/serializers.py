from rest_framework import serializers


class CollectionSerializer(serializers.Serializer):
    collection_name = serializers.CharField(source='name', max_length=200)
    collection_id = serializers.IntegerField(source='id')
    collection_cover_url = serializers.CharField(source='cover')
    collection_show = serializers.BooleanField(source='show')


class ImageSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField()
    image_id = serializers.IntegerField(source='id')
    image_url = serializers.CharField(source='image')


class StatSerializer(serializers.Serializer):
    # A scenario
    a_prob = serializers.FloatField()
    a_views = serializers.IntegerField()
    a_views_conv = serializers.IntegerField()
    a_conversion = serializers.FloatField()
    a_ci_bot = serializers.FloatField()
    a_ci_top = serializers.FloatField()
    # B scenario
    b_prob = serializers.FloatField()
    b_views = serializers.IntegerField()
    b_views_conv = serializers.IntegerField()
    b_conversion = serializers.FloatField()
    b_ci_bot = serializers.FloatField()
    b_ci_top = serializers.FloatField()
