from django.urls import path
from .viewsets import ExportDataView, ImportDataView, import_view

urlpatterns = [
    path('api/import/', ImportDataView.as_view(), name='import_data'),
    path('api/export/', ExportDataView.as_view(), name='export_data'),
    path('import/', import_view),
]
