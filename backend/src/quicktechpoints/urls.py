from django.urls import path
from .views import GetAllArticlesView, GetArticleView, GetTagsView, GetTodayArticleView

urlpatterns = [
    path('', GetAllArticlesView.as_view(), name='get_all_articles'),
    path('today/', GetTodayArticleView.as_view(), name='get_today_articles'),
    path('tags/', GetTagsView.as_view(), name='get_tags'),
    path('<slug:slug>/', GetArticleView.as_view(), name='get_article'),
]
