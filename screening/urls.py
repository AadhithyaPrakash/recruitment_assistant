from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_view, name='analyze'),
    path('result/<int:match_id>/', views.result_view, name='result'),
]