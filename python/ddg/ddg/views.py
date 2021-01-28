from django.shortcuts import render


def hello(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'hell.html', context)
