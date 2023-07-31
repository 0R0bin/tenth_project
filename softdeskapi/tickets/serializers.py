import tickets.models as tModels

from rest_framework import serializers


class IssuesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status']

        extra_kwargs = {
            'description': {'write_only': True},
            'tag': {'write_only': True},
            'priority': {'write_only': True},
            'status': {'write_only': True},
        }



class IssuesDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status']




class CommentsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Comments
        fields = ['id', 'description', 'issue']
        extra_kwargs = {
            'issue': {'write_only': True},
        }
    
    # Creation
    def create(self, validated_data):
        user = self.context['request'].user
        issue = validated_data.pop('issue', None)

        obj_to_save = {
            'description': validated_data.pop('description', None),
            'author_user': user,
            'issue': issue,
        }

        offer = tModels.Comments.objects.create(**obj_to_save)
        offer.save()

        return offer


class CommentsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Comments
        fields = ['id', 'description', 'created_time']
