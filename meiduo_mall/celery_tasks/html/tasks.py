import os

from django.conf import settings
from django.template import loader

from goods.utils import get_categories


def generate_static_list_search_html():
    """生成商品列表页的静态化页面"""
    # 获取页面需要的商品分类
    categories = get_categories()
    # 组装模板需要的数据
    context = {
        'categories': categories,
    }

    # 获取模板
    template = loader.get_template('list.html')

    # 渲染数据到模板中
    html_text = template.render(context)

    # 写html内容到前端front_end_pc目录中
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'list.html')
    with open(file_path, 'w') as f:
        f.write(html_text)