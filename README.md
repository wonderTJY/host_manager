# host_manager

用于管理企业内部的主机的 Python 项目。

## 项目简介

`host_manager` 是一个专为企业内部主机管理设计的系统，支持主机信息管理、任务调度等功能。

## 功能特性

- 用于管理企业内部的主机，包含主机、城市、机房等模型
- 提供对应模型的增删改查接口，主机连通性探测接口
- 每隔 8 小时随机修改每台主机的密码并记录，每天 00:00 按城市和机房维度统计主机数量，并把统计数据写入数据库
- 统计每个请求的请求耗时的中间件

## API接口
- 使用rest_framework标准返回
- 增加DjangoFilterBackend条件查询
- 使用drf_spectacular自动生成api使用说明，地址为"ip:port/swagger/"如图所示:
![image](https://github.com/user-attachments/assets/a0f55957-d1b0-4934-9480-570188aa42d7)

## 安装方法

1. 克隆仓库：

   ```bash
   git clone https://github.com/wonderTJY/host_manager.git
   cd host_manager/host_manager
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 初始化数据库

2. 启动django、celery服务：

   ```bash
   python manage.py runserver <ip:port>
   ```
   ```bash
   celery -A host_manager.celery worker --pool=solo -l info
   ```
--pool=solo防止windows报错

## 目录结构

```
host_manager/
├── app/                        # 业务模块目录
│   ├── __init__.py
│   ├── apps.py                 # Django App 配置
│   ├── middleware.py           # 中间件定义(记录请求耗时)
│   ├── migrations/             # 数据库迁移文件夹（使用postgresql）
│   ├── models.py               # 数据库模型（城市、机房、主机）
│   ├── serializers.py          # 序列化定义（DRF规范输出）
│   ├── tasks.py                # Celery 任务定义（其中实现8小时更新密码以及0点生成统计）
│   ├── urls.py                 # 子路由配置
│   └── views.py                # 视图及 API 逻辑（各模型CRUD，主机连通性探测）
├── host_manager/               # 主程序目录（Django 项目配置）
│   ├── __init__.py
│   ├── asgi.py                 # ASGI 启动入口
│   ├── celery.py               # Celery 配置
│   ├── settings.py             # 项目设置
│   ├── urls.py                 # 项目级路由
│   └── wsgi.py                 # WSGI 启动入口
├── manage.py                   # 管理脚本
├── requirements.txt            # 依赖列表
├── celerybeat-schedule.*       # 定时任务相关文件
```


## 依赖

见 `requirements.txt` 文件。

## 许可证

本项目基于 MIT 许可证，详情见 LICENSE 文件。
