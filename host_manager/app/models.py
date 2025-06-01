from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import secrets
import string


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True,
                            help_text="城市缩写代号（如 SZ）",
                            validators=[RegexValidator(r'^[A-Z]+$', '只允许大写字母')]
                            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataCenter(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'city')

    def __str__(self):
        return f"{self.name} ({self.city})"


class Host(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]

    hostname = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    data_center = models.ForeignKey(DataCenter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

    def save(self, *args, **kwargs):
        created = not self.pk  # 检查是否是新建记录
        super().save(*args, **kwargs)
        if created:
            self._create_password_record()

    def _create_password_record(self):
        """确保创建关联的密码记录"""
        if not hasattr(self, 'password_info'):
            HostPassword.objects.create(host=self)


class HostPassword(models.Model):
    host = models.OneToOneField(Host, on_delete=models.CASCADE, related_name='password_info')
    root_password = models.CharField(max_length=100)
    last_changed = models.DateTimeField(auto_now=True)
    history = models.JSONField(default=list)  # 存储历史密码记录

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
        return ''.join(secrets.choice(alphabet) for _ in range(16))

    def save(self, *args, **kwargs):
        if not self.pk or not self.root_password:
            self.root_password = self.generate_password()
            if not self.history:
                self.history = []
            self.history.append({
                'password': self.root_password,
                'changed_at': timezone.now().isoformat()
            })
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Password for {self.host.hostname}"


class HostStatistic(models.Model):
    date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    data_center = models.ForeignKey(DataCenter, on_delete=models.CASCADE)
    host_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'city', 'data_center')

    def __str__(self):
        return f"{self.date}: {self.data_center} - {self.host_count} hosts"
