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
        model = tModels.Issues
        fields = ['id', 'description']
    
    # Creation
    def create(self, validated_data):
        print(self.context['request'].query_params)
        user = self.context['request'].user
        issue_id = self.context.get('request').query_params.get('issue_id', None)


        obj_to_save = {
            'description': validated_data.pop('description', None),
            'author_user': user,
            'issue_id': issue_id,
        }

        offer = tModels.Comments.objects.create(**obj_to_save)
        offer.save()

        return offer


class CommentsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Issues
        fields = ['id', 'title', 'author_user_id', 'created_time']
