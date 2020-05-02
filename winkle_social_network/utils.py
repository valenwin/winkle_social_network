from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination(request, obj, paginate_by):
    page = request.GET.get('page')
    paginator = Paginator(obj, paginate_by)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return images
