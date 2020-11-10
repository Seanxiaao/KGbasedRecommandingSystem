from django.urls import path
from .views import RecommendingView

urlpatterns = [
    path('', RecommendingView.as_view(), name='recommending')
]