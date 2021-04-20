
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name = "home"),
    path('analysis', views.analysis, name='analysis'),
    path('reunion', views.reunion, name='reunion'),
    path('preloaded', views.preloaded, name='preloaded'),
    path('map', views.map, name='map'),
    path('upload/',views.upload,name="upload"),
]
