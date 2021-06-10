from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # 每一页的数量
    page_size = 2
    # 地址栏上分页数据量的名称
    page_size_query_param = 'page_size'
    # 分页数据量的最大值
    max_page_size = 20