from rest_framework.pagination import PageNumberPagination

class StorePagination(PageNumberPagination):
    page_size = 2  # how many stores in each page
    page_size_query_param = 'page_size'
    max_page_size = 100