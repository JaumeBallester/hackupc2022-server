from fileManager import views
from django.urls import path, re_path


urlpatterns = [
    re_path(r'^motorbike/(?P<bike_id>\w{0,11})/$',views.Bike.as_view())
    ]