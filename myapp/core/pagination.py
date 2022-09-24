import math

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        count = self.page.paginator.count
        current = self.page.number
        page_size = self.page_size
        previous = None
        next = None
        total_pages = math.ceil(count / page_size)
        if (self.page.has_previous()):
            previous = self.page.previous_page_number()
        if (self.page.has_next()):
            next = self.page.next_page_number()
        first = None if (previous is None or previous == 1) else ((previous - 1) if previous > 1 else None)  # noqa
        last = None if (next is None or next == total_pages) else total_pages
        return Response({
            'pagination': {
                'first': first,
                'last': last,
                'previous': previous,
                'next': next,
                'current': current,
                'page_size': page_size,
                'total_pages': total_pages,
            },
            'results': data
        })
