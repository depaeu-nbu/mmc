# 页面静态化处理逻辑
import os
import time
from collections import OrderedDict

from django.conf import settings
from django.template import loader

from contents.models import ContentCategory
from meiduo_mall.apps.goods.utils import get_categories

def generate_static_index_html():
    """生成静态主页"""
    print('%s:generate_static_index_html' % time.ctime())

    # 获取首页商品数据

    categories = get_categories()
    print(categories)

    # 获取广告数据
    contents = OrderedDict()
    # 获取广告分类
    content_categories = ContentCategory.objects.all()
    # 根据分类查询广告内容
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 将数据写入到模板中
    context = {
        'categories': categories,
        'contents': contents,
    }

    # 获取模板
    template = loader.get_template('index.html')
    # 把数据渲染到模板中
    html_text = template.render(context)

    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)

