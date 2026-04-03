from rest_framework import serializers
import datetime

from posts.models import Post, User, Group, Comment


class ModelWhithAuthorAndTimeObjectMixin(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )


    def create(self, validated_data, data_column_name, model):
        time_now = datetime.datetime.now()
        validated_data[data_column_name] = time_now
        object = model.objects.create(**validated_data)
        return object


class PostSerializer(ModelWhithAuthorAndTimeObjectMixin):
    image = serializers.ImageField(required=False)


    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image', 'group', 'pub_date'
            )
        read_only_fields = ('pub_date',)


    def create(self, validated_data):
        return super().create(validated_data, 'pub_date', Post)


class CommentSerializer(ModelWhithAuthorAndTimeObjectMixin):
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )


    class Meta:
        model = Comment
        fields = ('author', 'post', 'text', 'created')
        read_only_fields = ('created',)


    def create(self, validated_data):
        return super().create(validated_data, 'created', Comment)


class GroupSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Group
        fields = ('title', 'slug', 'description')
