from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import subprocess
from .models import City, DataCenter, Host, HostPassword, HostStatistic
from .serializers import (
    CitySerializer,
    DataCenterSerializer,
    HostSerializer,
    HostPasswordSerializer,
    HostStatisticSerializer
)


class FilterMixin:
    filter_backends = [DjangoFilterBackend]


class CityViewSet(FilterMixin, viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class DataCenterViewSet(FilterMixin, viewsets.ModelViewSet):
    queryset = DataCenter.objects.all()
    serializer_class = DataCenterSerializer
    filterset_fields = ['city_id']


class HostViewSet(FilterMixin, viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filterset_fields = ['data_center_id', 'status']

    @action(detail=True, methods=['get'])
    def check_ping(self, request, pk=None):
        host = self.get_object()
        try:
            # 使用系统ping命令检测主机可达性/windows
            result = subprocess.run(
                ['ping', '-n', '3', host.ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                shell=True
            )
            is_reachable = result.returncode == 0

            # 尝试UTF-8解码，失败则尝试本地编码/windows
            try:
                output = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                import locale
                output = result.stdout.decode(locale.getpreferredencoding())

            return Response({
                'host': host.hostname,
                'ip_address': host.ip_address,
                'is_reachable': is_reachable,
                'ping_output': output
            })
        except subprocess.TimeoutExpired:
            return Response({
                'host': host.hostname,
                'ip_address': host.ip_address,
                'is_reachable': False,
                'ping_output': 'Ping timeout'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)

    @action(detail=True, methods=['get'])
    def password(self, request, pk=None):
        host = self.get_object()
        password_info = get_object_or_404(HostPassword, host=host)
        serializer = HostPasswordSerializer(password_info)
        return Response(serializer.data)


class HostStatisticViewSet(FilterMixin, viewsets.ReadOnlyModelViewSet):
    queryset = HostStatistic.objects.all()
    serializer_class = HostStatisticSerializer
