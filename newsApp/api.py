from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from newsApp.models import Article
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


@api_view(['GET'])
def article(request):
    if request.method == 'GET':
        article_list = Article.objects.all()
        article_serializer = ArticleSerializer(article_list[:5], many=True)
        return Response(article_serializer.data)
