# from collections import OrderedDict
# from goods.models import GoodsChannel
# #
#
# def get_categories():
#     # 商品分类信息查询
#
#     categories = OrderedDict()
#
#     # 查询一级分类频道信息
#     channels = GoodsChannel.objects.order_by('group_id', 'sequence')
#     # 把查询出来的数据进行归纳分组
#     for channel in channels:
#         group_id = channel.group_id
#         # 生成不同的组
#         if group_id not in categories:
#             categories[group_id] = {'channels':[], 'sub_cats':[]}
#
#         # 保存一级分类信息
#         cat1 = channel.category
#     categories[group_id]['channels'].append({
#         'id': cat1.id,
#         'name': cat1.name,
#         'url': channel.url
#     })
#
#     # 构建当前类别的子类
#     for cat2 in cat1.goodscategory_set.all():
#         cat2.sub_cats = []
#         # 查询2级分类的子类
#         for cat3 in cat2.goodscategory_set.all():
#             cat2.sub_cats.append(cat3)
#         categories[group_id]['sub_cats'].append(cat2)
#
#     return categories

from collections import OrderedDict
from goods.models import GoodsChannel


def get_categories():
    # 商品频道及分类菜单[先查询一级分类[分组]，接着查询二级，最后是三级]
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':1, 'name':'手机', 'url':''},{'id':2,'name':'数码'}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     .....
    #     3: { # 组3
    #         'channels': [{'id':3,'name':'电脑','url':''},{'id':4,'name':'办公'...}]
    #     }
    # }

    categories = OrderedDict()
    # 1.1.1 查询一级分类的频道信息
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 把查询出来的数据按照不同组进行归纳
    for channel in channels:
        group_id = channel.group_id  # 当前组

        # 生成不同的组
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        # print(categories)
        # # 先把一级分类的信息查询出来保存组中
        cat1 = channel.category  # 当前频道的类别
        #
        # # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        # 构建当前类别的子类别
        for cat2 in cat1.goodscategory_set.all(): # 获取一级分类的每一个子分类
            cat2.sub_cats = []
            # 查询每一个２级分类的子分类
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)

    return categories