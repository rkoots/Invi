# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

class GlobalSearchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        search_query = request.GET.get('search')
        global_search_url = reverse('global_search_view')
        if search_query and request.path != global_search_url:
            query_string = urlencode({'search': search_query})
            search_url = f'{global_search_url}?{query_string}'
            return redirect(search_url)
        response = self.get_response(request)
        return response
