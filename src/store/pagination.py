from rest_framework.pagination import PageNumberPagination

class ItemsPagination(PageNumberPagination):
    page_size = 3  # how many items in each page
    page_size_query_param = 'page_size'
    max_page_size = 100