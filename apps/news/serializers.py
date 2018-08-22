# REST framework
from rest_framework import serializers

# Project
from apps.gauth.serializers import MeSerializer
from apps.shared.models import History
from apps.shared import messages as msg
from .models import News


# News crud serializer
class NewsCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        read_only_fields = ('created_date', 'modified_date',)
        exclude = ('is_deleted',)

    def to_representation(self, instance):
        self.fields['author'] = MeSerializer()

        return super().to_representation(instance)

    def create(self, validated_data):
        user = self.context['request'].user
        instance = News.objects.create(**validated_data)

        History.write_history(user, instance, msg.CREATED)
        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        news = super().update(instance, validated_data)

        History.write_history(user, news, msg.UPDATED)

        return news


# News public api serializer
class NewsPublicSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id', 'title', 'desc', 'content', 'author', 'published_date',
        )

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'name': obj.author.username
        }
