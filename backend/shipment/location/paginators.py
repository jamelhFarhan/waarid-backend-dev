from rest_framework.pagination import LimitOffsetPagination


class CityCountryPagination(LimitOffsetPagination):
    default_limit = 10
