# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import math

# django.core.paginator から pagerを生成する
def get_pager(query_set, limit=5, page=1, navigation_len=2):
    paginator = Paginator(query_set, limit)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        # ページが整数ではない
        p = paginator.page(1)
    except EmptyPage:
        # 空のページ
        if page <= 0:
            p = paginator.page(1)
        else:
            page = paginator.num_pages
            try:
                p = paginator.page(page)
            except EmptyPage:
                p = paginator.page(1)

    limit_page = int(navigation_len/2)
    min = p.number - limit_page
    max = p.number + limit_page

    if min <= 0:
        navigation_first_page = 1
    else:
        navigation_first_page = min

    if max > paginator.num_pages:
        navigation_last_page = paginator.num_pages
    else:
        navigation_last_page = max

    pager ={
        "total":paginator.count,
        "per_page":paginator.per_page,
        "first_page":1,
        "last_page":paginator.num_pages,
        "current_page":p.number,
        "previous_page":0,
        "next_page":0,
        "first":p.start_index(),
        "last":p.end_index(),
        "prev_navigation_page":0,
        "next_navigation_page":0,
        "navigation_first_page":navigation_first_page,
        "navigation_last_page":navigation_last_page,
        "navigation":[]
        };
    if p.has_previous():
        pager["previous_page"] = p.previous_page_number()
    if p.has_next():
        pager["next_page"] = p.next_page_number()

    if p.number >= limit_page:
        pager["prev_navigation_page"] = navigation_first_page - 1
    if p.number < paginator.num_pages - limit_page:
        pager["next_navigation_page"] = navigation_last_page + 1

    for n in paginator.page_range:
        if n >= min and n < max + 1:
            pager["navigation"].append(n)
    return pager, p.object_list

def get_pager_from_list(list, limit=5, page=1, navigation_len=10):
    """
    リストからページング
    Arguments:
    - `list`:
    
    """
    page = int(page)
    total = len(list)
    per_page = int(limit)
    last_page = int(total / limit)
    if total % limit > 0:
        last_page += 1
    first = per_page  * (page - 1) + 1
    last = first + per_page -1

    limit_page = int(navigation_len/2)
    min = page - limit_page
    max = page + limit_page

    if min <= 0:
        navigation_first_page = 1
    else:
        navigation_first_page = min

    if max > total:
        navigation_last_page = total
    else:
        navigation_last_page = max

    if last > total:
        last = total
    pager ={
        "total":total,
        "per_page":per_page,
        "first_page":1,
        "last_page":last_page,
        "current_page":page,
        "previous_page": 0,
        "next_page": 0,
        "first":first,
        "last":last,
        "prev_navigation_page":0,
        "next_navigation_page":0,
        "navigation_first_page":navigation_first_page,
        "navigation_last_page":navigation_last_page,
        "navigation":[]
        };
    if page > 1:
        pager["previous_page"] = page - 1
    if page < last_page:
        pager["next_page"] = page + 1

    if page>= limit_page:
        pager["prev_navigation_page"] = navigation_first_page - 1
    if page < total - limit_page:
        pager["next_navigation_page"] = navigation_last_page + 1

    for n in range(1,last_page + 1):
        if n >= min and n < max + 1:
            pager["navigation"].append(n)
    list = list[first-1:last]

    return pager, list
