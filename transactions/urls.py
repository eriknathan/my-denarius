from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='list'),
    path('nova/', views.TransactionCreateView.as_view(), name='create'),
    path('exportar/csv/', views.TransactionExportCSVView.as_view(), name='export_csv'),
    path('<int:pk>/editar/', views.TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.TransactionDeleteView.as_view(), name='delete'),
]
