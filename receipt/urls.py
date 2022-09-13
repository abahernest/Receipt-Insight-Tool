from django.urls import path
from .views import ReceiptView

urlpatterns =[
    path('', ReceiptView.as_view())
]