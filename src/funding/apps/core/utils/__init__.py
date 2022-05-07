from django.core.paginator import Paginator, EmptyPage
from ..exceptions import PageBoundException


def sorted_by(data, key, reverse=False):
    return sorted(data, key=lambda x: x[key], reverse=reverse)

def get_data_by_page(data, limit, offset):
    try:
        p = Paginator(data, limit)
        page = p.page(offset+1)
    except EmptyPage:
        raise PageBoundException(p.num_pages)

    return page.object_list
