from django.shortcuts import render


def error404_page(request, exception):
    return render(request, 'forum/error404_page.html', status=404)
