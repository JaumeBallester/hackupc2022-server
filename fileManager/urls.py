from fileManager import views
from django.urls import path


urlpatterns = [
    path('image/',views.Image.as_view())
    ]
