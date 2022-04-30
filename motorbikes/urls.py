from motorbikes import views
from django.urls import path, re_path


urlpatterns = [
    re_path(r'^motorbike/(?P<bike_id>\w{0,11})/$',views.Bike.as_view()),
    path('nextOld/',views.NextBikeOld.as_view()),
    path('next/',views.NextBike.as_view()),
    path('favourites/',views.Bikes.as_view()),
    path('stats/', views.BikeStats.as_view())
    ]