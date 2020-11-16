from django.urls import path
from .views import GraphView, NodeDetailView

urlpatterns = [
    path('', GraphView.as_view(), name='graph'),
    path(r'nodes/<int:node_id>', NodeDetailView.as_view())
]