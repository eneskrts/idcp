from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created_date', 'updated_date', 'user', 'category', 'image')
