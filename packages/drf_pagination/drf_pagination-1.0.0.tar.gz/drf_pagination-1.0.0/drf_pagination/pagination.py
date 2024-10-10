from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPaginationOptimization(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None
        self.offset = self.get_offset(request)
        self.count = self.get_count(queryset)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        if self.count == 0 or self.offset > self.count:
            return queryset.none()
        return queryset[self.offset:self.offset + self.limit]


class LimitOffsetPaginationForDataTable(LimitOffsetPaginationOptimization):
    limit_query_param = 'length'
    offset_query_param = 'start'

    def paginate_queryset(self, queryset, request, view=None):
        self.total = view.get_queryset().count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        params = self.request.query_params
        return Response(OrderedDict([
            ('draw', int(params.get('draw', 1))),
            ('recordsTotal', self.total),
            ('recordsFiltered', self.count),
            ('data', data),
        ]))


class LimitOffsetPaginationNoCount(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None
        self.offset = self.get_offset(request)
        self.count = 1000
        # self.count = _get_count(queryset)
        # self.request = request
        # if self.count > self.limit and self.template is not None:
        #     self.display_page_controls = True
        # if self.count == 0 or self.offset > self.count:
        #     return queryset.none()
        return queryset[self.offset:self.offset + self.limit]

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            # ('count', self.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('results', data)
        ]))
