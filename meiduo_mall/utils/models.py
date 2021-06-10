from django.db import models

class BaseModel(models.Model):
    """模型基类"""
    # auto_now_add 表示只有添加的时候，才会把当前时间戳修改作为字段的值
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # auto_now 表示在添加、修改的时候，自动补充当前时间戳作为字段的值
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True