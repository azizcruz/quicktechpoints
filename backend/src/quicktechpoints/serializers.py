from rest_framework import serializers
from .models import Article, Tag
from django.utils.html import format_html


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')
    
    def to_representation(self, instance):
        # Call the default to_representation method to serialize the instance
        representation = super().to_representation(instance)

        # Mark the HTML content in the body attribute as safe using SafeText
        representation['body'] = format_html(representation['body'])

        print(representation['body'])

        # Return the modified serialized representation
        return representation

    def create(self, validated_data):
        tags_data = validated_data.pop('tag', [])

        article = Article.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
            article.tag.add(tag)

        return article
