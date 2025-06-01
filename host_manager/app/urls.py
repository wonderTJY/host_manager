from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'datacenters', views.DataCenterViewSet)
router.register(r'hosts', views.HostViewSet)
router.register(r'statistics', views.HostStatisticViewSet)

app_name = 'host_app'
urlpatterns = [
    path('', include(router.urls)),
]