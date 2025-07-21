from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/analyze-repository/', views.analyze_repository, name='analyze_repository'),
    path('api/preview-file/<int:file_id>/', views.preview_file, name='preview_file'),
    path('api/analyze-file/', views.analyze_file, name='analyze_file'),
    path('api/search-code/', views.search_code, name='search_code'),
    path('api/llm-status/', views.llm_status, name='llm_status'),
]
