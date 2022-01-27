from rest_framework.pagination import PageNumberPagination


class FourPerPagePagination(PageNumberPagination):
    page_size = 4
