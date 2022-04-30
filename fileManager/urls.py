from fileManager import views
from django.urls import path, re_path


urlpatterns = [
    re_path(r'^image/(?P<image_id>\w{0,11})/$',views.Image.as_view())
    ]