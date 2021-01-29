from django.shortcuts import render


def login(request):
    # context = {'hello': 'Hello World!'}
    return render(request, 'login.html')


def chat(request):
    return render(request, 'chat.html')
