# utils
from collections import OrderedDict
from goods.models import GoodsChannel

def get_categories():
    # 商品分类信息查询

    categories = OrderedDict()

    # 查询一级分类频道信息
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 把查询出来的数据进行归纳分组
    for channel in channels:
        group_id = channel.group_id
        # 生成不同的组
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        # 保存一级分类信息
        cat1 = channel.category
    categories[group_id]['channels'].append({
        'id': cat1.id,
        'name': cat1.name,
        'url': channel.url
    })

    # 构建当前类别的子类
    for cat2 in cat1.goodscategory_set.all():
        cat2.sub_cats = []
        # 查询2级分类的子类
        for cat3 in cat2.goodscategory_set.all():
            cat2.sub_cats.append(cat3)
        categories[group_id]['sub_cats'].append(cat2)

    return categories
