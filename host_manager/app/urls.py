from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'datacenters', views.DataCenterViewSet)
router.register(r'hosts', views.HostViewSet)
router.register(r'statistics', views.HostStatisticViewSet)

# 应用特定的URL模式
app_name = 'host_app'
urlpatterns = [
    # DRF路由器生成的路由
    path('', include(router.urls)),

    # 如果需要添加额外的非视图集路由
    # path('custom-endpoint/', views.custom_view, name='custom-view'),
]