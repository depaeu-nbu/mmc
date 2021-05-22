
from celery import Celery

app = Celery("meiduo")

# 发送短信任务中需要使用的django配置信息

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 加载配置信息
app.config_from_object("celery_tasks.config")

# 申明获取异步任务的队列
app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.email"])


