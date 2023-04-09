from datetime import date, datetime
from django.utils import timezone
import math
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.safestring import mark_safe


from quicktechpoints.serializers import ArticleSerializer, TagSerializer

from .models import Article, Tag, User


def highlight_text(text, search_term):
    regex = re.compile(search_term, re.IGNORECASE)
    return regex.sub(f'<span class="highlight">{search_term}</span>', text)

    def post(self, request, format=None):
        try:
            user = User.objects.get(username=f'{process.env.user}')
        except ObjectDoesNotExist:
            User.objects.create(username=f'{process.env.user}', password=f'{process.env.password}')
            return Response({'msg': 'yes'}, status=status.HTTP_201_CREATED)

        return Response({'msg': 'no'}, status=status.HTTP_200_OK)


class GetAllArticlesView(APIView):
    serializer_class = ArticleSerializer
    
    def get(self, request, format=None):
        try:
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
            q = request.GET.get('q', '')
            tag = request.GET.get('tag', '')

            query = Q()

            if tag:
                tag_obj = Tag.objects.filter(name=tag).first()
                if tag_obj:
                    query &= Q(tag=tag_obj)

            if q:
                query &= Q(title__icontains=q)

            # Find articles that are published
            query &= Q(is_published=True)

            # Find total number of articles
            total_articles = Article.objects.filter(query).count()

            # Calculate total number of pages
            total_pages = math.ceil(total_articles / limit)

            # Calculate number of items to skip
            skip = (page - 1) * limit

            articles = Article.objects.filter(query).order_by('-created_at').prefetch_related('tag')[skip:skip+limit]

            if q:
                articles = [{
                    **article.__dict__,
                    'title': highlight_text(article.title, q)
                } for article in articles]

            articles = self.serializer_class(articles, many=True).data

            return Response({
                'data': {
                    'articles': articles
                },
                'pagination': {
                    'page': page,
                    'totalPages': total_pages,
                    'totalItems': total_articles,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetArticleView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, slug, format=None):
        try:
            # Find the article with the given slug
            article = Article.objects.filter(slug=slug).prefetch_related('tag').first()

            if not article:
                return Response({'message': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

            # Find the next and previous articles
            prev_article = Article.objects.filter(id__lt=article.id).order_by('-id').first()
            next_article = Article.objects.filter(id__gt=article.id).order_by('id').first()

            if article:
                article = self.serializer_class(article).data
            if prev_article:
                prev_article = self.serializer_class(prev_article).data
            if next_article:
                next_article = self.serializer_class(next_article).data

            return Response({
                'data': article,
                'nextArticle': next_article if next_article else None,
                'prevArticle': prev_article if prev_article else None,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetTodayArticleView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, format=None):
        try:
            id = request.GET.get('id', None)

            # Find articles of today
            today = timezone.now().date()
            start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))

            articles = Article.objects.filter(created_at__range=(start_of_day, end_of_day), is_published=True).order_by('created_at').prefetch_related('tag')
            total_articles = articles.count()
            
            if id:
                article = articles.filter(id=id).first()
            else:
                article = articles.first()

            if article:
                
                # Find the next and previous articles
                prev_articles = articles.filter(id__lt=article.id).order_by('-id') 
                next_articles = articles.filter(id__gt=article.id).order_by('id')
                prev_article = prev_articles.first()
                next_article = next_articles.first()
                first_article = articles.first()
                last_article = articles.last()

                article_position = total_articles - articles.filter(id__gt=article.id).count()

                article = self.serializer_class(article).data
                prev_article = self.serializer_class(prev_article).data if prev_article else None
                next_article = self.serializer_class(next_article).data if next_article else None
                first_article = self.serializer_class(first_article).data if first_article else None
                last_article = self.serializer_class(last_article).data if last_article else None

                return Response({
                    'data': article,
                    'nextArticle': next_article,
                    'prevArticle': prev_article,
                    'total_articles': total_articles,
                    'first_article': first_article,
                    'last_article': last_article,
                    'position': article_position
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': None,
                    'nextArticle': None,
                    'prevArticle': None,
                    'total_articles': total_articles,
                     'first_article': None,
                    'last_article': None,
                    'position': 0
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTagsView(APIView):
    serializer_class = TagSerializer

    def get(self, request, format=None):
        try:
            tags = Tag.objects.all()

            if not tags:
                return Response({'message': 'No tags found'}, status=status.HTTP_404_NOT_FOUND)

            tag_list = [{'id': tag.id, 'name': tag.name} for tag in tags]

            return Response({'tags': tag_list}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
