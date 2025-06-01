from celery import shared_task
from django.utils import timezone
from .models import Host, HostPassword, HostStatistic, City, DataCenter
import logging

logger = logging.getLogger(__name__)


@shared_task
def rotate_host_passwords():
    """每8小时轮换主机root密码"""
    hosts = Host.objects.all()
    for host in hosts:
        try:
            password_info, created = HostPassword.objects.get_or_create(host=host)
            password_info.root_password = None  #重置再生成
            password_info.save()  # 这会触发密码重新生成
            logger.info(f"Rotated password for host {host.hostname}")
        except Exception as e:
            logger.error(f"Failed to rotate password for host {host.hostname}: {str(e)}")


@shared_task
def generate_host_statistics():
    """每天00:00生成主机统计"""
    today = timezone.now().date()
    cities = City.objects.all()

    for city in cities:
        data_centers = DataCenter.objects.filter(city=city)
        for dc in data_centers:
            host_count = Host.objects.filter(data_center=dc).count()
            HostStatistic.objects.create(
                date=today,
                city=city,
                data_center=dc,
                host_count=host_count
            )
            logger.info(f"Created stats for {dc.name}: {host_count} hosts")
