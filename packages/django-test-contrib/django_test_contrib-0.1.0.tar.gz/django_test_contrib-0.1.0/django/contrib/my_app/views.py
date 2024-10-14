from django.http import HttpResponse


def my_app_view(request):

    return HttpResponse(b'Hello App')
